from fastapi import FastAPI, HTTPException, Depends, Query, status
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime

from app.database import create_db_and_tables, get_session
from app.models import Task, TaskCreate, TaskRead, TaskUpdate, TaskStatus, TaskPriority

# Create FastAPI app instance
app = FastAPI(
    title="Task Management API",
    description="A simple task management API",
    version="1.0.0",
)

# Event handler to create database tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Task Management API is running"}

# Task endpoints
@app.post("/tasks/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(*, session: Session = Depends(get_session), task: TaskCreate):
    """
    Create a new task.
    
    Args:
        session: Database session dependency
        task: Task data from request body
        
    Returns:
        The created task
    """
    db_task = Task.from_orm(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@app.get("/tasks/", response_model=List[TaskRead])
async def read_tasks(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None
):
    """
    Get all tasks with optional filtering.
    
    Args:
        session: Database session dependency
        offset: Number of records to skip
        limit: Maximum number of records to return
        status: Filter by task status
        priority: Filter by task priority
        
    Returns:
        List of tasks matching the criteria
    """
    query = select(Task)
    
    # Apply filters if provided
    if status:
        query = query.where(Task.status == status)
    if priority:
        query = query.where(Task.priority == priority)
        
    tasks = session.exec(query.offset(offset).limit(limit)).all()
    return tasks

@app.get("/tasks/{task_id}", response_model=TaskRead)
async def read_task(*, session: Session = Depends(get_session), task_id: int):
    """
    Get a specific task by ID.
    
    Args:
        session: Database session dependency
        task_id: Task ID from path
        
    Returns:
        The requested task if found
        
    Raises:
        HTTPException: If task not found
    """
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    return task

@app.patch("/tasks/{task_id}", response_model=TaskRead)
async def update_task(
    *,
    session: Session = Depends(get_session),
    task_id: int,
    task_update: TaskUpdate
):
    """
    Update a task partially.
    
    Args:
        session: Database session dependency
        task_id: Task ID from path
        task_update: Task update data from request body
        
    Returns:
        The updated task
        
    Raises:
        HTTPException: If task not found
    """
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    
    # Update task fields
    task_data = task_update.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)
    
    # Update the updated_at timestamp
    db_task.updated_at = datetime.utcnow()
    
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(*, session: Session = Depends(get_session), task_id: int):
    """
    Delete a task.
    
    Args:
        session: Database session dependency
        task_id: Task ID from path
        
    Returns:
        No content
        
    Raises:
        HTTPException: If task not found
    """
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    
    session.delete(task)
    session.commit()
    return None