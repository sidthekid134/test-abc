from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from enum import Enum as PyEnum

class TaskStatus(str, PyEnum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class TaskBase(SQLModel):
    """Base class for Task schema."""
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    due_date: Optional[datetime] = None

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
    due_date: Optional[datetime] = None

class TaskRead(TaskBase):
    """Schema for reading a task."""
    id: int
    created_at: datetime
    updated_at: datetime