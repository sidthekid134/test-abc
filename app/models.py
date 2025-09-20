from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class BaseModel(SQLModel, table=False):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)