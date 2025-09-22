"""
Database configuration module.
"""
import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

# Get database URL from environment variable or use a default SQLite database
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite+aiosqlite:///./tasks.db")

# Create async engine
engine = create_async_engine(
    DATABASE_URL, 
    echo=True,  # Set to False in production
    future=True,
)

# Create async session factory
async_session_factory = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False,
    autoflush=False,
)

# Create base model
Base = declarative_base()

async def create_db_and_tables():
    """
    Create database tables if they don't exist.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting async session.
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()