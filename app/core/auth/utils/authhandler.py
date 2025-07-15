import ast
import json
from typing import Any, Dict, Optional
from enum import Enum

# Simple replacement for removed dependency
class TokenType(Enum):
    ACCESS = "access"


class AuthHandler:
    IDENTIFIER_HEADER = "x-wi-auth-identifier"
    IDENTIFIER_HEADER_V2 = "x-wi-auth-identifier-v2"

    def __init__(self, headers: Dict[str, str], flavour: str):
        self.headers = headers
        self.flavour = flavour

    def resolve(self) -> Optional[Dict[str, Any]]:
        """
        Request Headers will contain header from Cloudfront which is attached via Edge Lambda Function to identify token
        configuration

        :return: Resolved token dict
        """
        if self.flavour in {"dev", "stag"}:
            return self._resolve_dev_token()
        else:
            return self._resolve_prod_token()

    def _resolve_dev_token(self) -> Optional[Dict[str, Any]]:
        """Resolve token for dev/staging environments"""
        _access_token = self.headers.get("AUTHORIZATION", "")
        _access_token = _access_token.replace("Bearer ", "").strip()

        if not _access_token:
            return None

        split_array = _access_token.split("_")
        _identifier = split_array[2]
        try:
            _identifier = int(_identifier)
        except ValueError:
            pass

        return {
            "expires": int(split_array[5]),
            "identifier": _identifier,
            "identifier_type": split_array[3],
            "token_type": split_array[0],
            "sub_identifier": ast.literal_eval(split_array[4]),
        }

    def _resolve_prod_token(self) -> Optional[Dict[str, Any]]:
        """Resolve token for production environment"""
        token_header = self.headers.get(AuthHandler.IDENTIFIER_HEADER_V2)
        if not token_header:
            token_header = self.headers.get(AuthHandler.IDENTIFIER_HEADER)

        if not token_header:
            return None

        if token_header == "legacy_token":
            return None

        token_header = json.loads(token_header)
        if not token_header["is_validated"]:
            return None

        _identifier = token_header["identifier"]
        try:
            _identifier = int(_identifier)
        except ValueError:
            pass

        return {
            "token_id": token_header.get("token_id"),
            "expires": int(token_header["expire_after"]),
            "identifier": _identifier,
            "identifier_type": token_header["identifier_type"],
            "sub_identifier": token_header.get("sub_identifier"),
            "token_type": token_header.get("token_type", TokenType.ACCESS),
        }
