from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from enum import Enum as PyEnum
from pydantic import validator


class TaskStatus(str, PyEnum):
    """Enum for task status"""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskPriority(str, PyEnum):
    """Enum for task priority"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskBase(SQLModel):
    """Base model with common task attributes"""
    title: str = Field(index=True)
    description: Optional[str] = None
    status: TaskStatus = Field(default=TaskStatus.TODO)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    due_date: Optional[datetime] = None


class Task(TaskBase, table=True):
    """Task database model"""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    @validator("updated_at", always=True)
    def set_updated_at(cls, v, values):
        """Always update the updated_at field"""
        return datetime.now()


class TaskCreate(TaskBase):
    """Model for creating a task"""
    pass


class TaskUpdate(SQLModel):
    """Model for updating a task (all fields optional)"""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None


class TaskRead(TaskBase):
    """Model for reading a task (includes id and timestamps)"""
    id: int
    created_at: datetime
    updated_at: datetime


class TaskBulkCreate(SQLModel):
    """Model for creating multiple tasks at once"""
    tasks: List[TaskCreate]


class TaskBulkUpdate(SQLModel):
    """Model for updating multiple tasks at once"""
    items: List[dict]  # List of {id: int, updates: TaskUpdate}