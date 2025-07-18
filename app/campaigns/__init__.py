from core.base.validator import BaseValidator, Operation
from campaigns.model import Campaign
from campaigns.validator import CampaignCreateValidator, CampaignUpdateValidator

# Register validators for Campaign entity
validator_instance = BaseValidator.get_instance()

# Register CREATE validator
validator_instance.register(Campaign, Operation.CREATE, CampaignCreateValidator)

# Register UPDATE validator
validator_instance.register(Campaign, Operation.UPDATE, CampaignUpdateValidator)

__all__ = ['Campaign', 'CampaignCreateValidator', 'CampaignUpdateValidator'] 