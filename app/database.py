from sqlmodel import SQLModel, Session, create_engine
import os

# Use SQLite as the database
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./todo_app.db")

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL, 
    echo=True,  # Set to False in production
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

def create_db_and_tables():
    """Create database tables from SQLModel models."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependency for database session."""
    with Session(engine) as session:
        yield session