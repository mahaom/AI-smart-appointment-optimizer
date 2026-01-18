from fastapi import FastAPI
from app.core.config import settings
from app.core.logging import setup_logging

setup_logging()

app = FastAPI(title=settings.app_name)

@app.get("/")
def root():
    return {"status": "ok", "service": settings.app_name}

@app.get(f"{settings.api_prefix}/health")
def health():
    return {"status": "healthy", "environment": settings.environment}
