from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from pydantic import validator

class TaskBase(SQLModel):
    """Base model for task data"""
    title: str
    description: Optional[str] = None
    is_completed: bool = False
    due_date: Optional[datetime] = None
    priority: Optional[int] = 0

class Task(TaskBase, table=True):
    """SQLModel for the task table"""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TaskCreate(TaskBase):
    """Model for creating a new task"""
    @validator('title')
    def title_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Title cannot be empty')
        return v

class TaskUpdate(SQLModel):
    """Model for updating a task with optional fields"""
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    due_date: Optional[datetime] = None
    priority: Optional[int] = None
    
    @validator('title')
    def title_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Title cannot be empty')
        return v

class TaskResponse(TaskBase):
    """Model for task response"""
    id: int
    created_at: datetime
    updated_at: datetime