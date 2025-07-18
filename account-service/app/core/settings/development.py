from typing import Any, Dict, Union
from .base import BaseConfig


class DevConfig(BaseConfig):
    """Development configuration for Account Service"""

    DEBUG: bool = True
    ALLOWED_HOSTS_REGEX: str = r"^.*$"

    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"

    # Database URL is set via environment variable SQLALCHEMY_DATABASE_URL
    # Default: postgresql://thuriyam_user:thuriyam_password@localhost:5432/account_db

    # Caching
    CACHES: Dict[str, Any] = {
        "default": {
            "LOCATION": "redis://127.0.0.1:6379/0",
            "SOCKET_CONNECT_TIMEOUT": 1,
            "SOCKET_TIMEOUT": 1,
            "KEY_PREFIX": "account",
        },
    }

    # StatsD
    STATSD_HOST: str = "localhost"
    STATSD_PORT: Union[str, int] = 9125
    STATSD_SERVICE_NAME: str = "account-service"
    STATSD_PREFIX: str = "account"
