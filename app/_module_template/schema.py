from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class __CLASS_NAME__Base(BaseModel):
    # TODO Add attributes from the model that will always be available in the schema of __SINGULAR_NAME__
    pass

class __CLASS_NAME__Create(__CLASS_NAME__Base):
    """Schema for creating a new __SINGULAR_NAME__ item"""
    pass

class __CLASS_NAME__Update(BaseModel):
    """Schema for updating a __SINGULAR_NAME__ item (all fields are optional)"""
    pass

class __CLASS_NAME__Response(__CLASS_NAME__Base):
    """Schema for __SINGULAR_NAME__ item responses"""
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True