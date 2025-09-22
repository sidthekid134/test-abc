from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime

from .models import Task, TaskCreate, TaskRead, TaskUpdate, TaskStatus
from .database import create_db_and_tables, get_session

from loguru import logger
import sys

# Configure logger
logger.remove()
logger.add(
    sys.stderr,
    format="{time} {level} {message}",
    level="INFO",
    serialize=False,
)

# Create FastAPI instance
app = FastAPI(
    title="Task Management API",
    description="A simple API for managing tasks",
    version="1.0.0",
)


@app.on_event("startup")
def on_startup():
    """Initialize database on startup"""
    create_db_and_tables()
    logger.info("Application started")


@app.on_event("shutdown")
def on_shutdown():
    """Shutdown event handler"""
    logger.info("Application shutdown")


# Health check endpoint
@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


# Task CRUD endpoints
@app.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(*, session: Session = Depends(get_session), task: TaskCreate):
    """Create a new task"""
    db_task = Task.from_orm(task)
    session.add(db_task)
    
    try:
        session.commit()
        session.refresh(db_task)
        logger.info(f"Task created: {db_task.id}")
        return db_task
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create task",
        )


@app.get("/tasks", response_model=List[TaskRead])
async def read_tasks(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    status: Optional[TaskStatus] = None
):
    """
    Get all tasks with optional filtering and pagination
    """
    query = select(Task)
    
    # Apply filter if status is provided
    if status:
        query = query.where(Task.status == status)
    
    tasks = session.exec(query.offset(offset).limit(limit)).all()
    return tasks


@app.get("/tasks/{task_id}", response_model=TaskRead)
async def read_task(*, session: Session = Depends(get_session), task_id: int):
    """Get a specific task by ID"""
    task = session.get(Task, task_id)
    if not task:
        logger.warning(f"Task not found: {task_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return task


@app.patch("/tasks/{task_id}", response_model=TaskRead)
async def update_task(
    *,
    session: Session = Depends(get_session),
    task_id: int,
    task_update: TaskUpdate,
):
    """Update a task"""
    db_task = session.get(Task, task_id)
    if not db_task:
        logger.warning(f"Task not found for update: {task_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    
    # Update task fields from the request
    task_data = task_update.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)
    
    # Update the updated_at field
    db_task.updated_at = datetime.now()
    
    try:
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        logger.info(f"Task updated: {task_id}")
        return db_task
    except Exception as e:
        logger.error(f"Error updating task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update task",
        )


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(*, session: Session = Depends(get_session), task_id: int):
    """Delete a task"""
    task = session.get(Task, task_id)
    if not task:
        logger.warning(f"Task not found for deletion: {task_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    
    try:
        session.delete(task)
        session.commit()
        logger.info(f"Task deleted: {task_id}")
    except Exception as e:
        logger.error(f"Error deleting task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete task",
        )