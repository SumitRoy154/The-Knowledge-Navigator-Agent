from app.models.schemas import ChatRequest, ChatResponse
from agent import Agent
from memory import Memory


class AgentService:
    """Service layer that delegates chat processing to the core Agent."""

    def __init__(self):
        self.agent = Agent()
        self.memory = Memory()

    def process_message(self, payload: ChatRequest) -> ChatResponse:
        user_text = payload.message.strip()
        agent_text = self.agent.invoke(user_text, self.memory.get_history())
        self.memory.add_message(user_text, agent_text)
        return ChatResponse(response=agent_text)
