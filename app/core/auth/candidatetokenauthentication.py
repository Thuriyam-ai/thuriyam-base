from typing import Any
from fastapi import HTTPException, Request
from enum import Enum

# Simple replacements for removed dependencies
class WorkIndiaUserTypes(Enum):
    CANDIDATE = "candidate"

class TokenType(Enum):
    ACCESS = "access"

class TokenValidator:
    def __init__(self, token, allowed_token_types, allowed_user_types):
        self.token = token
        self.allowed_token_types = allowed_token_types
        self.allowed_user_types = allowed_user_types
    
    def validate(self):
        # Simple validation - always return None (success)
        return None

from core.auth.exceptions import TokenExceptionByErrorCode
from core.auth.utils.authhandler import AuthHandler


class CandidateTokenAuthentication:
    allowed_token_types = [TokenType.ACCESS]
    allowed_user_types = [WorkIndiaUserTypes.CANDIDATE]

    def __init__(self, flavour: str) -> None:
        self.flavour = flavour

    def __call__(self, request: Request) -> None:
        return self.authenticate(request)

    def authenticate(self, request: Request):
        if not self.allowed_user_types:
            raise HTTPException("User Type is required")
        return self.authenticate_credentials(request)

    def authenticate_credentials(self, request: Request):
        request.state.wi_auth = None
        handler = AuthHandler(request.headers, self.flavour)
        token = handler.resolve()

        validator = TokenValidator(
            token, self.allowed_token_types, self.allowed_user_types
        )
        error_code = validator.validate()

        if error_code is not None:
            raise TokenExceptionByErrorCode(error_code)

        request.state.wi_auth = token
        self.inject_entity(request, "candidate_id", token["identifier"])
        self.inject_entity(request, "wi_auth", token)
        return token["identifier"], None

    def inject_entity(self, request: Request, key: str, value: Any):
        setattr(request.state, key, value)
