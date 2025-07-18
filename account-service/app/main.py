import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.settings import get_config, register
from core.settings.development import DevConfig
from core.settings.docker import DockerConfig
from core.database import test_database_connection

# Register configurations
register("dev", DevConfig)
register("docker", DockerConfig)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config = get_config()

app = FastAPI(
    title=config.APP_NAME,
    description="Account service for user management and authentication",
    version=config.VERSION,
    docs_url=config.DOCS_URL,
    redoc_url=config.REDOC_URL,
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=config.ALLOWED_HOSTS_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
from users.routes import router as users_router
from auth.routes import router as auth_router

app.include_router(users_router, prefix=config.API_PREFIX)
app.include_router(auth_router, prefix=config.API_PREFIX)

# Health check endpoint
@app.get("/", summary="Health Check", description="Check if the service is running")
async def root():
    """
    Health check endpoint.
    
    Returns the service status to verify the API is running.
    """
    db_status = "healthy" if test_database_connection() else "unhealthy"
    
    return {
        "message": f"{config.APP_NAME} is running", 
        "status": "healthy",
        "database": db_status,
        "version": config.VERSION
    }

@app.get("/health", summary="Health Check", description="Detailed health check")
async def health_check():
    """
    Detailed health check endpoint.
    """
    db_status = "healthy" if test_database_connection() else "unhealthy"
    
    return {
        "service": config.APP_NAME,
        "status": "healthy",
        "database": db_status,
        "version": config.VERSION
    } 