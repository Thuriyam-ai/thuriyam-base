# Module initialization
from core.base.validator import BaseValidator, Operation
from __MODULE_NAME__.model import __CLASS_NAME__
from __MODULE_NAME__.validator import __CLASS_NAME__CreateValidator

# Register validators
validator_instance = BaseValidator.get_instance()
validator_instance.register(__CLASS_NAME__, Operation.CREATE, __CLASS_NAME__CreateValidator)