from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from typing import List
import uvicorn
import logging

from app.database import get_session, create_db_and_tables
from app.models import Task, TaskCreate, TaskRead, TaskUpdate

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Task Management API",
    description="A simple task management API built with FastAPI and SQLModel",
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

@app.on_event("startup")
def on_startup():
    """Create database tables on startup."""
    logger.info("Creating database tables...")
    create_db_and_tables()

# Task endpoints
@app.post("/tasks/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate, 
    session: Session = Depends(get_session)
):
    """Create a new task."""
    db_task = Task.from_orm(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    logger.info(f"Task created: {db_task.id}")
    return db_task

@app.get("/tasks/", response_model=List[TaskRead])
async def read_tasks(
    skip: int = 0, 
    limit: int = 100, 
    session: Session = Depends(get_session)
):
    """Get all tasks with pagination."""
    tasks = session.exec(select(Task).offset(skip).limit(limit)).all()
    return tasks

@app.get("/tasks/{task_id}", response_model=TaskRead)
async def read_task(
    task_id: int, 
    session: Session = Depends(get_session)
):
    """Get a specific task by ID."""
    task = session.get(Task, task_id)
    if not task:
        logger.warning(f"Task not found: {task_id}")
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.patch("/tasks/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: int, 
    task_update: TaskUpdate, 
    session: Session = Depends(get_session)
):
    """Update a task."""
    db_task = session.get(Task, task_id)
    if not db_task:
        logger.warning(f"Task not found: {task_id}")
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update task attributes
    task_data = task_update.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)
    
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    logger.info(f"Task updated: {task_id}")
    return db_task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int, 
    session: Session = Depends(get_session)
):
    """Delete a task."""
    task = session.get(Task, task_id)
    if not task:
        logger.warning(f"Task not found: {task_id}")
        raise HTTPException(status_code=404, detail="Task not found")
    
    session.delete(task)
    session.commit()
    logger.info(f"Task deleted: {task_id}")
    return None

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)