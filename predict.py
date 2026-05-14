"""
Prediction Script
Make predictions on new data using the trained model.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import joblib

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))


def load_trained_model(model_path='models/best_model.joblib'):
    """Load trained model."""
    model_path = Path(model_path)
    if not model_path.exists():
        raise FileNotFoundError(f"Model not found at {model_path}")
    return joblib.load(model_path)


def make_prediction(model, data):
    """
    Make predictions on new data.
    
    Args:
        model: Trained sklearn pipeline
        data (dict or pd.DataFrame): Input data
        
    Returns:
        tuple: (predictions, probabilities)
    """
    if isinstance(data, dict):
        data = pd.DataFrame([data])
    
    predictions = model.predict(data)
    probabilities = model.predict_proba(data)[:, 1]
    
    return predictions, probabilities


def format_prediction(prediction, probability):
    """Format prediction output."""
    risk_level = "HIGH RISK" if prediction == 1 else "LOW RISK"
    return {
        'prediction': int(prediction),
        'risk_level': risk_level,
        'stroke_probability': float(probability),
        'confidence': max(probability, 1 - probability)
    }


def main():
    """Main prediction function."""
    
    print("\n" + "="*70)
    print("STROKE RISK PREDICTION - INFERENCE")
    print("="*70 + "\n")
    
    # Load model
    try:
        model = load_trained_model()
        print("✓ Model loaded successfully!\n")
    except FileNotFoundError as e:
        print(f"✗ Error: {e}")
        print("Please train the model first using: python train.py")
        return
    
    # Example prediction
    example_data = {
        'gender': 'Male',
        'age': 67.0,
        'hypertension': 0,
        'heart_disease': 1,
        'ever_married': 'Yes',
        'work_type': 'Private',
        'Residence_type': 'Urban',
        'avg_glucose_level': 228.69,
        'bmi': 36.6,
        'smoking_status': 'formerly smoked'
    }
    
    print("Example Patient Data:")
    for key, value in example_data.items():
        print(f"  {key}: {value}")
    
    # Make prediction
    prediction, probability = make_prediction(model, example_data)
    result = format_prediction(prediction[0], probability[0])
    
    print(f"\nPrediction Results:")
    print(f"  Stroke Risk: {result['risk_level']}")
    print(f"  Probability: {result['stroke_probability']:.2%}")
    print(f"  Confidence: {result['confidence']:.2%}")
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
