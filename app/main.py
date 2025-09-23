from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlmodel import Session, select
from typing import List, Dict, Any
from datetime import datetime
import logging

from .database import get_session, create_db_and_tables
from .models import Task, TaskCreate, TaskRead, TaskUpdate, TaskStatus

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Task Management API",
    description="A simple task management API with CRUD operations",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with a custom response format."""
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "message": "Validation error on request data"
        },
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle all other exceptions."""
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": str(exc),
            "message": "An unexpected error occurred"
        },
    )

@app.on_event("startup")
def on_startup():
    logger.info("Starting up the application...")
    create_db_and_tables()
    logger.info("Database and tables created")

# Task CRUD operations
@app.post("/tasks/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, session: Session = Depends(get_session)):
    """
    Create a new task with the given data.
    
    Args:
        task: The task data
        session: Database session
        
    Returns:
        The created task
    """
    try:
        logger.info(f"Creating new task: {task.title}")
        db_task = Task.from_orm(task)
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        logger.info(f"Task created with ID: {db_task.id}")
        return db_task
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}", exc_info=True)
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create task"
        )

@app.get("/tasks/", response_model=List[TaskRead])
async def read_tasks(
    skip: int = 0,
    limit: int = 100,
    status: TaskStatus = None,
    session: Session = Depends(get_session)
):
    """
    Get a list of tasks with optional filtering and pagination.
    
    Args:
        skip: Number of tasks to skip
        limit: Maximum number of tasks to return
        status: Filter tasks by status
        session: Database session
        
    Returns:
        List of tasks matching the criteria
    """
    try:
        logger.info(f"Fetching tasks with parameters: skip={skip}, limit={limit}, status={status}")
        
        if skip < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Skip parameter must be non-negative"
            )
            
        if limit < 1 or limit > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Limit must be between 1 and 100"
            )
            
        query = select(Task)
        if status:
            query = query.where(Task.status == status)
        
        tasks = session.exec(query.offset(skip).limit(limit)).all()
        logger.info(f"Retrieved {len(tasks)} tasks")
        
        return tasks
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching tasks: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch tasks"
        )

@app.get("/tasks/{task_id}", response_model=TaskRead)
async def read_task(task_id: int, session: Session = Depends(get_session)):
    """
    Get a specific task by ID.
    
    Args:
        task_id: The ID of the task to retrieve
        session: Database session
        
    Returns:
        The task if found
        
    Raises:
        HTTPException: If the task is not found
    """
    try:
        logger.info(f"Fetching task with ID: {task_id}")
        
        if task_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Task ID must be a positive integer"
            )
            
        task = session.get(Task, task_id)
        if not task:
            logger.warning(f"Task with ID {task_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Task not found"
            )
            
        logger.info(f"Retrieved task: {task.title}")
        return task
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching task {task_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve task"
        )

@app.patch("/tasks/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: int, 
    task_update: TaskUpdate,
    session: Session = Depends(get_session)
):
    """
    Update a task with the given data.
    
    Args:
        task_id: The ID of the task to update
        task_update: The update data
        session: Database session
        
    Returns:
        The updated task
        
    Raises:
        HTTPException: If the task is not found or update fails
    """
    try:
        logger.info(f"Updating task with ID: {task_id}")
        
        if task_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Task ID must be a positive integer"
            )
            
        db_task = session.get(Task, task_id)
        if not db_task:
            logger.warning(f"Task with ID {task_id} not found for update")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Task not found"
            )
        
        # Check if there's anything to update
        task_data = task_update.dict(exclude_unset=True)
        if not task_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No data provided for update"
            )
        
        # Update task fields
        logger.info(f"Updating task fields: {', '.join(task_data.keys())}")
        for key, value in task_data.items():
            setattr(db_task, key, value)
        
        # Update the updated_at timestamp
        db_task.updated_at = datetime.utcnow()
        
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        
        logger.info(f"Task {task_id} updated successfully")
        return db_task
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating task {task_id}: {str(e)}", exc_info=True)
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update task"
        )

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, session: Session = Depends(get_session)):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    session.delete(db_task)
    session.commit()
    return None

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)