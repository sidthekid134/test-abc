from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from datetime import datetime

from app.database import get_session
from app.models import Task, TaskCreate, TaskRead, TaskUpdate

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404: {"description": "Task not found"}},
)


@router.post("/", response_model=TaskRead)
async def create_task(task: TaskCreate, session: Session = Depends(get_session)):
    db_task = Task.from_orm(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.get("/", response_model=List[TaskRead])
async def read_tasks(
    skip: int = 0, 
    limit: int = 100, 
    completed: Optional[bool] = None,
    priority: Optional[int] = None,
    session: Session = Depends(get_session)
):
    query = select(Task)
    
    if completed is not None:
        query = query.where(Task.completed == completed)
    
    if priority is not None:
        query = query.where(Task.priority == priority)
    
    tasks = session.exec(query.offset(skip).limit(limit)).all()
    return tasks


@router.get("/{task_id}", response_model=TaskRead)
async def read_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: int, task_update: TaskUpdate, session: Session = Depends(get_session)
):
    db_task = session.get(Task, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_data = task_update.dict(exclude_unset=True)
    
    # Always update the updated_at timestamp
    task_data["updated_at"] = datetime.utcnow()
    
    for key, value in task_data.items():
        setattr(db_task, key, value)
    
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    
    return db_task


@router.delete("/{task_id}", response_model=TaskRead)
async def delete_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    session.delete(task)
    session.commit()
    
    return task