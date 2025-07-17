from typing import Any, Dict, Optional
from pydantic import Field
from pydantic_settings import BaseSettings
from uvicorn.logging import DefaultFormatter
from decouple import config


class BaseConfig(BaseSettings, extra="ignore"):
    """Base configuration"""

    FLAVOUR: str = Field(default="dev", env="FLAVOUR")
    DEBUG: bool = False

    ORG_NAME: str = "Thuriyam"
    APP_NAME: str = "Configuration Service"
    API_PREFIX: str = "/api/v1"
    VERSION: str = "0.1"
    DOCS_URL: Optional[str] = None
    REDOC_URL: Optional[str] = None
    ALLOWED_HOSTS: Optional[list] = None

    # Database
    SQLALCHEMY_DATABASE_URL: str = config("SQLALCHEMY_DATABASE_URL", default="postgresql://thuriyam_user:thuriyam_password@localhost:5432/thuriyam_base")
    
    # CORS
    ALLOWED_HOSTS_REGEX: str = r"^http://.*\.thuriyam\.local$|^https://.*\.thuriyam\.in$" # Matches URLs with 'http' that end with '.thuriyam.local' and only 'https' with '.thuriyam.in'.

    # Common Org Headers
    ORG_SHARED_REQUEST_HEADERS: Dict[str, str] = {
        "x-internal-communication-token": "TTbVBDmZ59d4xXLC",
        "User-Agent": f"{ORG_NAME}-servers",
    }
    
    # JWT
    SECRET_KEY: str = config("SECRET_KEY", default="your-secret-key-here")  # Change this in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    LOGGING_CONFIG: Dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "()": DefaultFormatter,  # Use Uvicorn's DefaultFormatter to keep colors
                "fmt": "%(levelprefix)s %(name)s: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "standard",
            },
        },
        "loggers": {
            "uvicorn": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            },
            "app": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "INFO",
        },
    }

    API_KEY: Dict[str, str] = {
        "DEFAULT": "26dbf0a5-e986-406e-bcd7-234835b68c77",
        "RELEVANT_JOBS": "26dbf0a5-e986-406e-bcd7-234835b68c88",
        "TEST_NOTIFICATION_TEMPLATE": "62dbf1c4-f976-406e-bcd7-34y436b88c12",
    }

    API_KEY_HEADER: str = "X-API-Key"

    class Config:
        env_prefix = "APP_"
