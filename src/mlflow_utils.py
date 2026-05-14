"""
MLflow Integration Module
Utilities for experiment tracking and model registry with MLflow.
"""

import mlflow
import mlflow.sklearn
import pandas as pd
from pathlib import Path


def setup_mlflow(experiment_name="Stroke_Prediction_Experiment", tracking_uri="file:./mlruns"):
    """
    Setup MLflow experiment and tracking.
    
    Args:
        experiment_name (str): Name of the experiment
        tracking_uri (str): URI for MLflow tracking
        
    Returns:
        str: Experiment ID
    """
    mlflow.set_tracking_uri(tracking_uri)
    experiment = mlflow.get_experiment_by_name(experiment_name)
    
    if experiment is None:
        experiment_id = mlflow.create_experiment(experiment_name)
        print(f"Created new experiment: {experiment_name} (ID: {experiment_id})")
    else:
        experiment_id = experiment.experiment_id
        print(f"Using existing experiment: {experiment_name} (ID: {experiment_id})")
    
    mlflow.set_experiment(experiment_name)
    return experiment_id


def log_training_params(dataset_info, split_info, preprocessing_info):
    """
    Log training parameters to MLflow.
    
    Args:
        dataset_info (dict): Dataset information
        split_info (dict): Train/test split information
        preprocessing_info (dict): Preprocessing configuration
    """
    # Dataset parameters
    mlflow.log_params({
        "dataset_samples": dataset_info.get("samples", 0),
        "num_features": dataset_info.get("num_features", 0),
        "target_positive_ratio": dataset_info.get("positive_ratio", 0),
    })
    
    # Split parameters
    mlflow.log_params({
        "test_split_ratio": split_info.get("test_ratio", 0.2),
        "train_samples": split_info.get("train_samples", 0),
        "test_samples": split_info.get("test_samples", 0),
        "stratified_split": split_info.get("stratified", True),
        "random_state": split_info.get("random_state", 42),
    })
    
    # Preprocessing parameters
    mlflow.log_params({
        "numeric_imputation_strategy": preprocessing_info.get("numeric_imputation", "median"),
        "categorical_imputation_strategy": preprocessing_info.get("categorical_imputation", "most_frequent"),
        "scaling_method": preprocessing_info.get("scaling", "StandardScaler"),
        "encoding_method": preprocessing_info.get("encoding", "OneHotEncoder"),
    })


def log_model_metrics(model_name, metrics_dict):
    """
    Log model evaluation metrics to MLflow.
    
    Args:
        model_name (str): Name of the model
        metrics_dict (dict): Dictionary of metrics
    """
    prefixed_metrics = {f"{model_name}_{key}": value 
                       for key, value in metrics_dict.items()}
    mlflow.log_metrics(prefixed_metrics)


def log_cv_results(cv_results_dict):
    """
    Log cross-validation results to MLflow.
    
    Args:
        cv_results_dict (dict): Cross-validation results
    """
    for model_name, cv_result in cv_results_dict.items():
        mlflow.log_metrics({
            f"{model_name}_cv_mean_f1": cv_result['mean_score'],
            f"{model_name}_cv_std_f1": cv_result['std_dev'],
        })


def save_and_log_model(model, model_name, artifact_path="models", register=False):
    """
    Save and log model to MLflow.
    
    Args:
        model: Trained sklearn model/pipeline
        model_name (str): Name of the model
        artifact_path (str): Path to save artifacts
        register (bool): Whether to register model
        
    Returns:
        str: MLflow run ID
    """
    mlflow.sklearn.log_model(
        model, 
        artifact_path=artifact_path,
        registered_model_name=f"StrokePrediction_{model_name}" if register else None
    )
    print(f"Model logged: {model_name}")


