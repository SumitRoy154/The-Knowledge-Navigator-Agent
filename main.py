import sys
from agent import KnowledgeNavigatorAgent
from agent import Agent
from memory import Memory
from tools.course_finder import search_online_courses  # added import

# This check is now primarily handled in config.py, but it's good practice
# to ensure the module is imported correctly.
from config import GEMINI_API_KEY

def _extract_topic_and_level(user_input: str):
    """Lightweight extractor for topic and level from user input."""
    ui = user_input.strip()
    level = None
    l = ui.lower()
    if any(k in l for k in ["beginner", "i'm a beginner", "i am a beginner", "new to", "start"]):
        level = "Beginner"
    elif any(k in l for k in ["intermediate", "some experience", "familiar"]):
        level = "Intermediate"
    elif any(k in l for k in ["advanced", "expert"]):
        level = "Advanced"
    # naive topic extraction: words after 'learn' or 'study' or 'want to learn'
    topic = None
    triggers = ["learn", "study", "want to learn", "i want to learn", "master", "explore"]
    for t in triggers:
        if t in l:
            # find position and take remainder
            idx = l.find(t)
            topic_part = ui[idx + len(t):].strip(" :,-.?")
            if topic_part:
                # take up to first 5 words
                topic = " ".join(topic_part.split()[:5])
            break
    return topic, level

def _format_learning_path(topic: str, level: str, courses: list) -> str:
    """Construct plain, numbered learning path and top-3 course list (with links)."""
    topic_clean = topic.title() if topic else "Topic"
    # Phases with simple descriptive text
    phases = [
        {
            "phase": "Phase I: The Foundation",
            "focus": "Terminology and Mechanics",
            "key_topics": "Core fundamentals, basic terminology and concepts",
            "duration": "4-8 Weeks"
        },
        {
            "phase": "Phase II: Core Application",
            "focus": "Practical application and hands-on skills",
            "key_topics": "Project work, applied techniques, model building",
            "duration": "6-10 Weeks"
        },
        {
            "phase": "Phase III: Analysis & Reporting",
            "focus": "Advanced topics and real-world scenarios",
            "key_topics": "Advanced concepts, deployment, evaluation and interpretation",
            "duration": "8-12 Weeks"
        }
    ]

    lines = []
    # 1. Introduction
    lines.append("1. Introduction")
    lines.append(f"1.1 {topic_clean} is an excellent subject to dive into. It builds practical skills that are widely applicable.")
    lines.append("1.2 As your Knowledge Navigator Agent and Academic Advisor, I searched the web for high-quality, beginner-friendly courses and structured them into a logical learning path tailored for a smooth start.")
    lines.append("")

    # 2. Learning Path
    lines.append(f"2. Learning Path: {topic_clean} Fundamentals")
    for idx, p in enumerate(phases, start=1):
        lines.append(f"2.{idx} {p['phase']}")
        lines.append(f"2.{idx}.1 Focus: {p['focus']}")
        lines.append(f"2.{idx}.2 Key Topics to Master: {p['key_topics']}")
        lines.append(f"2.{idx}.3 Estimated Duration: {p['duration']}")
        lines.append("")

    # 3. Top 3 Courses
    lines.append("3. Top 3 Courses to Start Your Journey")
    # Prefer Phase I courses, else top-rated overall
    phase_one = [c for c in courses if c.get("phase") == "Phase I"]
    candidates = phase_one or sorted(courses, key=lambda x: x.get("rating", 0), reverse=True)
    top3 = sorted(candidates, key=lambda x: x.get("rating", 0), reverse=True)[:3]

    if not top3:
        lines.append("3.1 No courses were found. You can try refining the query or enabling Google CSE keys for better results.")
    else:
        for i, c in enumerate(top3, start=1):
            name = c.get("name", "Unknown")
            platform = c.get("platform", "Unknown")
            focus = (c.get("focus") or c.get("key_topics") or "").replace("\n", " ")
            price = c.get("price", "Varies")
            rating = f"{float(c.get('rating')):.1f}" if c.get("rating") else "N/A"
            url = c.get("url", "N/A")
            lines.append(f"3.{i} Course Name: {name}")
            lines.append(f"3.{i}.1 Platform: {platform}")
            lines.append(f"3.{i}.2 Key Focus: {focus}")
            lines.append(f"3.{i}.3 Price (USD): {price}")
            lines.append(f"3.{i}.4 Rating: {rating}")
            lines.append(f"3.{i}.5 Link: {url}")
            lines.append("")

    # 4. Next Steps
    lines.append("4. Next Steps")
    if top3:
        lines.append(f"4.1 Recommendation: Start with \"{top3[0].get('name')}\" for a strong foundation.")
        lines.append("4.2 Study focus: Work through core concepts in Phase I and complete small practice exercises after each module.")
        lines.append("4.3 Would you like to filter results to free resources only, include hands-on projects/notebooks, or search for a specific platform?")
    else:
        lines.append("4.1 I couldn't identify clear Phase I courses. Try broadening the search or enabling API keys for more results.")
    lines.append("")

    return "\n".join(lines)

def main():
    """Main conversation loop"""
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

        try:
            # Initialize agent
            agent = KnowledgeNavigatorAgent()
            print("Agent initialized successfully!\n")

            while True:
                try:
                    # Get user input
                    user_input = input("You: ").strip()
                    if not user_input:
                        continue

                    command = user_input.lower()
                    if command == "quit":
                        # ...existing quit handling ...
                        break
                    if command == "reset":
                        agent.reset_conversation()
                        # ...existing reset handling ...
                        continue
                    if command == "summary":
                        # ...existing summary handling ...
                        continue

                    # New: attempt dynamic real-time course search + formatted output
                    topic, level = _extract_topic_and_level(user_input)
                    if topic:
                        # prefer explicit level if found otherwise default to agent memory inference
                        if not level:
                            # get level from agent memory if available
                            level = agent.get_session_summary().get("level", "Beginner")
                        # perform live search
                        courses = search_online_courses(topic, level=level, max_results=12)
                        if courses:
                            formatted = _format_learning_path(topic, level, courses)
                            print("\n" + formatted + "\n")
                            # also record in agent memory for continuity
                            agent.memory.add_message("user", user_input)
                            agent.memory.add_message("assistant", formatted)
                            continue
                        # if no courses found, fall back to LLM path
                        print("\nNo live course results found — falling back to the agent's LLM formatter.\n")

                    # fallback: use LLM agent (keeps existing behavior)
                    print_separator("Processing your request...")
                    print("Searching for courses and structuring your learning path...")
                    response = agent.generate_response(user_input)
                    print_response(response)

                except KeyboardInterrupt:
                    # ...existing interrupt handling ...
                    continue
                except Exception as e:
                    # ...existing exception handling ...
                    continue

        except Exception as e:
            # ...existing fatal error handling ...
            sys.exit(1)

if __name__ == "__main__":
    main()
