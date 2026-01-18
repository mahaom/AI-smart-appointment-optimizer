import joblib
import pandas as pd

from app.ml.feature_engineering import FEATURE_COLS
from app.models.appointment import Appointment

MODEL_PATH = "app/ml/artifacts/no_show_model.joblib"


def load_model():
    return joblib.load(MODEL_PATH)


def assign_risk_tier(score: float) -> str:
    if score >= 0.6:
        return "high"
    elif score >= 0.3:
        return "medium"
    return "low"


def score_appointments(db):
    model = load_model()

    appts = (
        db.query(Appointment)
        .filter(Appointment.no_show_label.is_(None))
        .all()
    )

    if not appts:
        return 0

    rows = []
    for a in appts:
        rows.append({
            "lead_time_days": a.lead_time_days,
            "prior_no_shows": a.prior_no_shows,
            "prior_shows": a.prior_shows,
            "dow": a.dow,
            "hour_of_day": a.hour_of_day,
        })

    df = pd.DataFrame(rows)
    scores = model.predict_proba(df[FEATURE_COLS])[:, 1]

    for appt, score in zip(appts, scores):
        appt.risk_score = float(score)
        appt.risk_tier = assign_risk_tier(score)

    db.commit()
    return len(appts)
