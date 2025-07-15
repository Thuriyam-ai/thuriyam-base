from fastapi import HTTPException, Request
from core import settings


class APIKeyAuthentication:
    def __init__(
        self, api_key: str = None, api_key_header: str = None
    ) -> None:
        self._api_key = api_key
        self._api_key_header = api_key_header

    @property
    def api_key(self):
        if self._api_key is None:
            config = settings.get_config()
            self._api_key = config.API_KEY["DEFAULT"]
        return self._api_key

    @property
    def api_key_header(self):
        if self._api_key_header is None:
            config = settings.get_config()
            self._api_key_header = config.API_KEY_HEADER
        return self._api_key_header

    def __call__(self, request: Request) -> None:
        api_key = request.headers.get(self.api_key_header)
        if not api_key or api_key != self.api_key:
            raise HTTPException(status_code=401, detail="Unauthorized")
