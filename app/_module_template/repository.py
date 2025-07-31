from typing import List, Optional
from sqlalchemy.orm import Session
from core.base.repository import BaseRepository
from __MODULE_NAME__.model import __CLASS_NAME__

class __CLASS_NAME__Repository(BaseRepository[__CLASS_NAME__]):
    def __init__(self, db: Session):
        super().__init__(db, __CLASS_NAME__)
