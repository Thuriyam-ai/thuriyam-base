from datetime import timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.settings import get_config
from core.database import get_db
from core.base.model import ModelBuilder, Operation
from core.security.auth import verify_password, get_password_hash
from core.security.jwt import create_access_token
from users.model import User
from users.schema import UserCreate, UserUpdate
from users.repository import UserRepository

settings = get_config()

class UserService:
    def __init__(self, db: Session = Depends(get_db)):
        self.repository = UserRepository(db)

    def create_user(self, input: UserCreate) -> User:

        # Validate user input
        # Building a model using the ModelBuilder instead of the existing build function.
        user = ModelBuilder.for_model(User).with_operation(
            Operation.CREATE
        ).with_attributes(
            input.model_dump(exclude_unset=True)
        ).build()

        # user = User.build(input.model_dump(exclude_unset=True))

        # Check if username or email already exists
        db_user = self.repository.get_user_by_username(user.username)
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )

        # Check if email already exists
        db_user = self.repository.get_user_by_email(user.email)
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Generate Hash password
        hashed_password = get_password_hash(user.password)
        user.hashed_password = hashed_password

        # Create new user
        return self.repository.save(user)

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = self.repository.get_user_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        return create_access_token(data, expires_delta)

    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.repository.get_user_by_username(username)

    def update(self, username: str, user_update: UserUpdate) -> Optional[User]:
        db_user = self.get_user_by_username(username)
        if not db_user:
            return None

        update_data = user_update.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

        return self.repository.update(db_user.id, update_data)

    def delete(self, username: str) -> bool:
        db_user = self.get_user_by_username(username)
        if not db_user:
            return False

        return self.repository.delete(db_user.id)

    def list_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        return self.repository.find_all(skip=skip, limit=limit) 