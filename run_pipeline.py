#!/usr/bin/env python
"""
Complete Pipeline Orchestration
Manages training, API, and UI components with MLflow dashboard.
"""

import subprocess
import sys
import time
import signal
import os
from pathlib import Path

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*70}")
    print(f"{text}")
    print(f"{'='*70}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def check_model_exists():
    """Check if trained model exists."""
    model_path = Path("models/best_model.joblib")
    return model_path.exists()

def run_training():
    """Run the training pipeline."""
    print_header("STEP 1: TRAINING THE MODEL")
    print_info("Starting model training with MLflow tracking...")
    
    try:
        result = subprocess.run(
            ["python", "main.py"],
            capture_output=False,
            timeout=3600
        )
        if result.returncode == 0:
            print_success("Model training completed successfully!")
            return True
        else:
            print_error("Training failed!")
            return False
    except subprocess.TimeoutExpired:
        print_error("Training timed out!")
        return False
    except Exception as e:
        print_error(f"Training error: {e}")
        return False

def main():
    """Main orchestration function."""
    
    print_header("STROKE PREDICTION SYSTEM - COMPLETE PIPELINE")
    
    # Check if model exists
    if not check_model_exists():
        print_warning("No trained model found. Training is required.")
        
        if not run_training():
            print_error("Training failed. Cannot proceed.")
            sys.exit(1)
    else:
        print_success("Trained model found! Skipping training...")
    
    print_header("STEP 2: SYSTEM STARTUP")
    
    processes = []
    
    try:
        # Start API
        print_info("Starting FastAPI backend (port 8000)...")
        api_proc = subprocess.Popen(
            ["python", "app.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        processes.append(("API", api_proc))
        print_success("API started!")
        time.sleep(2)  # Wait for API to start
        
        # Start MLflow UI
        print_info("Starting MLflow UI (port 5000)...")
        mlflow_proc = subprocess.Popen(
            ["mlflow", "ui", "--host", "0.0.0.0", "--port", "5000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        processes.append(("MLflow", mlflow_proc))
        print_success("MLflow UI started!")
        time.sleep(2)  # Wait for MLflow to start
        
        # Start Streamlit UI
        print_info("Starting Streamlit frontend (port 8501)...")
        streamlit_proc = subprocess.Popen(
            ["streamlit", "run", "streamlit_app.py", "--server.port=8501"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        processes.append(("Streamlit", streamlit_proc))
        print_success("Streamlit UI started!")
        
        print_header("SYSTEM RUNNING")
        
        print("\n" + Colors.BOLD + Colors.OKGREEN + "📊 SYSTEM COMPONENTS:" + Colors.ENDC)
        print(f"  🔌 API Backend:      http://localhost:8000")
        print(f"     - Swagger Docs:  http://localhost:8000/docs")
        print(f"     - ReDoc:         http://localhost:8000/redoc")
        print(f"\n  🎨 Web UI:           http://localhost:8501")
        print(f"\n  📈 MLflow Dashboard: http://localhost:5000")
        print(f"     - Experiments: Track all training runs")
        print(f"     - Models: View registered models")
        print(f"     - Artifacts: Check saved artifacts")
        
        print("\n" + Colors.BOLD + Colors.WARNING + "⌨️  CONTROLS:" + Colors.ENDC)
        print("  Press Ctrl+C to stop all services")
        
        print("\n" + Colors.BOLD + Colors.OKCYAN + "🚀 QUICK START:" + Colors.ENDC)
        print("  1. Go to http://localhost:8501 for the main interface")
        print("  2. Enter patient data to get predictions")
        print("  3. View MLflow metrics at http://localhost:5000")
        print("  4. API documentation at http://localhost:8000/docs")
        
        print("\n" + "="*70 + "\n")
        
        # Keep processes running
        while True:
            # Check if any process has died
            for name, proc in processes:
                if proc.poll() is not None:
                    print_error(f"{name} process has died!")
                    raise KeyboardInterrupt
            time.sleep(1)
            
    except KeyboardInterrupt:
        print_header("SHUTTING DOWN")
        
        # Terminate all processes
        for name, proc in processes:
            print_info(f"Stopping {name}...")
            proc.terminate()
            try:
                proc.wait(timeout=5)
                print_success(f"{name} stopped")
            except subprocess.TimeoutExpired:
                proc.kill()
                print_warning(f"{name} force killed")
        
        print_success("All services stopped!")
        sys.exit(0)
    except Exception as e:
        print_error(f"Error: {e}")
        # Cleanup
        for name, proc in processes:
            try:
                proc.terminate()
            except:
                pass
        sys.exit(1)

if __name__ == "__main__":
    main()
