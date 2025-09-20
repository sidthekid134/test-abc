from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class BaseModel(SQLModel):
    """Base model with common fields for all models."""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)