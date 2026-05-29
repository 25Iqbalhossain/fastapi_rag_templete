from typing import Annotated, Optional
from pathlib import Path
from secrets import token_urlsafe

import typer
from rich.console import Console
from rich.prompt import Prompt

from fastapi_rag.generators.project_generator import ProjectGenerator


app = typer.Typer(
    help="Generate production-grade FastAPI RAG backends with provider abstractions.",
    no_args_is_help=True,
)
console = Console()

LLM_PROVIDERS = ("echo", "openai", "ollama")
VECTOR_PROVIDERS = ("qdrant", "chroma", "pgvector", "pinecone")
DATABASE_PROVIDERS = ("postgresql", "mysql")
CACHE_PROVIDERS = ("redis", "dragonfly")


@app.callback()
def callback() -> None:
    """
    Enterprise AI backend template generator for FastAPI and RAG systems.
    """
    pass


@app.command("new")
def new(
    project_name: Annotated[
        Optional[str],
        typer.Argument(help="Project name (will prompt if not provided)")
    ] = None,
) -> None:
    """Generate a new backend project from the full_rag template."""
    console.print("[bold cyan]fastapi-rag[/bold cyan] project generator")
    final_project_name = Prompt.ask("Project name", default=project_name or "my-rag-backend").strip()
    package_name = final_project_name.lower().replace("-", "_").replace(" ", "_")
    llm_provider = _prompt_choice("LLM provider", LLM_PROVIDERS, default="echo")
    vector_db = _prompt_choice("Vector DB", VECTOR_PROVIDERS, default="qdrant")
    database_provider = _prompt_choice("Database provider", DATABASE_PROVIDERS, default="postgresql")
    cache_provider = _prompt_choice("Cache provider", CACHE_PROVIDERS, default="redis")

    generator = ProjectGenerator()
    destination = Path.cwd() / final_project_name
    generator.generate(
        destination=destination,
        context={
            "project_name": final_project_name,
            "package_name": package_name,
            "llm_provider": llm_provider,
            "vector_db": vector_db,
            "database_provider": database_provider,
            "cache_provider": cache_provider,
            "queue_provider": "celery",
            "secret_key": token_urlsafe(32),
        },
    )
    console.print(f"[green]Generated project:[/green] {destination}")
    console.print("Next steps:")
    console.print(f"  cd {final_project_name}")
    console.print("  docker compose up --build")


def _prompt_choice(label: str, choices: tuple[str, ...], default: str) -> str:
    value = Prompt.ask(
        f"{label} ({', '.join(choices)})",
        default=default,
    ).strip().lower()
    if value not in choices:
        raise typer.BadParameter(f"Unsupported value '{value}' for {label}")
    return value


if __name__ == "__main__":
    app()
