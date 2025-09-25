import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

# Use environment variable for database URL or default to SQLite for local development
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite+aiosqlite:///./tasks.db")

# Create async engine
engine = create_async_engine(
    DATABASE_URL, 
    echo=False, 
    future=True,
)

# Create async session
async_session = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False,
)

async def init_db():
    """Initialize the database by creating all tables."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting async db session."""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()