from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    username: str

class UserRead(BaseModel):
    id: str
    email: EmailStr
    username: str
    created_at: datetime