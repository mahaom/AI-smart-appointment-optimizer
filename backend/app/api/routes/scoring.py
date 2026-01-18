from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.db import SessionLocal
from app.services.scoring_service import score_appointments

router = APIRouter(prefix="/scoring", tags=["scoring"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/batch")
def batch_score(db: Session = Depends(get_db)):
    count = score_appointments(db)
    return {"status": "ok", "appointments_scored": count}
