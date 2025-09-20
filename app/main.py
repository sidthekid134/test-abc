from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select
from typing import List, Optional

from .database import get_session
from .models import *

app = FastAPI(title="FastAPI Application")

@app.get("/")
async def root():
    """Root endpoint returning a welcome message."""
    return {"message": "Welcome to the FastAPI Application"}

@app.get("/health-v2")
async def health_check_v2():
    """Health check endpoint for the application."""
    return {"status": "healthy"}