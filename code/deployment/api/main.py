"""Stage 3: Model API.

Loads the trained model and exposes a single POST /predict endpoint.
Run directly with: uvicorn main:app --host 0.0.0.0 --port 8000
(the Dockerfile does this for you inside the container).
"""
import os

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

MODEL_PATH = os.path.join("models", "model.joblib")
model = joblib.load(MODEL_PATH)

# Must match code/models/train.py exactly
GENDER_MAP = {"Female": 0, "Male": 1}
BMI_MAP = {"Normal": 0, "Overweight": 1, "Obese": 2}
FEATURE_COLUMNS = [
    "Gender", "Age", "Sleep Duration", "Quality of Sleep",
    "Physical Activity Level", "Stress Level", "BMI Category",
    "Systolic", "Diastolic", "Heart Rate", "Daily Steps",
]

app = FastAPI(title="Sleep Disorder Prediction API")


class PredictRequest(BaseModel):
    gender: str
    age: int
    sleep_duration: float
    quality_of_sleep: int
    physical_activity_level: int
    stress_level: int
    bmi_category: str
    systolic: int
    diastolic: int
    heart_rate: int
    daily_steps: int


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(req: PredictRequest):
    row = {
        "Gender": GENDER_MAP.get(req.gender, 0),
        "Age": req.age,
        "Sleep Duration": req.sleep_duration,
        "Quality of Sleep": req.quality_of_sleep,
        "Physical Activity Level": req.physical_activity_level,
        "Stress Level": req.stress_level,
        "BMI Category": BMI_MAP.get(req.bmi_category, 0),
        "Systolic": req.systolic,
        "Diastolic": req.diastolic,
        "Heart Rate": req.heart_rate,
        "Daily Steps": req.daily_steps,
    }
    X = pd.DataFrame([row])[FEATURE_COLUMNS]
    prediction = model.predict(X)[0]
    return {"sleep_disorder": prediction}
