from agent import Agent
from memory import Memory

# This check is now primarily handled in config.py, but it's good practice
# to ensure the module is imported correctly.
from config import GEMINI_API_KEY

def main():
    """The main function to run the terminal chat session."""
    # Initialize the agent and memory
    knowledge_agent = Agent()
    chat_memory = Memory()

    print("Welcome to the Knowledge Navigator! I'm your Academic Advisor.")
    print("You can ask me to find online courses for you. Type 'exit' to end the session.")

    while True:
        # Get user input from the terminal
        user_input = input("\nYou: ")

        if user_input.lower() == 'exit':
            print("Thank you for using the Knowledge Navigator. Goodbye!")
            break

        try:
            # Get the current chat history
            history = chat_memory.get_history()

            # Process the user input and get the agent's response
            agent_response = knowledge_agent.invoke(user_input, history)

            # Print the agent's response with proper formatting
            if isinstance(agent_response, str):
                print(f"\nAdvisor: {agent_response}")
            else:
                # Handle case where response is not a string
                print("\nAdvisor:", str(agent_response))
                
            # Add the interaction to memory if it's not a 'more' command
            if user_input.strip().lower() != 'more':
                chat_memory.add_message(user_input, agent_response)
                
        except Exception as e:
            error_msg = f"I'm sorry, but I encountered an error: {str(e)}"
            print(f"\nAdvisor: {error_msg}")
            logging.error(f"Error in main loop: {error_msg}")

if __name__ == "__main__":
    main()
