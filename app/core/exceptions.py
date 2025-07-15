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
