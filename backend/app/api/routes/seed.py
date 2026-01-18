import csv
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.db import SessionLocal
from app.models.appointment import Appointment

router = APIRouter(prefix="/seed", tags=["seed"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/appointments")
def seed_appointments(db: Session = Depends(get_db)):
    path = "data/synthetic/appointments.csv"
    created = 0

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            appt_dt = datetime.fromisoformat(row["appt_datetime"])
            appt = Appointment(
                clinic_id=row["clinic_id"],
                provider_id=row["provider_id"],
                appt_datetime=appt_dt,
                appt_type=row["appt_type"],
                lead_time_days=int(row["lead_time_days"]),
                prior_no_shows=int(row["prior_no_shows"]),
                prior_shows=int(row["prior_shows"]),
                dow=int(row["dow"]),
                hour_of_day=int(row["hour_of_day"]),
                no_show_label=bool(int(row["no_show_label"])),
            )
            db.add(appt)
            created += 1

    db.commit()
    return {"status": "ok", "created": created}
