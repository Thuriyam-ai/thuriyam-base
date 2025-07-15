import asyncio
import importlib
from typing import List
import typer
import uvicorn

from applifespan import app_lifespan

app = typer.Typer()

COMMAND_MODULE_PATHS = [
    "jobnotification.management.commands",
]


@app.command()
def runserver(host: str = "127.0.0.1", port: int = 8000, reload: bool = True):
    """Run the FastAPI server."""
    uvicorn.run("app:app", host=host, port=port, reload=reload)


@app.command()
def run_command(command: str, args: List[str] = typer.Option([])):
    """
    Run a management command.

    Args:
        command: Name of the command to run (e.g. 'cachewarmupcommand')
        args: List of arguments to pass to the command
    """
    import nest_asyncio

    nest_asyncio.apply()

    async def execute_command():
        async with app_lifespan(None):
            # Import and instantiate the command class
            module = None
            for module_path in COMMAND_MODULE_PATHS:
                try:
                    module = importlib.import_module(
                        f"{module_path}.{command}"
                    )
                    break
                except ImportError:
                    continue
            if module is None:
                raise typer.BadParameter(f"Command not found: '{command}'")

            if command_class := getattr(module, "Command", None):
                command_instance = command_class()
                command_instance.execute(args)
                return
            raise typer.BadParameter(
                f"Command not defined in module: '{command}'"
            )

    asyncio.run(execute_command())


if __name__ == "__main__":
    app()
