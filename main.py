"""
Main Entry Point for Stroke Prediction System
Runs the complete ML pipeline with MLflow tracking.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from train import main as train_main


if __name__ == "__main__":
    # Run training pipeline
    predictor, results_df = train_main()
    
    print("\n" + "="*70)
    print("NEXT STEPS:")
    print("="*70)
    print("\n1. View MLflow UI:")
    print("   mlflow ui --host 0.0.0.0 --port 5000")
    print("\n2. Run Streamlit App:")
    print("   streamlit run streamlit_app.py")
    print("\n3. Run FastAPI Backend:")
    print("   python app.py")
    print("\n" + "="*70 + "\n")
