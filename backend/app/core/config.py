from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "HealthBridge BD"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    SECRET_KEY: str

    DATABASE_URL: str
    DATABASE_SYNC_URL: str
    REDIS_URL: str = "redis://localhost:6379/0"

    FIREBASE_PROJECT_ID: str = ""
    FIREBASE_CREDENTIALS_PATH: str = ""

    FIRST_ADMIN_EMAIL: str = ""
    FIRST_ADMIN_PASSWORD: str = ""

    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
