from sqlmodel import SQLModel, Session, create_engine
import os
from typing import Generator

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tasks.db")

engine = create_engine(
    DATABASE_URL, 
    echo=True, 
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session