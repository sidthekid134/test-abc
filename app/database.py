from sqlmodel import SQLModel, create_engine, Session
import os
from typing import Generator

# Database URL (using SQLite for simplicity)
DATABASE_URL = "sqlite:///./task_management.db"

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False},
    echo=True
)

def create_db_and_tables():
    """Create database and tables."""
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """Dependency for database session."""
    with Session(engine) as session:
        yield session