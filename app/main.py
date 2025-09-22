from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
import logging
from loguru import logger

from .database import get_session, create_db_and_tables
from .models import Task, TaskCreate, TaskRead, TaskUpdate

# Configure logging
logger.add(
    "app.log",
    rotation="10 MB",
    level="INFO",
    format="{time} | {level} | {message}",
    backtrace=True,
    diagnose=True,
)

app = FastAPI(
    title="Task Management API",
    description="A simple task management API built with FastAPI",
    version="0.1.0",
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    """Initialize database on startup"""
    logger.info("Starting up the application")
    create_db_and_tables()


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    logger.debug("Health check called")
    return {"status": "healthy", "timestamp": datetime.utcnow()}


# CRUD operations for tasks
@app.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
async def create_task(task: TaskCreate, session: Session = Depends(get_session)):
    """Create a new task"""
    logger.info(f"Creating new task: {task.title}")
    db_task = Task.from_orm(task)
    
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    
    return db_task


@app.get("/tasks", response_model=List[TaskRead], tags=["Tasks"])
async def get_tasks(
    session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
    completed: Optional[bool] = None
):
    """Get all tasks with optional filtering"""
    logger.info(f"Retrieving tasks (skip={skip}, limit={limit}, completed={completed})")
    
    query = select(Task)
    
    # Apply filters if provided
    if completed is not None:
        query = query.where(Task.is_completed == completed)
    
    # Apply pagination
    query = query.offset(skip).limit(limit)
    
    tasks = session.exec(query).all()
    return tasks


@app.get("/tasks/{task_id}", response_model=TaskRead, tags=["Tasks"])
async def get_task(task_id: int, session: Session = Depends(get_session)):
    """Get a specific task by ID"""
    logger.info(f"Retrieving task with ID: {task_id}")
    
    task = session.get(Task, task_id)
    if not task:
        logger.warning(f"Task not found: {task_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    
    return task


@app.patch("/tasks/{task_id}", response_model=TaskRead, tags=["Tasks"])
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    session: Session = Depends(get_session)
):
    """Update a task"""
    logger.info(f"Updating task with ID: {task_id}")
    
    db_task = session.get(Task, task_id)
    if not db_task:
        logger.warning(f"Task not found for update: {task_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    
    # Update task fields
    task_data = task_update.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)
    
    # Update timestamp
    db_task.updated_at = datetime.utcnow()
    
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    
    return db_task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Tasks"])
async def delete_task(task_id: int, session: Session = Depends(get_session)):
    """Delete a task"""
    logger.info(f"Deleting task with ID: {task_id}")
    
    task = session.get(Task, task_id)
    if not task:
        logger.warning(f"Task not found for deletion: {task_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    
    session.delete(task)
    session.commit()
    
    return None