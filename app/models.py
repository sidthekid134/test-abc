from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from pydantic import BaseModel


class UserBase(SQLModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    tasks: List["Task"] = Relationship(back_populates="owner")


class UserRead(UserBase):
    id: int
    created_at: datetime


class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[int] = 1  # 1-5 scale, 1 is lowest priority
    completed: bool = False


class TaskCreate(TaskBase):
    pass


class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")
    
    owner: Optional[User] = Relationship(back_populates="tasks")


class TaskRead(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime
    owner_id: Optional[int]


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[int] = None
    completed: Optional[bool] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None