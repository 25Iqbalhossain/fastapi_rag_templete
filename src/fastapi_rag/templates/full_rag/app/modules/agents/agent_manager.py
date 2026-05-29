from typing import Any
from app.modules.agents.base import BaseAgent


class AgentManager:
    def __init__(self) -> None:
        self._agents: dict[str, BaseAgent] = {}

    def register(self, agent: BaseAgent) -> None:
        self._agents[agent.name] = agent

    async def execute(self, agent_name: str, task: str, **kwargs: Any) -> dict[str, Any]:
        agent = self._agents.get(agent_name)
        if agent is None:
            # Fallback logic could go here
            if "fallback" in self._agents:
                return await self._agents["fallback"].run(task, **kwargs)
            raise ValueError(f"Unknown agent: {agent_name}")
        return await agent.run(task, **kwargs)

    def list_agents(self) -> list[dict[str, str]]:
        return [
            {"name": a.name, "description": a.description}
            for a in self._agents.values()
        ]
