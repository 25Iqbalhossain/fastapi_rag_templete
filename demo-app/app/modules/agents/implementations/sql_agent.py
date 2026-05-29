from typing import Any
from sqlalchemy import text
from app.modules.agents.base import BaseAgent
from app.providers.database.base import BaseDatabaseProvider


class SQLAgent(BaseAgent):
    def __init__(self, db_provider: BaseDatabaseProvider) -> None:
        super().__init__(
            name="sql_agent",
            description="Agent that executes read-only SQL queries on the database."
        )
        self.db_provider = db_provider

    async def run(self, task: str, **kwargs: Any) -> dict[str, Any]:
        # In a real scenario, you'd use an LLM to generate the SQL.
        # Here we simulate a simple query for demonstration.
        async with self.db_provider.session_manager.session() as session:
            try:
                # Example: "SELECT count(*) FROM users"
                result = await session.execute(text(task))
                data = result.fetchall()
                return {"results": [dict(row._mapping) for row in data]}
            except Exception as e:
                return {"error": str(e)}