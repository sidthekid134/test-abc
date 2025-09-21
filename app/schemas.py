from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime

from .models import TaskPriority, TaskCategory, UserRole


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str

    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None


class UserProfileBase(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    theme_preference: Optional[str] = Field(default="light")


class UserProfileCreate(UserProfileBase):
    pass


class UserProfileUpdate(UserProfileBase):
    pass


class UserProfileResponse(UserProfileBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserResponse(UserBase):
    id: int
    is_active: bool
    role: UserRole
    created_at: datetime
    updated_at: datetime
    profile: Optional[UserProfileResponse] = None

    class Config:
        orm_mode = True


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: TaskPriority = TaskPriority.MEDIUM
    category: TaskCategory = TaskCategory.OTHER


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[TaskPriority] = None
    category: Optional[TaskCategory] = None


class TaskResponse(TaskBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None