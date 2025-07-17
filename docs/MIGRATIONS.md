# Database Migrations with Alembic

This project uses Alembic for database migrations. Alembic is a database migration tool for SQLAlchemy.

## Setup

1. Install Alembic (already included in development requirements):
   ```bash
   pip install alembic
   ```

2. Initialize Alembic (if not already done):
   ```bash
   python scripts/manage_db.py init
   ```

## Usage

### Running Migrations

Apply all pending migrations:
```bash
python scripts/manage_db.py migrate
```

### Creating New Migrations

Create a new migration based on model changes:
```bash
python scripts/manage_db.py revision --message "Add new field to users table"
```

### Checking Migration Status

View current migration revision:
```bash
python scripts/manage_db.py current
```

View migration history:
```bash
python scripts/manage_db.py history
```

### Rolling Back Migrations

Rollback one migration:
```bash
python scripts/manage_db.py rollback
```

Rollback to specific revision:
```bash
python scripts/manage_db.py rollback --revision 0001
```

### Database Operations

Test database connection:
```bash
python scripts/manage_db.py test-connection
```

Reset database (drop all tables and recreate):
```bash
python scripts/manage_db.py reset
```

## Migration Workflow

1. **Make model changes**: Update your SQLAlchemy models in the appropriate files
2. **Generate migration**: Run `python scripts/manage_db.py revision --message "Description of changes"`
3. **Review migration**: Check the generated migration file in `alembic/versions/`
4. **Apply migration**: Run `python scripts/manage_db.py migrate`
5. **Test**: Verify your changes work as expected

## Important Notes

- Always review auto-generated migrations before applying them
- Test migrations in development before applying to production
- Keep migrations small and focused on specific changes
- Never modify existing migration files that have been applied to production
- Use descriptive migration messages

## Troubleshooting

### Common Issues

1. **Migration conflicts**: If you have conflicts between migrations, you may need to merge them manually
2. **Model import errors**: Ensure all models are imported in `alembic/env.py`
3. **Database connection issues**: Check your database configuration in settings

### Getting Help

- Check Alembic documentation: https://alembic.sqlalchemy.org/
- Review the generated migration files in `alembic/versions/`
- Test migrations in a development environment first 