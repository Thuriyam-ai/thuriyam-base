from sqlalchemy import Column, String, Boolean
from core.base.model import BaseModel
from core.base.validator import Operation

class Todo(BaseModel):
    __tablename__ = "todos"

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)

    _unset = []

    @classmethod
    def get_validator(cls, operation: Operation):
        from todos.validator import TodoCreateValidator
        return TodoCreateValidator