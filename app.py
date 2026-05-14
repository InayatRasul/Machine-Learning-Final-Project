"""
FastAPI Backend for Stroke Prediction
Provides REST API for model predictions with MLflow tracking.
"""

import sys
from pathlib import Path
from typing import Dict, Optional
import logging

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib
import mlflow
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Stroke Risk Prediction API",
    description="API for predicting stroke risk based on patient health data",
    version="1.0.0"
)

# Add CORS middleware for Streamlit communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model cache
_model = None
_model_path = Path(__file__).parent / 'models' / 'best_model.joblib'


class PatientData(BaseModel):
    """Patient data model for prediction."""
    gender: str
    age: float
    hypertension: int
    heart_disease: int
    ever_married: str
    work_type: str
    Residence_type: str
    avg_glucose_level: float
    bmi: float
    smoking_status: str


class PredictionResponse(BaseModel):
    """Prediction response model."""
    stroke_risk: int
    probability: float
    risk_level: str
    confidence: float


def load_model():
    """Load the trained model."""
    global _model
    if _model is None:
        if not _model_path.exists():
            raise FileNotFoundError(f"Model not found at {_model_path}")
        _model = joblib.load(_model_path)
        logger.info(f"Model loaded from {_model_path}")
    return _model


def log_prediction_to_mlflow(patient_data: PatientData, prediction: int, probability: float):
    """Log prediction to MLflow for monitoring."""
    try:
        mlflow.set_tracking_uri("file:./mlruns")
        with mlflow.start_run(run_name="inference"):
            mlflow.log_param("age", patient_data.age)
            mlflow.log_param("gender", patient_data.gender)
            mlflow.log_param("hypertension", patient_data.hypertension)
            mlflow.log_param("heart_disease", patient_data.heart_disease)
            mlflow.log_metric("prediction", prediction)
            mlflow.log_metric("probability", probability)
    except Exception as e:
        logger.warning(f"Could not log to MLflow: {e}")


@app.on_event("startup")
async def startup_event():
    """Load model on startup."""
    try:
        load_model()
        logger.info("API startup successful")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Stroke Risk Prediction API",
        "endpoints": {
            "predict": "/predict",
            "batch_predict": "/batch_predict",
            "health": "/health",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        model = load_model()
        return {
            "status": "healthy",
            "model_loaded": model is not None
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }


@app.post("/predict", response_model=PredictionResponse)
async def predict(patient_data: PatientData, background_tasks: BackgroundTasks):
    """
    Predict stroke risk for a single patient.
    
    Args:
        patient_data: Patient health information
        
    Returns:
        PredictionResponse: Prediction with probability and confidence
    """
    try:
        model = load_model()
        
        # Convert to DataFrame
        data_dict = patient_data.dict()
        df = pd.DataFrame([data_dict])
        
        # Make prediction
        prediction = model.predict(df)[0]
        probability = model.predict_proba(df)[0, 1]
        confidence = max(probability, 1 - probability)
        
        # Determine risk level
        risk_level = "HIGH RISK" if prediction == 1 else "LOW RISK"
        
        # Log prediction in background
        background_tasks.add_task(log_prediction_to_mlflow, patient_data, prediction, probability)
        
        return PredictionResponse(
            stroke_risk=int(prediction),
            probability=float(probability),
            risk_level=risk_level,
            confidence=float(confidence)
        )
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/batch_predict")
async def batch_predict(patients: list[PatientData]):
    """
    Predict stroke risk for multiple patients.
    
    Args:
        patients: List of patient health information
        
    Returns:
        dict: List of predictions with details
    """
    try:
        model = load_model()
        
        # Convert to DataFrame
        data_list = [p.dict() for p in patients]
        df = pd.DataFrame(data_list)
        
        # Make predictions
        predictions = model.predict(df)
        probabilities = model.predict_proba(df)[:, 1]
        
        # Format results
        results = []
        for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
            confidence = max(prob, 1 - prob)
            risk_level = "HIGH RISK" if pred == 1 else "LOW RISK"
            results.append({
                "patient_id": i,
                "stroke_risk": int(pred),
                "probability": float(prob),
                "risk_level": risk_level,
                "confidence": float(confidence)
            })
        
        return {
            "total_patients": len(patients),
            "predictions": results
        }
    except Exception as e:
        logger.error(f"Batch prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/model_info")
async def model_info():
    """Get information about the loaded model."""
    try:
        model = load_model()
        return {
            "model_type": type(model).__name__,
            "model_path": str(_model_path),
            "n_features": model.named_steps['preprocessor'].n_features_in_
            if hasattr(model.named_steps['preprocessor'], 'n_features_in_') else "unknown"
        }
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    print("\n" + "="*70)
    print("Starting Stroke Prediction API")
    print("="*70)
    print("\nAPI Documentation: http://localhost:8000/docs")
    print("="*70 + "\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
