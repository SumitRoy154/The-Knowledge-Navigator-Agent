from langchain_core.messages import HumanMessage, AIMessage


class Memory:
    """
    Manages the chat history for the agent, compatible with LangChain.
    """

    def __init__(self):
        self.chat_history = []

    def add_message(self, user_input: str, agent_response: str):
        self.chat_history.append(HumanMessage(content=user_input))
        self.chat_history.append(AIMessage(content=agent_response))

    def get_history(self):
        return self.chat_history

    def clear_history(self):
        self.chat_history = []

    def get_summary(self):
        summary = {
            "turns": len(self.chat_history) // 2,
            "last_user_input": None,
            "last_agent_response": None,
        }
        if len(self.chat_history) >= 2:
            summary["last_user_input"] = self.chat_history[-2].content
            summary["last_agent_response"] = self.chat_history[-1].content
        return summary
