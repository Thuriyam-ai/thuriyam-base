from pydantic import BaseModel, Field, validator
from typing import Optional
from decimal import Decimal
from datetime import datetime

class CampaignCreateValidator(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Campaign name")
    description: Optional[str] = Field(default=None, description="Campaign description")
    campaign_type: str = Field(..., min_length=1, max_length=50, description="Campaign type (email, social, display, etc.)")
    status: str = Field(default="draft", description="Campaign status")
    start_date: Optional[datetime] = Field(default=None, description="Campaign start date")
    end_date: Optional[datetime] = Field(default=None, description="Campaign end date")
    budget: Optional[Decimal] = Field(default=None, ge=0, description="Campaign budget")
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

class CampaignUpdateValidator(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200, description="Campaign name")
    description: Optional[str] = Field(None, description="Campaign description")
    campaign_type: Optional[str] = Field(None, min_length=1, max_length=50, description="Campaign type")
    status: Optional[str] = Field(None, description="Campaign status")
    start_date: Optional[datetime] = Field(None, description="Campaign start date")
    end_date: Optional[datetime] = Field(None, description="Campaign end date")
    budget: Optional[Decimal] = Field(None, ge=0, description="Campaign budget")
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