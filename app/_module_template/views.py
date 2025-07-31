from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Security
from sqlalchemy.orm import Session
from core.database import get_db
from core.base.model import ModelBuilder
from core.base.validator import Operation
from core.security import get_current_user, User
from __MODULE_NAME__.repository import __CLASS_NAME__Repository
from __MODULE_NAME__.service import __CLASS_NAME__Service
from __MODULE_NAME__.schema import __CLASS_NAME__Create, __CLASS_NAME__Update, __CLASS_NAME__Response
from __MODULE_NAME__.model import __CLASS_NAME__

router = APIRouter(prefix="/__MODULE_NAME__", tags=["__MODULE_NAME__"])

@router.post("/", response_model=__CLASS_NAME__Response, summary="Create a new __SINGULAR_NAME__", description="Create a new __SINGULAR_NAME__ item with the provided data")
async def create___SINGULAR_VAR_NAME__(
    __SINGULAR_VAR_NAME___data: __CLASS_NAME__Create,
    __SINGULAR_VAR_NAME___service: __CLASS_NAME__Service = Depends(__CLASS_NAME__Service),
    current_user: User = Security(get_current_user, scopes=["admin"]), # TODO: Add appropriate scopes for the operation
):
    """
    Create a new __SINGULAR_NAME__ item.
    
    - **title**: The title of the __SINGULAR_NAME__ (required)
    - **description**: Optional description of the __SINGULAR_NAME__
    - **completed**: Whether the __SINGULAR_NAME__ is completed (defaults to False)
    
    Returns the created __SINGULAR_NAME__ item with generated ID and timestamps.
    """
    return __SINGULAR_VAR_NAME___service.create___SINGULAR_VAR_NAME__(__SINGULAR_VAR_NAME___data)

@router.get("/", response_model=List[__CLASS_NAME__Response], summary="Get all __MODULE_NAME__", description="Retrieve all __MODULE_NAME__ with optional filtering and pagination")
async def get___MODULE_NAME__(
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    __SINGULAR_VAR_NAME___service: __CLASS_NAME__Service = Depends(__CLASS_NAME__Service),
    current_user: User = Security(get_current_user, scopes=["admin"]), # TODO: Add appropriate scopes for the operation
):
    """
    Get all __MODULE_NAME__ with optional filtering and pagination.
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return (1-1000)
    - **completed**: Filter by completion status (optional)
    - **title**: Search by title containing text (optional)
    
    Returns a list of __SINGULAR_NAME__ items matching the criteria.
    """
    return __SINGULAR_VAR_NAME___service.list(skip, limit)

@router.get("/{{ '{' }}__SINGULAR_VAR_NAME___id{{ '}' }}", response_model=__CLASS_NAME__Response, summary="Get a specific __SINGULAR_NAME__", description="Retrieve a specific __SINGULAR_NAME__ by its ID")
async def get___SINGULAR_VAR_NAME__(
    __SINGULAR_VAR_NAME___id: str,
    __SINGULAR_VAR_NAME___service: __CLASS_NAME__Service = Depends(__CLASS_NAME__Service),
    current_user: User = Security(get_current_user, scopes=["admin"]), # TODO: Add appropriate scopes for the operation
):
    """
    Get a specific __SINGULAR_NAME__ by ID.
    
    - **__SINGULAR_VAR_NAME___id**: The unique identifier of the __SINGULAR_NAME__
    
    Returns the __SINGULAR_NAME__ item if found, otherwise returns 404.
    """
    __SINGULAR_VAR_NAME__ = __SINGULAR_VAR_NAME___service.get(__SINGULAR_VAR_NAME___id)
    if not __SINGULAR_VAR_NAME__:
        raise HTTPException(status_code=404, detail="__CLASS_NAME__ not found")
    return __SINGULAR_VAR_NAME__

@router.put("/{{ '{' }}__SINGULAR_VAR_NAME___id{{ '}' }}", response_model=__CLASS_NAME__Response, summary="Update a __SINGULAR_NAME__", description="Update an existing __SINGULAR_NAME__ with new data")
async def update___SINGULAR_VAR_NAME__(
    __SINGULAR_VAR_NAME___id: str,
    __SINGULAR_VAR_NAME___data: __CLASS_NAME__Update,
    __SINGULAR_VAR_NAME___service: __CLASS_NAME__Service = Depends(__CLASS_NAME__Service),
    current_user: User = Security(get_current_user, scopes=["admin"]), # TODO: Add appropriate scopes for the operation
):
    """
    Update an existing __SINGULAR_NAME__.
    
    - **__SINGULAR_VAR_NAME___id**: The unique identifier of the __SINGULAR_NAME__ to update
    - **__SINGULAR_VAR_NAME___data**: The updated __SINGULAR_NAME__ data (all fields are optional for partial updates)
    
    Returns the updated __SINGULAR_NAME__ item if found, otherwise returns 404.
    """
    # Filter out None values for partial update
    update_data = {k: v for k, v in __SINGULAR_VAR_NAME___data.model_dump().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No valid fields to update")
    
    __SINGULAR_VAR_NAME__ = __SINGULAR_VAR_NAME___service.update(__SINGULAR_VAR_NAME___id, update_data)
    if not __SINGULAR_VAR_NAME__:
        raise HTTPException(status_code=404, detail="__CLASS_NAME__ not found")
    return __SINGULAR_VAR_NAME__

@router.patch("/{{ '{' }}__SINGULAR_VAR_NAME___id{{ '}' }}/", response_model=__CLASS_NAME__Response, summary="Patch __SINGULAR_NAME__", description="Patch the data of a __SINGULAR_NAME__")
async def patch___SINGULAR_VAR_NAME__(
    __SINGULAR_VAR_NAME___id: str,
    __SINGULAR_VAR_NAME___service: __CLASS_NAME__Service = Depends(__CLASS_NAME__Service),
    current_user: User = Security(get_current_user, scopes=["admin"]), # TODO: Add appropriate scopes for the operation
):
    """
    Patch the data of a __SINGULAR_NAME__.
    
    - **__SINGULAR_VAR_NAME___id**: The unique identifier of the __SINGULAR_NAME__ to toggle
    
    Returns the updated __SINGULAR_NAME__ item if found, otherwise returns 404.
    """
    raise NotImplementedError("Patch operation is not implemented")

@router.delete("/{{ '{' }}__SINGULAR_VAR_NAME___id{{ '}' }}", summary="Delete a __SINGULAR_NAME__", description="Delete a __SINGULAR_NAME__ by its ID")
async def delete___SINGULAR_VAR_NAME__(
    __SINGULAR_VAR_NAME___id: str,
    __SINGULAR_VAR_NAME___service: __CLASS_NAME__Service = Depends(__CLASS_NAME__Service),
    current_user: User = Security(get_current_user, scopes=["admin"]), # TODO: Add appropriate scopes for the operation
):
    """
    Delete a __SINGULAR_NAME__ by ID.
    
    - **__SINGULAR_VAR_NAME___id**: The unique identifier of the __SINGULAR_NAME__ to delete
    
    Returns a success message if the __SINGULAR_NAME__ was deleted, otherwise returns 404.
    """
    success = __SINGULAR_VAR_NAME___service.delete(__SINGULAR_VAR_NAME___id)
    if not success:
        raise HTTPException(status_code=404, detail="__CLASS_NAME__ not found")
    return {"message": "__CLASS_NAME__ deleted successfully"}