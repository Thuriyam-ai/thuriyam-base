from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TodoBase(BaseModel):
    title: str = Field(..., description="The title of the todo item", min_length=1, max_length=200)
    description: Optional[str] = Field(default="", description="Optional description of the todo item", max_length=1000)
    completed: bool = Field(default=False, description="Whether the todo item is completed")

class TodoCreate(TodoBase):
    """Schema for creating a new todo item"""
    pass

class TodoUpdate(BaseModel):
    """Schema for updating a todo item (all fields are optional)"""
    title: Optional[str] = Field(None, description="The title of the todo item", min_length=1, max_length=200)
    description: Optional[str] = Field(None, description="Optional description of the todo item", max_length=1000)
    completed: Optional[bool] = Field(None, description="Whether the todo item is completed")

class TodoResponse(TodoBase):
    """Schema for todo item responses"""
    id: str = Field(..., description="Unique identifier for the todo item")
    created_at: datetime = Field(..., description="Timestamp when the todo was created")
    updated_at: datetime = Field(..., description="Timestamp when the todo was last updated")

    class Config:
        from_attributes = True 