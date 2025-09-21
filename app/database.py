from sqlmodel import SQLModel, Session, create_engine
import os
from typing import Generator

# SQLite database URL
# For production, you would use PostgreSQL or another production-ready database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tasks.db")

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False},  # Only needed for SQLite
    echo=False  # Set to True to see SQL queries
)

def create_db_and_tables():
    """Create database tables from SQLModel models."""
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """Dependency for getting a SQLModel session."""
    with Session(engine) as session:
        yield session