from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Query

from app.core.config import get_settings
from app.core.dependencies import AgentManager, get_agent_manager, get_current_user
from app.db.models.user import User


settings = get_settings()
router = APIRouter(prefix=f"{settings.api_prefix}/agents", tags=["agents"])


@router.get("/")
async def list_agents(
    agent_manager: AgentManager = Depends(get_agent_manager),
    current_user: User = Depends(get_current_user),
) -> list[dict[str, str]]:
    return agent_manager.list_agents()


@router.post("/{agent_name}/execute")
async def execute_agent(
    agent_name: str,
    task: str = Query(..., min_length=1),
    agent_manager: AgentManager = Depends(get_agent_manager),
    current_user: User = Depends(get_current_user),
) -> dict[str, Any]:
    try:
        return await agent_manager.execute(
            agent_name, 
            task, 
            user_id=current_user.id
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))