from sqlalchemy import Column, String, Boolean, Integer
from core.base.model import BaseModel
from core.base.validator import Operation

class Note(BaseModel):
    __tablename__ = "notes"

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    active = Column(Boolean, default=False)
    folder_id = Column(Integer, nullable=False)
    