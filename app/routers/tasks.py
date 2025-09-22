from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from datetime import datetime

from ..database import get_session
from ..models import Task, TaskCreate, TaskRead, TaskUpdate, User
from ..auth import get_current_active_user

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=TaskRead)
async def create_task(
    task: TaskCreate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new task for the current user"""
    db_task = Task.from_orm(task)
    db_task.owner_id = current_user.id
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    return db_task

@router.get("/", response_model=List[TaskRead])
async def read_tasks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Get all tasks for the current user"""
    tasks = db.exec(
        select(Task)
        .where(Task.owner_id == current_user.id)
        .offset(skip)
        .limit(limit)
    ).all()
    
    return tasks

@router.get("/{task_id}", response_model=TaskRead)
async def read_task(
    task_id: int,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific task by ID"""
    task = db.exec(
        select(Task)
        .where(Task.id == task_id, Task.owner_id == current_user.id)
    ).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    
    return task

@router.patch("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Update a task"""
    db_task = db.exec(
        select(Task)
        .where(Task.id == task_id, Task.owner_id == current_user.id)
    ).first()
    
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    
    # Update task fields
    task_data = task_update.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)
    
    # Update the updated_at field
    db_task.updated_at = datetime.utcnow()
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    return db_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a task"""
    db_task = db.exec(
        select(Task)
        .where(Task.id == task_id, Task.owner_id == current_user.id)
    ).first()
    
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    
    db.delete(db_task)
    db.commit()
    
    return None