from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "AI Smart Appointment Optimizer API"
    environment: str = "dev"
    api_prefix: str = "/api"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
