from sqlmodel import SQLModel, create_engine, Session
import os
from typing import Generator

# Get the database URL from environment variable or use a default SQLite database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tasks.db")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

def create_db_and_tables():
    """Create database tables from SQLModel models."""
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """Dependency for database session."""
    with Session(engine) as session:
        yield session