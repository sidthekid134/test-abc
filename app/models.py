from sqlmodel import Field, SQLModel
from typing import Optional


class BaseModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    class Config:
        arbitrary_types_allowed = True