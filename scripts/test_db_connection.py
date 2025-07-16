#!/usr/bin/env python3
"""
Database connection test script.
This script tests database connectivity for both SQLite and PostgreSQL.
"""

import sys
import os
import logging

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_sqlite_connection():
    """Test SQLite connection"""
    logger.info("Testing SQLite connection...")
    
    # Set environment for SQLite
    os.environ.setdefault("FLAVOUR", "dev")
    os.environ.setdefault("SQLALCHEMY_DATABASE_URL", "sqlite:///./thuriyam.db")
    
    try:
        from core import settings
        from core.settings.development import DevConfig
        from core.database import test_database_connection
        
        # Register the development configuration
        settings.register("dev", DevConfig)
        
        # Test connection
        if test_database_connection():
            logger.info("✅ SQLite connection test successful")
            return True
        else:
            logger.error("❌ SQLite connection test failed")
            return False
    except Exception as e:
        logger.error(f"❌ SQLite connection test failed: {e}")
        return False

def test_postgresql_connection():
    """Test PostgreSQL connection"""
    logger.info("Testing PostgreSQL connection...")
    
    # Set environment for PostgreSQL
    os.environ.setdefault("FLAVOUR", "docker")
    os.environ.setdefault("SQLALCHEMY_DATABASE_URL", "postgresql://thuriyam_user:thuriyam_password@postgres:5432/thuriyam_base")
    
    try:
        from core import settings
        from core.settings.docker import DockerConfig
        from core.database import test_database_connection
        
        # Register the docker configuration
        settings.register("docker", DockerConfig)
        
        # Test connection
        if test_database_connection():
            logger.info("✅ PostgreSQL connection test successful")
            return True
        else:
            logger.error("❌ PostgreSQL connection test failed")
            return False
    except Exception as e:
        logger.error(f"❌ PostgreSQL connection test failed: {e}")
        return False

def main():
    """Main test function"""
    logger.info("Starting database connection tests...")
    
    # Test SQLite
    sqlite_success = test_sqlite_connection()
    
    # Test PostgreSQL
    postgres_success = test_postgresql_connection()
    
    # Summary
    logger.info("\n" + "="*50)
    logger.info("DATABASE CONNECTION TEST RESULTS")
    logger.info("="*50)
    logger.info(f"SQLite: {'✅ PASS' if sqlite_success else '❌ FAIL'}")
    logger.info(f"PostgreSQL: {'✅ PASS' if postgres_success else '❌ FAIL'}")
    logger.info("="*50)
    
    if sqlite_success and postgres_success:
        logger.info("🎉 All database connection tests passed!")
        return 0
    else:
        logger.error("💥 Some database connection tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 