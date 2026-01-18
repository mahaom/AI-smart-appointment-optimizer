from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.models.db import SessionLocal
from app.models.appointment import Appointment

router = APIRouter(prefix="/appointments", tags=["appointments"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def list_appointments(
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return db.query(Appointment).order_by(Appointment.appt_datetime.desc()).limit(limit).all()


@router.post("/")
def create_appointment(
    clinic_id: str,
    provider_id: str,
    appt_datetime: datetime,
    appt_type: str,
    db: Session = Depends(get_db),
):
    appt = Appointment(
        clinic_id=clinic_id,
        provider_id=provider_id,
        appt_datetime=appt_datetime,
        appt_type=appt_type,
        lead_time_days=7,
        prior_no_shows=0,
        prior_shows=0,
        dow=appt_datetime.weekday(),
        hour_of_day=appt_datetime.hour,
    )
    db.add(appt)
    db.commit()
    db.refresh(appt)
    return appt
