# Thuriyam Microservice Template

This is a [Copier](https://github.com/copier-org/copier) template for generating FastAPI-based microservices based on the Thuriyam architecture.

## Prerequisites

- Python 3.11+
- [Copier](https://github.com/copier-org/copier) tool

Install Copier:
```bash
pip install copier
```

## Usage

### Generate a new microservice

```bash
copier copy thuriyam-base/ thuriyam-service/
```

You'll be prompted for various configuration options:

- **project_name**: Name of your microservice (e.g., "user-service", "payment-service")
- **service_description**: Brief description of the service
- **python_module_name**: Python module name (auto-generated from project name)
- **org_name**: Organization name (default: "Thuriyam")
- **version**: Initial version (default: "0.1.0")
- **author_name**: Author name
- **author_email**: Author email
- **modules**: Comma-separated list of module names (e.g., "users,products,orders"). Each module will have its own complete CRUD API with models, repositories, schemas, and views. (default: "items")
- **use_postgres**: Use PostgreSQL instead of SQLite (default: true)
- **database_name**: Database name (when using PostgreSQL)
- **database_user**: Database user (when using PostgreSQL)
- **database_password**: Database password (when using PostgreSQL)
- **include_docker**: Include Docker configuration files (default: true)
- **include_alembic**: Include Alembic for database migrations (default: true)
- **api_prefix**: API prefix path (default: "/api/v1")
- **jwt_secret_key**: JWT secret key for authentication

### Example

```bash
$ copier copy thuriyam-base/ user-service/

🎤 What is the name of your microservice? (e.g., user-service, payment-service)
   thuriyam-service
❯ user-service

🎤 Brief description of what this service does
   A FastAPI-based microservice
❯ User management and authentication service

🎤 Python module name (snake_case version of project name)
   user_service
❯ user_service

🎤 Organization name
   Thuriyam
❯ Thuriyam

🎤 Initial version
   0.1.0
❯ 0.1.0

🎤 Author name
   Thuriyam
❯ Thuriyam

🎤 Author email
   contact@thuriyam.ai
❯ contact@thuriyam.ai

🎤 Name for the example module (e.g., users, orders, products)
   items
❯ users

🎤 Use PostgreSQL instead of SQLite?
   True
❯ True

🎤 Database name
   user_service_db
❯ user_service_db

🎤 Database user
   user_service_user
❯ user_service_user

🎤 Database password
   user_service_password
❯ user_service_password

🎤 Include Docker configuration files?
   True
❯ True

🎤 Include Alembic for database migrations?
   True
❯ True

🎤 API prefix path
   /api/v1
❯ /api/v1

🎤 JWT secret key for authentication
   your-secret-key-change-in-production
❯ your-jwt-secret-key-here

Microservice user-service created successfully!
Next steps:
1. cd user-service
2. Review and update .env files
3. Run: python -m venv venv && source venv/bin/activate
4. Run: pip install -e .
5. Run database migrations if using PostgreSQL
6. Start development: python main.py runserver
Or use Docker: cd build && docker-compose up -d
```

## Generated Structure

The template creates a complete FastAPI microservice with:

### Core Features
- FastAPI application with automatic documentation
- SQLAlchemy ORM with PostgreSQL/SQLite support
- Pydantic for data validation
- Repository pattern for data access
- Model builder pattern with validation
- Environment-based configuration
- Comprehensive logging
- JWT authentication support
- CORS middleware
- Health check endpoints

### Docker & Infrastructure
- Multi-service Docker Compose setup (PostgreSQL, Redis, MongoDB, Kafka)
- Development and production Docker configurations
- Hot reload development environment
- Infrastructure management scripts

### Database Management
- Alembic migrations (optional)
- Database initialization scripts
- Connection testing utilities
- Management command-line tools

### Utility Scripts
- Docker environment setup
- Database management and testing
- JWT token generation for testing
- Script deployment utilities

### Project Structure
```
{project_name}/
├── README.md                          # Project documentation
├── build/                             # Docker infrastructure (optional)
│   ├── docker-compose.yml            # Multi-service Docker setup
│   ├── docker.env                    # Docker environment variables
│   └── README.md                     # Docker setup documentation
├── scripts/                           # Utility scripts
│   ├── setup_docker.sh              # Docker environment setup
│   ├── manage_db.py                  # Database management CLI
│   ├── init_docker_db.py             # Docker DB initialization
│   ├── test_db_connection.py         # Connection testing
│   ├── generate-jwt-30-mins.py       # JWT token generation
│   └── copy_scripts_to_app.sh        # Script deployment utility
├── app/                             # Main application code
│   ├── main.py                       # CLI entry point
│   ├── app.py                        # FastAPI application
│   ├── applifespan.py                # Application lifecycle
│   ├── pyproject.toml                # Project configuration
│   ├── env.example                   # Environment variables template
│   ├── README.md                     # Project-specific documentation
│   ├── core/                         # Core infrastructure
│   │   ├── settings/                 # Environment configurations
│   │   ├── base/                     # Base classes (Model, Repository, etc.)
│   │   ├── database.py               # Database configuration
│   │   └── adapter/                  # Adapter classes (stubs)
│   ├── {example_module}/             # Example module
│   │   ├── __init__.py               # Module initialization
│   │   ├── model.py                  # Database model
│   │   ├── schema.py                 # Pydantic schemas
│   │   ├── repository.py             # Data access layer
│   │   ├── validator.py              # Input validation
│   │   └── views.py                  # API endpoints
│   ├── DockerfileLocal               # Development Docker (optional)
│   ├── DockerfileProd                # Production Docker (optional)
│   ├── alembic.ini                   # Alembic configuration (optional)
│   └── alembic/                      # Database migrations (optional)
│       └── versions/                 # Migration files
└── __init__.py                       # Root package initialization
```

## Development Workflow

### Local Development (Python)
```bash
cd my-new-service
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e .
python app/main.py runserver
```

### Docker Development
```bash
cd my-new-service/build
docker-compose up -d
# Or use the setup script:
cd ../scripts
./setup_docker.sh
```

### Database Management
```bash
# Test database connections
python scripts/test_db_connection.py

# Run database migrations (if Alembic enabled)
python scripts/manage_db.py migrate

# Generate JWT tokens for testing
python scripts/generate-jwt-30-mins.py

# Initialize Docker database
python scripts/init_docker_db.py
```

## Updating the Template

To update an existing project with template changes:

```bash
copier update
```

This will apply any template updates while preserving your customizations.

## Template Development

To modify this template:

1. Edit the template files (`.jinja` files)
2. Update `copier.yml` for new configuration options
3. Test the template with `copier copy`

### Template Variables

The template uses Jinja2 templating with these key variables:

- `{{ project_name }}` - Project name
- `{{ python_module_name }}` - Python module name (used for service names, but app code is in `app/` directory)
- `{{ modules }}` - Comma-separated list of module names
- `{{ org_name }}` - Organization name
- `{{ service_description }}` - Service description
- `{{ version }}` - Project version
- `{{ use_postgres }}` - Boolean for PostgreSQL vs SQLite
- `{{ include_docker }}` - Boolean for Docker files
- `{{ include_alembic }}` - Boolean for Alembic migrations
- `{{ database_name }}`, `{{ database_user }}`, `{{ database_password }}` - Database configuration

### Conditional Files

Some files are only generated based on configuration:

- **Docker files**: Generated when `include_docker` is true
- **Alembic configuration**: Generated when `include_alembic` is true
- **PostgreSQL configuration**: Used when `use_postgres` is true

## Features by Category

### 🚀 **Core Application**
- FastAPI with automatic OpenAPI documentation
- Environment-based configuration (dev/prod/docker)
- Comprehensive logging and error handling
- Health check and monitoring endpoints

### 🗄️ **Database & Persistence**
- SQLAlchemy ORM with migration support
- Repository pattern for clean data access
- Model builder pattern with validation
- Support for PostgreSQL and SQLite
- Database connection testing and management

### 🐳 **Infrastructure & Deployment**
- Multi-service Docker Compose setup
- Development and production containers
- Hot reload development environment
- Service discovery and networking

### 🔐 **Security & Authentication**
- JWT token authentication
- API key support
- CORS configuration
- Input validation and sanitization

### 🛠️ **Development Tools**
- Database migration management
- Connection testing utilities
- JWT token generation for testing
- Script deployment and management
- Comprehensive project documentation

## Support

For issues with the template or generated projects, please check:

1. The generated `README.md` for setup instructions
2. `build/README.md` for Docker-specific setup
3. Environment configuration in `.env` files
4. Database connection settings
5. Python virtual environment setup

## License

This template is provided by Thuriyam for creating microservices based on our established patterns and best practices. 