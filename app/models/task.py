from datetime import datetime
from typing import Optional, List as TypeList
from sqlmodel import SQLModel, Field
from enum import Enum as PyEnum
from pydantic import validator

class TaskStatus(str, PyEnum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class TaskPriority(str, PyEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TaskBase(SQLModel):
    """Base class for Task schema."""
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None
    tags: Optional[TypeList[str]] = Field(default=[])
    completed_at: Optional[datetime] = None

    @validator('title')
    def title_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Title cannot be empty')
        return v

class Task(TaskBase, table=True):
    """Task model for database storage."""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        arbitrary_types_allowed = True

class TaskCreate(TaskBase):
    """Schema for task creation."""
    pass

class TaskUpdate(SQLModel):
    """Schema for task update."""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    tags: Optional[TypeList[str]] = None
    completed_at: Optional[datetime] = None

    @validator('title')
    def title_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Title cannot be empty')
        return v

class TaskRead(TaskBase):
    """Schema for reading a task."""
    id: int
    created_at: datetime
    updated_at: datetime