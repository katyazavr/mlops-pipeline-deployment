"""Stage 2: Model Engineering.

Builds features from the processed train/test data, trains a classifier
that predicts Sleep Disorder (None / Insomnia / Sleep Apnea), evaluates it,
logs the testing metrics, and saves the trained model.

Run from the repository root:
    python code/models/train.py
"""
import json
import os

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score

PROCESSED_DIR = os.path.join("data", "processed")
MODELS_DIR = "models"

# Same encoding used by the API at inference time: keep both in sync.
GENDER_MAP = {"Female": 0, "Male": 1}
BMI_MAP = {"Normal": 0, "Overweight": 1, "Obese": 2}

FEATURE_COLUMNS = [
    "Gender", "Age", "Sleep Duration", "Quality of Sleep",
    "Physical Activity Level", "Stress Level", "BMI Category",
    "Systolic", "Diastolic", "Heart Rate", "Daily Steps",
]


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Gender"] = df["Gender"].map(GENDER_MAP)
    df["BMI Category"] = df["BMI Category"].map(BMI_MAP)
    bp = df["Blood Pressure"].str.split("/", expand=True)
    df["Systolic"] = bp[0].astype(int)
    df["Diastolic"] = bp[1].astype(int)
    return df


def load_processed():
    train_df = pd.read_csv(os.path.join(PROCESSED_DIR, "train.csv"))
    test_df = pd.read_csv(os.path.join(PROCESSED_DIR, "test.csv"))
    return train_df, test_df


def main():
    train_df, test_df = load_processed()
    train_feat = build_features(train_df)
    test_feat = build_features(test_df)

    X_train, y_train = train_feat[FEATURE_COLUMNS], train_feat["Sleep Disorder"]
    X_test, y_test = test_feat[FEATURE_COLUMNS], test_feat["Sleep Disorder"]

    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    metrics = {
        "accuracy": accuracy_score(y_test, preds),
        "f1_macro": f1_score(y_test, preds, average="macro"),
    }
    print("test metrics:", metrics)

    os.makedirs(MODELS_DIR, exist_ok=True)
    joblib.dump(model, os.path.join(MODELS_DIR, "model.joblib"))
    with open(os.path.join(MODELS_DIR, "metrics.json"), "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"model saved to {MODELS_DIR}/model.joblib")


if __name__ == "__main__":
    main()
