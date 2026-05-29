from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Query

from app.core.config import get_settings
from app.core.dependencies import (
    Orchestrator, 
    get_orchestrator, 
    get_current_user,
    ConversationRepository,
    get_conversation_repository
)
from app.db.models.user import User
from app.db.models.conversation import MessageRole


settings = get_settings()
router = APIRouter(prefix=f"{settings.api_prefix}/chat", tags=["chat"])


@router.post("/conversations")
async def create_conversation(
    title: str | None = Query(None),
    current_user: User = Depends(get_current_user),
    conv_repo: ConversationRepository = Depends(get_conversation_repository),
):
    return await conv_repo.create(current_user.id, title)


@router.get("/conversations")
async def list_conversations(
    current_user: User = Depends(get_current_user),
    conv_repo: ConversationRepository = Depends(get_conversation_repository),
):
    return await conv_repo.list_by_user(current_user.id)


@router.post("/conversations/{conversation_id}/message")
async def send_message(
    conversation_id: int,
    content: str = Query(..., min_length=1),
    orchestrator: Orchestrator = Depends(get_orchestrator),
    current_user: User = Depends(get_current_user),
    conv_repo: ConversationRepository = Depends(get_conversation_repository),
) -> dict[str, Any]:
    # 1. Verify conversation belongs to user
    conv = await conv_repo.get_by_id(conversation_id)
    if not conv or conv.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # 2. Save User Message
    await conv_repo.add_message(conversation_id, MessageRole.USER, content)
    
    # 3. Intelligent Orchestration
    # Note: We could pass the conversation history to the orchestrator here
    # For now, we pass the latest message
    result = await orchestrator.route_and_execute(
        content, 
        user_id=current_user.id,
        history=[{"role": m.role, "content": m.content} for m in conv.messages]
    )
    
    # 4. Save Assistant Message
    assistant_content = str(result.get("output", {}).get("answer", result.get("output", result)))
    await conv_repo.add_message(conversation_id, MessageRole.ASSISTANT, assistant_content)
    
    return {
        "conversation_id": conversation_id,
        "user_message": content,
        "assistant_response": assistant_content,
        "orchestration_details": {
            "agent_used": result.get("agent_used"),
            "reasoning": result.get("reasoning")
        }
    }