"""
Utility Functions
Various utility functions for analysis and visualization.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


def set_plot_style():
    """Set matplotlib and seaborn style."""
    plt.style.use('seaborn-v0_8-darkgrid')
    sns.set_palette("husl")
    plt.rcParams['figure.figsize'] = (12, 6)
    plt.rcParams['font.size'] = 10


def save_figure(fig, filepath, dpi=300, bbox_inches='tight'):
    """
    Save figure to file.
    
    Args:
        fig (matplotlib.figure.Figure): Figure object
        filepath (str): Path to save figure
        dpi (int): Resolution
        bbox_inches (str): Bbox setting
    """
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, dpi=dpi, bbox_inches=bbox_inches)
    print(f"Figure saved to {filepath}")


def plot_distribution(data, column, title=None, bins=30):
    """
    Plot distribution of a column.
    
    Args:
        data (pd.DataFrame): Input dataframe
        column (str): Column name
        title (str): Plot title
        bins (int): Number of bins
        
    Returns:
        matplotlib.figure.Figure: Figure object
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(data[column], bins=bins, edgecolor='black', alpha=0.7)
    ax.set_xlabel(column)
    ax.set_ylabel('Frequency')
    ax.set_title(title or f'Distribution of {column}')
    plt.tight_layout()
    return fig


def plot_categorical(data, column, hue=None, title=None):
    """
    Plot categorical distribution.
    
    Args:
        data (pd.DataFrame): Input dataframe
        column (str): Column name
        hue (str): Column for color coding
        title (str): Plot title
        
    Returns:
        matplotlib.figure.Figure: Figure object
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    
    if hue:
        sns.countplot(data=data, x=column, hue=hue, ax=ax)
    else:
        sns.countplot(data=data, x=column, ax=ax)
    
    ax.set_title(title or f'Distribution of {column}')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


def plot_correlation_heatmap(data, numeric_cols, title='Correlation Heatmap'):
    """
    Plot correlation heatmap.
    
    Args:
        data (pd.DataFrame): Input dataframe
        numeric_cols (list): List of numeric column names
        title (str): Plot title
        
    Returns:
        matplotlib.figure.Figure: Figure object
    """
    fig, ax = plt.subplots(figsize=(12, 10))
    corr_matrix = data[numeric_cols].corr()
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                center=0, square=True, ax=ax, cbar_kws={"shrink": 0.8})
    ax.set_title(title)
    plt.tight_layout()
    return fig


def plot_comparison(feature, target, data, title=None):
    """
    Plot feature vs target using boxplot.
    
    Args:
        feature (str): Feature column name
        target (str): Target column name
        data (pd.DataFrame): Input dataframe
        title (str): Plot title
        
    Returns:
        matplotlib.figure.Figure: Figure object
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(data=data, x=target, y=feature, ax=ax, palette='Set2')
    ax.set_title(title or f'{feature} vs {target}')
    plt.tight_layout()
    return fig


def plot_roc_curve(fpr, tpr, auc_score, model_name='Model', ax=None):
    """
    Plot ROC curve.
    
    Args:
        fpr (array): False positive rate
        tpr (array): True positive rate
        auc_score (float): AUC score
        model_name (str): Model name
        ax (matplotlib.axes.Axes): Axes object
        
    Returns:
        matplotlib.figure.Figure or None: Figure object if ax is None
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))
    else:
        fig = None
    
    ax.plot(fpr, tpr, label=f'{model_name} (AUC = {auc_score:.3f})', linewidth=2)
    ax.plot([0, 1], [0, 1], 'k--', linewidth=1, label='Random Classifier')
    ax.set_xlabel('False Positive Rate')
    ax.set_ylabel('True Positive Rate')
    ax.set_title('ROC Curve')
    ax.legend()
    ax.grid(alpha=0.3)
    
    if fig:
        plt.tight_layout()
        return fig


def plot_confusion_matrix(cm, model_name='Model', ax=None):
    """
    Plot confusion matrix.
    
    Args:
        cm (array): Confusion matrix
        model_name (str): Model name
        ax (matplotlib.axes.Axes): Axes object
        
    Returns:
        matplotlib.figure.Figure or None: Figure object if ax is None
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))
    else:
        fig = None
    
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
                xticklabels=['No Stroke', 'Stroke'],
                yticklabels=['No Stroke', 'Stroke'])
    ax.set_title(f'Confusion Matrix - {model_name}')
    ax.set_xlabel('Predicted')
    ax.set_ylabel('Actual')
    
    if fig:
        plt.tight_layout()
        return fig


def plot_feature_importance(feature_imp_df, title='Feature Importance', ax=None):
    """
    Plot feature importance.
    
    Args:
        feature_imp_df (pd.DataFrame): Feature importance dataframe
        title (str): Plot title
        ax (matplotlib.axes.Axes): Axes object
        
    Returns:
        matplotlib.figure.Figure or None: Figure object if ax is None
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
    else:
        fig = None
    
    ax.barh(feature_imp_df['Feature'], feature_imp_df['Importance'])
    ax.set_xlabel('Importance')
    ax.set_title(title)
    ax.invert_yaxis()
    
    if fig:
        plt.tight_layout()
        return fig
    
    return None


def create_summary_report(results_df, filepath=None):
    """
    Create a summary report of model evaluation.
    
    Args:
        results_df (pd.DataFrame): Results dataframe
        filepath (str): Path to save report
        
    Returns:
        str: Report text
    """
    report = "\n" + "="*60 + "\n"
    report += "MODEL EVALUATION REPORT\n"
    report += "="*60 + "\n\n"
    
    report += results_df.to_string(index=False)
    report += "\n\n" + "="*60 + "\n"
    
    if filepath:
        with open(filepath, 'w') as f:
            f.write(report)
    
    return report
