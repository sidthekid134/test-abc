from fastapi import FastAPI, Depends, HTTPException, Query, status, Body
from sqlmodel import Session, select
from typing import List, Optional, Dict, Any
from datetime import datetime

from .models import Task, TaskCreate, TaskRead, TaskUpdate, TaskStatus, TaskBulkCreate, TaskBulkUpdate
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
    status: Optional[TaskStatus] = None,
    priority: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: Optional[str] = Query(default="created_at", regex="^(id|title|created_at|updated_at|priority|status|due_date)$"),
    sort_order: Optional[str] = Query(default="desc", regex="^(asc|desc)$")
):
    """
    Get all tasks with optional filtering, searching, sorting and pagination
    
    - offset/limit: For pagination
    - status: Filter by task status
    - priority: Filter by priority level
    - search: Search in title and description
    - sort_by: Field to sort by
    - sort_order: Sort direction (asc or desc)
    """
    query = select(Task)
    
    # Apply filters
    if status:
        query = query.where(Task.status == status)
    
    if priority:
        query = query.where(Task.priority == priority)
    
    # Apply search if provided
    if search:
        search_term = f"%{search}%"
        query = query.where(
            (Task.title.ilike(search_term)) | 
            (Task.description.ilike(search_term))
        )
    
    # Apply sorting
    sort_column = getattr(Task, sort_by)
    if sort_order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column)
    
    # Execute query with pagination
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


@app.post("/tasks/bulk", response_model=List[TaskRead], status_code=status.HTTP_201_CREATED)
async def create_tasks_bulk(
    *, 
    session: Session = Depends(get_session), 
    bulk_create: TaskBulkCreate
):
    """
    Create multiple tasks in a single request
    """
    db_tasks = []
    
    try:
        # Convert all TaskCreate objects to Task model instances
        for task_create in bulk_create.tasks:
            db_task = Task.from_orm(task_create)
            session.add(db_task)
            db_tasks.append(db_task)
        
        # Commit all tasks at once (atomic operation)
        session.commit()
        
        # Refresh all tasks to get their IDs
        for task in db_tasks:
            session.refresh(task)
        
        logger.info(f"Bulk created {len(db_tasks)} tasks")
        return db_tasks
    
    except Exception as e:
        logger.error(f"Error bulk creating tasks: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to bulk create tasks",
        )


@app.patch("/tasks/bulk", response_model=List[TaskRead])
async def update_tasks_bulk(
    *,
    session: Session = Depends(get_session),
    bulk_update: TaskBulkUpdate
):
    """
    Update multiple tasks in a single request
    
    Each item in the items list should have:
    - id: The task ID to update
    - updates: The TaskUpdate data
    """
    updated_tasks = []
    not_found_ids = []
    
    try:
        # Process each update request
        for item in bulk_update.items:
            task_id = item.get("id")
            updates = item.get("updates", {})
            
            if not task_id or not isinstance(updates, dict):
                continue
            
            # Get task from database
            db_task = session.get(Task, task_id)
            if not db_task:
                not_found_ids.append(task_id)
                continue
            
            # Apply updates
            for key, value in updates.items():
                if hasattr(db_task, key):
                    setattr(db_task, key, value)
            
            # Set updated_at timestamp
            db_task.updated_at = datetime.now()
            session.add(db_task)
            updated_tasks.append(db_task)
        
        # If all tasks were not found, return 404
        if not updated_tasks and not_found_ids:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No tasks found with the provided IDs: {not_found_ids}"
            )
        
        # Commit all updates
        session.commit()
        
        # Refresh all tasks
        for task in updated_tasks:
            session.refresh(task)
        
        logger.info(f"Bulk updated {len(updated_tasks)} tasks")
        
        # If some tasks were not found, include this in response headers
        if not_found_ids:
            logger.warning(f"Some tasks not found for bulk update: {not_found_ids}")
        
        return updated_tasks
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error bulk updating tasks: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to bulk update tasks",
        )


@app.delete("/tasks/bulk", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tasks_bulk(
    *,
    session: Session = Depends(get_session),
    task_ids: List[int] = Body(...)
):
    """
    Delete multiple tasks by their IDs
    """
    if not task_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No task IDs provided"
        )
    
    try:
        # Find all tasks with the given IDs
        query = select(Task).where(Task.id.in_(task_ids))
        tasks = session.exec(query).all()
        found_ids = [task.id for task in tasks]
        
        # Check if any tasks were not found
        not_found_ids = list(set(task_ids) - set(found_ids))
        if not_found_ids:
            logger.warning(f"Some tasks not found for bulk deletion: {not_found_ids}")
        
        # Delete all found tasks
        for task in tasks:
            session.delete(task)
        
        # Commit deletion
        session.commit()
        logger.info(f"Bulk deleted {len(tasks)} tasks")
    
    except Exception as e:
        logger.error(f"Error bulk deleting tasks: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to bulk delete tasks",
        )