from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
from uuid import UUID, uuid4

class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="The health status of the application")
    
class TodoCreate(BaseModel):
    """Model for creating a new Todo item."""
    title: str = Field(..., description="The title of the todo item", min_length=1, max_length=100)
    description: Optional[str] = Field(None, description="The description of the todo item")
    completed: bool = Field(False, description="Whether the todo item is completed")
    
class Todo(TodoCreate):
    """Model for a Todo item with additional fields set by the server."""
    id: str = Field(default_factory=lambda: str(uuid4()), description="The unique identifier for the todo item")
    created_at: datetime = Field(default_factory=datetime.now, description="The time the todo item was created")
    updated_at: datetime = Field(default_factory=datetime.now, description="The time the todo item was last updated")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": False,
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            }
        }
        
class TodoUpdate(BaseModel):
    """Model for updating an existing Todo item."""
    title: Optional[str] = Field(None, description="The title of the todo item", min_length=1, max_length=100)
    description: Optional[str] = Field(None, description="The description of the todo item")
    completed: Optional[bool] = Field(None, description="Whether the todo item is completed")
    
class TodoResponse(Todo):
    """Model for the response of a Todo item."""
    pass
    
class TodoListResponse(BaseModel):
    """Model for the response of a list of Todo items."""
    items: List[Todo] = Field(..., description="The list of todo items")
    count: int = Field(..., description="The number of todo items")
    
    class Config:
        json_schema_extra = {
            "example": {
                "items": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "title": "Buy groceries",
                        "description": "Milk, eggs, bread",
                        "completed": False,
                        "created_at": "2023-01-01T00:00:00",
                        "updated_at": "2023-01-01T00:00:00"
                    }
                ],
                "count": 1
            }
        }