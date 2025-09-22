from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
import os
from loguru import logger

# Database URL - in production, use environment variables or a config file
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tasks.db")

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL, 
    echo=False,  # Set to True to see SQL queries
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

def create_db_and_tables() -> None:
    """Create database tables from SQLModel metadata."""
    logger.info("Creating database and tables")
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """Dependency for database session."""
    with Session(engine) as session:
        logger.debug("Database session started")
        try:
            yield session
            logger.debug("Database session committed")
        except Exception as e:
            logger.error(f"Database session error: {e}")
            session.rollback()
            raise