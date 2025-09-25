import os
from sqlmodel import Session, SQLModel, create_engine
from typing import Generator

# Database URL
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./tasks.db")

# Create engine with proper connect args for SQLite
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args)


def get_session() -> Generator[Session, None, None]:
    """
    Creates a new database session for dependency injection.
    """
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    """
    Creates database tables based on SQLModel models.
    """
    SQLModel.metadata.create_all(engine)