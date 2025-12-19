"""
Configuration settings for the Apollo application.
"""
import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    # Base settings
    APP_NAME: str = "Apollo"
    API_V1_STR: str = "/api"

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-for-development-only")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "sqlite:///./apollo.db"
    )
    DB_ECHO_LOG: bool = False

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()