from typing import List, Optional
from sqlalchemy.orm import Session
from core.base.repository import BaseRepository
from todos.model import Todo

class TodoRepository(BaseRepository[Todo]):
    def __init__(self, db: Session):
        super().__init__(db, Todo)
    
    def find_by_completed(self, completed: bool, skip: int = 0, limit: int = 100) -> List[Todo]:
        """
        Find todos by completion status with pagination.
        
        Args:
            completed: Filter by completion status
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Todo]: List of todos matching the criteria
        """
        return self.db.query(self.model).filter(
            self.model.completed == completed
        ).offset(skip).limit(limit).all()
    
    def find_by_title_contains(self, title: str, skip: int = 0, limit: int = 100) -> List[Todo]:
        """
        Find todos by title containing the given string.
        
        Args:
            title: String to search for in title
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Todo]: List of todos matching the criteria
        """
        return self.db.query(self.model).filter(
            self.model.title.contains(title)
        ).offset(skip).limit(limit).all()
    
    def toggle_completed(self, id: str) -> Optional[Todo]:
        """
        Toggle the completed status of a todo.
        
        Args:
            id: The ID of the todo to toggle
            
        Returns:
            Optional[Todo]: The updated todo or None if not found
        """
        todo = self.find(id)
        if not todo:
            return None
        
        todo.completed = not todo.completed
        self.db.commit()
        self.db.refresh(todo)
        return todo 