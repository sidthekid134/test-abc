from sqlmodel import SQLModel, Session, create_engine
import os
from typing import Generator

DATABASE_URL = os.environ.get("DATABASE_URL") or "sqlite:///./tasks.db"

# Create SQLite engine
engine = create_engine(
    DATABASE_URL, 
    echo=True,  # Set to False in production
    connect_args={"check_same_thread": False}  # Only needed for SQLite
)

def create_db_and_tables():
    """Create all tables in the database"""
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """Dependency for getting a database session"""
    with Session(engine) as session:
        yield session