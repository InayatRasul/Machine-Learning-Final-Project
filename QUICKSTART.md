# Quick Start Guide - Stroke Prediction ML System

## ⚡ 5-Minute Quick Start

### 1. Setup Virtual Environment (First Time Only)
```bash
cd final-project
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Train the Model
```bash
python train.py
```
✓ Trains 3 models and selects the best one  
✓ Saves models to `models/` folder  
✓ Generates evaluation report  

**Expected Output**: 
```
Best Model: Logistic Regression
Accuracy: 74.56%
F1-Score: 0.2353
ROC-AUC: 0.8436
```

### 3. Make Predictions
```bash
python predict.py
```

**Output Example**:
```
Stroke Risk: HIGH RISK
Probability: 82.56%
Confidence: 82.56%
```

## 📊 Explore Analysis Notebook

```bash
jupyter notebook notebooks/Stroke_Prediction_Analysis.ipynb
```

**Includes**:
- Exploratory Data Analysis (EDA)
- Data preprocessing steps
- Model training and evaluation
- Feature importance analysis
- Visualizations and insights

## 📁 Project Structure

```
final-project/
├── data/raw/                               # Raw dataset
├── src/                                    # Python modules
│   ├── data_loader.py                     # Load and explore data
│   ├── preprocessing.py                   # Feature engineering
│   ├── models.py                          # Model training
│   └── utils.py                           # Visualization
├── models/                                # Saved trained models
├── results/                               # Evaluation reports
├── notebooks/Stroke_Prediction_Analysis.ipynb
├── train.py                               # Training script
├── predict.py                             # Prediction script
├── README.md                              # Full documentation
├── ARCHITECTURE.md                        # System architecture
├── SYSTEM_LOGIC.md                        # Clinical perspective
└── requirements.txt                       # Dependencies
```

## 🔧 Available Commands

### Training
```bash
# Full training pipeline
python train.py

# Outputs:
# - models/best_model.joblib
# - models/logistic_regression_model.joblib
# - models/random_forest_model.joblib
# - models/gradient_boosting_model.joblib
# - results/evaluation_report.txt
```

### Predictions
```bash
# Make predictions on new data
python predict.py

# Uses best_model.joblib for inference
```

### Jupyter Notebook
```bash
# Start Jupyter server
jupyter notebook

# Open: notebooks/Stroke_Prediction_Analysis.ipynb
# Features:
# - Complete EDA
# - Model training walkthrough
# - Evaluation metrics
# - Visualizations
```

### Virtual Environment
```bash
# Activate
source venv/bin/activate

# Deactivate
deactivate
```

## 📈 Model Performance

| Metric | Logistic Regression | Random Forest | Gradient Boosting |
|--------|-------------------|----------------|-------------------|
| Accuracy | 74.56% | 95.01% | 95.11% |
| Precision | 13.79% | 0.00% | 50.00% |
| Recall | 80.00% | 0.00% | 4.00% |
| F1-Score | 23.53% | 0.00% | 7.41% |
| ROC-AUC | 0.8436 | 0.7967 | 0.8159 |

**Best Model**: Logistic Regression (High recall for clinical use)

## 💡 Key Insights

### Top Risk Factors
1. **Age** - Strongest predictor
2. **Glucose Level** - Significant indicator
3. **Heart Disease** - Important comorbidity
4. **Hypertension** - Major risk factor
5. **Smoking Status** - Clear correlation

### Dataset Info
- **Samples**: 5,110 patients
- **Features**: 10 health indicators
- **Target**: Stroke outcome (95% no stroke, 5% stroke)
- **Class Balance**: Handled through stratified split and class weighting

## 🚀 Features

✓ **Multiple Models**: Compare 3 different algorithms  
✓ **Comprehensive EDA**: Understand your data  
✓ **Robust Preprocessing**: Handle missing values and scaling  
✓ **Model Evaluation**: Multiple metrics and cross-validation  
✓ **Feature Importance**: Identify key risk factors  
✓ **Production Ready**: Save and load models easily  
✓ **Well Documented**: Clear code with docstrings  
✓ **Reproducible**: Fixed random seeds  

## 🔍 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'pandas'"
**Solution**: Ensure virtual environment is activated
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "FileNotFoundError: Dataset not found"
**Solution**: Ensure dataset is in correct location
```bash
ls data/raw/StrockDataset.csv  # Should exist
```

### Issue: Jupyter notebook not starting
**Solution**: Install jupyter in virtual environment
```bash
source venv/bin/activate
pip install jupyter
```

### Issue: Model file not found when predicting
**Solution**: Train the model first
```bash
python train.py  # Creates models/best_model.joblib
python predict.py
```

## 📚 Documentation Files

- **README.md** - Complete project documentation
- **ARCHITECTURE.md** - System design and data flow
- **SYSTEM_LOGIC.md** - Clinical use cases and business logic
- **requirements.txt** - Python dependencies
- **This file** - Quick start guide

## 💻 System Requirements

- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Disk**: 500MB for installation
- **OS**: Linux, macOS, or Windows

## 🎯 Next Steps

1. **Understand the data**: Run EDA in notebook
2. **Train models**: Execute `python train.py`
3. **Evaluate results**: Review `results/evaluation_report.txt`
4. **Make predictions**: Run `python predict.py`
5. **Explore code**: Check `src/` modules for details
6. **Deploy**: Integrate into your system

## 📖 Learning Resources

- **Jupyter Notebook**: Full workflow with explanations
- **Source Code**: Well-documented modules in `src/`
- **Architecture**: Complete system design in ARCHITECTURE.md
- **Clinical Logic**: Real-world applications in SYSTEM_LOGIC.md

## ✅ Verification Checklist

After setup, verify everything works:

```bash
# ✓ Data exists
ls data/raw/StrockDataset.csv

# ✓ Modules loadable
python -c "import src.data_loader; print('OK')"

# ✓ Training works
python train.py

# ✓ Predictions work
python predict.py

# ✓ Notebook opens
jupyter notebook notebooks/Stroke_Prediction_Analysis.ipynb
```

## 🔐 Important Notes

1. **Always use virtual environment** to isolate dependencies
2. **Train before predicting** - model must exist first
3. **Use stratified split** - preserves class distribution
4. **Model is supplementary** - complements clinical judgment
5. **Regular retraining recommended** with new data

## 📞 Support

For issues or questions:
1. Check the README.md for detailed documentation
2. Review ARCHITECTURE.md for system design
3. See SYSTEM_LOGIC.md for clinical applications
4. Check source code comments in `src/`

## 🏆 Project Highlights

✨ **Complete ML Pipeline**: Data → Model → Prediction  
✨ **Production Ready**: Saved models, error handling  
✨ **Well Structured**: Modular code, clear separation  
✨ **Thoroughly Documented**: Code comments and guides  
✨ **Evaluated Models**: Multiple metrics and cross-validation  
✨ **Reproducible**: Fixed random seeds, documented process  

---

**Version**: 1.0  
**Status**: ✓ Ready to Use  
**Last Updated**: 2026-05-14  

Happy analyzing! 🎉
