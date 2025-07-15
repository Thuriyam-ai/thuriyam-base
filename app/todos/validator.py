from pydantic import BaseModel, Field

class TodoCreateValidator(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Todo title")
    description: str = Field(default="", max_length=1000, description="Todo description")
    completed: bool = Field(default=False, description="Todo completion status")

class TodoUpdateValidator(BaseModel):
    title: str = Field(None, min_length=1, max_length=200, description="Todo title")
    description: str = Field(None, max_length=1000, description="Todo description")
    completed: bool = Field(None, description="Todo completion status")