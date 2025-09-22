from sqlmodel import SQLModel, Session, create_engine
import os
from loguru import logger

# Database URL (use environment variable or default to SQLite)
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./task_manager.db")

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    echo=False,  # Set to True for debugging SQL queries
)


def get_session():
    """
    Dependency for getting a database session.
    Used by FastAPI dependency injection system.
    """
    with Session(engine) as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {str(e)}")
            session.rollback()
            raise
        finally:
            session.close()


def create_db_and_tables():
    """
    Create database tables if they don't exist.
    Should be called on application startup.
    """
    try:
        logger.info("Creating database tables")
        SQLModel.metadata.create_all(engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        raise