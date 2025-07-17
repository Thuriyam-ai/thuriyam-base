#!/usr/bin/env python3
"""
Database connection test script.
This script tests database connectivity for PostgreSQL (development and docker environments).
"""

import sys
import os
import logging

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_development_connection():
    """Test PostgreSQL connection for development environment"""
    logger.info("Testing PostgreSQL connection (development)...")
    
    # Set environment for development
    os.environ.setdefault("FLAVOUR", "dev")
    os.environ.setdefault("SQLALCHEMY_DATABASE_URL", "postgresql://thuriyam_user:thuriyam_password@localhost:5432/thuriyam_base")
    
    try:
        from core import settings
        from core.settings.development import DevConfig
        from core.database import test_database_connection
        
        # Register the development configuration
        settings.register("dev", DevConfig)
        
        # Test connection
        if test_database_connection():
            logger.info("✅ Development PostgreSQL connection test successful")
            return True
        else:
            logger.error("❌ Development PostgreSQL connection test failed")
            return False
    except Exception as e:
        logger.error(f"❌ Development PostgreSQL connection test failed: {e}")
        return False

def test_docker_connection():
    """Test PostgreSQL connection for docker environment"""
    logger.info("Testing PostgreSQL connection (docker)...")
    
    # Set environment for docker
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
            logger.info("✅ Docker PostgreSQL connection test successful")
            return True
        else:
            logger.error("❌ Docker PostgreSQL connection test failed")
            return False
    except Exception as e:
        logger.error(f"❌ Docker PostgreSQL connection test failed: {e}")
        return False

def main():
    """Main test function"""
    logger.info("Starting PostgreSQL database connection tests...")
    
    # Test development environment
    dev_success = test_development_connection()
    
    # Test docker environment
    docker_success = test_docker_connection()
    
    # Summary
    logger.info("\n" + "="*50)
    logger.info("POSTGRESQL DATABASE CONNECTION TEST RESULTS")
    logger.info("="*50)
    logger.info(f"Development: {'✅ PASS' if dev_success else '❌ FAIL'}")
    logger.info(f"Docker: {'✅ PASS' if docker_success else '❌ FAIL'}")
    logger.info("="*50)
    
    if dev_success and docker_success:
        logger.info("🎉 All PostgreSQL database connection tests passed!")
        return 0
    else:
        logger.error("💥 Some PostgreSQL database connection tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 