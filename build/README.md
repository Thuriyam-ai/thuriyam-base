# Docker Setup with PostgreSQL

This directory contains the Docker configuration for the Thuriyam Base application.

## Services

The Docker Compose setup includes the following services:

- **thuriyam-base-ms**: Main FastAPI application
- **postgres**: PostgreSQL database
- **redis**: Redis cache
- **mongo**: MongoDB database
- **kafka**: Apache Kafka message broker
- **kafka_zookeeper**: Zookeeper for Kafka
- **statsd**: StatsD metrics collection

## Database Configuration

### Local Development
- Uses SQLite database (`thuriyam.db`)
- No additional setup required

### Docker Environment
- Uses PostgreSQL database
- Database: `thuriyam_base`
- User: `thuriyam_user`
- Password: `thuriyam_password`
- Host: `postgres` (Docker service name)
- Port: `5432`

## Environment Variables

The Docker environment uses the `docker.env` file which contains:

```env
# Database URL for Docker environment (PostgreSQL)
SQLALCHEMY_DATABASE_URL=postgresql://thuriyam_user:thuriyam_password@postgres:5432/thuriyam_base

# Other services
REDIS_HOST=redis
REDIS_PORT=6379
MONGO_DATABASE_HOST=mongo
MONGO_DATABASE_PORT=27017
KAFKA_BOOTSTRAP_SERVER=kafka:9092
STATSD_HOST=statsd
STATSD_PORT=9125

# Application settings
FLAVOUR=docker
DEBUG=true
```

## Running the Application

### Local Development
```bash
cd app
python main.py runserver
```

### Docker Environment
```bash
cd build
docker-compose up -d
```

## Database Migration

When running in Docker for the first time, you may need to initialize the PostgreSQL database. The application will automatically create tables when it starts.

## Health Checks

- PostgreSQL: `pg_isready -U thuriyam_user -d thuriyam_base`
- Application: `http://localhost:8000/` (health check endpoint)

## Ports

- Application: `8000`
- PostgreSQL: `5432`
- Redis: `6379`
- MongoDB: `27017`
- Kafka: `9092`
- StatsD: `9125`

## Volumes

- `postgres_data`: PostgreSQL data persistence
- `redis_data`: Redis data persistence
- `kafka_data`: Kafka data persistence
- `zookeeper_data`: Zookeeper data persistence 