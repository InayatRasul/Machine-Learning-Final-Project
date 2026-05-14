# Stroke Prediction System - Complete Setup Guide

## 🚀 Quick Start (1 Command)

### For Linux/Mac:
```bash
bash start.sh
```

This will:
1. ✓ Create virtual environment
2. ✓ Install all dependencies
3. ✓ Train the model (if needed)
4. ✓ Start all services (API, UI, MLflow)
5. ✓ Display access URLs

### For Windows:
```bash
python run_pipeline.py
```

---

## 📋 Prerequisites

- Python 3.8+
- pip (Python package manager)
- 4GB RAM minimum
- Internet connection (for first-time dependency download)

---

## 🔧 Manual Setup (Step-by-Step)

### Step 1: Navigate to Project Directory
```bash
cd final-project
```

### Step 2: Create Virtual Environment
```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Train the Model
```bash
python main.py
```

This will:
- Load and explore the dataset
- Preprocess and prepare features
- Train 3 ML models (Logistic Regression, Random Forest, Gradient Boosting)
- Evaluate models and select the best one
- Save models and log metrics to MLflow
- Display results

### Step 5: Start the API Backend
In a new terminal (keep venv activated):
```bash
python app.py
```

The API will be available at: `http://localhost:8000`

### Step 6: Start the Web UI
In another terminal (keep venv activated):
```bash
streamlit run streamlit_app.py
```

The UI will be available at: `http://localhost:8501`

### Step 7: View MLflow Dashboard (Optional)
In another terminal (keep venv activated):
```bash
mlflow ui --host 0.0.0.0 --port 5000
```

MLflow dashboard will be available at: `http://localhost:5000`

---

## 🌐 Access Points

Once everything is running, you can access:

1. **Main Web Interface (Streamlit)**
   - URL: http://localhost:8501
   - Purpose: Make predictions, view results, analyze data
   - Features: Single prediction, batch analysis, statistics

2. **API Backend (FastAPI)**
   - URL: http://localhost:8000
   - Swagger Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc
   - Purpose: REST API for predictions

3. **MLflow Dashboard**
   - URL: http://localhost:5000
   - Purpose: Track experiments, view metrics, monitor models

---

## 📊 Using the System

### Single Patient Prediction (Web UI)
1. Open http://localhost:8501
2. Click "🔮 Prediction" tab
3. Enter patient information:
   - Demographics (age, gender, marital status, etc.)
   - Medical history (hypertension, heart disease)
   - Health metrics (glucose level, BMI, smoking status)
4. Click "Get Prediction"
5. View results with risk level and probability

### Batch Analysis (Web UI)
1. Open http://localhost:8501
2. Click "📊 Batch Analysis" tab
3. Upload CSV file with patient data
4. Click "Process Batch"
5. View statistics and visualizations

### API Prediction (Programmatic)
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "gender": "Male",
    "age": 50,
    "hypertension": 0,
    "heart_disease": 0,
    "ever_married": "Yes",
    "work_type": "Private",
    "Residence_type": "Urban",
    "avg_glucose_level": 120.5,
    "bmi": 25.0,
    "smoking_status": "never smoked"
  }'
```

### View Training Metrics
1. Open http://localhost:5000
2. Click on "Stroke_Prediction_Experiment"
3. View model metrics, parameters, and artifacts

---

## 🛑 Stopping Services

### If using start.sh or run_pipeline.py:
Press `Ctrl+C` to stop all services gracefully

### Manual Services:
Stop each terminal with `Ctrl+C`:
- Streamlit UI: `Ctrl+C`
- API: `Ctrl+C`
- MLflow: `Ctrl+C`

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution**: Make sure virtual environment is activated and dependencies are installed
```bash
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

### Issue: "Port already in use"
**Solution**: Change port or kill the process using the port
```bash
# Linux/Mac - kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Issue: "Model not found" (API error)
**Solution**: Train the model first
```bash
python main.py
```

### Issue: "Connection refused" (Streamlit to API)
**Solution**: Make sure API is running in another terminal
```bash
python app.py
```

### Issue: Memory error during training
**Solution**: Reduce dataset size or close other applications

---

## 📁 Project Structure

```
final-project/
├── main.py                          # Entry point for training
├── app.py                           # FastAPI backend
├── streamlit_app.py                 # Web UI
├── train.py                         # Training pipeline
├── predict.py                       # Prediction utilities
├── run_pipeline.py                  # Orchestration script
├── start.sh                         # Quick start script
│
├── data/
│   ├── raw/
│   │   └── StrockDataset.csv        # Raw dataset
│   └── processed/
│
├── src/
│   ├── data_loader.py               # Data loading
│   ├── preprocessing.py             # Feature preprocessing
│   ├── models.py                    # ML models
│   ├── utils.py                     # Utilities
│   └── mlflow_utils.py              # MLflow integration
│
├── models/
│   ├── best_model.joblib            # Trained model
│   ├── logistic_regression_model.joblib
│   ├── random_forest_model.joblib
│   └── gradient_boosting_model.joblib
│
├── notebooks/
│   └── Stroke_Prediction_Analysis.ipynb
│
├── results/
│   ├── evaluation_report.txt
│   └── model_evaluation_results.csv
│
├── mlruns/                          # MLflow tracking data
│
└── venv/                            # Virtual environment
```

---

## 📚 API Documentation

### GET /
Returns API information and available endpoints

### GET /health
Returns API health status

### POST /predict
Make a single prediction
```json
{
  "gender": "Male",
  "age": 50,
  "hypertension": 0,
  "heart_disease": 0,
  "ever_married": "Yes",
  "work_type": "Private",
  "Residence_type": "Urban",
  "avg_glucose_level": 120.5,
  "bmi": 25.0,
  "smoking_status": "never smoked"
}
```

### POST /batch_predict
Make multiple predictions at once

### GET /model_info
Get information about the loaded model

### GET /docs
Swagger UI for interactive API exploration

### GET /redoc
ReDoc for API documentation

---

## 🎯 Model Performance

The trained models are evaluated on:
- Accuracy: Percentage of correct predictions
- Precision: True positives / (True positives + False positives)
- Recall: True positives / (True positives + False negatives)
- F1-Score: Harmonic mean of precision and recall
- ROC-AUC: Area under receiver operating characteristic curve

View detailed metrics in:
1. Console output after training
2. MLflow dashboard at http://localhost:5000
3. Results file at `results/evaluation_report.txt`

---

## 🔄 Retraining the Model

To retrain with the latest data:
```bash
python main.py
```

This will:
- Reload data
- Retrain all models
- Update metrics in MLflow
- Save new models

---

## 🚢 Docker Deployment (Optional)

Build Docker image:
```bash
docker build -t stroke-predictor .
```

Run containers:
```bash
docker-compose up
```

---

## ❓ FAQ

**Q: How long does training take?**
A: Typically 2-5 minutes depending on system specs

**Q: Can I use the API without the UI?**
A: Yes! The API is fully independent - use curl, Python, JavaScript, etc.

**Q: What's the model accuracy?**
A: Check results after training or view in MLflow dashboard (~92% typically)

**Q: Can I add more models?**
A: Yes, modify `src/models.py` and `train.py`

**Q: How do I deploy to production?**
A: Use Docker, see Docker Deployment section

---

## 📞 Support

For issues:
1. Check Troubleshooting section above
2. Review console error messages
3. Check MLflow dashboard for training errors
4. Review code documentation in comments

---

## 📝 License

University Final Project - Machine Learning

---

Made with ❤️ for healthcare ML
