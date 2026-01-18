import pandas as pd

FEATURE_COLS = [
    "lead_time_days",
    "prior_no_shows",
    "prior_shows",
    "dow",
    "hour_of_day",
]

TARGET_COL = "no_show_label"


def prepare_features(df: pd.DataFrame):
    X = df[FEATURE_COLS]
    y = df[TARGET_COL]
    return X, y
