from typing import Any, Dict, Union
from .base import BaseConfig


_MONGO_HOST = "127.0.0.1"
_MONGO_PORT = "27017"
_MONGO_SHOULD_AUTHENTICATE = False
_MONGO_USERNAME = None
_MONGO_PASSWORD = None


class DevConfig(BaseConfig):
    """Development configuration"""

    DEBUG: bool = True
    ALLOWED_HOSTS_REGEX: str = r"^.*$"

    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"

    NOSQL_DATABASES: Dict[str, Any] = {
        "mongodb": {
            "HOST": _MONGO_HOST,
            "PORT": _MONGO_PORT,
            "NAME": "WorkIndia",
            "SHOULD_AUTHENTICATE": _MONGO_SHOULD_AUTHENTICATE,
            "USERNAME": _MONGO_USERNAME,
            "PASSWORD": _MONGO_PASSWORD,
            "READ_REPLICAS": [
                {"HOST": _MONGO_HOST, "PORT": _MONGO_PORT},
                {"HOST": _MONGO_HOST, "PORT": _MONGO_PORT},
            ],
        },
    }

    # Caching
    CACHES: Dict[str, Any] = {
        "default": {
            "LOCATION": "redis://127.0.0.1:6379/0",
            "SOCKET_CONNECT_TIMEOUT": 1,  # in seconds
            "SOCKET_TIMEOUT": 1,  # in seconds
            "KEY_PREFIX": "wjn",
        },
        "shard_1": {
            "LOCATION": "redis://127.0.0.1:6379/0",
            "SOCKET_CONNECT_TIMEOUT": 1,  # in seconds
            "SOCKET_TIMEOUT": 1,  # in seconds
            "KEY_PREFIX": "wjn",
        },
        "shard_2": {
            "LOCATION": "redis://127.0.0.1:6379/0",
            "SOCKET_CONNECT_TIMEOUT": 1,  # in seconds
            "SOCKET_TIMEOUT": 1,  # in seconds
            "KEY_PREFIX": "wjn",
        },
        "shard_3": {
            "LOCATION": "redis://127.0.0.1:6379/0",
            "SOCKET_CONNECT_TIMEOUT": 1,  # in seconds
            "SOCKET_TIMEOUT": 1,  # in seconds
            "KEY_PREFIX": "wjn",
        },
        "shard_4": {
            "LOCATION": "redis://127.0.0.1:6379/0",
            "SOCKET_CONNECT_TIMEOUT": 1,  # in seconds
            "SOCKET_TIMEOUT": 1,  # in seconds
            "KEY_PREFIX": "wjn",
        },
    }

    # Kafka Cluster
    KAFKA_LOGGING_CLUSTER: Dict[str, str] = {"brokers": "127.0.0.1:9092"}
    KAFKA_CLUSTER: Dict[str, str] = {"brokers": "127.0.0.1:9092"}
    KAFKA_MANAGED_INTERNAL_CLUSTER: Dict[str, str] = {
        "brokers": "127.0.0.1:9092"
    }
    KAFKA_MKS_CLUSTER: Dict[str, str] = {"brokers": "127.0.0.1:9092"}

    AWS_CONFIG: Dict[str, str] = {
        "access_key": "",
        "access_secret": "",
        "region": "us-east-1",
        "s3_staging_dir": "",
    }

    ETL_CONFIG: Dict[str, Any] = {
        "HOST": "wi-data-access-ms-api.wi-data-access-ms",
        "PORT": 8080,
    }

    # StatsD
    STATSD_HOST: str = "localhost"
    STATSD_PORT: Union[str, int] = 9125
    STATSD_SERVICE_NAME: str = "wi-job-notification-ms"
    STATSD_PREFIX: str = "jobnotification"

    WI_JOBS_MS: Dict[str, Any] = {
        "url": "http://localhost:8001/api/jobs",
        "timeout": 10,
    }

    SLACK_TEMPLATE_CHANGE_APP: Dict[str, str] = {"url": ""}
