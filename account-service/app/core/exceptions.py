from typing import Any

from starlette import status
from fastapi import HTTPException


class ValidationError(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail: Any = None) -> None:
        super().__init__(status_code=self.status_code, detail=detail)


class NotFoundError(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, detail: Any = None) -> None:
        super().__init__(status_code=self.status_code, detail=detail)

class AccountServiceException(Exception):
    """Base exception for account service"""
    pass

class UserNotFoundException(AccountServiceException):
    """Raised when user is not found"""
    pass

class UserAlreadyExistsException(AccountServiceException):
    """Raised when user already exists"""
    pass

class InvalidCredentialsException(AccountServiceException):
    """Raised when credentials are invalid"""
    pass

class InsufficientPermissionsException(AccountServiceException):
    """Raised when user lacks required permissions"""
    pass
