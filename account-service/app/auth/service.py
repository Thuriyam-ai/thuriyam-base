from datetime import timedelta
from typing import Optional, List
from sqlalchemy.orm import Session
from core.base.model import ModelBuilder, Operation
from auth.model import JWTToken
from auth.schema import LoginRequest, TokenResponse, TokenValidationResponse
from auth.repository import JWTTokenRepository
from users.service import UserService
from shared.utils.jwt import create_access_token, decode_token, get_jwks
import hashlib
import json

class AuthService:
    def __init__(self, db: Session):
        self.user_service = UserService(db)
        self.token_repository = JWTTokenRepository(db)
    
    def authenticate_user(self, login_data: LoginRequest) -> Optional[TokenResponse]:
        """Authenticate user and return access token"""
        user = self.user_service.authenticate_user(login_data.username, login_data.password)
        if not user:
            return None
        
        # Create access token
        scopes = login_data.scopes or ["me"]
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={
                "sub": user.username,
                "user_id": user.id,
                "email": user.email,
                "scopes": scopes
            },
            expires_delta=access_token_expires
        )
        
        # Store token hash for potential revocation
        token_hash = hashlib.sha256(access_token.encode()).hexdigest()
        token_model = ModelBuilder.for_model(JWTToken).with_operation(
            Operation.CREATE
        ).with_attributes({
            "token_hash": token_hash,
            "user_id": user.id,
            "expires_at": user.last_login + access_token_expires,
            "scopes": json.dumps(scopes),
            "is_revoked": False
        }).build()
        
        self.token_repository.save(token_model)
        
        return TokenResponse(
            access_token=access_token,
            expires_in=access_token_expires.seconds,
            scopes=scopes
        )
    
    def validate_token(self, token: str) -> TokenValidationResponse:
        """Validate JWT token and return user information"""
        try:
            payload = decode_token(token)
            if not payload:
                return TokenValidationResponse(valid=False, error="Invalid token")
            
            username = payload.get("sub")
            if not username:
                return TokenValidationResponse(valid=False, error="Missing user information")
            
            # Check if token is revoked
            token_hash = hashlib.sha256(token.encode()).hexdigest()
            stored_token = self.token_repository.get_by_hash(token_hash)
            if stored_token and stored_token.is_revoked:
                return TokenValidationResponse(valid=False, error="Token revoked")
            
            # Get user information
            user = self.user_service.get_user_by_username(username)
            if not user:
                return TokenValidationResponse(valid=False, error="User not found")
            
            return TokenValidationResponse(
                valid=True,
                user={
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "roles": ["user", "admin"] if user.is_admin else ["user"],
                    "scopes": payload.get("scopes", [])
                }
            )
        except Exception as e:
            return TokenValidationResponse(valid=False, error=str(e))
    
    def get_jwks(self) -> dict:
        """Get JSON Web Key Set for JWT validation"""
        return get_jwks() 