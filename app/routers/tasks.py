from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlmodel import Session, select, or_, col
from typing import List, Optional
from datetime import datetime

from app.database import get_session
from app.models.task import Task, TaskCreate, TaskRead, TaskUpdate, TaskStatus, TaskPriority

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={
        404: {"description": "Not found"},
        400: {"description": "Bad request"},
        500: {"description": "Internal server error"}
    },
)

@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, session: Session = Depends(get_session)):
    """
    Create a new task.
    
    - **title**: Required task title (cannot be empty)
    - **description**: Optional task description
    - **status**: Task status (todo, in_progress, done)
    - **priority**: Task priority (low, medium, high)
    - **due_date**: Optional due date
    - **tags**: Optional list of tags
    """
    try:
        db_task = Task.from_orm(task)
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"An error occurred while creating the task: {str(e)}"
        )

@router.get("/", response_model=List[TaskRead])
async def read_tasks(
    skip: int = Query(0, ge=0, description="Skip N records"),
    limit: int = Query(100, ge=1, le=1000, description="Limit the number of records returned"),
    status: Optional[TaskStatus] = Query(None, description="Filter by task status"),
    priority: Optional[TaskPriority] = Query(None, description="Filter by task priority"),
    search: Optional[str] = Query(None, description="Search in title and description"),
    session: Session = Depends(get_session)
):
    """
    Read all tasks with filtering, search, and pagination.
    
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    - **status**: Filter tasks by status
    - **priority**: Filter tasks by priority
    - **search**: Search for text in title and description
    """
    try:
        query = select(Task)
        
        # Apply filters
        if status:
            query = query.where(Task.status == status)
        if priority:
            query = query.where(Task.priority == priority)
        if search:
            query = query.where(
                or_(
                    col(Task.title).contains(search),
                    col(Task.description).contains(search)
                )
            )
        
        # Apply pagination
        tasks = session.exec(query.offset(skip).limit(limit)).all()
        return tasks
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving tasks: {str(e)}"
        )

@router.get("/{task_id}", response_model=TaskRead)
async def read_task(
    task_id: int = Path(..., gt=0, description="The ID of the task to retrieve"),
    session: Session = Depends(get_session)
):
    """
    Read a specific task by ID.
    
    - **task_id**: The ID of the task to retrieve
    """
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Task with ID {task_id} not found"
        )
    return task

@router.patch("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: int = Path(..., gt=0, description="The ID of the task to update"),
    task_update: TaskUpdate = None, 
    session: Session = Depends(get_session)
):
    """
    Update a specific task.
    
    - **task_id**: The ID of the task to update
    - **task_update**: The fields to update
    """
    try:
        db_task = session.get(Task, task_id)
        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Task with ID {task_id} not found"
            )
        
        # Update the fields that are provided
        update_data = task_update.dict(exclude_unset=True)
        
        # If status is changed to DONE and completed_at is not set, set it
        if "status" in update_data and update_data["status"] == TaskStatus.DONE and "completed_at" not in update_data:
            update_data["completed_at"] = datetime.utcnow()
        
        for key, value in update_data.items():
            setattr(db_task, key, value)
        
        # Update the updated_at timestamp
        db_task.updated_at = datetime.utcnow()
        
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating the task: {str(e)}"
        )

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int = Path(..., gt=0, description="The ID of the task to delete"),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task.
    
    - **task_id**: The ID of the task to delete
    """
    try:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Task with ID {task_id} not found"
            )
        
        session.delete(task)
        session.commit()
        return None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while deleting the task: {str(e)}"
        )

@router.post("/{task_id}/complete", response_model=TaskRead)
async def complete_task(
    task_id: int = Path(..., gt=0, description="The ID of the task to mark as complete"),
    session: Session = Depends(get_session)
):
    """
    Mark a task as complete.
    
    - **task_id**: The ID of the task to mark as complete
    """
    try:
        db_task = session.get(Task, task_id)
        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Task with ID {task_id} not found"
            )
        
        db_task.status = TaskStatus.DONE
        db_task.completed_at = datetime.utcnow()
        db_task.updated_at = datetime.utcnow()
        
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while marking the task as complete: {str(e)}"
        )

@router.get("/status/{status}", response_model=List[TaskRead])
async def get_tasks_by_status(
    status: TaskStatus = Path(..., description="The status to filter tasks by"),
    skip: int = Query(0, ge=0, description="Skip N records"),
    limit: int = Query(100, ge=1, le=1000, description="Limit the number of records returned"),
    session: Session = Depends(get_session)
):
    """
    Get all tasks with a specific status.
    
    - **status**: The status to filter tasks by
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    """
    try:
        query = select(Task).where(Task.status == status)
        tasks = session.exec(query.offset(skip).limit(limit)).all()
        return tasks
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving tasks: {str(e)}"
        )

@router.get("/priority/{priority}", response_model=List[TaskRead])
async def get_tasks_by_priority(
    priority: TaskPriority = Path(..., description="The priority to filter tasks by"),
    skip: int = Query(0, ge=0, description="Skip N records"),
    limit: int = Query(100, ge=1, le=1000, description="Limit the number of records returned"),
    session: Session = Depends(get_session)
):
    """
    Get all tasks with a specific priority.
    
    - **priority**: The priority to filter tasks by
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    """
    try:
        query = select(Task).where(Task.priority == priority)
        tasks = session.exec(query.offset(skip).limit(limit)).all()
        return tasks
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving tasks: {str(e)}"
        )