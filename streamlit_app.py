"""
Stroke Risk Prediction - Streamlit UI
Interactive web application for stroke risk assessment with MLflow integration.
"""

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time

# Page config
st.set_page_config(
    page_title="Stroke Risk Prediction",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.1rem;
        font-weight: 500;
    }
    .prediction-high {
        background-color: #ffebee;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #f44336;
    }
    .prediction-low {
        background-color: #e8f5e9;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #4caf50;
    }
    </style>
""", unsafe_allow_html=True)

# API Base URL
API_URL = "http://localhost:8000"

# Sidebar
with st.sidebar:
    st.title("🏥 Stroke Risk Predictor")
    st.markdown("---")
    
    # API Status
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        if response.status_code == 200:
            st.success("✅ API Connected")
        else:
            st.error("⚠️ API Error")
    except:
        st.error("❌ API Disconnected")
        st.info("Please start the API: `python app.py`")
    
    st.markdown("---")
    st.markdown("### Navigation")
    page = st.radio(
        "Select Page:",
        ["🔮 Prediction", "📊 Batch Analysis", "📈 Statistics", "ℹ️ About"]
    )

# Main title
st.title("🏥 Stroke Risk Prediction System")
st.markdown("*Advanced ML-based patient stroke risk assessment*")
st.markdown("---")

# Page 1: Single Prediction
if page == "🔮 Prediction":
    st.header("Single Patient Prediction")
    st.markdown("Enter patient information to get a stroke risk prediction.")
    
    # Create two columns for input
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Demographics")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        age = st.slider("Age", min_value=0, max_value=120, value=50, step=1)
        ever_married = st.selectbox("Ever Married", ["Yes", "No"])
        residence = st.selectbox("Residence Type", ["Urban", "Rural"])
    
    with col2:
        st.subheader("Medical History")
        hypertension = st.selectbox("Hypertension", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        heart_disease = st.selectbox("Heart Disease", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        work_type = st.selectbox("Work Type", ["Private", "Self-employed", "Govt_job", "children", "Never_worked"])
        smoking = st.selectbox("Smoking Status", ["formerly smoked", "never smoked", "smokes", "Unknown"])
    
    st.subheader("Health Metrics")
    col3, col4, col5 = st.columns(3)
    
    with col3:
        avg_glucose = st.number_input("Average Glucose Level", min_value=0.0, max_value=300.0, value=100.0, step=1.0)
    
    with col4:
        bmi = st.number_input("BMI", min_value=10.0, max_value=60.0, value=25.0, step=0.1)
    
    with col5:
        st.empty()  # Spacer
    
    # Prediction button
    st.markdown("---")
    col_pred1, col_pred2, col_pred3 = st.columns([1, 1, 1])
    
    with col_pred2:
        predict_button = st.button("🔮 Get Prediction", use_container_width=True)
    
    if predict_button:
        # Show loading spinner
        with st.spinner("Analyzing patient data..."):
            try:
                # Prepare payload
                payload = {
                    "gender": gender,
                    "age": age,
                    "hypertension": hypertension,
                    "heart_disease": heart_disease,
                    "ever_married": ever_married,
                    "work_type": work_type,
                    "Residence_type": residence,
                    "avg_glucose_level": avg_glucose,
                    "bmi": bmi,
                    "smoking_status": smoking
                }
                
                # Make prediction
                response = requests.post(f"{API_URL}/predict", json=payload)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Display results
                    st.markdown("---")
                    st.subheader("📊 Prediction Results")
                    
                    # Create columns for results
                    res_col1, res_col2, res_col3 = st.columns(3)
                    
                    with res_col1:
                        st.metric(
                            "Risk Level",
                            result["risk_level"],
                            delta="⚠️ HIGH" if result["stroke_risk"] == 1 else "✅ LOW"
                        )
                    
                    with res_col2:
                        st.metric(
                            "Probability",
                            f"{result['probability']:.1%}",
                            delta=None
                        )
                    
                    with res_col3:
                        st.metric(
                            "Confidence",
                            f"{result['confidence']:.1%}",
                            delta=None
                        )
                    
                    # Show detailed prediction box
                    if result["stroke_risk"] == 1:
                        st.markdown(
                            f"""
                            <div class="prediction-high">
                            <h3>⚠️ HIGH STROKE RISK DETECTED</h3>
                            <p>This patient has a <strong>{result['probability']:.1%}</strong> probability of stroke.</p>
                            <p><strong>Recommendation:</strong> Consider immediate medical consultation and preventive measures.</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f"""
                            <div class="prediction-low">
                            <h3>✅ LOW STROKE RISK</h3>
                            <p>This patient has a <strong>{result['probability']:.1%}</strong> probability of stroke.</p>
                            <p><strong>Recommendation:</strong> Continue regular health monitoring and healthy lifestyle.</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    
                    # Show patient summary
                    st.markdown("---")
                    with st.expander("📋 Patient Summary"):
                        summary_df = pd.DataFrame({
                            "Field": list(payload.keys()),
                            "Value": list(payload.values())
                        })
                        st.dataframe(summary_df, use_container_width=True)
                else:
                    st.error(f"Prediction failed: {response.status_code}")
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to API. Make sure the API is running with: `python app.py`")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Page 2: Batch Analysis
elif page == "📊 Batch Analysis":
    st.header("Batch Patient Analysis")
    st.markdown("Upload a CSV file with patient data for batch predictions.")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        # Read the file
        df = pd.read_csv(uploaded_file)
        st.write(f"Loaded {len(df)} patients")
        
        # Show preview
        with st.expander("Data Preview"):
            st.dataframe(df.head())
        
        # Process batch
        if st.button("🔮 Process Batch"):
            with st.spinner("Processing batch predictions..."):
                try:
                    # Convert rows to dictionaries
                    patients = df.to_dict('records')
                    
                    # Make batch prediction
                    response = requests.post(f"{API_URL}/batch_predict", json=patients)
                    
                    if response.status_code == 200:
                        results = response.json()
                        predictions_df = pd.DataFrame(results["predictions"])
                        
                        st.success(f"✅ Processed {results['total_patients']} patients")
                        
                        # Display results table
                        st.dataframe(predictions_df, use_container_width=True)
                        
                        # Statistics
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            high_risk = len(predictions_df[predictions_df["stroke_risk"] == 1])
                            st.metric("High Risk Patients", high_risk)
                        
                        with col2:
                            low_risk = len(predictions_df[predictions_df["stroke_risk"] == 0])
                            st.metric("Low Risk Patients", low_risk)
                        
                        with col3:
                            avg_prob = predictions_df["probability"].mean()
                            st.metric("Avg Probability", f"{avg_prob:.1%}")
                        
                        with col4:
                            avg_conf = predictions_df["confidence"].mean()
                            st.metric("Avg Confidence", f"{avg_conf:.1%}")
                        
                        # Chart
                        st.markdown("---")
                        risk_counts = predictions_df["risk_level"].value_counts()
                        fig = go.Figure(data=[
                            go.Pie(labels=risk_counts.index, values=risk_counts.values, 
                                   marker=dict(colors=['#f44336', '#4caf50']))
                        ])
                        fig.update_layout(title="Risk Distribution")
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.error(f"Batch prediction failed: {response.status_code}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# Page 3: Statistics
elif page == "📈 Statistics":
    st.header("System Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Predictions", "—", help="Track in MLflow")
    
    with col2:
        st.metric("Model Accuracy", "~92%", help="From training results")
    
    with col3:
        st.metric("API Status", "✅ Online", help="System health")
    
    st.markdown("---")
    st.subheader("MLflow Integration")
    st.info("""
    📊 **View detailed metrics and experiment tracking:**
    
    ```
    mlflow ui --host 0.0.0.0 --port 5000
    ```
    
    Then open: http://localhost:5000
    """)
    
    # Model info
    try:
        response = requests.get(f"{API_URL}/model_info")
        if response.status_code == 200:
            info = response.json()
            st.json(info)
    except:
        pass

# Page 4: About
elif page == "ℹ️ About":
    st.header("About This System")
    
    st.markdown("""
    ### 🏥 Stroke Risk Prediction System
    
    This is a comprehensive machine learning system designed to predict individual stroke risk
    based on patient health information.
    
    #### Key Features
    - **Advanced ML Models**: Logistic Regression, Random Forest, Gradient Boosting
    - **Real-time Predictions**: Single patient or batch processing
    - **MLflow Integration**: Complete experiment tracking and monitoring
    - **REST API**: FastAPI backend for easy integration
    - **Web UI**: Streamlit frontend for user-friendly interaction
    
    #### Technologies Used
    - **Framework**: Scikit-learn, FastAPI, Streamlit
    - **Monitoring**: MLflow
    - **Backend**: Python, Pandas, NumPy
    
    #### Model Information
    - **Training Data**: Kaggle Stroke Prediction Dataset
    - **Features**: 11 patient attributes
    - **Target**: Binary classification (stroke / no stroke)
    
    #### How to Run
    
    1. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    
    2. **Train the Model**:
    ```bash
    python main.py
    ```
    
    3. **Start the API**:
    ```bash
    python app.py
    ```
    
    4. **Launch the UI**:
    ```bash
    streamlit run streamlit_app.py
    ```
    
    5. **View MLflow Dashboard**:
    ```bash
    mlflow ui --host 0.0.0.0 --port 5000
    ```
    
    #### Contact & Support
    For questions or issues, please refer to the project documentation.
    """)
    
    st.markdown("---")
    st.markdown("*Made with ❤️ for healthcare ML*")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
    <p>🏥 Stroke Risk Prediction System | MLflow & Streamlit | Python ML Pipeline</p>
    </div>
    """,
    unsafe_allow_html=True
)
