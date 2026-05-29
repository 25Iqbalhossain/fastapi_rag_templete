from typing import Any
from app.modules.agents.base import BaseAgent
from app.modules.rag.pipeline import RAGPipeline


class RAGAgent(BaseAgent):
    def __init__(self, rag_pipeline: RAGPipeline) -> None:
        super().__init__(
            name="rag_agent",
            description="Agent that uses RAG to answer questions based on indexed documents."
        )
        self.rag_pipeline = rag_pipeline

    async def run(self, task: str, **kwargs: Any) -> dict[str, Any]:
        user_id = kwargs.get("user_id")
        if user_id is None:
            return {"error": "user_id is required for RAGAgent"}
        
        response = await self.rag_pipeline.run(
            user_id=user_id,
            query=task,
            limit=kwargs.get("limit", 3)
        )
        return response.model_dump()