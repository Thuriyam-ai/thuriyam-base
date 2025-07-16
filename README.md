# Thuriyam Base Template

A FastAPI-based microservice template with MongoDB, Redis, and SQLite support.

## Features

- FastAPI web framework
- SQLAlchemy ORM with SQLite database
- MongoDB integration with Motor async driver
- Redis caching support
- JWT authentication
- API key authentication
- Comprehensive logging and monitoring
- Docker support for development and production

## Directory Structure

```
.
├── app/                    # FastAPI Application
│   ├── core/              # Core modules (auth, database, settings)
│   ├── todos/             # Todo module (example implementation)
│   ├── requirements/      # Python dependencies
│   ├── app.py            # FastAPI application
│   ├── main.py           # CLI entry point
│   └── applifespan.py    # Application lifecycle management
├── scripts/               # Database initialization scripts
├── test/                  # Postman collections and test files
├── DockerfileLocal        # Development Docker configuration
├── DockerfileProd         # Production Docker configuration
├── DockerfileStag         # Staging Docker configuration
└── Makefile              # Build and deployment commands
```

## Prerequisites

- Python 3.11
- pip (Python package manager)
- SQLite (included with Python)
- Redis (optional, for caching)
- MongoDB (optional, for NoSQL data)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd thuriyam-base-template
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install base dependencies
pip install -r app/requirements/base.txt

# For development, also install development dependencies
pip install -r app/requirements/development.txt
```

## Database Setup

### Initialize SQLite Database

The application uses SQLite by default. Initialize the database with the required tables:

```bash
# From the app directory
cd app
python ../scripts/init_db.py
```

This will:
- Create the SQLite database file (`app/thuriyam.db`)
- Create all necessary tables (including `todos` table)
- Set up the database schema

**Important**: Make sure to run this from the app directory to ensure the database is created in the correct location where the FastAPI application expects it.

## Running the Application

### Development Mode

```bash
# From the project root directory
cd app
python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

### Using the CLI

```bash
# From the project root directory
cd app
python main.py runserver --host 127.0.0.1 --port 8000 --reload
```

### Production Mode

```bash
# From the project root directory
cd app
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

## API Endpoints

Once the application is running, you can access:

- **Health Check**: `GET http://localhost:8000/`
- **API Documentation**: `GET http://localhost:8000/docs`
- **ReDoc Documentation**: `GET http://localhost:8000/redoc`

### Todo API Endpoints

- **Get all todos**: `GET http://localhost:8000/api/v1/todos`
- **Create todo**: `POST http://localhost:8000/api/v1/todos`
- **Get specific todo**: `GET http://localhost:8000/api/v1/todos/{todo_id}`
- **Update todo**: `PUT http://localhost:8000/api/v1/todos/{todo_id}`
- **Toggle todo**: `PATCH http://localhost:8000/api/v1/todos/{todo_id}/toggle`
- **Delete todo**: `DELETE http://localhost:8000/api/v1/todos/{todo_id}`

## Configuration

The application uses environment-based configuration:

- **Development**: Uses `DevConfig` from `app/core/settings/development.py`
- **Production**: Uses `ProdConfig` from `app/core/settings/production.py`

### Environment Variables

Set the `FLAVOUR` environment variable to switch configurations:

```bash
export FLAVOUR=dev  # For development
export FLAVOUR=prod # For production
```

### Database Configuration

The default SQLite database URL is: `sqlite:///./thuriyam.db`

You can override this by setting the `SQLALCHEMY_DATABASE_URL` environment variable:

```bash
export SQLALCHEMY_DATABASE_URL="sqlite:///./my_database.db"
```

## Docker Support

### Local Development (SQLite)

For local development, the application uses SQLite by default:

```bash
docker build -f DockerfileLocal -t thuriyam-dev .
docker run -p 8000:8000 thuriyam-dev
```

### Docker Environment (PostgreSQL)

For a complete Docker environment with PostgreSQL, Redis, MongoDB, and Kafka:

```bash
cd build
docker-compose up -d
```

This will start:
- **PostgreSQL**: Database server on port 5432
- **Redis**: Cache server on port 6379
- **MongoDB**: NoSQL database on port 27017
- **Kafka**: Message broker on port 9092
- **FastAPI Application**: On port 8000

#### Database Configuration

- **Local Development**: Uses SQLite (`thuriyam.db`)
- **Docker Environment**: Uses PostgreSQL with the following configuration:
  - Database: `thuriyam_base`
  - User: `thuriyam_user`
  - Password: `thuriyam_password`
  - Host: `postgres` (Docker service name)
  - Port: `5432`

#### Environment Variables

The Docker environment uses `build/docker.env` which sets:
- `FLAVOUR=docker` (uses DockerConfig)
- `SQLALCHEMY_DATABASE_URL=postgresql://thuriyam_user:thuriyam_password@postgres:5432/thuriyam_base`
- Service hostnames for Redis, MongoDB, Kafka, etc.

### Production

```bash
docker build -f DockerfileProd -t thuriyam-prod .
docker run -p 8000:8000 thuriyam-prod
```

## Testing

### Using Postman

Import the Postman collection from `test/wi-job-notification-ms.postman_collection.json` and use the environment files:

- `test/local.postman_environment.json` for local development
- `test/stag.postman_environment.json` for staging
- `test/prod.postman_environment.json` for production

### Manual Testing

```bash
# Test health endpoint
curl http://localhost:8000/

# Test todos endpoint
curl http://localhost:8000/api/v1/todos

# Create a todo
curl -X POST http://localhost:8000/api/v1/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Todo", "description": "This is a test todo"}'
```

## Troubleshooting

### Common Issues

1. **"no such table: todos" error**
   - Make sure you've run the database initialization script
   - Ensure you're running the script from the app directory: `cd app && python ../scripts/init_db.py`
   - Check that the database file exists in the app directory and has the correct tables

2. **Port already in use**
   - Kill any existing processes on port 8000
   - Use a different port: `--port 8001`

3. **Import errors with motor/pymongo**
   - Ensure you have the correct versions installed
   - The requirements file specifies compatible versions

### Database Reset

If you need to reset the database:

```bash
# Remove the existing database
rm app/thuriyam.db

# Reinitialize the database
cd app
python ../scripts/init_db.py
```

## Development

### Adding New Modules

1. Create a new directory in `app/` for your module
2. Follow the pattern of the `todos/` module
3. Include `model.py`, `repository.py`, `schema.py`, `validator.py`, and `views.py`
4. Register your router in `app/app.py`

### Code Style

The project uses:
- `flake8` for linting
- `pre-commit` for git hooks
- Type hints throughout the codebase

## Deployment

### Using Makefile

```bash
# Build and run locally
make runserver

# Build Docker image
make build

# Deploy to staging
make deploy-stag

# Deploy to production
make deploy-prod
```

### Kubernetes Deployment

The project includes Kubernetes manifests for deployment:

- `JenkinsfileStag` for staging deployment
- `JenkinsfileProd` for production deployment

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is proprietary and confidential.

## Authors

This template was created by the Thuriyam team.