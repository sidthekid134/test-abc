from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, status, Response
from sqlmodel import Session, select, or_, and_, col

from app.database import get_session
from app.models import Task, TaskCreate, TaskRead, TaskUpdate, TaskStatus

router = APIRouter()


@router.get("/tasks", response_model=List[TaskRead])
def get_tasks(
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    status: Optional[TaskStatus] = None,
    title_contains: Optional[str] = None,
    priority_ge: Optional[int] = None,
    priority_le: Optional[int] = None,
    tags_contain: Optional[str] = None,
    due_before: Optional[datetime] = None,
    due_after: Optional[datetime] = None,
    sort_by: Optional[str] = Query(None, pattern="^(title|created_at|updated_at|due_date|priority)$"),
    sort_order: str = Query("asc", pattern="^(asc|desc)$"),
    session: Session = Depends(get_session),
):
    """
    Retrieve a list of tasks with pagination, filtering, and sorting options.
    
    Parameters:
    - status: Filter by task status
    - title_contains: Filter tasks where title contains this string
    - priority_ge: Filter tasks with priority greater than or equal to this value
    - priority_le: Filter tasks with priority less than or equal to this value
    - tags_contain: Filter tasks that have this tag
    - due_before: Filter tasks due before this date
    - due_after: Filter tasks due after this date
    - sort_by: Field to sort by (title, created_at, updated_at, due_date, priority)
    - sort_order: Sort order (asc, desc)
    """
    query = select(Task)
    
    # Apply filters
    filters = []
    
    if status:
        filters.append(Task.status == status)
    
    if title_contains:
        filters.append(Task.title.contains(title_contains))
    
    if priority_ge is not None:
        filters.append(Task.priority >= priority_ge)
    
    if priority_le is not None:
        filters.append(Task.priority <= priority_le)
    
    if tags_contain:
        filters.append(Task.tags.contains(tags_contain))
    
    if due_before:
        filters.append(Task.due_date <= due_before)
    
    if due_after:
        filters.append(Task.due_date >= due_after)
    
    if filters:
        query = query.where(and_(*filters))
    
    # Apply sorting
    if sort_by:
        sort_column = getattr(Task, sort_by)
        if sort_order == "desc":
            sort_column = sort_column.desc()
        query = query.order_by(sort_column)
    
    # Apply pagination
    query = query.offset(offset).limit(limit)
    
    tasks = session.exec(query).all()
    return tasks


@router.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(
    task_id: int,
    session: Session = Depends(get_session),
):
    """
    Get a specific task by ID.
    """
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )
    return task


@router.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    session: Session = Depends(get_session),
):
    """
    Create a new task.
    
    Validates input data including:
    - Title length and content
    - Description length
    - Due date is in the future if provided
    - Priority value is within allowed range
    """
    # Validate due date is in the future
    if task.due_date and task.due_date < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Due date must be in the future",
        )
    
    # Create and save task
    db_task = Task.from_orm(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.put("/tasks/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    session: Session = Depends(get_session),
):
    """
    Update an existing task by ID.
    
    Validates update data including:
    - Title length and content (if provided)
    - Description length (if provided)
    - Due date is in the future (if provided)
    - Priority value is within allowed range (if provided)
    """
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )
    
    # Validate due date is in the future if provided
    if task_update.due_date and task_update.due_date < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Due date must be in the future",
        )
    
    # Update task attributes
    task_data = task_update.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)
    
    # Update the updated_at timestamp
    db_task.updated_at = datetime.utcnow()
    
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    session: Session = Depends(get_session),
):
    """
    Delete a task by ID.
    """
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )
    
    session.delete(db_task)
    session.commit()
    return None


@router.get("/tasks/search", response_model=List[TaskRead])
def search_tasks(
    query: str = Query(..., min_length=1, description="Search query - will search in title and description"),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    session: Session = Depends(get_session),
):
    """
    Search tasks by title or description.
    
    This endpoint performs a case-insensitive search across task titles and descriptions.
    """
    search_query = select(Task).where(
        or_(
            Task.title.contains(query),
            Task.description.contains(query)
        )
    ).offset(offset).limit(limit)
    
    tasks = session.exec(search_query).all()
    return tasks


@router.patch("/tasks/{task_id}/status", response_model=TaskRead)
def update_task_status(
    task_id: int,
    status: TaskStatus,
    session: Session = Depends(get_session),
):
    """
    Update only the status of a task.
    
    This is a dedicated endpoint for quickly changing a task's status.
    """
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )
    
    db_task.status = status
    db_task.updated_at = datetime.utcnow()
    
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.get("/tasks/count", response_model=dict)
def count_tasks(
    status: Optional[TaskStatus] = None,
    session: Session = Depends(get_session),
):
    """
    Count tasks, optionally filtered by status.
    
    Returns a dictionary with the count.
    """
    query = select(Task)
    if status:
        query = query.where(Task.status == status)
    
    count = len(session.exec(query).all())
    return {"count": count}