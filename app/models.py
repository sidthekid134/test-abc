from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from pydantic import BaseModel, EmailStr


class UserBase(SQLModel):
    """Base model for user data."""
    email: EmailStr
    username: str
    is_active: bool = True


class User(UserBase, table=True):
    """User model for database storage."""
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship with tasks
    tasks: List["Task"] = Relationship(back_populates="owner")


class UserCreate(UserBase):
    """Model for user creation."""
    password: str


class UserRead(UserBase):
    """Model for user response."""
    id: int
    created_at: datetime


class UserUpdate(SQLModel):
    """Model for user update."""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None


class TaskBase(SQLModel):
    """Base model for task data."""
    title: str
    description: Optional[str] = None
    status: str = "pending"  # pending, in_progress, completed
    priority: str = "medium"  # low, medium, high
    due_date: Optional[datetime] = None


class Task(TaskBase, table=True):
    """Task model for database storage."""
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship with user
    owner: User = Relationship(back_populates="tasks")


class TaskCreate(TaskBase):
    """Model for task creation."""
    pass


class TaskRead(TaskBase):
    """Model for task response."""
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime


class TaskUpdate(SQLModel):
    """Model for task update."""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None


class Token(BaseModel):
    """Token model for authentication."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data model for authentication."""
    username: Optional[str] = None