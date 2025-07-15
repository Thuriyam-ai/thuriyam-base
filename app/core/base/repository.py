from typing import TypeVar, Generic, Type, Optional, Any, List
from sqlalchemy.orm import Session
import time
import base58
import random
from core.base.validator import Operation, BaseValidator

T = TypeVar('T')

class BaseRepository(Generic[T]):
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model: Type[T] = model

    @staticmethod
    def generate_id() -> str:
        """
        Generates a transaction ID where:
        - First 13 positions are base58 encoded nanosecond timestamp
        - Last 4 positions are random numbers
        """
        # Get current time in nanoseconds
        timestamp_ns = int(time.time_ns())
        
        # Convert to base58
        base58_timestamp = base58.b58encode(timestamp_ns.to_bytes(8, 'big')).decode('ascii')
        
        # Take first 13 characters
        base58_timestamp = base58_timestamp[:13]
        
        # Generate 4 random digits
        random_digits = ''.join(str(random.randint(0, 9)) for _ in range(4))
        
        # Combine timestamp and random digits
        return f"{base58_timestamp}{random_digits}"
    
    def save(self, entity: T) -> T:
        try:
            if hasattr(entity, 'id'):
                entity.id = self.generate_id()

            self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)
            return entity
        except Exception:
            self.db.rollback()
            raise

    def delete(self, id: str) -> bool:
        entity = self.db.query(self.model).filter(self.model.id == id).first()
        if not entity:
            return False

        self.db.delete(entity)
        self.db.commit()
        return True

    def update(self, id: str, update_data: dict[str, Any], operation: Operation = Operation.UPDATE) -> Optional[T]:
        entity = self.db.query(self.model).filter(self.model.id == id).first()
        if not entity:
            return None

        BaseValidator.get_instance().validate(self.model, operation, update_data)

        for field, value in update_data.items():
            setattr(entity, field, value)

        self.db.commit()
        self.db.refresh(entity)
        return entity

    def find_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """
        Get all entities with pagination support.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[T]: List of entities
        """
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def find(self, id: str) -> Optional[T]:
        """
        Find an entity by its ID.
        
        Args:
            id: The ID of the entity to find
            
        Returns:
            Optional[T]: The found entity or None if not found
        """
        return self.db.query(self.model).filter(self.model.id == id).first() 