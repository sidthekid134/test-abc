import os
from sqlmodel import SQLModel, Session, create_engine
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database URL from environment variables or use a default SQLite database
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./tasks.db")

# Create database engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    echo=True  # Log generated SQL statements (set to False in production)
)

def create_db_and_tables():
    """Create database tables if they don't exist"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Get a database session"""
    with Session(engine) as session:
        yield session