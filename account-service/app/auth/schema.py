from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class LoginRequest(BaseModel):
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")
    scopes: Optional[List[str]] = Field(default=["me"], description="Requested scopes")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    scopes: List[str]

class TokenValidationRequest(BaseModel):
    token: str = Field(..., description="JWT token to validate")

class TokenValidationResponse(BaseModel):
    valid: bool
    user: Optional[dict] = None
    error: Optional[str] = None

class JWKSResponse(BaseModel):
    keys: List[dict] 