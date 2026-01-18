import json
import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, accuracy_score
from sqlalchemy import text

from app.models.db import engine
from app.ml.feature_engineering import prepare_features

MODEL_PATH = "app/ml/artifacts/no_show_model.joblib"
METRICS_PATH = "app/ml/artifacts/metrics.json"


def load_training_data():
    query = text("""
        SELECT
            lead_time_days,
            prior_no_shows,
            prior_shows,
            dow,
            hour_of_day,
            no_show_label
        FROM appointments
        WHERE no_show_label IS NOT NULL
    """)
    return pd.read_sql(query, engine)


def main():
    df = load_training_data()
    if df.empty:
        raise RuntimeError("No training data found")

    X, y = prepare_features(df)

    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)

    preds = model.predict_proba(X)[:, 1]

    metrics = {
        "rows": len(df),
        "auc": roc_auc_score(y, preds),
        "accuracy": accuracy_score(y, preds > 0.5),
    }

    joblib.dump(model, MODEL_PATH)
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=2)

    print("Model trained successfully")
    print(metrics)


if __name__ == "__main__":
    main()
