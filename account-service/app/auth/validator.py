from pydantic import BaseModel, Field
from datetime import datetime

class CreateJWTTokenValidator(BaseModel):
    token_hash: str = Field(...)
    user_id: str = Field(...)
    expires_at: datetime = Field(...)
    scopes: str = Field(default="")
    is_revoked: bool = Field(default=False) 