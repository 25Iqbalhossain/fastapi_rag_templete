from pathlib import Path
import shutil
import tempfile

from fastapi_rag.renderer.jinja_renderer import render_directory
from fastapi_rag.utils.package_resources import copy_package_tree, get_template_resource


class ProjectGenerator:
    def __init__(self, template_root=None) -> None:
        self.template_root = template_root

    def generate(self, destination: Path, context: dict[str, str]) -> None:
        if destination.exists():
            raise FileExistsError(f"Destination already exists: {destination}")
        render_context = dict(context)
        render_context.setdefault(
            "package_name",
            render_context["project_name"].lower().replace("-", "_").replace(" ", "_"),
        )
        render_context.setdefault("queue_provider", "celery")
        template_root = self.template_root or get_template_resource("full_rag")

        destination.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="fastapi-rag-") as temp_dir:
            temp_path = Path(temp_dir) / destination.name
            copy_package_tree(template_root, temp_path)
            render_directory(temp_path, render_context)
            shutil.move(str(temp_path), str(destination))
