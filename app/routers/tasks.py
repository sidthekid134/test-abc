from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select
from datetime import datetime
from pydantic import ValidationError
import logging

from app.database import get_session
from app.models import Task, TaskCreate, TaskRead, TaskUpdate

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404: {"description": "Task not found"}},
)


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED, responses={
    201: {"description": "Task created successfully"},
    422: {"description": "Validation error"},
    500: {"description": "Internal server error"}
})
async def create_task(task: TaskCreate, session: Session = Depends(get_session)):
    try:
        # Create task instance from input model
        db_task = Task.from_orm(task)
        
        # Validate priority range
        if db_task.priority is not None and (db_task.priority < 1 or db_task.priority > 5):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Priority must be between 1 and 5"
            )
            
        # Add task to database
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        
        logger.info(f"Created task with ID: {db_task.id}")
        return db_task
        
    except ValidationError as e:
        logger.error(f"Validation error when creating task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create task"
        )


@router.get("/", response_model=List[TaskRead], responses={
    200: {"description": "List of tasks"},
    500: {"description": "Internal server error"}
})
async def read_tasks(
    skip: int = Query(0, ge=0, description="Number of tasks to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of tasks to return"),
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    priority: Optional[int] = Query(None, ge=1, le=5, description="Filter by priority level (1-5)"),
    title: Optional[str] = Query(None, description="Filter by task title (case insensitive, partial match)"),
    sort_by: str = Query("created_at", description="Sort field"),
    sort_order: str = Query("desc", description="Sort order (asc or desc)"),
    session: Session = Depends(get_session)
):
    try:
        # Build query
        query = select(Task)
        
        # Apply filters
        if completed is not None:
            query = query.where(Task.completed == completed)
        
        if priority is not None:
            query = query.where(Task.priority == priority)
            
        if title is not None:
            query = query.where(Task.title.contains(title))
        
        # Apply sorting
        if sort_by not in ["created_at", "updated_at", "due_date", "priority", "title"]:
            sort_by = "created_at"
            
        if sort_order.lower() not in ["asc", "desc"]:
            sort_order = "desc"
            
        sort_column = getattr(Task, sort_by)
        if sort_order.lower() == "desc":
            sort_column = sort_column.desc()
        else:
            sort_column = sort_column.asc()
            
        query = query.order_by(sort_column)
        
        # Execute query with pagination
        tasks = session.exec(query.offset(skip).limit(limit)).all()
        logger.info(f"Retrieved {len(tasks)} tasks")
        return tasks
        
    except Exception as e:
        logger.error(f"Error retrieving tasks: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve tasks"
        )


@router.get("/{task_id}", response_model=TaskRead, responses={
    200: {"description": "Task details"},
    404: {"description": "Task not found"},
    500: {"description": "Internal server error"}
})
async def read_task(task_id: int, session: Session = Depends(get_session)):
    try:
        task = session.get(Task, task_id)
        if task is None:
            logger.warning(f"Task with ID {task_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        logger.info(f"Retrieved task with ID: {task_id}")
        return task
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving task {task_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve task"
        )


@router.patch("/{task_id}", response_model=TaskRead, responses={
    200: {"description": "Task updated successfully"},
    404: {"description": "Task not found"},
    422: {"description": "Validation error"},
    500: {"description": "Internal server error"}
})
async def update_task(
    task_id: int, task_update: TaskUpdate, session: Session = Depends(get_session)
):
    try:
        # Find task
        db_task = session.get(Task, task_id)
        if db_task is None:
            logger.warning(f"Task with ID {task_id} not found when attempting update")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
            
        # Extract valid update data
        task_data = task_update.dict(exclude_unset=True)
        
        # Validate priority if provided
        if "priority" in task_data and task_data["priority"] is not None:
            if task_data["priority"] < 1 or task_data["priority"] > 5:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Priority must be between 1 and 5"
                )
        
        # Always update the updated_at timestamp
        task_data["updated_at"] = datetime.utcnow()
        
        # Apply updates
        for key, value in task_data.items():
            setattr(db_task, key, value)
        
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        
        logger.info(f"Updated task with ID: {task_id}")
        return db_task
        
    except ValidationError as e:
        logger.error(f"Validation error when updating task {task_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating task {task_id}: {str(e)}")
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update task"
        )


@router.delete("/{task_id}", response_model=TaskRead, responses={
    200: {"description": "Task deleted successfully"},
    404: {"description": "Task not found"},
    500: {"description": "Internal server error"}
})
async def delete_task(task_id: int, session: Session = Depends(get_session)):
    try:
        task = session.get(Task, task_id)
        if task is None:
            logger.warning(f"Task with ID {task_id} not found when attempting delete")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        session.delete(task)
        session.commit()
        
        logger.info(f"Deleted task with ID: {task_id}")
        return task
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting task {task_id}: {str(e)}")
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete task"
        )