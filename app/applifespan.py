import logging
import warnings
from fastapi import FastAPI
from contextlib import asynccontextmanager
from core import settings
# from widataaccess import DataAccessAdapter

from core.adapter.asyncio.mongo.mongodbadapter import (
    MongoDBAsyncAdapter,
)
from core.adapter.statsd import StatsdClientManager
from core.adapter.asyncio.caching.client import RedisClientManager

logger = logging.getLogger(__name__)


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    config = settings.get_config()
    # Initialize logging
    logging.config.dictConfig(config.LOGGING_CONFIG)
    warnings.simplefilter("default", category=RuntimeWarning)

    logger.info(f"Initializing App | Flavour: {config.FLAVOUR}")

    # Initialize StatsD Default Client
    logger.debug("Initializing StatsD Default Client")
    StatsdClientManager(
        host=config.STATSD_HOST,
        port=config.STATSD_PORT,
        service_name=config.STATSD_SERVICE_NAME,
        prefix=config.STATSD_PREFIX,
    ).init_default_client()

    # Initialize DataAccessAdapter
    # logger.debug("Initializing DataAccessAdapter")
    # DataAccessAdapter(
    #     host=config.ETL_CONFIG["HOST"],
    #     port=config.ETL_CONFIG["PORT"],
    # )

    yield

    # Cleanup code here:
    logger.info("Shutting down App")
    MongoDBAsyncAdapter.close_all()
    await RedisClientManager.close_all()
