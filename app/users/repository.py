from typing import Optional, List
from users.model import User
from core.config import get_settings
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from core.base import BaseRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
settings = get_settings()

class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(db, User)

    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()