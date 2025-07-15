from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from core.database import get_db
from todos.repository import TodoRepository
from todos.schema import TodoCreate, TodoUpdate, TodoResponse
from todos.model import Todo
from core.base.model import ModelBuilder
from core.base.validator import Operation

router = APIRouter(prefix="/todos", tags=["todos"])

def get_todo_repository(db: Session = Depends(get_db)) -> TodoRepository:
    return TodoRepository(db)

@router.post("/", response_model=TodoResponse, summary="Create a new todo", description="Create a new todo item with the provided data")
async def create_todo(
    todo_data: TodoCreate,
    repo: TodoRepository = Depends(get_todo_repository)
):
    """
    Create a new todo item.
    
    - **title**: The title of the todo (required)
    - **description**: Optional description of the todo
    - **completed**: Whether the todo is completed (defaults to False)
    
    Returns the created todo item with generated ID and timestamps.
    """
    todo = ModelBuilder.for_model(Todo).with_operation(
        Operation.CREATE
    ).with_attributes(
        todo_data.model_dump(exclude_unset=True)
    ).build()
    todo = repo.save(todo)
    return TodoResponse.model_validate(todo)

@router.get("/", response_model=List[TodoResponse], summary="Get all todos", description="Retrieve all todos with optional filtering and pagination")
async def get_todos(
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    completed: Optional[bool] = Query(None, description="Filter by completion status (true/false)"),
    title: Optional[str] = Query(None, description="Search by title containing this text"),
    repo: TodoRepository = Depends(get_todo_repository)
):
    """
    Get all todos with optional filtering and pagination.
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return (1-1000)
    - **completed**: Filter by completion status (optional)
    - **title**: Search by title containing text (optional)
    
    Returns a list of todo items matching the criteria.
    """
    if completed is not None:
        return repo.find_by_completed(completed, skip, limit)
    elif title:
        return repo.find_by_title_contains(title, skip, limit)
    else:
        return repo.find_all(skip, limit)

@router.get("/{todo_id}", response_model=TodoResponse, summary="Get a specific todo", description="Retrieve a specific todo by its ID")
async def get_todo(
    todo_id: str,
    repo: TodoRepository = Depends(get_todo_repository)
):
    """
    Get a specific todo by ID.
    
    - **todo_id**: The unique identifier of the todo
    
    Returns the todo item if found, otherwise returns 404.
    """
    todo = repo.find(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.put("/{todo_id}", response_model=TodoResponse, summary="Update a todo", description="Update an existing todo with new data")
async def update_todo(
    todo_id: str,
    todo_data: TodoUpdate,
    repo: TodoRepository = Depends(get_todo_repository)
):
    """
    Update an existing todo.
    
    - **todo_id**: The unique identifier of the todo to update
    - **todo_data**: The updated todo data (all fields are optional for partial updates)
    
    Returns the updated todo item if found, otherwise returns 404.
    """
    # Filter out None values for partial update
    update_data = {k: v for k, v in todo_data.model_dump().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No valid fields to update")
    
    todo = repo.update(todo_id, update_data)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.patch("/{todo_id}/toggle", response_model=TodoResponse, summary="Toggle todo completion", description="Toggle the completed status of a todo")
async def toggle_todo(
    todo_id: str,
    repo: TodoRepository = Depends(get_todo_repository)
):
    """
    Toggle the completed status of a todo.
    
    - **todo_id**: The unique identifier of the todo to toggle
    
    Switches the completed status from true to false or vice versa.
    Returns the updated todo item if found, otherwise returns 404.
    """
    todo = repo.toggle_completed(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.delete("/{todo_id}", summary="Delete a todo", description="Delete a todo by its ID")
async def delete_todo(
    todo_id: str,
    repo: TodoRepository = Depends(get_todo_repository)
):
    """
    Delete a todo by ID.
    
    - **todo_id**: The unique identifier of the todo to delete
    
    Returns a success message if the todo was deleted, otherwise returns 404.
    """
    success = repo.delete(todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"} 