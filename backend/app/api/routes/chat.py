from fastapi import APIRouter

from app.models.schemas import ChatRequest, ChatResponse
from app.services.agent_service import AgentService

router = APIRouter(prefix="/api", tags=["chat"])
service = AgentService()


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    return service.process_message(payload)
