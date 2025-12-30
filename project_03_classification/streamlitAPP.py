# bank_deposit_app.py
import streamlit as st
import pandas as pd
import numpy as np
import joblib

# -------------------
# Load preprocessor and stacked model
# -------------------
preprocessor = joblib.load('preprocessor.pkl')   # your saved preprocessor
stack_pipeline = joblib.load('stacked_bank_model.pkl')  # your stacked model pipeline

# -------------------
# App Layout / Introduction
# -------------------
st.set_page_config(page_title="Bank Deposit Prediction", layout="centered")

st.title("🏦 Bank Deposit Prediction App")
st.markdown("""
Welcome to the **Bank Deposit Prediction App**!  

This app predicts whether a customer is likely to **subscribe to a term deposit** based on their profile.  

**Important Notes:**
- Models were trained on limited historical data, so predictions are indicative.  
- Overall model performance (ROC-AUC) is ~**80%**.  
- Threshold for recommending bank contact: **0.7** probability.  
- Predictions include both **yes/no** and **probability score**.
""")

st.write("---")

# -------------------
# Sidebar for multi-step form
# -------------------
if 'step' not in st.session_state:
    st.session_state.step = 1

# -------------------
# Step 1: Basic Info
# -------------------
if st.session_state.step == 1:
    st.subheader("Step 1: Basic Customer Info")

    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", min_value=18, max_value=95, value=30)
        job = st.selectbox("Job", ['admin.', 'technician', 'services', 'management', 'retired', 
                                   'blue-collar', 'unemployed', 'entrepreneur', 'housemaid', 
                                   'self-employed', 'student', 'unknown'])
        marital = st.selectbox("Marital Status", ['married', 'single', 'divorced'])
    with col2:
        education = st.selectbox("Education", ['primary', 'secondary', 'tertiary', 'unknown'])
        default = st.selectbox("Has credit default?", ['yes', 'no'])
        housing = st.selectbox("Has housing loan?", ['yes', 'no'])

    if st.button("Next"):
        st.session_state.step = 2
        st.session_state.inputs = {
            'age': age, 'job': job, 'marital': marital, 'education': education,
            'default': default, 'housing': housing
        }

# -------------------
# Step 2: Banking Info
# -------------------
elif st.session_state.step == 2:
    st.subheader("Step 2: Banking Info")

    col1, col2 = st.columns(2)
    with col1:
        balance = st.number_input("Account Balance", min_value=-2000, max_value=100000, value=1000)
        loan = st.selectbox("Has personal loan?", ['yes', 'no'])
        contact = st.selectbox("Contact type", ['cellular', 'telephone'])
    with col2:
        day = st.number_input("Last contact day of month", min_value=1, max_value=31, value=15)
        month = st.selectbox("Last contact month", ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
                                                   'jul', 'aug', 'sep', 'oct', 'nov', 'dec'])
        campaign = st.number_input("Number of contacts during campaign", min_value=1, max_value=50, value=1)
        pdays = st.number_input("Days since last contact (-1 = never)", min_value=-1, max_value=999, value=-1)
        previous = st.number_input("Number of contacts before this campaign", min_value=0, max_value=50, value=0)
        poutcome = st.selectbox("Outcome of previous campaign", ['unknown', 'failure', 'success', 'other'])

    if st.button("Predict"):
        # Merge all inputs
        st.session_state.inputs.update({
            'balance': balance, 'loan': loan, 'contact': contact, 'day': day,
            'month': month, 'campaign': campaign, 'pdays': pdays,
            'previous': previous, 'poutcome': poutcome
        })

        # Convert to dataframe
        input_df = pd.DataFrame([st.session_state.inputs])

        # Preprocess & predict
        prob = stack_pipeline.predict_proba(input_df)[:, 1][0]
        prediction = "Yes" if prob >= 0.5 else "No"
        action = "✅ Contact Customer" if prob >= 0.7 else "❌ Do not contact"

        st.write("---")
        st.subheader("Prediction Result")
        st.write(f"**Will subscribe to deposit?**: {prediction}")
        st.write(f"**Probability**: {prob:.2f}")
        st.write(f"**Recommended Action**: {action}")

# -------------------
# CSV Upload for bulk predictions
# -------------------
st.write("---")
st.subheader("Bulk Predictions via CSV Upload")
uploaded_file = st.file_uploader("Upload CSV file with customer data", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(f"Uploaded file: {df.shape[0]} rows, {df.shape[1]} columns")

    # Predict
    probs = stack_pipeline.predict_proba(df)[:, 1]
    preds = np.where(probs >= 0.5, 'Yes', 'No')
    actions = np.where(probs >= 0.7, '✅ Contact Customer', '❌ Do not contact')

    results_df = df.copy()
    results_df['Prediction'] = preds
    results_df['Probability'] = probs
    results_df['Action'] = actions

    st.write("Bulk Prediction Results")
    st.dataframe(results_df.head(20))  # show first 20 rows
    st.download_button(
        "Download Results as CSV",
        results_df.to_csv(index=False),
        file_name="bank_deposit_predictions.csv"
    )

   