from datetime import datetime
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.db import Base
from app.models.appointment import Appointment
from app.api.routes import analytics as analytics_routes
from sqlalchemy.pool import StaticPool


def test_risk_tier_distribution_endpoint_returns_points():
    
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    db.add_all([
        Appointment(
            clinic_id="clinic_a",
            provider_id="prov_01",
            appt_datetime=datetime(2026, 1, 20, 10, 0, 0),
            appt_type="primary_care",
            lead_time_days=3,
            prior_no_shows=0,
            prior_shows=5,
            dow=1,
            hour_of_day=10,
            no_show_label=None,
            risk_tier="high",
            risk_score=0.8,
        ),
        Appointment(
            clinic_id="clinic_a",
            provider_id="prov_02",
            appt_datetime=datetime(2026, 1, 20, 11, 0, 0),
            appt_type="lab",
            lead_time_days=1,
            prior_no_shows=1,
            prior_shows=2,
            dow=1,
            hour_of_day=11,
            no_show_label=None,
            risk_tier="medium",
            risk_score=0.4,
        ),
        Appointment(
            clinic_id="clinic_b",
            provider_id="prov_03",
            appt_datetime=datetime(2026, 1, 20, 12, 0, 0),
            appt_type="dental",
            lead_time_days=8,
            prior_no_shows=0,
            prior_shows=7,
            dow=1,
            hour_of_day=12,
            no_show_label=None,
            risk_tier="medium",
            risk_score=0.35,
        ),
    ])
    db.commit()

    app = FastAPI()
    app.include_router(analytics_routes.router)

    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[analytics_routes.get_db] = override_get_db

    client = TestClient(app)
    res = client.get("/analytics/risk_tier_distribution")
    assert res.status_code == 200

    body = res.json()
    assert "points" in body
    assert isinstance(body["points"], list)
        
    db.close()

   
