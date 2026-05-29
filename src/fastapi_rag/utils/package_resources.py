from importlib.resources import files
from pathlib import Path
from typing import Protocol


class TraversableLike(Protocol):
    name: str

    def is_dir(self) -> bool: ...
    def is_file(self) -> bool: ...
    def iterdir(self): ...
    def joinpath(self, *descendants: str): ...
    def read_bytes(self) -> bytes: ...


def get_template_resource(template_name: str = "full_rag") -> TraversableLike:
    return files("fastapi_rag").joinpath("templates", template_name)


def copy_package_tree(source: TraversableLike, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for child in source.iterdir():
        target = destination / child.name
        if child.is_dir():
            copy_package_tree(child, target)
        elif child.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(child.read_bytes())
