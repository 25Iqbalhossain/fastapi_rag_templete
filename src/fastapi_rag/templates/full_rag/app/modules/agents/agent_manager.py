from collections.abc import Awaitable, Callable


AgentHandler = Callable[[str], Awaitable[dict[str, object]]]


class AgentManager:
    def __init__(self) -> None:
        self._handlers: dict[str, AgentHandler] = {}

    def register(self, name: str, handler: AgentHandler) -> None:
        self._handlers[name] = handler

    async def execute(self, agent_name: str, task: str) -> dict[str, object]:
        handler = self._handlers.get(agent_name)
        if handler is None:
            raise ValueError(f"Unknown agent: {agent_name}")
        return await handler(task)
