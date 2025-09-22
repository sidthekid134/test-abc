from sqlmodel import SQLModel, Session, create_engine
import os
from typing import Generator

# Use environment variable for database URL or default to SQLite
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./tasks.db")

# Create engine for SQLModel
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    echo=False  # Set to True to see SQL queries in console
)

def create_db_and_tables() -> None:
    """Create database tables from SQLModel models."""
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """Dependency for getting database sessions."""
    with Session(engine) as session:
        yield session