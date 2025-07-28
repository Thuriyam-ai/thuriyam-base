from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Security
from sqlalchemy.orm import Session
from datetime import datetime
from core.database import get_db
from campaigns.repository import CampaignRepository
from campaigns.schema import CampaignCreate, CampaignUpdate, CampaignResponse
from campaigns.model import Campaign
from core.base.model import ModelBuilder
from core.base.validator import Operation
from core.security.auth import get_current_user, User

router = APIRouter(prefix="/campaigns", tags=["campaigns"])

def get_campaign_repository(db: Session = Depends(get_db)) -> CampaignRepository:
    return CampaignRepository(db)

@router.post("/", response_model=CampaignResponse, summary="Create a new campaign", description="Create a new marketing campaign with the provided data")
async def create_campaign(
    campaign_data: CampaignCreate,
    current_user: User = Security(get_current_user, scopes=["campaigns:write"]),
    repo: CampaignRepository = Depends(get_campaign_repository)
):
    """
    Create a new campaign.
    
    - **name**: The name of the campaign (required)
    - **description**: Optional description of the campaign
    - **campaign_type**: Type of campaign (email, social, display, search, content, influencer, other)
    - **status**: Campaign status (draft, active, paused, completed, cancelled)
    - **start_date**: Campaign start date (optional)
    - **end_date**: Campaign end date (optional)
    - **budget**: Campaign budget (optional)
    - **target_audience**: Target audience description (optional)
    - **is_active**: Whether the campaign is active (defaults to True)
    
    Returns the created campaign with generated ID and timestamps.
    """
    campaign_attrs = campaign_data.model_dump(exclude_unset=True)
    campaign_attrs["created_by"] = current_user.username
    campaign = ModelBuilder.for_model(Campaign).with_operation(
        Operation.CREATE
    ).with_attributes(campaign_attrs).build()
    campaign = repo.save(campaign)
    return CampaignResponse.model_validate(campaign)

@router.get("/", response_model=List[CampaignResponse], summary="Get all campaigns", description="Retrieve all campaigns with optional filtering and pagination")
async def get_campaigns(
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    status: Optional[str] = Query(None, description="Filter by campaign status"),
    campaign_type: Optional[str] = Query(None, description="Filter by campaign type"),
    name: Optional[str] = Query(None, description="Search by name containing this text"),
    active_only: bool = Query(False, description="Show only active campaigns"),
    current_user: User = Security(get_current_user, scopes=["campaigns:read"]),
    repo: CampaignRepository = Depends(get_campaign_repository)
):
    """
    Get all campaigns with optional filtering and pagination.
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return (1-1000)
    - **status**: Filter by campaign status (optional)
    - **campaign_type**: Filter by campaign type (optional)
    - **name**: Search by name containing text (optional)
    - **active_only**: Show only active campaigns (optional)
    
    Returns a list of campaigns matching the criteria.
    """
    if active_only:
        return repo.find_active_campaigns(skip, limit)
    elif status:
        return repo.find_by_status(status, skip, limit)
    elif campaign_type:
        return repo.find_by_campaign_type(campaign_type, skip, limit)
    elif name:
        return repo.find_by_name_contains(name, skip, limit)
    else:
        return repo.find_all(skip, limit)

@router.get("/{campaign_id}", response_model=CampaignResponse, summary="Get a specific campaign", description="Retrieve a specific campaign by its ID")
async def get_campaign(
    campaign_id: str,
    current_user: User = Security(get_current_user, scopes=["campaigns:read"]),
    repo: CampaignRepository = Depends(get_campaign_repository)
):
    """
    Get a specific campaign by ID.
    
    - **campaign_id**: The unique identifier of the campaign
    
    Returns the campaign if found, otherwise returns 404.
    """
    campaign = repo.find(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

@router.put("/{campaign_id}", response_model=CampaignResponse, summary="Update a campaign", description="Update an existing campaign with new data")
async def update_campaign(
    campaign_id: str,
    campaign_data: CampaignUpdate,
    current_user: User = Security(get_current_user, scopes=["campaigns:write"]),
    repo: CampaignRepository = Depends(get_campaign_repository)
):
    """
    Update an existing campaign.
    
    - **campaign_id**: The unique identifier of the campaign to update
    - **campaign_data**: The updated campaign data (all fields are optional for partial updates)
    
    Returns the updated campaign if found, otherwise returns 404.
    """
    # Filter out None values for partial update
    update_data = {k: v for k, v in campaign_data.model_dump().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No valid fields to update")
    
    campaign = repo.update(campaign_id, update_data)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

@router.patch("/{campaign_id}/status", response_model=CampaignResponse, summary="Update campaign status", description="Update the status of a campaign")
async def update_campaign_status(
    campaign_id: str,
    new_status: str = Query(..., description="New status (draft, active, paused, completed, cancelled)"),
    current_user: User = Security(get_current_user, scopes=["campaigns:manage"]),
    repo: CampaignRepository = Depends(get_campaign_repository)
):
    """
    Update the status of a campaign.
    
    - **campaign_id**: The unique identifier of the campaign
    - **new_status**: The new status to set
    
    Returns the updated campaign if found, otherwise returns 404.
    """
    allowed_statuses = ['draft', 'active', 'paused', 'completed', 'cancelled']
    if new_status not in allowed_statuses:
        raise HTTPException(status_code=400, detail=f"Status must be one of {allowed_statuses}")
    
    campaign = repo.update_status(campaign_id, new_status)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

@router.patch("/{campaign_id}/toggle-active", response_model=CampaignResponse, summary="Toggle campaign active status", description="Toggle the active status of a campaign")
async def toggle_campaign_active(
    campaign_id: str,
    current_user: User = Security(get_current_user, scopes=["campaigns:manage"]),
    repo: CampaignRepository = Depends(get_campaign_repository)
):
    """
    Toggle the active status of a campaign.
    
    - **campaign_id**: The unique identifier of the campaign to toggle
    
    Switches the is_active status from true to false or vice versa.
    Returns the updated campaign if found, otherwise returns 404.
    """
    campaign = repo.toggle_active_status(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

@router.get("/date-range/", response_model=List[CampaignResponse], summary="Get campaigns by date range", description="Retrieve campaigns within a specific date range")
async def get_campaigns_by_date_range(
    start_date: datetime = Query(..., description="Start date for the range"),
    end_date: datetime = Query(..., description="End date for the range"),
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    current_user: User = Security(get_current_user, scopes=["campaigns:read"]),
    repo: CampaignRepository = Depends(get_campaign_repository)
):
    """
    Get campaigns within a specific date range.
    
    - **start_date**: Start date for the range
    - **end_date**: End date for the range
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return (1-1000)
    
    Returns campaigns that overlap with the specified date range.
    """
    if end_date <= start_date:
        raise HTTPException(status_code=400, detail="End date must be after start date")
    
    return repo.find_by_date_range(start_date, end_date, skip, limit)

@router.delete("/{campaign_id}", summary="Delete a campaign", description="Delete a campaign by its ID")
async def delete_campaign(
    campaign_id: str,
    current_user: User = Security(get_current_user, scopes=["campaigns:manage"]),
    repo: CampaignRepository = Depends(get_campaign_repository)
):
    """
    Delete a campaign by ID.
    
    - **campaign_id**: The unique identifier of the campaign to delete
    
    Returns a success message if the campaign was deleted, otherwise returns 404.
    """
    success = repo.delete(campaign_id)
    if not success:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return {"message": "Campaign deleted successfully"} 