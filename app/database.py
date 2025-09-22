from sqlmodel import SQLModel, create_engine, Session
import os
from typing import Generator

# Use an environment variable or default to a SQLite database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tasks.db")

# Create the database engine
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    echo=True  # Set to False in production
)

def create_db_and_tables() -> None:
    """Create database tables if they don't exist"""
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """Dependency for database session"""
    with Session(engine) as session:
        yield session