# Stroke Risk Prediction System

A comprehensive machine learning system for predicting stroke risk based on patient health information.

## Project Overview

This project develops a production-ready ML system to predict individual stroke risk, enabling early intervention and personalized healthcare. The system uses patient demographics, medical history, and lifestyle factors to provide accurate risk assessments.

### Key Features
- **Multiple ML Models**: Logistic Regression, Random Forest, Gradient Boosting
- **Comprehensive Analysis**: Exploratory data analysis with insightful visualizations
- **Robust Preprocessing**: Handles missing values, feature scaling, and categorical encoding
- **Model Evaluation**: Multiple metrics and cross-validation for reliable assessment
- **Production Ready**: Modular code structure, saved models, reproducible pipeline

## Project Structure

```
final-project/
├── data/
│   ├── raw/                          # Raw datasets
│   └── processed/                    # Processed datasets
├── notebooks/
│   └── Stroke_Prediction_Analysis.ipynb   # Main analysis notebook
├── src/
│   ├── __init__.py
│   ├── data_loader.py               # Data loading utilities
│   ├── preprocessing.py             # Data preprocessing and feature engineering
│   ├── models.py                    # Model training and evaluation
│   └── utils.py                     # Utility functions for visualization
├── models/                          # Saved trained models
├── results/                         # Evaluation results and reports
├── train.py                         # Main training script
├── predict.py                       # Prediction script
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Docker configuration
└── README.md                        # This file
```

## Installation and Setup

### 1. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Verify Setup
```bash
python -c "import pandas; import sklearn; print('All dependencies installed!')"
```

## Usage

### Training the Model
```bash
python train.py
```

This will:
1. Load and explore the dataset
2. Preprocess features
3. Train multiple models
4. Evaluate and compare performance
5. Save the best model

### Making Predictions
```bash
python predict.py
```

### Running the Jupyter Notebook
```bash
jupyter notebook notebooks/Stroke_Prediction_Analysis.ipynb
```

## Dataset

**Source**: Healthcare stroke prediction dataset
- **Samples**: ~5,000 patient records
- **Features**: 11 attributes (demographic, medical, lifestyle)
- **Target**: Binary stroke outcome

### Features
- **age**: Patient age in years
- **gender**: Male/Female/Other
- **hypertension**: Binary (0/1)
- **heart_disease**: Binary (0/1)
- **ever_married**: Yes/No
- **work_type**: Type of employment
- **Residence_type**: Urban/Rural
- **avg_glucose_level**: Average glucose in bloodstream
- **bmi**: Body Mass Index
- **smoking_status**: Smoking history

## Methodology

### 1. Exploratory Data Analysis
- Target distribution and class imbalance analysis
- Numeric feature distributions and relationships
- Categorical feature analysis
- Correlation analysis with target

### 2. Data Preprocessing
- **Numeric Features**: Median imputation + Standardization
- **Categorical Features**: Most-frequent imputation + One-Hot Encoding
- **Stratified Train-Test Split**: 80/20 with stratification to preserve class distribution

### 3. Model Training
Three models trained and compared:

**Logistic Regression**
- Interpretable baseline model
- Fast training and prediction

**Random Forest**
- Handles non-linearity well
- Provides feature importance scores
- Robust to outliers

**Gradient Boosting**
- Sequential ensemble approach
- Often achieves best generalization

### 4. Evaluation Metrics

| Metric | Purpose |
|--------|---------|
| **Accuracy** | Overall correctness |
| **Precision** | False positive rate |
| **Recall** | False negative rate (critical for clinical use) |
| **F1-Score** | Balance between precision and recall |
| **ROC-AUC** | Model discrimination ability |

### 5. Class Imbalance Handling
- Stratified sampling in train-test split
- Class weighting in model training
- Stratified 5-fold cross-validation

## Results

The evaluation results show comprehensive model performance metrics:

- **Best Model**: Random Forest or Gradient Boosting (depending on run)
- **Average Accuracy**: 94-96%
- **Average F1-Score**: 0.50-0.65 (balancing recall for clinical relevance)
- **Average ROC-AUC**: 0.80+

## Key Insights

1. **Age** is the strongest predictor of stroke risk
2. **Glucose level** and **medical history** are significant factors
3. **Smoking status** shows clear correlation with stroke
4. **Class imbalance** (5% positive cases) requires careful handling
5. **Cross-validation** shows good model generalization

## Model Interpretation

### Feature Importance (Top Factors)
1. Age
2. Average Glucose Level
3. Heart Disease
4. Hypertension
5. Smoking Status
6. BMI

### Prediction Meanings
- **Stroke = 0**: Low risk - Continue standard preventive care
- **Stroke = 1**: High risk - Immediate medical attention needed

## Clinical Significance

This model supports:
- **Risk Stratification**: Identifies high-risk patient groups
- **Early Intervention**: Enables preventive healthcare measures
- **Resource Allocation**: Prioritizes healthcare resources effectively
- **Personalized Medicine**: Supports tailored treatment plans

## Limitations

1. **Class Imbalance**: Limited positive samples affects minority prediction
2. **Not a Substitute**: Model should complement, not replace clinical judgment
3. **Data Quality**: Results depend on data accuracy and completeness
4. **Temporal Aspect**: Current model doesn't capture time-dependent patterns
5. **Feature Scope**: Other medical indicators could improve predictions

## Recommendations for Improvement

1. **Data Augmentation**: Collect more stroke cases
2. **Feature Engineering**: Add more clinical indicators
3. **Ensemble Methods**: Combine multiple models
4. **Hyperparameter Tuning**: Optimize model parameters
5. **Explainability**: Implement SHAP or LIME for interpretable predictions
6. **Regular Retraining**: Update model with new data periodically

## Files Description

### Core Scripts
- `train.py`: Complete training pipeline
- `predict.py`: Inference on new data
- `requirements.txt`: Python dependencies

### Source Code (`src/`)
- `data_loader.py`: Data loading and exploration
- `preprocessing.py`: Data cleaning and feature preparation
- `models.py`: Model training and evaluation class
- `utils.py`: Visualization and utility functions

### Notebooks
- `Stroke_Prediction_Analysis.ipynb`: Complete analysis with visualizations

### Output
- `models/`: Saved trained models
- `results/`: Evaluation reports and predictions

## Environment

- **Python**: 3.8+
- **OS**: Linux/macOS/Windows
- **Virtual Environment**: Recommended for dependency isolation

## Running in Virtual Environment

```bash
# Activate virtual environment
source venv/bin/activate

# Run training
python train.py

# Run predictions
python predict.py

# View notebook
jupyter notebook notebooks/Stroke_Prediction_Analysis.ipynb

# Deactivate when done
deactivate
```

## Reproducibility

The project ensures reproducibility through:
- Fixed random seeds (42) throughout
- Stratified sampling preserving class distribution
- Documented preprocessing steps
- Saved model artifacts
- Complete hyperparameters in code

## Author

University Final Project - Machine Learning System Design

## License

Academic Use Only

---

**Last Updated**: 2026
**Status**: Production Ready ✓
