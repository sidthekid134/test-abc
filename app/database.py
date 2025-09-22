from sqlmodel import SQLModel, Session, create_engine
import os
from typing import Generator

# For a real production application, use environment variables
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./tasks.db")

# Create SQLite engine
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    echo=False  # Set to True for debugging
)

def create_db_and_tables():
    """Create database tables from SQLModel models"""
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """Database session dependency"""
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()