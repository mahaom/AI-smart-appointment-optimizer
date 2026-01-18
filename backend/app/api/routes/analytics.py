from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, Integer

from app.models.db import SessionLocal
from app.models.appointment import Appointment

router = APIRouter(prefix="/analytics", tags=["analytics"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/no_show_rate_trend")
def no_show_rate_trend(
    start: datetime | None = None,
    end: datetime | None = None,
    group_by: str = Query("day", pattern="^(day|week)$"),
    db: Session = Depends(get_db),
):
    q = db.query(Appointment).filter(Appointment.no_show_label.isnot(None))

    if start:
        q = q.filter(Appointment.appt_datetime >= start)
    if end:
        q = q.filter(Appointment.appt_datetime <= end)

    if group_by == "week":
        bucket = func.date_trunc("week", Appointment.appt_datetime).label("bucket")
    else:
        bucket = func.date_trunc("day", Appointment.appt_datetime).label("bucket")

    total = func.count().label("total")
    no_shows = func.sum(func.cast(Appointment.no_show_label, Integer)).label("no_shows")

    rows = (
        db.query(bucket, total, no_shows)
        .select_from(Appointment)
        .filter(Appointment.no_show_label.isnot(None))
    )

    if start:
        rows = rows.filter(Appointment.appt_datetime >= start)
    if end:
        rows = rows.filter(Appointment.appt_datetime <= end)

    rows = rows.group_by(bucket).order_by(bucket).all()

    result = []
    for b, t, ns in rows:
        t = int(t or 0)
        ns = int(ns or 0)
        rate = (ns / t) if t else 0.0
        result.append({"bucket": b.isoformat(), "total": t, "no_shows": ns, "no_show_rate": rate})

    return {"group_by": group_by, "points": result}


@router.get("/no_shows_by_dow")
def no_shows_by_dow(
    start: datetime | None = None,
    end: datetime | None = None,
    db: Session = Depends(get_db),
):
    q = db.query(Appointment).filter(Appointment.no_show_label.isnot(None))

    if start:
        q = q.filter(Appointment.appt_datetime >= start)
    if end:
        q = q.filter(Appointment.appt_datetime <= end)

    rows = (
        db.query(
            Appointment.dow.label("dow"),
            func.count().label("total"),
            func.sum(func.cast(Appointment.no_show_label, Integer)).label("no_shows"),

            
        )
        .select_from(Appointment)
        .filter(Appointment.no_show_label.isnot(None))
    )

    if start:
        rows = rows.filter(Appointment.appt_datetime >= start)
    if end:
        rows = rows.filter(Appointment.appt_datetime <= end)

    rows = rows.group_by(Appointment.dow).order_by(Appointment.dow).all()

    result = []
    for dow, total, no_shows in rows:
        total = int(total or 0)
        no_shows = int(no_shows or 0)
        rate = (no_shows / total) if total else 0.0
        result.append({"dow": int(dow), "total": total, "no_shows": no_shows, "no_show_rate": rate})

    return {"points": result}


@router.get("/risk_tier_distribution")
def risk_tier_distribution(db: Session = Depends(get_db)):
    rows = (
        db.query(Appointment.risk_tier, func.count().label("count"))
        .filter(Appointment.risk_tier.isnot(None))
        .group_by(Appointment.risk_tier)
        .order_by(Appointment.risk_tier)
        .all()
    )
    return {"points": [{"risk_tier": (rt or "unknown"), "count": int(c)} for rt, c in rows]}
