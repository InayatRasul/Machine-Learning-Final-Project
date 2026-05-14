"""
Model Training and Evaluation Module
Handles model training, evaluation, and comparison.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report, roc_curve
)
import joblib


class StrokePredictor:
    """Main class for stroke prediction model."""
    
    def __init__(self, preprocessor):
        """
        Initialize the stroke predictor.
        
        Args:
            preprocessor: Sklearn preprocessor/transformer
        """
        self.preprocessor = preprocessor
        self.models = {}
        self.best_model = None
        self.results = {}
        
    def create_pipeline(self, estimator, name):
        """
        Create a pipeline with preprocessing and estimator.
        
        Args:
            estimator: Sklearn estimator
            name (str): Model name
            
        Returns:
            Pipeline: Complete pipeline
        """
        pipeline = Pipeline([
            ('preprocessor', self.preprocessor),
            ('classifier', estimator)
        ])
        self.models[name] = pipeline
        return pipeline
    
    def train_models(self, X_train, y_train):
        """
        Train multiple models.
        
        Args:
            X_train (array-like): Training features
            y_train (array-like): Training target
        """
        models_to_train = {
            'Logistic Regression': LogisticRegression(
                max_iter=1000, random_state=42, class_weight='balanced'
            ),
            'Random Forest': RandomForestClassifier(
                n_estimators=100, random_state=42, 
                class_weight='balanced', n_jobs=-1
            ),
            'Gradient Boosting': GradientBoostingClassifier(
                n_estimators=100, learning_rate=0.1, 
                random_state=42, max_depth=5
            )
        }
        
        for name, estimator in models_to_train.items():
            print(f"\nTraining {name}...")
            pipeline = self.create_pipeline(estimator, name)
            pipeline.fit(X_train, y_train)
            print(f"{name} trained successfully!")
    
    def evaluate_models(self, X_test, y_test):
        """
        Evaluate all trained models.
        
        Args:
            X_test (array-like): Test features
            y_test (array-like): Test target
            
        Returns:
            pd.DataFrame: Evaluation metrics
        """
        results = []
        
        for name, model in self.models.items():
            print(f"\nEvaluating {name}...")
            
            # Predictions
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)[:, 1]
            
            # Metrics
            metrics = {
                'Model': name,
                'Accuracy': accuracy_score(y_test, y_pred),
                'Precision': precision_score(y_test, y_pred),
                'Recall': recall_score(y_test, y_pred),
                'F1-Score': f1_score(y_test, y_pred),
                'ROC-AUC': roc_auc_score(y_test, y_pred_proba),
            }
            
            results.append(metrics)
            self.results[name] = {
                'metrics': metrics,
                'y_pred': y_pred,
                'y_pred_proba': y_pred_proba,
                'confusion_matrix': confusion_matrix(y_test, y_pred),
                'classification_report': classification_report(y_test, y_pred)
            }
        
        results_df = pd.DataFrame(results)
        self.best_model_name = results_df.loc[results_df['F1-Score'].idxmax(), 'Model']
        self.best_model = self.models[self.best_model_name]
        
        print(f"\n\nBest Model: {self.best_model_name}")
        return results_df
    
    def cross_validate(self, X, y, cv=5):
        """
        Perform cross-validation on all models.
        
        Args:
            X (array-like): Features
            y (array-like): Target
            cv (int): Number of folds
            
        Returns:
            dict: Cross-validation scores
        """
        cv_results = {}
        
        for name, model in self.models.items():
            scores = cross_val_score(model, X, y, cv=cv, scoring='f1')
            cv_results[name] = {
                'mean_score': scores.mean(),
                'std_dev': scores.std(),
                'scores': scores
            }
            print(f"{name} CV F1-Score: {scores.mean():.4f} (+/- {scores.std():.4f})")
        
        return cv_results
    
    def get_feature_importance(self, top_n=10):
        """
        Get feature importance from tree-based models.
        
        Args:
            top_n (int): Number of top features to return
            
        Returns:
            pd.DataFrame: Feature importance dataframe
        """
        if self.best_model is None:
            raise ValueError("No model has been trained yet")
        
        # Get the classifier from pipeline
        classifier = self.best_model.named_steps['classifier']
        
        if not hasattr(classifier, 'feature_importances_'):
            return None
        
        # Get feature names
        preprocessor = self.best_model.named_steps['preprocessor']
        feature_names = self._get_feature_names(preprocessor)
        
        importances = classifier.feature_importances_
        feature_imp_df = pd.DataFrame({
            'Feature': feature_names,
            'Importance': importances
        }).sort_values('Importance', ascending=False).head(top_n)
        
        return feature_imp_df
    
    def _get_feature_names(self, preprocessor):
        """Get feature names from preprocessor."""
        feature_names = []
        
        for name, trans, columns in preprocessor.transformers_:
            if name == 'num':
                feature_names.extend(columns)
            elif name == 'cat':
                # For OneHotEncoder
                if hasattr(trans, 'named_steps'):
                    ohe = trans.named_steps['onehot']
                    cat_features = ohe.get_feature_names_out(columns)
                    feature_names.extend(cat_features)
        
        return feature_names
    
    def save_model(self, filepath):
        """
        Save the best model.
        
        Args:
            filepath (str): Path to save model
        """
        if self.best_model is None:
            raise ValueError("No model has been trained yet")
        
        joblib.dump(self.best_model, filepath)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath):
        """
        Load a trained model.
        
        Args:
            filepath (str): Path to model file
        """
        self.best_model = joblib.load(filepath)
        print(f"Model loaded from {filepath}")
    
    def predict(self, X):
        """
        Make predictions using best model.
        
        Args:
            X (array-like): Features
            
        Returns:
            tuple: (predictions, probabilities)
        """
        if self.best_model is None:
            raise ValueError("No model has been trained yet")
        
        y_pred = self.best_model.predict(X)
        y_pred_proba = self.best_model.predict_proba(X)[:, 1]
        
        return y_pred, y_pred_proba
