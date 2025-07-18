from sqlalchemy import Column, String, Boolean, DateTime, Text, Numeric
from core.base.model import BaseModel
from core.base.validator import Operation
from typing import Any

class Campaign(BaseModel):
    """Campaign model for marketing campaigns management"""
    __tablename__ = "campaigns"

    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    campaign_type = Column(String(50), nullable=False)  # email, social, display, etc.
    status = Column(String(20), default="draft")  # draft, active, paused, completed, cancelled
    start_date = Column(DateTime(timezone=True), nullable=True)
    end_date = Column(DateTime(timezone=True), nullable=True)
    budget = Column(Numeric(precision=10, scale=2), nullable=True)
    target_audience = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)

    _unset = []

    @classmethod
    def get_validator(cls, operation: Operation) -> Any:
        from campaigns.validator import CampaignCreateValidator, CampaignUpdateValidator
        if operation == Operation.CREATE:
            return CampaignCreateValidator
        elif operation == Operation.UPDATE:
            return CampaignUpdateValidator
        raise ValueError(f"Unknown operation: {operation}") 