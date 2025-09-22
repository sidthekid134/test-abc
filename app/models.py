from sqlmodel import Field, SQLModel
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr, validator

# SQLModel models for database tables
class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    is_completed: bool = False
    priority: Optional[str] = "medium"  # low, medium, high

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    is_completed: Optional[bool] = None
    priority: Optional[str] = None
    
    @validator('priority')
    def validate_priority(cls, v):
        if v not in ["low", "medium", "high", None]:
            raise ValueError('Priority must be low, medium, or high')
        return v

# User models
class UserBase(SQLModel):
    email: EmailStr
    username: str
    is_active: bool = True

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    created_at: datetime

# Response models
class GenericResponse(BaseModel):
    message: str
    
class ErrorResponse(BaseModel):
    detail: str