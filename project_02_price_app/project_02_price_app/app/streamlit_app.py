import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ------------------------------
# Page Configuration
# ------------------------------
st.set_page_config(
    page_title="House Price Estimator",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -------------------------------
# Load Model
# -------------------------------
@st.cache_resource
def load_model():
    return joblib.load("xgboost_model.joblib")

model = load_model()

# -------------------------------
# Session State (Steps)
# -------------------------------
if "step" not in st.session_state:
    st.session_state.step = 0

# -------------------------------
# App Header
# -------------------------------
st.title("House Price Estimator")
st.caption("ML-based house price prediction using Ames Housing data")
st.divider()

# ===============================
# STEP 0 — IMPORTANT INFORMATION
# ===============================
if st.session_state.step == 0:
    st.subheader("Important Information")

    st.info(
        "This application uses a machine learning model trained on historical housing data. "
        "The predicted price is an informed estimate based on patterns learned from past sales, "
        "not an exact or guaranteed market value.\n\n"
        "The model performs well within its defined scope and is suitable for demonstration and "
        "portfolio purposes. Real-world property prices may vary due to market trends, location-specific "
        "factors, and economic conditions."
    )

    if st.button("Start Estimation ➡️"):
        st.session_state.step = 1
        st.rerun()

# ===============================
# STEP 1 — PROPERTY QUALITY
# ===============================
elif st.session_state.step == 1:
    st.subheader("Step 1: Property Quality")

    overall_qual = st.select_slider(
        "Overall Quality (1 = Poor, 10 = Excellent)",
        options=list(range(1, 11)),
        value=6
    )

    if st.button("Next ➡️"):
        st.session_state.overall_qual = overall_qual
        st.session_state.step = 2
        st.rerun()

# ===============================
# STEP 2 — SIZE & STRUCTURE
# ===============================
elif st.session_state.step == 2:
    st.subheader("Step 2: Size & Structure")

    gr_liv_area = st.number_input(
        "Above Ground Living Area (sq ft)",
        min_value=300,
        max_value=6000,
        step=50,
        value=1500,
        help="Type here (e.g. 1500 sq ft)"
    )

    total_bsmt_sf = st.number_input(
        "Total Basement Area (sq ft)",
        min_value=0,
        max_value=3000,
        step=50,
        value=800,
        help="Type here (e.g. 800 sq ft)"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅️ Back"):
            st.session_state.step = 1
            st.rerun()

    with col2:
        if st.button("Next ➡️"):
            st.session_state.gr_liv_area = gr_liv_area
            st.session_state.total_bsmt_sf = total_bsmt_sf
            st.session_state.step = 3
            st.rerun()

# ===============================
# STEP 3 — AMENITIES
# ===============================
elif st.session_state.step == 3:
    st.subheader("Step 3: Amenities")

    garage_cars = st.radio(
        "Garage Capacity (Cars)",
        options=[0, 1, 2, 3, 4],
        horizontal=True,
        index=2
    )

    year_built = st.slider(
        "Year Built",
        min_value=1870,
        max_value=2010,
        value=2005
    )

    central_air = st.toggle("Central Air Conditioning")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅️ Back"):
            st.session_state.step = 2
            st.rerun()

    with col2:
        if st.button("Next ➡️"):
            st.session_state.garage_cars = garage_cars
            st.session_state.year_built = year_built
            st.session_state.central_air = central_air
            st.session_state.step = 4
            st.rerun()

# ===============================
# STEP 4 — PREDICT PRICE
# ===============================
elif st.session_state.step == 4:
    st.subheader("Step 4: Price Prediction")

    if st.button("Predict House Price 💰"):
        input_data = pd.DataFrame({
            "OverallQual": [st.session_state.overall_qual],
            "GrLivArea": [st.session_state.gr_liv_area],
            "TotalBsmtSF": [st.session_state.total_bsmt_sf],
            "GarageCars": [st.session_state.garage_cars],
            "YearBuilt": [st.session_state.year_built],
            "CentralAir_Y": [1 if st.session_state.central_air else 0]
        })

        model_features = model.get_booster().feature_names
        input_data = input_data.reindex(columns=model_features, fill_value=0)

        log_price = model.predict(input_data)[0]
        price = np.expm1(log_price)

        st.success(f"Estimated Sale Price: ${price:,.0f}")

        st.caption(
            "This estimate is generated using an XGBoost regression model trained on historical data. "
            "Predictions are indicative and may vary under real-world conditions."
        )

    st.divider()

    with st.expander("Model Notes"):
        st.markdown("""
        - **Model:** XGBoost Regressor  
        - **Target:** Log-transformed SalePrice  
        - **Evaluation Metric:** RMSE  
        - **Project Scope:** Portfolio-grade baseline model  
        - **Future Improvements:** Hyperparameter tuning, feature interactions, market calibration
        """)

    if st.button("🔄 Start Over"):
        st.session_state.step = 0
        st.rerun()
