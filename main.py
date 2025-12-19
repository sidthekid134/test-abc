"""
Apollo Application - FastAPI Backend
Entry point for the application.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.database.database import create_db_and_tables
from app.routers import user, item

# Initialize FastAPI app
app = FastAPI(
    title="Apollo API",
    description="FastAPI backend for Apollo project",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user.router, prefix="/api/users", tags=["users"])
app.include_router(item.router, prefix="/api/items", tags=["items"])

# Startup event
@app.on_event("startup")
async def on_startup():
    create_db_and_tables()

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Apollo API",
        "version": "0.1.0",
        "docs_url": "/docs",
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)