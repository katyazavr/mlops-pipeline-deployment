"""Stage 3: Web app.

Simple Streamlit UI: input fields, a button, and the prediction, obtained by
calling the model API (running in a separate container).
"""
import os

import requests
import streamlit as st

API_URL = os.environ.get("API_URL", "http://localhost:8000")

st.title("Sleep Disorder Predictor")

gender = st.selectbox("Gender", ["Male", "Female"])
age = st.number_input("Age", min_value=18, max_value=100, value=30)
sleep_duration = st.number_input(
    "Sleep Duration (hours)", min_value=0.0, max_value=12.0, value=7.0, step=0.1
)
quality_of_sleep = st.slider("Quality of Sleep (1-10)", 1, 10, 6)
physical_activity_level = st.slider(
    "Physical Activity Level (minutes/day)", 0, 120, 40
)
stress_level = st.slider("Stress Level (1-10)", 1, 10, 5)
bmi_category = st.selectbox("BMI Category", ["Normal", "Overweight", "Obese"])
systolic = st.number_input("Systolic Blood Pressure", min_value=80, max_value=200, value=120)
diastolic = st.number_input("Diastolic Blood Pressure", min_value=50, max_value=130, value=80)
heart_rate = st.number_input("Heart Rate", min_value=40, max_value=120, value=70)
daily_steps = st.number_input("Daily Steps", min_value=0, max_value=30000, value=6000)

if st.button("Predict"):
    payload = {
        "gender": gender,
        "age": age,
        "sleep_duration": sleep_duration,
        "quality_of_sleep": quality_of_sleep,
        "physical_activity_level": physical_activity_level,
        "stress_level": stress_level,
        "bmi_category": bmi_category,
        "systolic": systolic,
        "diastolic": diastolic,
        "heart_rate": heart_rate,
        "daily_steps": daily_steps,
    }
    try:
        response = requests.post(f"{API_URL}/predict", json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()["sleep_disorder"]
        st.success(f"Predicted Sleep Disorder: {result}")
    except Exception as e:
        st.error(f"Request to the API failed: {e}")
