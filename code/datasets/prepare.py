"""Stage 1: Data Engineering.

Loads the raw Sleep Health and Lifestyle dataset, cleans it, and splits it
into train/test sets saved under data/processed/.

Run from the repository root:
    python code/datasets/prepare.py
"""
import os

import pandas as pd
from sklearn.model_selection import train_test_split

RAW_PATH = os.path.join("data", "raw", "sleep_health_and_lifestyle_dataset.csv")
PROCESSED_DIR = os.path.join("data", "processed")


def load_data(path: str = RAW_PATH) -> pd.DataFrame:
    return pd.read_csv(path)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates()

    # "Sleep Disorder" is empty for people who don't have a diagnosed
    # disorder, so it's imputed as "Healthy"
    df["Sleep Disorder"] = df["Sleep Disorder"].fillna("Healthy")

    # "Normal" and "Normal Weight" are the same category
    df["BMI Category"] = df["BMI Category"].replace("Normal Weight", "Normal")

    # Remove outliers in Heart Rate using the standard IQR rule
    q1, q3 = df["Heart Rate"].quantile([0.25, 0.75])
    iqr = q3 - q1
    low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    df = df[(df["Heart Rate"] >= low) & (df["Heart Rate"] <= high)]

    return df.reset_index(drop=True)


def split_and_save(df: pd.DataFrame, out_dir: str = PROCESSED_DIR) -> None:
    os.makedirs(out_dir, exist_ok=True)
    train_df, test_df = train_test_split(
        df, test_size=0.2, random_state=42, stratify=df["Sleep Disorder"]
    )
    train_df.to_csv(os.path.join(out_dir, "train.csv"), index=False)
    test_df.to_csv(os.path.join(out_dir, "test.csv"), index=False)
    print(f"train: {len(train_df)} rows, test: {len(test_df)} rows -> {out_dir}")


if __name__ == "__main__":
    raw = load_data()
    print(f"loaded {len(raw)} raw rows")
    cleaned = clean_data(raw)
    print(f"{len(cleaned)} rows after cleaning ({len(raw) - len(cleaned)} removed)")
    split_and_save(cleaned)
