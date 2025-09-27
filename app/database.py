from sqlmodel import SQLModel, Session, create_engine
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)

# Create the SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,  # Set to False in production
    connect_args={"check_same_thread": False}  # Only needed for SQLite
)

def get_session():
    """Get a new database session."""
    with Session(engine) as session:
        yield session

def init_db():
    """Initialize the database schema."""
    try:
        # Create all tables based on SQLModel models
        SQLModel.metadata.create_all(engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise