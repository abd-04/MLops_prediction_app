import streamlit as st
import requests

# 🔹 Page configuration
st.set_page_config(
    page_title="Diabetes Risk Predictor",
    page_icon="🩺",
    layout="centered"
)

st.title("🩺 Diabetes Risk Prediction System")
st.markdown(
    "This tool estimates the probability of diabetes using clinical indicators. "
    "Made as a hobby project. Not for actual medical use. "
)

st.divider()

# 🔹 Input Section
st.subheader("📋 Patient Information")

pregnancies = st.number_input(
    "Pregnancies",
    min_value=0,
    step=1,
    help="Number of times the patient has been pregnant."
)

glucose = st.number_input(
    "Glucose Level (mg/dL)",
    min_value=0,
    step=1,
    help="Plasma glucose concentration. Normal fasting range: 70–99 mg/dL."
)

blood_pressure = st.number_input(
    "Blood Pressure (mm Hg)",
    min_value=0,
    step=1,
    help="Diastolic blood pressure. Normal range: ~60–80 mm Hg."
)

skin_thickness = st.number_input(
    "Skin Thickness (mm)",
    min_value=0,
    step=1,
    help="Triceps skin fold thickness. Indicator of body fat."
)

insulin = st.number_input(
    "Insulin Level (μU/mL)",
    min_value=0,
    step=1,
    help="serum insulin. Abnormal values may indicate insulin resistance."
)

bmi = st.number_input(
    "BMI (Body Mass Index)",
    min_value=0,
    step=1,
    help="Weight-to-height ratio. Normal: 18.5–24.9. Overweight: 25–29.9."
)

diabetes_pedigree_function = st.number_input(
    "Diabetes Pedigree Function",
    min_value=0.0,
    help="Score estimating genetic influence of diabetes. 0 - 2.5+ range."
)

age = st.number_input(
    "Age",
    min_value=0,
    step=1,
    help="Risk of Type 2 diabetes increases with age (especially >40)."
)

st.divider()

# 🔹 Predict Button
if st.button("🔍 Predict Risk"):

    data = {
        "pregnancies": pregnancies,
        "glucose": glucose,
        "blood_pressure": blood_pressure,
        "skin_thickness": skin_thickness,
        "insulin": insulin,
        "bmi": bmi,
        "diabetes_pedigree_function": diabetes_pedigree_function,
        "age": age
    }

    try:
        response = requests.post(
            "https://mlops-prediction-app.onrender.com/predict",
            json=data
        )

        if response.status_code == 200:
            result = response.json()["prediction"]
            probability = response.json()["probability"]

            st.subheader("📊 Prediction Result")

            if result == "Diabetic":
                st.error(f"⚠️ Prediction: {result}")
            else:
                st.success(f"✅ Prediction: {result}")

            st.info(f"Model Confidence Score: {probability:.2f}")

        else:
            response = requests.post(
    "https://mlops-prediction-app.onrender.com/predict",
    json=data
)

        st.write("Status Code:", response.status_code)
        st.write("Response:", response.text)
           # st.error("API Error. Please try again.")
           

    except Exception:
        st.error("Could not connect to backend (Render server may be sleeping).")