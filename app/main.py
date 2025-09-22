from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from typing import List, Optional
import logging

from .database import get_session, create_db_and_tables
from .models import (
    Task, TaskCreate, TaskRead, TaskUpdate,
    User, UserCreate, UserRead,
    GenericResponse, ErrorResponse
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Task Management API",
    description="A simple task management API built with FastAPI and SQLModel",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event
@app.on_event("startup")
def on_startup():
    logger.info("Starting up the application")
    create_db_and_tables()

# Shutdown event
@app.on_event("shutdown")
def on_shutdown():
    logger.info("Shutting down the application")

# Root endpoint
@app.get("/", response_model=GenericResponse)
async def root():
    return {"message": "Welcome to the Task Management API"}

# Task endpoints
@app.post("/tasks/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate,
    session: Session = Depends(get_session)
):
    # In a real application, you would get the user_id from the authenticated user
    # For now, we'll use a placeholder
    new_task = Task.from_orm(task)
    new_task.user_id = 1  # Placeholder
    
    try:
        session.add(new_task)
        session.commit()
        session.refresh(new_task)
        return new_task
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create task"
        )

@app.get("/tasks/", response_model=List[TaskRead])
async def read_tasks(
    skip: int = 0,
    limit: int = 100,
    completed: Optional[bool] = None,
    session: Session = Depends(get_session)
):
    try:
        query = select(Task)
        
        # Filter by completion status if provided
        if completed is not None:
            query = query.where(Task.is_completed == completed)
        
        tasks = session.exec(query.offset(skip).limit(limit)).all()
        return tasks
    except Exception as e:
        logger.error(f"Error reading tasks: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not retrieve tasks"
        )

@app.get("/tasks/{task_id}", response_model=TaskRead)
async def read_task(
    task_id: int,
    session: Session = Depends(get_session)
):
    try:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID {task_id} not found"
            )
        return task
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error reading task {task_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not retrieve task {task_id}"
        )

@app.patch("/tasks/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    session: Session = Depends(get_session)
):
    try:
        db_task = session.get(Task, task_id)
        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID {task_id} not found"
            )
            
        task_data = task_update.dict(exclude_unset=True)
        for key, value in task_data.items():
            setattr(db_task, key, value)
            
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating task {task_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not update task {task_id}"
        )

@app.delete("/tasks/{task_id}", response_model=GenericResponse)
async def delete_task(
    task_id: int,
    session: Session = Depends(get_session)
):
    try:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID {task_id} not found"
            )
            
        session.delete(task)
        session.commit()
        return {"message": f"Task {task_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting task {task_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not delete task {task_id}"
        )