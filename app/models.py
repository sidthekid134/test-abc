from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4

class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="The health status of the application")
    
# Placeholder for future Todo models that will be implemented in next stories