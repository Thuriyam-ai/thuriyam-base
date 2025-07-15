from decouple import config
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model_config = {
        "case_sensitive": True,
        "extra": "ignore"
    }

    PROJECT_NAME: str = "Thuriyam"
    API_V1_STR: str = "/api/v1"
    VERSION: str = '0.1'
    
    # Database
    SQLALCHEMY_DATABASE_URL: str = config("SQLALCHEMY_DATABASE_URL", default="sqlite:///./thuriyam.db")
    
    # CORS
    # BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # JWT
    SECRET_KEY: str = config("SECRET_KEY", default="your-secret-key-here")  # Change this in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # File Storage
    UPLOAD_DIR: str = "uploads"

settings = Settings() 

def get_settings() -> Settings:
    return settings