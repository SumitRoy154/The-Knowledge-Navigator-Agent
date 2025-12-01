
import logging
from agent import Agent
from memory import Memory
from config import GEMINI_API_KEY

logging.basicConfig(level=logging.WARNING)

def main():
    if not GEMINI_API_KEY:
        logging.warning("GEMINI_API_KEY not set. LLM features may not work. Live web search still functions (DuckDuckGo).")

    try:
        agent = Agent()
    except Exception as e:
        logging.error(f"Failed to initialize Agent: {e}")
        print("Agent initialization failed. Exiting.")
        return

    memory = Memory()

    print("Welcome to the Knowledge Navigator! I'm your Academic Advisor.")
    print("Type 'quit' or 'exit' to end, 'reset' to clear memory, 'summary' for session info.")

    while True:
        user_input = input("\nYou: ").strip()
        if not user_input:
            continue
        cmd = user_input.lower().strip()
        if cmd in ("exit", "quit"):
            print("Thank you for using the Knowledge Navigator. Goodbye!")
            break
        if cmd == "reset":
            memory.clear_history()
            print("Conversation memory cleared.")
            continue
        if cmd == "summary":
            summary = memory.get_summary()
            print("Session Summary:")
            for k, v in summary.items():
                print(f"  {k}: {v}")
            continue

        # Use the improved agent logic for all queries
        response = agent.invoke(user_input, memory.get_history())
        print("\nAdvisor:")
        print(response)
        memory.add_message(user_input, response)


if __name__ == "__main__":
    main()
