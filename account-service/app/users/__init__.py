from core.base.validator import BaseValidator, Operation
from users.model import User
from users.validator import CreateUserValidator, UpdateUserValidator, DeleteUserValidator

# Register validators for User model
base_validator = BaseValidator.get_instance()
base_validator.register(User, Operation.CREATE, CreateUserValidator)
base_validator.register(User, Operation.UPDATE, UpdateUserValidator)
base_validator.register(User, Operation.DELETE, DeleteUserValidator)
        