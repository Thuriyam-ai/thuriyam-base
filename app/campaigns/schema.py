from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from decimal import Decimal

class CampaignBase(BaseModel):
    name: str = Field(..., description="The name of the campaign", min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, description="Optional description of the campaign")
    campaign_type: str = Field(..., description="Type of campaign (email, social, display, search, content, influencer, other)")
    status: str = Field(default="draft", description="Campaign status (draft, active, paused, completed, cancelled)")
    start_date: Optional[datetime] = Field(default=None, description="Campaign start date")
    end_date: Optional[datetime] = Field(default=None, description="Campaign end date")
    budget: Optional[Decimal] = Field(default=None, description="Campaign budget", ge=0)
    target_audience: Optional[str] = Field(default=None, description="Target audience description")
    is_active: bool = Field(default=True, description="Whether the campaign is active")

    @validator('status')
    def validate_status(cls, v):
        allowed_statuses = ['draft', 'active', 'paused', 'completed', 'cancelled']
        if v not in allowed_statuses:
            raise ValueError(f'Status must be one of {allowed_statuses}')
        return v

    @validator('campaign_type')
    def validate_campaign_type(cls, v):
        allowed_types = ['email', 'social', 'display', 'search', 'content', 'influencer', 'other']
        if v not in allowed_types:
            raise ValueError(f'Campaign type must be one of {allowed_types}')
        return v

    @validator('end_date')
    def validate_end_date(cls, v, values):
        if v and 'start_date' in values and values['start_date']:
            if v <= values['start_date']:
                raise ValueError('End date must be after start date')
        return v

class CampaignCreate(CampaignBase):
    """Schema for creating a new campaign"""
    pass

class CampaignUpdate(BaseModel):
    """Schema for updating a campaign (all fields are optional)"""
    name: Optional[str] = Field(None, description="The name of the campaign", min_length=1, max_length=200)
    description: Optional[str] = Field(None, description="Optional description of the campaign")
    campaign_type: Optional[str] = Field(None, description="Type of campaign")
    status: Optional[str] = Field(None, description="Campaign status")
    start_date: Optional[datetime] = Field(None, description="Campaign start date")
    end_date: Optional[datetime] = Field(None, description="Campaign end date")
    budget: Optional[Decimal] = Field(None, description="Campaign budget", ge=0)
    target_audience: Optional[str] = Field(None, description="Target audience description")
    is_active: Optional[bool] = Field(None, description="Whether the campaign is active")

    @validator('status')
    def validate_status(cls, v):
        if v is not None:
            allowed_statuses = ['draft', 'active', 'paused', 'completed', 'cancelled']
            if v not in allowed_statuses:
                raise ValueError(f'Status must be one of {allowed_statuses}')
        return v

    @validator('campaign_type')
    def validate_campaign_type(cls, v):
        if v is not None:
            allowed_types = ['email', 'social', 'display', 'search', 'content', 'influencer', 'other']
            if v not in allowed_types:
                raise ValueError(f'Campaign type must be one of {allowed_types}')
        return v

class CampaignResponse(CampaignBase):
    """Schema for campaign responses"""
    id: str = Field(..., description="Unique identifier for the campaign")
    created_at: datetime = Field(..., description="Timestamp when the campaign was created")
    updated_at: datetime = Field(..., description="Timestamp when the campaign was last updated")

    class Config:
        from_attributes = True 