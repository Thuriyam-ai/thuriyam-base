from typing import Any, Dict, Union
from .base import BaseConfig


class DockerConfig(BaseConfig):
    """Docker configuration with PostgreSQL"""

    DEBUG: bool = True
    ALLOWED_HOSTS_REGEX: str = r"^.*$"

    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"

    # Database URL is set via environment variable SQLALCHEMY_DATABASE_URL
    # Default: postgresql://thuriyam_user:thuriyam_password@postgres:5432/thuriyam_base

    NOSQL_DATABASES: Dict[str, Any] = {
        "mongodb": {
            "HOST": "mongo",  # Use Docker service name
            "PORT": "27017",
            "NAME": "WorkIndia",
            "SHOULD_AUTHENTICATE": False,
            "USERNAME": None,
            "PASSWORD": None,
            "READ_REPLICAS": [
                {"HOST": "mongo", "PORT": "27017"},
                {"HOST": "mongo", "PORT": "27017"},
            ],
        },
    }

    # Caching - use Redis from Docker
    CACHES: Dict[str, Any] = {
        "default": {
            "LOCATION": "redis://redis:6379/0",
            "SOCKET_CONNECT_TIMEOUT": 1,  # in seconds
            "SOCKET_TIMEOUT": 1,  # in seconds
            "KEY_PREFIX": "wjn",
        },
        "shard_1": {
            "LOCATION": "redis://redis:6379/0",
            "SOCKET_CONNECT_TIMEOUT": 1,  # in seconds
            "SOCKET_TIMEOUT": 1,  # in seconds
            "KEY_PREFIX": "wjn",
        },
        "shard_2": {
            "LOCATION": "redis://redis:6379/0",
            "SOCKET_CONNECT_TIMEOUT": 1,  # in seconds
            "SOCKET_TIMEOUT": 1,  # in seconds
            "KEY_PREFIX": "wjn",
        },
        "shard_3": {
            "LOCATION": "redis://redis:6379/0",
            "SOCKET_CONNECT_TIMEOUT": 1,  # in seconds
            "SOCKET_TIMEOUT": 1,  # in seconds
            "KEY_PREFIX": "wjn",
        },
        "shard_4": {
            "LOCATION": "redis://redis:6379/0",
            "SOCKET_CONNECT_TIMEOUT": 1,  # in seconds
            "SOCKET_TIMEOUT": 1,  # in seconds
            "KEY_PREFIX": "wjn",
        },
    }

    # Kafka Cluster - use Kafka from Docker
    KAFKA_LOGGING_CLUSTER: Dict[str, str] = {"brokers": "kafka:9092"}
    KAFKA_CLUSTER: Dict[str, str] = {"brokers": "kafka:9092"}
    KAFKA_MANAGED_INTERNAL_CLUSTER: Dict[str, str] = {
        "brokers": "kafka:9092"
    }
    KAFKA_MKS_CLUSTER: Dict[str, str] = {"brokers": "kafka:9092"}

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

    # StatsD - use StatsD from Docker
    STATSD_HOST: str = "statsd"
    STATSD_PORT: Union[str, int] = 9125
    STATSD_SERVICE_NAME: str = "wi-job-notification-ms"
    STATSD_PREFIX: str = "jobnotification"

    WI_JOBS_MS: Dict[str, Any] = {
        "url": "http://localhost:8001/api/jobs",
        "timeout": 10,
    }

    SLACK_TEMPLATE_CHANGE_APP: Dict[str, str] = {"url": ""} 