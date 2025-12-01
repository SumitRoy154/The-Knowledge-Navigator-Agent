from langchain_core.messages import HumanMessage, AIMessage

class Memory:
    """
    Manages the chat history for the agent, compatible with LangChain.
    Provides methods to add, clear, and summarize conversation history.
    """
    def __init__(self):
        self.chat_history = []

    def add_message(self, user_input: str, agent_response: str):
        """
        Adds a user message and the corresponding AI response to the history.
        """
        self.chat_history.append(HumanMessage(content=user_input))
        self.chat_history.append(AIMessage(content=agent_response))

    def get_history(self):
        """
        Returns the current chat history as a list of LangChain message objects.
        """
        return self.chat_history

    def clear_history(self):
        """
        Clears the chat history (for session reset).
        """
        self.chat_history = []

    def get_summary(self):
        """
        Returns a summary of the session (number of turns, last user input, last agent response).
        """
        summary = {
            "turns": len(self.chat_history) // 2,
            "last_user_input": None,
            "last_agent_response": None
        }
        if len(self.chat_history) >= 2:
            summary["last_user_input"] = self.chat_history[-2].content
            summary["last_agent_response"] = self.chat_history[-1].content
        return summary
