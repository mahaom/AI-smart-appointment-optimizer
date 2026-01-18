import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, Integer, Float, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.models.db import Base

class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    clinic_id: Mapped[str] = mapped_column(String(64), nullable=False)
    provider_id: Mapped[str] = mapped_column(String(64), nullable=False)

    appt_datetime: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    appt_type: Mapped[str] = mapped_column(String(64), nullable=False)

    lead_time_days: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    prior_no_shows: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    prior_shows: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    dow: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    hour_of_day: Mapped[int] = mapped_column(Integer, nullable=False, default=9)

    no_show_label: Mapped[bool] = mapped_column(Boolean, nullable=True)

    risk_score: Mapped[float] = mapped_column(Float, nullable=True)
    risk_tier: Mapped[str] = mapped_column(String(16), nullable=True)
