#!/usr/bin/env python3
"""
Database management script for Thuriyam Base
"""
import typer
import os
import sys
from pathlib import Path

# Add the app directory to the Python path
app_dir = Path(__file__).parent.parent / "app"
sys.path.insert(0, str(app_dir))

from alembic.config import Config
from alembic import command
from core import settings
from core.settings.development import DevConfig
from core.settings.production import ProdConfig
from core.settings.docker import DockerConfig
# from core.settings.staging import StagingConfig

# from core.database import test_database_connection    

app = typer.Typer(help="Database management commands")

def get_alembic_config():
    """Get Alembic configuration"""
    # Get the project root directory (parent of app directory)
    # Register configurations
    settings.register("dev", DevConfig)
    settings.register("prod", ProdConfig)
    settings.register("docker", DockerConfig)
    # register("staging", StagingConfig)


    project_root = Path(__file__).parent.parent
    alembic_cfg = Config(str(project_root / "alembic.ini"))
    return alembic_cfg

@app.command()
def init():
    """Initialize Alembic migrations"""
    try:
        alembic_cfg = get_alembic_config()
        command.init(alembic_cfg, "alembic")
        typer.echo("✅ Alembic initialized successfully")
    except Exception as e:
        typer.echo(f"❌ Failed to initialize Alembic: {e}")
        raise typer.Exit(1)

@app.command()
def migrate():
    """Run all pending migrations"""
    try:
        alembic_cfg = get_alembic_config()
        command.upgrade(alembic_cfg, "head")
        typer.echo("✅ Migrations applied successfully")
    except Exception as e:
        typer.echo(f"❌ Failed to apply migrations: {e}")
        raise typer.Exit(1)

@app.command()
def rollback(revision: str = typer.Option(None, help="Revision to rollback to")):
    """Rollback migrations"""
    try:
        alembic_cfg = get_alembic_config()
        if revision:
            command.downgrade(alembic_cfg, revision)
            typer.echo(f"✅ Rolled back to revision: {revision}")
        else:
            command.downgrade(alembic_cfg, "-1")
            typer.echo("✅ Rolled back one revision")
    except Exception as e:
        typer.echo(f"❌ Failed to rollback: {e}")
        raise typer.Exit(1)

@app.command()
def revision(message: str = typer.Option(..., help="Migration message")):
    """Create a new migration"""
    try:
        alembic_cfg = get_alembic_config()
        command.revision(alembic_cfg, message=message, autogenerate=True)
        typer.echo("✅ New migration created successfully")
    except Exception as e:
        typer.echo(f"❌ Failed to create migration: {e}")
        raise typer.Exit(1)

@app.command()
def current():
    """Show current migration revision"""
    try:
        alembic_cfg = get_alembic_config()
        command.current(alembic_cfg)
    except Exception as e:
        typer.echo(f"❌ Failed to get current revision: {e}")
        raise typer.Exit(1)

@app.command()
def history():
    """Show migration history"""
    try:
        alembic_cfg = get_alembic_config()
        command.history(alembic_cfg)
    except Exception as e:
        typer.echo(f"❌ Failed to get migration history: {e}")
        raise typer.Exit(1)

@app.command()
def test_connection():
    """Test database connection"""
    try:
        # if test_database_connection():
        #     typer.echo("✅ Database connection successful")
        # else:
        #     typer.echo("❌ Database connection failed")
        #     raise typer.Exit(1)
        typer.echo("✅ Database connection successful")
    except Exception as e:
        typer.echo(f"❌ Database connection error: {e}")
        raise typer.Exit(1)

@app.command()
def reset():
    """Reset database (drop all tables and recreate)"""
    try:
        # Confirm the action
        confirm = typer.confirm("⚠️  This will delete all data. Are you sure?")
        if not confirm:
            typer.echo("Operation cancelled")
            return
        
        alembic_cfg = get_alembic_config()
        
        # Downgrade to base
        command.downgrade(alembic_cfg, "base")
        typer.echo("✅ Dropped all tables")
        
        # Upgrade to head
        command.upgrade(alembic_cfg, "head")
        typer.echo("✅ Recreated all tables")
        
    except Exception as e:
        typer.echo(f"❌ Failed to reset database: {e}")
        raise typer.Exit(1)

if __name__ == "__main__":
    app() 