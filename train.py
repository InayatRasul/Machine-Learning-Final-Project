"""
Training Script for Stroke Prediction Model
Main script to train and evaluate the stroke prediction model with MLflow tracking.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import mlflow

from data_loader import load_dataset, get_data_info
from preprocessing import prepare_data, get_feature_groups, create_feature_preprocessor
from models import StrokePredictor
from utils import set_plot_style, create_summary_report


def main():
    """Main training function with MLflow tracking."""
    
    print("\n" + "="*70)
    print("STROKE PREDICTION MODEL - TRAINING PIPELINE (with MLflow)")
    print("="*70 + "\n")
    
    # Set MLflow tracking URI and experiment
    mlflow.set_tracking_uri("file:./mlruns")
    mlflow.set_experiment("Stroke_Prediction_Experiment")
    
    # 1. Load Dataset
    print("Step 1: Loading Dataset...")
    dataset_path = Path(__file__).parent / 'data' / 'raw' / 'StrockDataset.csv'
    df = load_dataset(dataset_path)
    
    # 2. Explore Data
    print("\nStep 2: Exploring Dataset...")
    info = get_data_info(df)
    print(f"Dataset shape: {info['shape']}")
    print(f"Missing values:\n{pd.Series(info['missing_values']).head()}")
    print(f"Target distribution:\n{df['stroke'].value_counts()}")
    
    # 3. Prepare Data
    print("\nStep 3: Preparing Data...")
    X, y = prepare_data(df, target_col='stroke', drop_cols=['id'])
    numeric_features, categorical_features = get_feature_groups(X)
    
    print(f"Features shape: {X.shape}")
    print(f"Numeric features: {numeric_features}")
    print(f"Categorical features: {categorical_features}")
    print(f"Target distribution:\n{y.value_counts()}")
    
    # 4. Split Data
    print("\nStep 4: Splitting Data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )
    print(f"Training set size: {X_train.shape[0]}")
    print(f"Test set size: {X_test.shape[0]}")
    print(f"Training set stroke distribution:\n{y_train.value_counts()}")
    
    # 5. Create Preprocessor
    print("\nStep 5: Creating Feature Preprocessor...")
    preprocessor = create_feature_preprocessor(numeric_features, categorical_features)
    
    # 6-9. Train Models with MLflow Tracking
    print("\nStep 6: Training Models with MLflow...")
    predictor = StrokePredictor(preprocessor)
    
    with mlflow.start_run(run_name="stroke_prediction_training"):
        # Log dataset parameters
        mlflow.log_param("dataset_samples", X.shape[0])
        mlflow.log_param("num_features", X.shape[1])
        mlflow.log_param("train_size", X_train.shape[0])
        mlflow.log_param("test_size", X_test.shape[0])
        mlflow.log_param("test_split_ratio", 0.2)
        mlflow.log_param("random_state", 42)
        mlflow.log_param("stratified_split", True)
        mlflow.log_param("numeric_features", len(numeric_features))
        mlflow.log_param("categorical_features", len(categorical_features))
        
        predictor.train_models(X_train, y_train)
        
        # 7. Evaluate Models
        print("\nStep 7: Evaluating Models...")
        results_df = predictor.evaluate_models(X_test, y_test)
        print("\n" + results_df.to_string(index=False))
        
        # Log evaluation metrics for each model
        for idx, row in results_df.iterrows():
            model_name = row['Model']
            mlflow.log_metrics({
                f"{model_name}_accuracy": row['Accuracy'],
                f"{model_name}_precision": row['Precision'],
                f"{model_name}_recall": row['Recall'],
                f"{model_name}_f1_score": row['F1-Score'],
                f"{model_name}_roc_auc": row['ROC-AUC'],
            })
        
        # 8. Cross-Validation
        print("\nStep 8: Cross-Validation...")
        cv_results = predictor.cross_validate(X, y, cv=5)
        
        # Log cross-validation results
        for model_name, cv_result in cv_results.items():
            mlflow.log_metrics({
                f"{model_name}_cv_mean_f1": cv_result['mean_score'],
                f"{model_name}_cv_std_f1": cv_result['std_dev'],
            })
        
        # 9. Feature Importance
        print("\nStep 9: Extracting Feature Importance...")
        try:
            feature_importance = predictor.get_feature_importance(top_n=15)
            if feature_importance is not None:
                print("\nTop 15 Features:")
                print(feature_importance.to_string(index=False))
                
                # Log feature importance as artifacts
                feature_importance.to_csv("feature_importance.csv", index=False)
                mlflow.log_artifact("feature_importance.csv")
        except Exception as e:
            print(f"Could not extract feature importance: {e}")
        
        # 10. Save Models and Log to MLflow
        print("\nStep 10: Saving Models...")
        models_dir = Path(__file__).parent / 'models'
        models_dir.mkdir(exist_ok=True)
        
        for name, model in predictor.models.items():
            model_path = models_dir / f"{name.replace(' ', '_').lower()}_model.joblib"
            import joblib
            joblib.dump(model, model_path)
            print(f"Saved: {model_path}")
            
            # Log model to MLflow
            mlflow.sklearn.log_model(model, artifact_path=f"models/{name.replace(' ', '_').lower()}")
        
        # Save and log best model
        best_model_path = models_dir / 'best_model.joblib'
        predictor.save_model(best_model_path)
        mlflow.sklearn.log_model(predictor.best_model, artifact_path="models/best_model", 
                                registered_model_name="StrokePredictionBestModel")
        
        # 11. Save Results Report
        print("\nStep 11: Saving Results Report...")
        report_path = Path(__file__).parent / 'results' / 'evaluation_report.txt'
        report_path.parent.mkdir(exist_ok=True)
        create_summary_report(results_df, report_path)
        print(f"Report saved to: {report_path}")
        
        # Log evaluation report as artifact
        mlflow.log_artifact(str(report_path))
        
        # Log results dataframe as CSV
        results_csv_path = Path(__file__).parent / 'results' / 'model_evaluation_results.csv'
        results_df.to_csv(results_csv_path, index=False)
        mlflow.log_artifact(str(results_csv_path))
        
        print("\n" + "="*70)
        print("TRAINING PIPELINE COMPLETED SUCCESSFULLY!")
        print(f"Best Model: {predictor.best_model_name}")
        print(f"MLflow tracking URI: {mlflow.get_tracking_uri()}")
        print(f"Experiment: {mlflow.get_experiment_by_name('Stroke_Prediction_Experiment').name}")
        print("="*70 + "\n")
    
    return predictor, results_df


if __name__ == "__main__":
    predictor, results = main()