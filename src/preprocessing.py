"""
Data Preprocessing Module
Handles data cleaning, feature engineering, and transformation.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer


def handle_missing_values(df, strategy='median'):
    """
    Handle missing values in the dataset.
    
    Args:
        df (pd.DataFrame): Input dataframe
        strategy (str): Imputation strategy ('median', 'mean', 'most_frequent')
        
    Returns:
        pd.DataFrame: Dataframe with missing values handled
    """
    df_cleaned = df.copy()
    
    # Get numeric columns
    numeric_cols = df_cleaned.select_dtypes(include=['float64', 'int64']).columns
    
    # Impute missing values
    imputer = SimpleImputer(strategy=strategy)
    df_cleaned[numeric_cols] = pd.DataFrame(
        imputer.fit_transform(df_cleaned[numeric_cols]),
        columns=numeric_cols,
        index=df_cleaned.index
    )
    
    # Remove rows with missing categorical values
    df_cleaned = df_cleaned.dropna()
    
    print(f"Missing values handled. Remaining rows: {len(df_cleaned)}")
    return df_cleaned


def remove_outliers(df, column, threshold=3):
    """
    Remove outliers using z-score method.
    
    Args:
        df (pd.DataFrame): Input dataframe
        column (str): Column name
        threshold (float): Z-score threshold
        
    Returns:
        pd.DataFrame: Dataframe without outliers
    """
    z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
    return df[z_scores < threshold]


def create_feature_preprocessor(numeric_features, categorical_features):
    """
    Create a preprocessing pipeline for features.
    
    Args:
        numeric_features (list): List of numeric column names
        categorical_features (list): List of categorical column names
        
    Returns:
        ColumnTransformer: Preprocessing pipeline
    """
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'))
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ],
        remainder='passthrough',
        n_jobs=1  # Avoid parallel processing issues
    )
    
    return preprocessor


def prepare_data(df, target_col='stroke', drop_cols=['id']):
    """
    Prepare data for model training.
    
    Args:
        df (pd.DataFrame): Input dataframe
        target_col (str): Target column name
        drop_cols (list): Columns to drop
        
    Returns:
        tuple: (X, y) feature and target arrays
    """
    # Handle missing values
    df_clean = handle_missing_values(df)
    
    # Drop unnecessary columns
    X = df_clean.drop(columns=[target_col] + drop_cols, errors='ignore')
    y = df_clean[target_col]
    
    return X, y


def get_feature_groups(X):
    """
    Get numeric and categorical features from X.
    
    Args:
        X (pd.DataFrame): Feature dataframe
        
    Returns:
        tuple: (numeric_features, categorical_features)
    """
    numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = X.select_dtypes(include=['object']).columns.tolist()
    
    return numeric_features, categorical_features
