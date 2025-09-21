from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime


class UserBase(SQLModel):
    """Base class for User models."""
    email: str = Field(index=True)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool = True


class User(UserBase, table=True):
    """User database model."""
    id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships can be defined here
    # items: List["Item"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    """User creation model."""
    password: str


class UserRead(UserBase):
    """User response model."""
    id: int
    created_at: datetime
    updated_at: datetime


# Add more models as needed
# class Item(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     name: str
#     description: Optional[str] = None
#     user_id: Optional[int] = Field(default=None, foreign_key="user.id")
#     user: Optional[User] = Relationship(back_populates="items")