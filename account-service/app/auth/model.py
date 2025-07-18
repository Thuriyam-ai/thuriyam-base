from sqlalchemy import Column, String, DateTime, Text
from core.base.model import BaseModel
from core.base.validator import Operation
from typing import Any

class JWTToken(BaseModel):
    """JWT token model for tracking issued tokens"""
    __tablename__ = "jwt_tokens"

    token_hash = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(String, nullable=False, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    scopes = Column(Text, nullable=True)  # JSON string of scopes
    is_revoked = Column(String, default=False)
    
    @classmethod
    def get_validator(cls, operation: Operation) -> Any:
        from auth.validator import CreateJWTTokenValidator
        if operation == Operation.CREATE:
            return CreateJWTTokenValidator
        raise ValueError(f"Unknown operation: {operation}") 