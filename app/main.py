from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List, Optional
import logging

from .database import get_session
from .models import TaskCreate, TaskResponse, TaskUpdate, Task

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Task Management API",
    description="A RESTful API for managing tasks",
    version="1.0.0"
)

@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "Task Management API is running"}

@app.post("/tasks/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, session: Session = Depends(get_session)):
    """Create a new task"""
    try:
        db_task = Task.from_orm(task)
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        logger.info(f"Task created: {db_task.id}")
        return db_task
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create task"
        )

@app.get("/tasks/", response_model=List[TaskResponse], status_code=status.HTTP_200_OK)
async def read_tasks(
    skip: int = 0,
    limit: int = 100,
    completed: Optional[bool] = None,
    session: Session = Depends(get_session)
):
    """Get all tasks with optional filtering by completion status"""
    try:
        query = select(Task)
        
        if completed is not None:
            query = query.where(Task.is_completed == completed)
            
        tasks = session.exec(query.offset(skip).limit(limit)).all()
        return tasks
    except Exception as e:
        logger.error(f"Error retrieving tasks: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve tasks"
        )

@app.get("/tasks/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def read_task(task_id: int, session: Session = Depends(get_session)):
    """Get a specific task by ID"""
    try:
        task = session.get(Task, task_id)
        if not task:
            logger.warning(f"Task not found: {task_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        return task
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving task {task_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve task"
        )

@app.put("/tasks/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    session: Session = Depends(get_session)
):
    """Update an existing task"""
    try:
        db_task = session.get(Task, task_id)
        if not db_task:
            logger.warning(f"Task not found for update: {task_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
            
        task_data = task_update.dict(exclude_unset=True)
        for key, value in task_data.items():
            setattr(db_task, key, value)
            
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        
        logger.info(f"Task updated: {task_id}")
        return db_task
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating task {task_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update task"
        )

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, session: Session = Depends(get_session)):
    """Delete a task"""
    try:
        db_task = session.get(Task, task_id)
        if not db_task:
            logger.warning(f"Task not found for deletion: {task_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
            
        session.delete(db_task)
        session.commit()
        
        logger.info(f"Task deleted: {task_id}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting task {task_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete task"
        )