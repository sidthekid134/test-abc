from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API settings
    API_PREFIX: str = "/api"
    
    # Database settings
    DATABASE_URL: str = "sqlite:///./task_management.db"
    
    # CORS settings
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    class Config:
        env_file = ".env"

settings = Settings()