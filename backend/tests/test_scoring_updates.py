from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.db import Base
from app.models.appointment import Appointment
import app.services.scoring_service as scoring_service

import numpy as np

class FakeModel:
    def predict_proba(self, X):
        out = []
        for i in range(len(X)):
            if i == 0:
                out.append([0.2, 0.8])  # high
            elif i == 1:
                out.append([0.6, 0.4])  # medium
            else:
                out.append([0.9, 0.1])  # low
        return np.array(out, dtype=float)

def test_score_appointments_updates_fields(monkeypatch):
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    appt1 = Appointment(
        clinic_id="clinic_a",
        provider_id="prov_01",
        appt_datetime=datetime(2026, 1, 20, 10, 0, 0),
        appt_type="primary_care",
        lead_time_days=5,
        prior_no_shows=2,
        prior_shows=6,
        dow=1,
        hour_of_day=10,
        no_show_label=None,
    )
    appt2 = Appointment(
        clinic_id="clinic_a",
        provider_id="prov_02",
        appt_datetime=datetime(2026, 1, 20, 11, 0, 0),
        appt_type="lab",
        lead_time_days=2,
        prior_no_shows=1,
        prior_shows=3,
        dow=1,
        hour_of_day=11,
        no_show_label=None,
    )
    appt3 = Appointment(
        clinic_id="clinic_b",
        provider_id="prov_03",
        appt_datetime=datetime(2026, 1, 20, 12, 0, 0),
        appt_type="dental",
        lead_time_days=15,
        prior_no_shows=0,
        prior_shows=10,
        dow=1,
        hour_of_day=12,
        no_show_label=None,
    )

    db.add_all([appt1, appt2, appt3])
    db.commit()

    monkeypatch.setattr(scoring_service, "load_model", lambda: FakeModel())

    count = scoring_service.score_appointments(db)
    assert count == 3

    rows = db.query(Appointment).order_by(Appointment.hour_of_day).all()
    assert rows[0].risk_score is not None
    assert rows[0].risk_tier == "high"
    assert rows[1].risk_tier == "medium"
    assert rows[2].risk_tier == "low"
