from sqlmodel import SQLModel, Field, create_engine, Session
from typing import Optional
import os

# Database URL would typically be stored in an environment variable
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./sql_app.db")

engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session