import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core import settings
from core.settings.development import DevConfig
from core.settings.production import ProdConfig
from core.settings.docker import DockerConfig
# from core.settings.staging import StagingConfig

from applifespan import app_lifespan

logger = logging.getLogger(__name__)

# Register configurations
settings.register("dev", DevConfig)
settings.register("prod", ProdConfig)
settings.register("docker", DockerConfig)
# register("staging", StagingConfig)

config = settings.get_config()

app = FastAPI(
    title=config.ORG_NAME,
    description="A FastAPI-based microservice template with comprehensive API documentation",
    version=config.VERSION,
    docs_url=config.DOCS_URL,
    redoc_url=config.REDOC_URL,
    openapi_url="/openapi.json",
    lifespan=app_lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=config.ALLOWED_HOSTS_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
from todos.views import router as todos_router
from campaigns.views import router as campaigns_router

# Import modules to register validators
import todos
import campaigns

app.include_router(todos_router, prefix=config.API_PREFIX)
app.include_router(campaigns_router, prefix=config.API_PREFIX)

# Add a simple root health check
@app.get("/", summary="Health Check", description="Check if the service is running")
async def root():
    """
    Health check endpoint.
    
    Returns the service status to verify the API is running.
    """
    from core.database import test_database_connection
    
    db_status = "healthy" if test_database_connection() else "unhealthy"
    
    return {
        "message": "Thuriyam Base Template Service is running", 
        "status": "healthy",
        "database": db_status
    }
