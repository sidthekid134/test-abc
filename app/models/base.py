from datetime import datetime
from enum import Enum
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

from app.database import create_db_and_tables as create_tables


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskBase(SQLModel):
    title: str = Field(index=True, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: TaskStatus = Field(default=TaskStatus.TODO)
    due_date: Optional[datetime] = Field(default=None)
    priority: Optional[int] = Field(default=0, ge=0, le=10, description="Priority level (0-10)")
    tags: Optional[str] = Field(default=None, max_length=200, description="Comma-separated tags")


class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")


class TaskCreate(TaskBase):
    due_date: Optional[datetime] = Field(
        default=None, 
        description="Must be a future date if provided"
    )


class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: Optional[TaskStatus] = None
    due_date: Optional[datetime] = None
    priority: Optional[int] = Field(default=None, ge=0, le=10)
    tags: Optional[str] = Field(default=None, max_length=200)


class TaskRead(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime


class UserBase(SQLModel):
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    full_name: Optional[str] = None


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    is_active: bool = True
    tasks: List["Task"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int


# Re-export the create_db_and_tables function
create_db_and_tables = create_tables