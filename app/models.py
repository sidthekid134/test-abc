from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from enum import Enum, auto


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELED = "canceled"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class UserBase(SQLModel):
    """Base model for user data"""
    email: str = Field(index=True)
    username: str = Field(index=True)
    is_active: bool = True
    is_superuser: bool = False


class User(UserBase, table=True):
    """User model for database"""
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    
    # Relationships
    tasks: List["Task"] = Relationship(back_populates="owner")


class UserCreate(UserBase):
    """User model for creation"""
    password: str


class UserRead(UserBase):
    """User model for reading"""
    id: int


class UserUpdate(SQLModel):
    """User model for updating"""
    email: Optional[str] = None
    username: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None


class TaskBase(SQLModel):
    """Base model for task data"""
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None


class Task(TaskBase, table=True):
    """Task model for database"""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")
    
    # Relationships
    owner: Optional[User] = Relationship(back_populates="tasks")


class TaskCreate(TaskBase):
    """Task model for creation"""
    pass


class TaskRead(TaskBase):
    """Task model for reading"""
    id: int
    created_at: datetime
    updated_at: datetime
    owner_id: Optional[int] = None


class TaskUpdate(SQLModel):
    """Task model for updating"""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)