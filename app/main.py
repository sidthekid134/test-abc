import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.routers import users, tasks, auth

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan events for the application.
    Initialize database on startup.
    """
    # Initialize the database on startup
    logger.info("Initializing database")
    await init_db()
    
    logger.info("Application startup complete")
    yield
    logger.info("Application shutdown complete")


# Create FastAPI application
app = FastAPI(
    title="Task Management API",
    description="A simple but production-ready task management API",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this in production to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint to check if the API is running."""
    return {"message": "Task Management API is running"}