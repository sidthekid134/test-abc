"""
SQLModel models for the Apollo application.
"""
from typing import Optional, List
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship


class UserBase(SQLModel):
    """Base model for User data."""
    username: str = Field(index=True)
    email: str = Field(unique=True, index=True)
    full_name: Optional[str] = None
    is_active: bool = True


class User(UserBase, table=True):
    """User model for database table."""
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    items: List["Item"] = Relationship(back_populates="owner")


class UserCreate(UserBase):
    """User model for creation endpoints."""
    password: str


class UserRead(UserBase):
    """User model for read operations."""
    id: int
    created_at: datetime


class UserUpdate(SQLModel):
    """User model for update operations."""
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None


class ItemBase(SQLModel):
    """Base model for Item data."""
    name: str
    description: Optional[str] = None
    price: float = Field(ge=0)
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")


class Item(ItemBase, table=True):
    """Item model for database table."""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    owner: Optional[User] = Relationship(back_populates="items")


class ItemCreate(ItemBase):
    """Item model for creation endpoints."""
    pass


class ItemRead(ItemBase):
    """Item model for read operations."""
    id: int
    created_at: datetime


class ItemUpdate(SQLModel):
    """Item model for update operations."""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(default=None, ge=0)