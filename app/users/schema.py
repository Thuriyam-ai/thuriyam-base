from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Username must be between 3 and 50 characters")
    email: EmailStr = Field(..., description="Valid email address")
    full_name: Optional[str] = Field(None, max_length=100, description="Full name of the user")

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters long")

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, description="Valid email address")
    full_name: Optional[str] = Field(None, max_length=100, description="Full name of the user")
    password: Optional[str] = Field(None, min_length=8, description="Password must be at least 8 characters long")

class UserInDBBase(UserBase):
    id: str
    is_active: bool = True
    is_admin: bool = False
    disabled: bool = False

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "user123",
                "username": "johndoe",
                "email": "john@example.com",
                "full_name": "John Doe",
                "is_active": True,
                "is_admin": False,
                "disabled": False
            }
        }

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str 