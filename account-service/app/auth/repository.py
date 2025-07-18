from typing import Optional
from sqlalchemy.orm import Session
from core.base.repository import BaseRepository
from auth.model import JWTToken

class JWTTokenRepository(BaseRepository[JWTToken]):
    def __init__(self, db: Session):
        super().__init__(db, JWTToken)
    
    def get_by_hash(self, token_hash: str) -> Optional[JWTToken]:
        """Find token by hash"""
        return self.db.query(self.model).filter(self.model.token_hash == token_hash).first()
    
    def get_by_user_id(self, user_id: str) -> list[JWTToken]:
        """Find all tokens for a user"""
        return self.db.query(self.model).filter(self.model.user_id == user_id).all()
    
    def revoke_token(self, token_hash: str) -> bool:
        """Revoke a token"""
        token = self.get_by_hash(token_hash)
        if not token:
            return False
        
        self.update(token.id, {"is_revoked": True})
        return True 