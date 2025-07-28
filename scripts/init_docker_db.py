#!/usr/bin/env python3
"""
Docker-specific database initialization script.
This script sets up the PostgreSQL database tables for the Docker environment.
"""

import sys
import os
import logging
import time

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

# Set environment for Docker
os.environ.setdefault("FLAVOUR", "docker")
os.environ.setdefault("SQLALCHEMY_DATABASE_URL", "postgresql://thuriyam_user:thuriyam_password@localhost:5432/thuriyam_base")

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
from core import settings
from core.settings.docker import DockerConfig
from core.base.model import Base

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def wait_for_postgres(config, max_retries=30, retry_interval=2):
    """Wait for PostgreSQL to be ready"""
    logger.info("Waiting for PostgreSQL to be ready...")
    
    for attempt in range(max_retries):
        try:
            # Create a temporary engine to test connection
            engine = create_engine(config.SQLALCHEMY_DATABASE_URL)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("✅ PostgreSQL is ready!")
            return True
        except Exception as e:
            if attempt < max_retries - 1:
                logger.info(f"PostgreSQL not ready yet (attempt {attempt + 1}/{max_retries}): {e}")
                time.sleep(retry_interval)
            else:
                logger.error(f"PostgreSQL failed to start after {max_retries} attempts")
                return False
    
    return False

def init_docker_db(config):
    """Initialize PostgreSQL database for Docker environment"""
    logger.info("Initializing database tables...")
    try:
        logger.info("Waiting for PostgreSQL to be ready...")
        # Wait for PostgreSQL to be ready
        if not wait_for_postgres(config):
            raise Exception("PostgreSQL is not available")
        
        logger.info(f"Using database URL: {config.SQLALCHEMY_DATABASE_URL}")
        
        # Create SQLAlchemy engine
        engine = create_engine(
            config.SQLALCHEMY_DATABASE_URL,
            connect_args={}  # No special args needed for PostgreSQL
        )
        
        logger.info("Creating database tables...")
        
        # Import all models to ensure they are registered with SQLAlchemy
        from todos.model import Todo  # Import todo model
        
        # Check if tables already exist
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        
        if existing_tables:
            logger.info(f"Tables already exist: {existing_tables}")
            logger.info("Skipping table creation as tables already exist.")
            return
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        logger.info("Database tables created successfully!")
        
        # Verify tables were created
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logger.info(f"Created tables: {tables}")
        
        if not tables:
            logger.error("No tables were created!")
            raise Exception("Database initialization failed - no tables were created")
        
        logger.info("Database initialization completed successfully!")
        
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        raise

def main():
    """Main function to run database initialization"""
    try:
        # Register the Docker configuration
        settings.register("docker", DockerConfig)
        
        # Get configuration
        config = settings.get_config()
        init_docker_db(config)
        print("✅ Docker database initialized successfully!")
    except Exception as e:
        print(f"❌ Docker database initialization failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 