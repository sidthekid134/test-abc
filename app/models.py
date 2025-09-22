from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel, EmailStr


class TaskBase(SQLModel):
    """Base model for task with common attributes"""
    title: str = Field(index=True)
    description: Optional[str] = Field(default=None)
    due_date: Optional[datetime] = Field(default=None)
    is_completed: bool = Field(default=False)
    priority: Optional[str] = Field(default="medium")


class Task(TaskBase, table=True):
    """Task database model"""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")


class TaskCreate(TaskBase):
    """Schema for creating a task"""
    pass


class TaskRead(TaskBase):
    """Schema for reading a task"""
    id: int
    created_at: datetime
    updated_at: datetime


class TaskUpdate(SQLModel):
    """Schema for updating a task"""
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    is_completed: Optional[bool] = None
    priority: Optional[str] = None


class UserBase(SQLModel):
    """Base model for user with common attributes"""
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)


class User(UserBase, table=True):
    """User database model"""
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    tasks: List["Task"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    """Schema for creating a user"""
    password: str


class UserRead(UserBase):
    """Schema for reading a user"""
    id: int
    created_at: datetime


class UserUpdate(SQLModel):
    """Schema for updating a user"""
    email: Optional[str] = None
    username: Optional[str] = None
    is_active: Optional[bool] = None


class Token(BaseModel):
    """Schema for authentication token"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for token data"""
    username: Optional[str] = None