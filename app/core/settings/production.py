from typing import Any, Dict, Union
from .base import BaseConfig

# Simple consul settings replacement
def get_consul_setting(key: str, default: str = "") -> str:
    """Simple replacement for consul settings"""
    return default

class ConsulSettings:
    def get(self, key: str, default: str = "") -> str:
        return default

consul_settings = ConsulSettings()


class ProdConfig(BaseConfig):
    """Production configuration"""

    DEBUG: bool = False
    ALLOWED_HOSTS_REGEX: str = r"^http://.*\.workindia\.local$|^https://.*\.workindia\.in$" # Matches URLs with 'http' that end with '.workindia.local' and only 'https' with '.workindia.in'.

    NOSQL_DATABASES: Dict[str, Any] = {
        "mongodb": {
            "HOST": consul_settings.get("MONGO_DATABASE_HOST", ""),
            "PORT": "27017",
            "NAME": "WorkIndia",
            "SHOULD_AUTHENTICATE": True,  # Should be True only in production and staging
            "USERNAME": consul_settings.get("MONGO_DATABASE_USERNAME", ""),
            "PASSWORD": consul_settings.get("MONGO_DATABASE_PASSWORD", ""),
            "READ_REPLICAS": [
                {
                    "HOST": consul_settings.get("MONGO_DATABASE_HOST", ""),
                    "PORT": "27017",
                },
                {
                    "HOST": consul_settings.get("MONGO_DATABASE_HOST", ""),
                    "PORT": "27017",
                },
            ],
        },
    }

    # Caching
    CACHES: Dict[str, Any] = {
        "default": {
            "LOCATION": consul_settings.get("CACHE_DEFAULT", ""),
            "SOCKET_CONNECT_TIMEOUT": 1,  # in seconds
            "SOCKET_TIMEOUT": 1,  # in seconds
            "KEY_PREFIX": "wjn",
        },
        "shard_1": {
            "LOCATION": consul_settings.get("CACHE_SHARD_1", ""),
            "SOCKET_CONNECT_TIMEOUT": 1,  # in seconds
            "SOCKET_TIMEOUT": 1,  # in seconds
            "KEY_PREFIX": "wjn",
        },
        "shard_2": {
            "LOCATION": consul_settings.get("CACHE_SHARD_2", ""),
            "SOCKET_CONNECT_TIMEOUT": 1,  # in seconds
            "SOCKET_TIMEOUT": 1,  # in seconds
            "KEY_PREFIX": "wjn",
        },
        "shard_3": {
            "LOCATION": consul_settings.get("CACHE_SHARD_3", ""),
            "SOCKET_CONNECT_TIMEOUT": 1,  # in seconds
            "SOCKET_TIMEOUT": 1,  # in seconds
            "KEY_PREFIX": "wjn",
        },
        "shard_4": {
            "LOCATION": consul_settings.get("CACHE_SHARD_4", ""),
            "SOCKET_CONNECT_TIMEOUT": 1,  # in seconds
            "SOCKET_TIMEOUT": 1,  # in seconds
            "KEY_PREFIX": "wjn",
        },
    }

    # Kafka Cluster
    KAFKA_LOGGING_CLUSTER: Dict[str, str] = {
        "brokers": consul_settings.get("KAFKA_LOGGING_CLUSTER_BROKERS")
    }
    KAFKA_CLUSTER: Dict[str, str] = {
        "brokers": consul_settings.get("KAFKA_CLUSTER_BROKERS")
    }
    KAFKA_MANAGED_INTERNAL_CLUSTER: Dict[str, str] = {
        "brokers": consul_settings.get("KAFKA_MSK_INTERNAL_SERVER")
    }
    KAFKA_MKS_CLUSTER: Dict[str, str] = {
        "brokers": consul_settings.get("KAFKA_MKS_CLUSTER_BROKERS")
    }

    AWS_CONFIG: Dict[str, str] = {
        "access_key": consul_settings.get("AWS_ACCESS_KEY"),
        "access_secret": consul_settings.get("AWS_ACCESS_SECRET"),
        "region": "us-east-1",
        "s3_staging_dir": consul_settings.get("S3_STAGING_DIR"),
    }

    ETL_CONFIG: Dict[str, str] = {
        "HOST": consul_settings.get("ETL_HOST"),
        "PORT": consul_settings.get("ETL_PORT"),
    }

    # StatsD
    STATSD_HOST: str = consul_settings.get("STATSD_HOST", "statsd")
    STATSD_PORT: Union[str, int] = consul_settings.get("STATSD_PORT", 9125)
    STATSD_SERVICE_NAME: str = "wi-job-notification-ms"
    STATSD_PREFIX: str = "jobnotification"

    WI_JOBS_MS: Dict[str, Any] = {
        "url": consul_settings.get("WI_JOBS_MS_URL"),
        "timeout": consul_settings.get("WI_JOBS_MS_TIMEOUT", 2.0),
    }

    SLACK_TEMPLATE_CHANGE_APP: Dict[str, str] = consul_settings.get(
        "SLACK_TEMPLATE_CHANGE_APP", {}
    )

    API_KEY: Dict[str, str] = {
        "DEFAULT": consul_settings.get("API_KEY_DEFAULT"),
        "RELEVANT_JOBS": consul_settings.get("API_KEY_RELEVANT_JOBS"),
        "TEST_NOTIFICATION_TEMPLATE": consul_settings.get("API_KEY_TEST_NOTIFICATION_TEMPLATE"),
    }