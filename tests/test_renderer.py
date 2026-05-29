from pathlib import Path

from fastapi_rag.generators.project_generator import ProjectGenerator
from fastapi_rag.renderer.jinja_renderer import render_directory, render_file
from fastapi_rag.utils.package_resources import get_template_resource


def test_render_file_renders_jinja_variables(tmp_path: Path) -> None:
    file_path = tmp_path / "config.txt"
    file_path.write_text("name={{ project_name }}", encoding="utf-8")
    render_file(file_path, {"project_name": "My App"})
    assert file_path.read_text(encoding="utf-8") == "name=My App"


def test_render_directory_creates_backend_scaffold(tmp_path: Path) -> None:
    destination = tmp_path / "myapp"
    generator = ProjectGenerator()
    generator.generate(
        destination=destination,
        context={
            "project_name": "My AI Backend",
            "llm_provider": "echo",
            "vector_db": "qdrant",
            "database_provider": "postgresql",
            "cache_provider": "redis",
            "secret_key": "unit-test-secret",
        },
    )

    assert (destination / "app" / "main.py").exists()
    assert (destination / "docker-compose.yml").exists()
    assert (destination / ".env.example").exists()
    rendered_readme = (destination / "README.md").read_text(encoding="utf-8")
    rendered_env = (destination / ".env.example").read_text(encoding="utf-8")
    assert "# My AI Backend" in rendered_readme
    assert "PROJECT_NAME=My AI Backend" in rendered_env
    assert "SECRET_KEY=unit-test-secret" in rendered_env


def test_project_generator_rejects_existing_destination(tmp_path: Path) -> None:
    destination = tmp_path / "existing"
    destination.mkdir()
    (destination / "keep.txt").write_text("occupied", encoding="utf-8")
    generator = ProjectGenerator()

    try:
        generator.generate(
            destination=destination,
            context={
                "project_name": "Blocked",
                "llm_provider": "echo",
                "vector_db": "qdrant",
                "database_provider": "postgresql",
                "cache_provider": "redis",
                "secret_key": "secret",
            },
        )
    except FileExistsError:
        return
    raise AssertionError("Expected FileExistsError for non-empty destination")


def test_template_resource_is_available_from_package() -> None:
    resource = get_template_resource("full_rag")
    assert resource.is_dir()
    assert resource.joinpath("docker-compose.yml").is_file()
