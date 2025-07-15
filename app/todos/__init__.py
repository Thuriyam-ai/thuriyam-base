from core.base.validator import BaseValidator, Operation
from todos.model import Todo
from todos.validator import TodoCreateValidator, TodoUpdateValidator

# Register validators for Todo entity
validator_instance = BaseValidator.get_instance()

# Register CREATE validator
validator_instance.register(Todo, Operation.CREATE, TodoCreateValidator)

# Register UPDATE validator
validator_instance.register(Todo, Operation.UPDATE, TodoUpdateValidator)

__all__ = ['Todo', 'TodoCreateValidator', 'TodoUpdateValidator']