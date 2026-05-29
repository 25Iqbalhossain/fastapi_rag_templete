from pathlib import Path

from jinja2 import Environment


TEXT_EXTENSIONS = {
    ".py",
    ".md",
    ".toml",
    ".yml",
    ".yaml",
    ".json",
    ".ini",
    ".txt",
    ".example",
    ".env",
    ".cfg",
}
TEXT_FILENAMES = {"Dockerfile", ".env.example", "LICENSE", "README.md", "alembic.ini"}


def render_file(path: Path, context: dict[str, str]) -> None:
    if not _is_text_file(path):
        return
    template = Environment(autoescape=False).from_string(path.read_text(encoding="utf-8"))
    path.write_text(template.render(**context), encoding="utf-8")


def render_directory(directory: Path, context: dict[str, str]) -> None:
    for file_path in sorted(directory.rglob("*")):
        if file_path.is_file() and "__pycache__" not in file_path.parts:
            render_file(file_path, context)


def _is_text_file(path: Path) -> bool:
    return path.name in TEXT_FILENAMES or path.suffix in TEXT_EXTENSIONS
