from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
import logging

from .database import create_db_and_tables, get_session
from .models import Task, TaskCreate, TaskRead, TaskUpdate

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Task Management API",
    description="A simple task management API built with FastAPI and SQLModel",
    version="1.0.0",
)

@app.on_event("startup")
def on_startup():
    """Create database tables on startup"""
    create_db_and_tables()
    logger.info("Database tables created")


@app.get("/")
async def root():
    """Root endpoint for API health check"""
    return {"message": "Task Management API is running"}


# Import and include routers
from .routers import tasks

# Include routers
app.include_router(tasks.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)