def load_best_run(experiment_name="Stroke_Prediction_Experiment"):
    """
    Load best run from experiment based on F1-score.
    
    Args:
        experiment_name (str): Name of the experiment
        
    Returns:
        dict: Best run information
    """
    experiment = mlflow.get_experiment_by_name(experiment_name)
    if experiment is None:
        raise ValueError(f"Experiment {experiment_name} not found")
    
    client = mlflow.tracking.MlflowClient()
    runs = client.search_runs(experiment_ids=[experiment.experiment_id])
    
    if not runs:
        raise ValueError(f"No runs found in experiment {experiment_name}")
    
    # Find best run (highest F1-score for best model)
    best_run = max(runs, key=lambda r: r.data.metrics.get('Logistic Regression_f1_score', 0))
    
    return {
        "run_id": best_run.info.run_id,
        "metrics": best_run.data.metrics,
        "params": best_run.data.params,
        "start_time": best_run.info.start_time,
        "end_time": best_run.info.end_time
    }


def get_experiment_summary(experiment_name="Stroke_Prediction_Experiment"):
    """
    Get summary of all runs in an experiment.
    
    Args:
        experiment_name (str): Name of the experiment
        
    Returns:
        pd.DataFrame: Summary of all runs
    """
    experiment = mlflow.get_experiment_by_name(experiment_name)
    if experiment is None:
        raise ValueError(f"Experiment {experiment_name} not found")
    
    client = mlflow.tracking.MlflowClient()
    runs = client.search_runs(experiment_ids=[experiment.experiment_id])
    
    if not runs:
        return pd.DataFrame()
    
    # Extract key metrics from each run
    data = []
    for run in runs:
        data.append({
            "Run ID": run.info.run_id[:8],
            "Status": run.info.status,
            "Start Time": pd.Timestamp(run.info.start_time, unit='ms'),
            "Duration (s)": (run.info.end_time - run.info.start_time) / 1000 if run.info.end_time else None,
            "Best Model F1": run.data.metrics.get('Logistic Regression_f1_score', None),
            "Best Model Accuracy": run.data.metrics.get('Logistic Regression_accuracy', None),
        })
    
    return pd.DataFrame(data)


def load_logged_model(run_id, artifact_path="models/best_model"):
    """
    Load a logged model from MLflow.
    
    Args:
        run_id (str): MLflow run ID
        artifact_path (str): Path to model artifacts
        
    Returns:
        Loaded model
    """
    model = mlflow.sklearn.load_model(f"runs:/{run_id}/{artifact_path}")
    print(f"Model loaded from run {run_id}")
    return model


def log_artifacts_from_directory(directory_path, artifact_path="results"):
    """
    Log all files from a directory as artifacts.
    
    Args:
        directory_path (str): Path to directory
        artifact_path (str): Artifact path in MLflow
    """
    directory_path = Path(directory_path)
    if directory_path.exists() and directory_path.is_dir():
        for file_path in directory_path.glob('*'):
            if file_path.is_file():
                mlflow.log_artifact(str(file_path), artifact_path)
                print(f"Logged artifact: {file_path.name}")


class MLflowTracker:
    """Context manager for MLflow tracking."""
    
    def __init__(self, run_name="stroke_prediction", experiment_name="Stroke_Prediction_Experiment"):
        self.run_name = run_name
        self.experiment_name = experiment_name
        self.run = None
    
    def __enter__(self):
        setup_mlflow(self.experiment_name)
        self.run = mlflow.start_run(run_name=self.run_name)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            mlflow.end_run(status="FAILED")
        else:
            mlflow.end_run(status="FINISHED")
    
    def log_params(self, params_dict):
        """Log parameters."""
        mlflow.log_params(params_dict)
    
    def log_metrics(self, metrics_dict):
        """Log metrics."""
        mlflow.log_metrics(metrics_dict)
    
    def log_model(self, model, artifact_path="models"):
        """Log model."""
        mlflow.sklearn.log_model(model, artifact_path)
    
    def log_file(self, file_path, artifact_path=None):
        """Log file as artifact."""
        mlflow.log_artifact(str(file_path), artifact_path)


# MLflow UI command helper
def start_mlflow_ui(port=5000):
    """
    Print command to start MLflow UI.
    
    Args:
        port (int): Port for MLflow UI
    """
    print(f"\nTo view MLflow dashboard, run:")
    print(f"mlflow ui --host 0.0.0.0 --port {port}")
    print(f"Then open: http://localhost:{port}")
