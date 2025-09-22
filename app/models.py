from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime
from enum import Enum
import uuid


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None


class Task(TaskBase, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: str = Field(foreign_key="user.id")


class TaskCreate(TaskBase):
    pass


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None


class TaskResponse(TaskBase):
    id: str
    created_at: datetime
    updated_at: datetime


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)


class User(UserBase, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True
    tasks: List["Task"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: str
    created_at: datetime
    is_active: bool


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: Optional[str] = None