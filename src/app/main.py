from fastapi import FastAPI, Depends, HTTPException
from typing import List, Optional
import logging
from sqlmodel import Session

from .database import get_session
from .models import UserRead, UserCreate

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Starter Onboarding API",
    description="API for the Starter Onboarding Flow",
    version="0.1.0",
)


@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {"message": "Welcome to the Starter Onboarding API"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# Include additional routers here
# app.include_router(users_router, prefix="/users", tags=["users"])


@app.on_event("startup")
async def startup_event():
    """Runs on application startup."""
    logger.info("Starting up API server")


@app.on_event("shutdown")
async def shutdown_event():
    """Runs on application shutdown."""
    logger.info("Shutting down API server")