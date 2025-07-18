from typing import Any, Dict, Union
from .base import BaseConfig


class DockerConfig(BaseConfig):
    """Docker configuration for Account Service"""

    DEBUG: bool = True
    ALLOWED_HOSTS_REGEX: str = r"^.*$"

    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"

    # Database URL is set via environment variable SQLALCHEMY_DATABASE_URL
    # Default: postgresql://thuriyam_user:thuriyam_password@account-db:5432/account_db

    # Caching - use Redis from Docker
    CACHES: Dict[str, Any] = {
        "default": {
            "LOCATION": "redis://redis:6379/0",
            "SOCKET_CONNECT_TIMEOUT": 1,
            "SOCKET_TIMEOUT": 1,
            "KEY_PREFIX": "account",
        },
    }

    # StatsD - use StatsD from Docker
    STATSD_HOST: str = "statsd"
    STATSD_PORT: Union[str, int] = 9125
    STATSD_SERVICE_NAME: str = "account-service"
    STATSD_PREFIX: str = "account" 