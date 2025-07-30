# Thuriyam Microservice Template

A comprehensive [Copier](https://github.com/copier-org/copier) template for generating FastAPI-based microservices with all the infrastructure and best practices from the Thuriyam architecture.

## What This Template Generates

This template creates a production-ready FastAPI microservice with:

### 🚀 **Core Features**
- **FastAPI** application with automatic OpenAPI documentation
- **SQLAlchemy ORM** with PostgreSQL or SQLite support
- **Pydantic** schemas for data validation
- **Repository pattern** for clean data access layer
- **Model builder pattern** with comprehensive validation
- **Environment-based configuration** (dev/prod/docker)
- **JWT authentication** support
- **CORS middleware** configuration
- **Health check endpoints**

### 🏢 **Multi-Module Architecture**
- **Multiple Business Domains**: Generate multiple modules (e.g., users, products, orders) in one service
- **Complete CRUD APIs**: Each module gets full Create, Read, Update, Delete endpoints
- **Automatic Integration**: All modules are automatically registered in the main application
- **Database Schema Support**: Alembic migrations include all module models
- **Consistent Structure**: Every module follows the same architectural patterns

### 🐳 **Docker & Infrastructure**
- **Multi-stage Docker setup** (development & production)
- **Docker Compose** with PostgreSQL, Redis, MongoDB, Kafka
- **Development hot-reload** with volume mounting
- **Production-optimized** containers

### 🛠 **Development Tools**
- **Database migrations** with Alembic
- **Management scripts** for common tasks
- **Database initialization** scripts
- **Testing utilities**
- **Environment setup** scripts

### 📊 **Monitoring & Observability**
- **StatsD integration** for metrics
- **Comprehensive logging** configuration
- **Health check endpoints**
- **Service adapters** for external systems

## Quick Start

### Prerequisites

- Python 3.11+
- [Copier](https://github.com/copier-org/copier)
- Docker & Docker Compose (optional but recommended)

### Install Copier

```bash
pip install copier
```

### Generate a New Microservice

```bash
copier copy https://github.com/pmundhra/thuriyam-base/ new-service
```

Follow the interactive prompts to configure your service.

### Multi-Module Example

Generate a service with multiple business domains:

```bash
copier copy https://github.com/pmundhra/thuriyam-base/ user-management-service
# When prompted for modules, enter: users,roles,permissions
cd user-management-service
```

This creates a service with three complete modules:
- **Users Module**: `/api/v1/users` endpoints for user management
- **Roles Module**: `/api/v1/roles` endpoints for role management  
- **Permissions Module**: `/api/v1/permissions` endpoints for permission management

Each module includes:
- Database model with SQLAlchemy
- Pydantic schemas for validation
- Repository for data access
- Complete CRUD API endpoints
- Input validators

### What You'll Be Asked

- **Project name** (e.g., "user-service", "payment-service")
- **Service description**
- **Organization details**
- **Database choice** (PostgreSQL or SQLite)
- **Module names** (comma-separated list e.g., "users,roles,permissions" or single module "users")
- **Optional features** (Docker, Alembic migrations)
- **Authentication settings**

## Generated Project Structure

```
new-service/
├── build/                     # Docker infrastructure
│   ├── docker-compose.yml    # Multi-service Docker setup
│   ├── docker.env           # Docker environment variables
│   └── README.md            # Docker setup documentation
├── scripts/                   # Utility scripts
│   ├── setup_docker.sh      # Docker environment setup
│   ├── manage_db.py         # Database management
│   ├── init_docker_db.py    # Docker DB initialization
│   ├── test_db_connection.py # Connection testing
│   └── generate-jwt-30-mins.py # JWT token generation
├── my_new_service/           # Main application code
│   ├── main.py              # CLI entry point
│   ├── app.py               # FastAPI application
│   ├── core/                # Core infrastructure
│   ├── example_module/      # Generated example module
│   ├── DockerfileLocal      # Development container
│   └── DockerfileProd       # Production container
├── README.md                 # Project documentation
└── env.example              # Environment variables template
```

## Development Workflow

After generating your service:

### 1. Set up environment
```bash
cd my-new-service
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e .
```

### 2. Configure environment
```bash
cp env.example .env
# Edit .env with your settings
```

### 3. Start development

**Option A: Local development (SQLite)**
```bash
python main.py runserver
```

**Option B: Full Docker environment**
```bash
cd build
docker-compose up -d
```

## Docker Environment

The template includes a complete Docker Compose setup with:

- **Your FastAPI service** (port 8000)
- **PostgreSQL** database (port 5432)
- **Redis** cache (port 6379) 
- **MongoDB** NoSQL (port 27017)
- **Apache Kafka** messaging (port 9092)
- **StatsD** metrics (port 9125)

### Quick Docker Setup

```bash
cd my-new-service/build
./scripts/setup_docker.sh  # Automated setup
# Or manually:
docker-compose up -d
```

## Database Migrations with Alembic

The template includes Alembic for database migrations when the `include_alembic` option is enabled. Alembic is a database migration tool for SQLAlchemy that allows you to manage database schema changes over time.

### Migration Setup

1. **Alembic is pre-configured** in the generated project
2. **Models are automatically detected** - just import them in your modules
3. **Environment configuration** is handled automatically

### Common Migration Commands

#### Running Migrations

Apply all pending migrations:
```bash
python scripts/manage_db.py migrate
```

#### Creating New Migrations

Create a new migration based on model changes:
```bash
python scripts/manage_db.py revision --message "Add new field to users table"
```

#### Checking Migration Status

View current migration revision:
```bash
python scripts/manage_db.py current
```

View migration history:
```bash
python scripts/manage_db.py history
```

#### Rolling Back Migrations

Rollback one migration:
```bash
python scripts/manage_db.py rollback
```

Rollback to specific revision:
```bash
python scripts/manage_db.py rollback --revision abc123
```

#### Database Operations

Test database connection:
```bash
python scripts/manage_db.py test-connection
```

Reset database (drop all tables and recreate):
```bash
python scripts/manage_db.py reset
```

### Migration Workflow

1. **Make model changes**: Update your SQLAlchemy models in the appropriate module files
2. **Generate migration**: Run `python scripts/manage_db.py revision --message "Description of changes"`
3. **Review migration**: Check the generated migration file in `alembic/versions/`
4. **Apply migration**: Run `python scripts/manage_db.py migrate`
5. **Test**: Verify your changes work as expected

### Important Migration Notes

- **Always review auto-generated migrations** before applying them
- **Test migrations in development** before applying to production
- **Keep migrations small and focused** on specific changes
- **Never modify existing migration files** that have been applied to production
- **Use descriptive migration messages** for better tracking

### Migration Troubleshooting

#### Common Issues

1. **Migration conflicts**: If you have conflicts between migrations, you may need to merge them manually
2. **Model import errors**: Ensure all models are imported in `alembic/env.py`
3. **Database connection issues**: Check your database configuration in settings

#### Getting Help

- Check [Alembic documentation](https://alembic.sqlalchemy.org/)
- Review the generated migration files in `alembic/versions/`
- Test migrations in a development environment first

## Template Features

### 📝 **Complete CRUD API**
Every generated service includes a working example module with:
- Create, Read, Update, Delete operations
- Pagination and filtering
- Input validation and error handling
- Comprehensive API documentation

### 🗄️ **Database Management**
- Automatic table creation
- Migration management with Alembic
- Connection pooling and error handling
- Support for both PostgreSQL and SQLite

### 🔐 **Security & Authentication**
- JWT token support
- API key authentication
- CORS configuration
- Input validation and sanitization

### 🧪 **Testing & Development**
- Hot reload in development
- Database testing utilities
- Health check endpoints
- Comprehensive logging

## Customization

### Adding New Modules

The template follows a clear pattern for adding new modules:

1. Create module directory with standard files:
   - `model.py` - Database model
   - `schema.py` - Pydantic schemas
   - `repository.py` - Data access layer
   - `validator.py` - Input validation
   - `views.py` - API endpoints
   - `__init__.py` - Module registration

2. Register the module in `app.py`
3. Add routes to the FastAPI app

### Environment Configuration

Three pre-configured environments:
- **Development** (`FLAVOUR=dev`) - Debug enabled, local SQLite
- **Production** (`FLAVOUR=prod`) - Optimized, docs disabled
- **Docker** (`FLAVOUR=docker`) - PostgreSQL, all services

### Extending the Template

To modify this template for your organization:

1. Fork/clone this repository
2. Edit the template files (`.jinja` files)
3. Update `copier.yml` for new variables
4. Test with `copier copy`

## Support & Documentation

- **Generated project documentation**: See `README.md` in generated projects
- **API documentation**: Available at `/docs` when running the service
- **Docker setup**: See `build/README.md` in generated projects

## Contributing

This template embodies Thuriyam's microservice best practices. When contributing:

1. Follow the established patterns
2. Update documentation
3. Test template generation
4. Ensure Docker compatibility

## License

Created and maintained by Thuriyam for internal microservice development. 