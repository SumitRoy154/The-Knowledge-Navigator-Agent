from langchain_core.messages import HumanMessage, AIMessage

class Memory:
    """Manages the chat history for the agent, compatible with LangChain."""
    def __init__(self):
        self.chat_history = []

    def add_message(self, user_input: str, agent_response: str):
        """Adds a user message and the corresponding AI response to the history."""
        self.chat_history.append(HumanMessage(content=user_input))
        self.chat_history.append(AIMessage(content=agent_response))

    def get_history(self):
        """Returns the current chat history."""
        return self.chat_history
