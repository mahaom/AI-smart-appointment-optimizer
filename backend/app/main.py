from fastapi import FastAPI
from app.core.config import settings
from app.core.logging import setup_logging
from app.models.db import engine, Base
from app.models import appointment, reminder, user, audit_log
from app.api.routes import appointments
from app.api.routes.appointments import router as appointments_router
from app.api.routes.seed import router as seed_router


setup_logging()

app = FastAPI(title=settings.app_name)

Base.metadata.create_all(bind=engine)

app.include_router(appointments.router)

app.include_router(seed_router)

@app.get("/")
def root():
    return {"status": "ok", "service": settings.app_name}

@app.get(f"{settings.api_prefix}/health")
def health():
    return {"status": "healthy", "environment": settings.environment}
