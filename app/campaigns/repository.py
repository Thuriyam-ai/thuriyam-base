from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime
from core.base.repository import BaseRepository
from campaigns.model import Campaign

class CampaignRepository(BaseRepository[Campaign]):
    def __init__(self, db: Session):
        super().__init__(db, Campaign)
    
    def find_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[Campaign]:
        """
        Find campaigns by status with pagination.
        
        Args:
            status: Filter by campaign status
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Campaign]: List of campaigns matching the criteria
        """
        return self.db.query(self.model).filter(
            self.model.status == status
        ).offset(skip).limit(limit).all()
    
    def find_by_campaign_type(self, campaign_type: str, skip: int = 0, limit: int = 100) -> List[Campaign]:
        """
        Find campaigns by type with pagination.
        
        Args:
            campaign_type: Filter by campaign type
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Campaign]: List of campaigns matching the criteria
        """
        return self.db.query(self.model).filter(
            self.model.campaign_type == campaign_type
        ).offset(skip).limit(limit).all()
    
    def find_active_campaigns(self, skip: int = 0, limit: int = 100) -> List[Campaign]:
        """
        Find active campaigns (status = 'active' and is_active = True).
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Campaign]: List of active campaigns
        """
        return self.db.query(self.model).filter(
            and_(
                self.model.status == 'active',
                self.model.is_active == True
            )
        ).offset(skip).limit(limit).all()
    
    def find_by_date_range(self, start_date: datetime, end_date: datetime, skip: int = 0, limit: int = 100) -> List[Campaign]:
        """
        Find campaigns within a date range.
        
        Args:
            start_date: Start of the date range
            end_date: End of the date range
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Campaign]: List of campaigns within the date range
        """
        return self.db.query(self.model).filter(
            or_(
                and_(
                    self.model.start_date >= start_date,
                    self.model.start_date <= end_date
                ),
                and_(
                    self.model.end_date >= start_date,
                    self.model.end_date <= end_date
                ),
                and_(
                    self.model.start_date <= start_date,
                    self.model.end_date >= end_date
                )
            )
        ).offset(skip).limit(limit).all()
    
    def find_by_name_contains(self, name: str, skip: int = 0, limit: int = 100) -> List[Campaign]:
        """
        Find campaigns by name containing the given string.
        
        Args:
            name: String to search for in campaign name
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Campaign]: List of campaigns matching the criteria
        """
        return self.db.query(self.model).filter(
            self.model.name.contains(name)
        ).offset(skip).limit(limit).all()
    
    def update_status(self, id: str, new_status: str) -> Optional[Campaign]:
        """
        Update the status of a campaign.
        
        Args:
            id: The ID of the campaign to update
            new_status: The new status to set
            
        Returns:
            Optional[Campaign]: The updated campaign or None if not found
        """
        campaign = self.find(id)
        if not campaign:
            return None
        
        campaign.status = new_status
        self.db.commit()
        self.db.refresh(campaign)
        return campaign
    
    def toggle_active_status(self, id: str) -> Optional[Campaign]:
        """
        Toggle the active status of a campaign.
        
        Args:
            id: The ID of the campaign to toggle
            
        Returns:
            Optional[Campaign]: The updated campaign or None if not found
        """
        campaign = self.find(id)
        if not campaign:
            return None
        
        campaign.is_active = not campaign.is_active
        self.db.commit()
        self.db.refresh(campaign)
        return campaign 