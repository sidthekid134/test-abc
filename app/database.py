from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# PostgreSQL connection URL
# In production, use environment variables for these values
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost/todo_db"

# Create engine instance
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get a DB session that automatically
    handles closing the session at the end of the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()