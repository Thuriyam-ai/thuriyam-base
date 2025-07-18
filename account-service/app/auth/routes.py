from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from auth.schema import LoginRequest, TokenResponse, TokenValidationRequest, TokenValidationResponse, JWKSResponse
from auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """Authenticate user and return access token"""
    service = AuthService(db)
    token_response = service.authenticate_user(login_data)
    if not token_response:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_response

@router.post("/validate", response_model=TokenValidationResponse)
async def validate_token(
    token_request: TokenValidationRequest,
    db: Session = Depends(get_db)
):
    """Validate JWT token and return user information"""
    service = AuthService(db)
    return service.validate_token(token_request.token)

@router.get("/jwks", response_model=JWKSResponse)
async def get_jwks(
    db: Session = Depends(get_db)
):
    """Get JSON Web Key Set for JWT validation"""
    service = AuthService(db)
    return service.get_jwks() 