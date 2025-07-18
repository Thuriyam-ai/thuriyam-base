from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from sqlalchemy.orm import Session
from core.database import get_db
from users.schema import User, UserCreate, UserUpdate
from users.service import UserService
from core.settings import get_config
from core.security.auth import get_current_user
from datetime import timedelta

router = APIRouter(prefix="/users", tags=["users"])
settings = get_config()

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    
    This endpoint allows registration of new users with username, email, and password.
    """
    user_service = UserService(db)
    return user_service.create_user(user)

@router.post("/token", response_model=dict)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    
    This endpoint allows users to authenticate and receive an access token.
    
    Available scopes:
    - me: Read information about the current user
    - users: Read information about all users
    - admin: Admin access to all operations
    - campaigns:read: Read campaign information
    - campaigns:write: Create and update campaigns
    - campaigns:manage: Full campaign management including status changes
    """
    user_service = UserService(db)
    user = user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # Set default scopes if none provided
    scopes = form_data.scopes or ["me"]
    access_token = user_service.create_access_token(
        data={"sub": user.username, "scopes": scopes},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
def read_users_me(
    current_user: User = Security(get_current_user, scopes=["me"])
):
    """
    Get current user information.
    
    Returns the profile of the currently authenticated user.
    """
    return current_user

@router.get("/", response_model=List[User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Security(get_current_user, scopes=["users"]),
    db: Session = Depends(get_db)
):
    """
    Retrieve users.
    
    Returns a list of users with pagination support.
    Requires 'users' scope permission.
    """
    user_service = UserService(db)
    return user_service.list_users(skip=skip, limit=limit)

@router.get("/{username}", response_model=User)
def read_user_by_username(
    username: str,
    current_user: User = Security(get_current_user, scopes=["admin"]),
    db: Session = Depends(get_db)
):
    """
    Get a specific user by username.
    
    Returns user details for the specified username.
    Requires 'admin' scope permission.
    """
    user_service = UserService(db)
    user = user_service.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{username}", response_model=User)
def update_user(
    username: str,
    user_update: UserUpdate,
    current_user: User = Security(get_current_user, scopes=["admin"]),
    db: Session = Depends(get_db)
):
    """
    Update a user by username.
    
    Updates user information for the specified username.
    Requires 'admin' scope permission.
    """
    user_service = UserService(db)
    user = user_service.update(username, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{username}")
def delete_user(
    username: str,
    current_user: User = Security(get_current_user, scopes=["admin"]),
    db: Session = Depends(get_db)
):
    """
    Delete a user by username.
    
    Permanently deletes the user with the specified username.
    Requires 'admin' scope permission.
    """
    user_service = UserService(db)
    if not user_service.delete(username):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"} 