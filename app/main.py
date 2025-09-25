import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from app.database import create_db_and_tables
from app.routers import tasks, users

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="Task Management API",
    description="A simple task management API built with FastAPI and SQLModel",
    version="1.0.0",
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tasks.router)
app.include_router(users.router)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )

# Create tables on startup
@app.on_event("startup")
def on_startup():
    logger.info("Creating database tables if they don't exist...")
    create_db_and_tables()
    logger.info("Database setup complete")


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to the Task Management API",
        "documentation": "/docs",
        "endpoints": {
            "tasks": "/tasks",
            "users": "/users"
        }
    }