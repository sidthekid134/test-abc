import os
from typing import Generator
from sqlmodel import SQLModel, Session, create_engine

# Database URL can be configured via environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./onboarding.db")

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production
    connect_args={"check_same_thread": False}  # Only needed for SQLite
)


def create_db_and_tables():
    """Create database tables if they don't exist."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Dependency for getting DB session."""
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()


# Additional database utility functions can be added here