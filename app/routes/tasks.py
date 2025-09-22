from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from datetime import datetime
from typing import List

from ..database import get_session
from ..models import Task, TaskCreate, TaskUpdate, TaskResponse, User
from ..auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Create a new task for the current user"""
    db_task = Task.from_orm(task, update={"user_id": current_user.id})
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get all tasks for the current user"""
    tasks = db.exec(
        select(Task)
        .where(Task.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
    ).all()
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: str,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get a specific task by ID"""
    task = db.exec(
        select(Task)
        .where(Task.id == task_id, Task.user_id == current_user.id)
    ).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    task_update: TaskUpdate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Update a specific task by ID"""
    db_task = db.exec(
        select(Task)
        .where(Task.id == task_id, Task.user_id == current_user.id)
    ).first()
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Update the task with the new values
    task_data = task_update.dict(exclude_unset=True)
    task_data["updated_at"] = datetime.utcnow()
    
    for key, value in task_data.items():
        setattr(db_task, key, value)
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    return db_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Delete a specific task by ID"""
    db_task = db.exec(
        select(Task)
        .where(Task.id == task_id, Task.user_id == current_user.id)
    ).first()
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    db.delete(db_task)
    db.commit()
    return None