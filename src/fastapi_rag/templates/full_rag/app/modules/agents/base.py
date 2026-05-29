from abc import ABC, abstractmethod
from typing import Any


class BaseAgent(ABC):
    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description

    @abstractmethod
    async def run(self, task: str, **kwargs: Any) -> dict[str, Any]:
        """Execute the agent's logic for a given task."""
        pass
