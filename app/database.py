from sqlmodel import SQLModel, Session, create_engine
import os
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Use SQLite as the database
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./onboarding_app.db")

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL, 
    echo=True,  # Set to False in production
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

def create_db_and_tables():
    """Create database tables from SQLModel models."""
    try:
        logger.info(f"Creating database tables with connection: {DATABASE_URL}")
        SQLModel.metadata.create_all(engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        raise

def get_session():
    """Dependency for database session."""
    with Session(engine) as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {str(e)}")
            session.rollback()
            raise
        finally:
            session.close()