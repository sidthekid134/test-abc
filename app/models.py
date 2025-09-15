from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import EmailStr

class UserBase(SQLModel):
    username: str = Field(unique=True, index=True)
    email: EmailStr = Field(unique=True, index=True)

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)