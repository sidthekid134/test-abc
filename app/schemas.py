from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


# Enums for task properties
class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in-progress"
    completed = "completed"


class TaskPriority(str, Enum):
    low = "low"
    medium = "medium" 
    high = "high"


class TaskCategory(str, Enum):
    work = "work"
    personal = "personal"
    health = "health"
    finance = "finance"
    education = "education"
    other = "other"


# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)


class UserInDB(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class User(UserInDB):
    pass


# User preference schemas
class UserPreferenceBase(BaseModel):
    default_task_view: Optional[str] = "all"
    default_sort_field: Optional[str] = "created_at"
    default_sort_direction: Optional[str] = "desc"
    theme: Optional[str] = "light"
    notifications_enabled: Optional[bool] = True


class UserPreferenceCreate(UserPreferenceBase):
    pass


class UserPreferenceUpdate(UserPreferenceBase):
    pass


class UserPreferenceInDB(UserPreferenceBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class UserPreference(UserPreferenceInDB):
    pass


# Task schemas
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.pending
    priority: TaskPriority = TaskPriority.medium
    category: TaskCategory = TaskCategory.other


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    category: Optional[TaskCategory] = None


class TaskInDB(TaskBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class Task(TaskInDB):
    pass


# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# Task filter schemas
class TaskFilter(BaseModel):
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None 
    category: Optional[TaskCategory] = None
    search_term: Optional[str] = None


# Response models
class UserWithPreferences(User):
    preferences: Optional[UserPreference] = None


class UserWithTasks(User):
    tasks: List[Task] = []