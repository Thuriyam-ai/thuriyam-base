from .model import JWTToken
from .validator import CreateJWTTokenValidator

# Register validators
from core.base.validator import BaseValidator, Operation
validator_instance = BaseValidator.get_instance()
validator_instance.register(JWTToken, Operation.CREATE, CreateJWTTokenValidator)

__all__ = ['JWTToken', 'CreateJWTTokenValidator'] 