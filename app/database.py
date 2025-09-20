from sqlmodel import create_engine, Session, SQLModel
from typing import Generator
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    """Create database tables from SQLModel models."""
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """Dependency for getting a database session."""
    with Session(engine) as session:
        yield session