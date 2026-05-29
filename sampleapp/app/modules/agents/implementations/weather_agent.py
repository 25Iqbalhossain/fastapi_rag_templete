from typing import Any
from app.modules.agents.base import BaseAgent


class WeatherAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            name="weather_agent",
            description="Agent that provides weather information (Mocked)."
        )

    async def run(self, task: str, **kwargs: Any) -> dict[str, Any]:
        # Simulated weather logic
        location = task.lower()
        if "london" in location:
            return {"location": "London", "temperature": "15C", "condition": "Cloudy"}
        return {"location": task, "temperature": "Unknown", "condition": "No data"}