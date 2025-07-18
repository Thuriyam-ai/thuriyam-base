from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship, declared_attr
from core.base.model import BaseModel
from core.base.validator import Operation
from users.validator import CreateUserValidator, UpdateUserValidator, DeleteUserValidator
from typing import Any

class User(BaseModel):
    """User model for authentication and authorization"""
    __tablename__ = "users"

    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    @classmethod
    def get_validator(cls, operation: Operation) -> Any:
        if operation == Operation.CREATE:
            return CreateUserValidator
        elif operation == Operation.UPDATE:
            return UpdateUserValidator
        elif operation == Operation.DELETE:
            return DeleteUserValidator
        raise ValueError(f"Unknown operation: {operation}")
