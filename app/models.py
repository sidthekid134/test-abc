from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel

class TaskBase(SQLModel):
    """Base model with shared attributes for Task."""
    title: str = Field(index=True)
    description: Optional[str] = None
    is_completed: bool = Field(default=False)
    due_date: Optional[datetime] = None
    priority: Optional[str] = Field(default="medium")  # low, medium, high

class Task(TaskBase, table=True):
    """Task database model."""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    
    # Relationship
    user: Optional["User"] = Relationship(back_populates="tasks")

class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    pass

class TaskRead(TaskBase):
    """Schema for reading a task."""
    id: int
    created_at: datetime
    updated_at: datetime

class TaskUpdate(SQLModel):
    """Schema for updating a task."""
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    due_date: Optional[datetime] = None
    priority: Optional[str] = None

class UserBase(SQLModel):
    """Base model with shared attributes for User."""
    email: str = Field(index=True, unique=True)
    username: str = Field(index=True, unique=True)
    full_name: Optional[str] = None
    is_active: bool = Field(default=True)

class User(UserBase, table=True):
    """User database model."""
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship
    tasks: List[Task] = Relationship(back_populates="user")

class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str

class UserRead(UserBase):
    """Schema for reading a user."""
    id: int
    created_at: datetime

class UserUpdate(SQLModel):
    """Schema for updating a user."""
    email: Optional[str] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

class Token(BaseModel):
    """Token schema."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Token data schema."""
    username: Optional[str] = None