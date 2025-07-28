#!/usr/bin/env python3
"""
Database initialization script.
This script sets up the database tables for the application.
"""

import sys
import os
import logging

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

# Set environment variable for configuration
os.environ.setdefault("FLAVOUR", "dev")

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from core import settings
from core.settings.development import DevConfig
from core.settings.docker import DockerConfig
from core.base.model import Base

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    """Initialize database by creating all tables"""
    try:
        # Detect environment and register appropriate configuration
        flavour = os.environ.get("FLAVOUR", "dev")
        logger.info(f"Using configuration flavour: {flavour}")
        
        if flavour == "docker":
            settings.register("docker", DockerConfig)
        else:
            settings.register("dev", DevConfig)
        
        # Get configuration
        config = settings.get_config()
        
        # Create SQLAlchemy engine with conditional connect_args
        def get_connect_args(database_url: str):
            """Get appropriate connect_args based on database type"""
            if database_url.startswith("sqlite"):
                return {"check_same_thread": False}  # Needed for SQLite
            return {}  # No special args needed for PostgreSQL
        
        engine = create_engine(
            config.SQLALCHEMY_DATABASE_URL,
            connect_args=get_connect_args(config.SQLALCHEMY_DATABASE_URL)
        )
        
        logger.info("Creating database tables...")
        
        # Import all models to ensure they are registered with SQLAlchemy
        # This ensures all models are imported and registered before creating tables
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
        init_db()
        print("✅ Database initialized successfully!")
    except Exception as e:
        print(f"❌ Database initialization failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 