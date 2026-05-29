import json
from typing import Any
from app.modules.agents.agent_manager import AgentManager
from app.providers.llm.base import BaseLLMProvider


class Orchestrator:
    def __init__(self, agent_manager: AgentManager, llm: BaseLLMProvider) -> None:
        self.agent_manager = agent_manager
        self.llm = llm

    async def route_and_execute(self, task: str, **kwargs: Any) -> dict[str, Any]:
        agents_info = self.agent_manager.list_agents()
        
        # Build a prompt for the router
        router_prompt = (
            "You are an intelligent AI Orchestrator. Your task is to select the best agent "
            "to handle the user's request from the list of available agents below.\n\n"
            f"Available Agents:\n{json.dumps(agents_info, indent=2)}\n\n"
            "Respond ONLY with a JSON object in this format:\n"
            '{"selected_agent": "agent_name", "reason": "why this agent was selected"}\n\n'
            f"User Request: {task}"
        )
        
        try:
            # Get decision from LLM
            routing_response = await self.llm.generate(router_prompt)
            # Basic JSON cleanup in case of extra text
            start = routing_response.find("{")
            end = routing_response.rfind("}") + 1
            decision = json.loads(routing_response[start:end])
            
            agent_name = decision.get("selected_agent")
            if not agent_name:
                raise ValueError("LLM failed to select an agent")
            
            # Execute selected agent
            result = await self.agent_manager.execute(agent_name, task, **kwargs)
            
            return {
                "agent_used": agent_name,
                "reasoning": decision.get("reason"),
                "output": result
            }
            
        except Exception as e:
            # Fallback to RAG Agent if routing fails
            return {
                "agent_used": "rag_agent (fallback)",
                "error": str(e),
                "output": await self.agent_manager.execute("rag_agent", task, **kwargs)
            }