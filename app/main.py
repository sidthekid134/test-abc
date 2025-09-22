from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import uvicorn
import os

from app.database import create_db_and_tables
from app.routes.task_routes import router as task_router

# Create FastAPI app instance
app = FastAPI(
    title="Task Management API",
    description="A FastAPI-based task management application with user authentication",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify the exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(task_router, prefix="/api/tasks", tags=["tasks"])

# Setup logging
logger.add(
    "logs/app.log",
    rotation="10 MB",
    retention="1 week",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)

@app.on_event("startup")
def on_startup():
    """Create database tables on startup"""
    logger.info("Creating database tables if they don't exist")
    create_db_and_tables()

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to the Task Management API"}

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    # Run the application using uvicorn when script is executed directly
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)