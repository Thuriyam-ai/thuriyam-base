#!/bin/bash

# Thuriyam Base Docker Setup Script
# This script sets up the Docker environment with PostgreSQL

set -e

echo "🐳 Setting up Thuriyam Base Docker Environment..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed. Please install it and try again."
    exit 1
fi

# Navigate to build directory
cd "$(dirname "$0")/../build"

echo "📦 Starting Docker services..."
docker-compose up -d

echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if PostgreSQL is ready
echo "🔍 Checking PostgreSQL connection..."
if docker-compose exec -T postgres pg_isready -U thuriyam_user -d thuriyam_base; then
    echo "✅ PostgreSQL is ready!"
    
    # Check if database exists, create if it doesn't
    echo "🔍 Checking if database exists..."
    db_exists=$(docker-compose exec -T postgres psql -U thuriyam_user -lqt | cut -d \| -f 1 | grep -qw thuriyam_base || echo "not_found")
    
    if [ "$db_exists" = "not_found" ]; then
        echo "📊 Database 'thuriyam_base' not found. Creating database..."
        docker-compose exec -T postgres createdb -U thuriyam_user thuriyam_base
        echo "✅ Database 'thuriyam_base' created successfully!"
    else
        echo "✅ Database 'thuriyam_base' already exists"
    fi
    
    # Check if tables exist
    echo "🔍 Checking if database tables exist..."
    table_count=$(docker-compose exec -T postgres psql -U thuriyam_user -d thuriyam_base -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" | tr -d ' ')
    
    if [ "$table_count" -eq "0" ]; then
        echo "📊 No tables found. Creating database tables..."
        # Run Docker-specific database initialization
        docker-compose exec -T thuriyam-base-ms python3 /src/scripts/init_docker_db.py
        if [ $? -eq 0 ]; then
            echo "✅ Database tables created successfully!"
        else
            echo "❌ Failed to create database tables"
            exit 1
        fi
    else
        echo "✅ Database tables already exist ($table_count tables found)"
    fi
else
    echo "⚠️  PostgreSQL might still be starting up. Please wait a moment and check again."
fi

# Check if the application is responding
echo "🔍 Checking application health..."
if curl -f http://localhost:8000/ > /dev/null 2>&1; then
    echo "✅ Application is running!"
    echo "🌐 API Documentation: http://localhost:8000/docs"
    echo "📊 Health Check: http://localhost:8000/"
else
    echo "⚠️  Application might still be starting up. Please wait a moment and check again."
fi

echo ""
echo "🎉 Docker environment setup complete!"
echo ""
echo "📋 Service URLs:"
echo "   - Application: http://localhost:8000"
echo "   - PostgreSQL: localhost:5432"
echo "   - Redis: localhost:6379"
echo "   - MongoDB: localhost:27017"
echo "   - Kafka: localhost:9092"
echo ""
echo "🔧 Useful commands:"
echo "   - View logs: docker-compose logs -f"
echo "   - Stop services: docker-compose down"
echo "   - Restart services: docker-compose restart"
echo "   - Access PostgreSQL: docker-compose exec postgres psql -U thuriyam_user -d thuriyam_base"
echo "   - Initialize database manually: docker-compose exec thuriyam-base-ms python3 /src/scripts/init_docker_db.py" 