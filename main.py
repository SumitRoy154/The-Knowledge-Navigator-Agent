import sys
import logging
from typing import List
from tools.course_finder import search_online_courses
from agent import KnowledgeNavigatorAgent
from memory import ConversationMemory
from config import GEMINI_API_KEY

logging.basicConfig(level=logging.WARNING)


def _extract_topic_and_level(user_input: str):
    ui = user_input.strip()
    level = None
    l = ui.lower()
    if any(k in l for k in ["beginner", "i'm a beginner", "i am a beginner", "new to", "start"]):
        level = "Beginner"
    elif any(k in l for k in ["intermediate", "some experience", "familiar"]):
        level = "Intermediate"
    elif any(k in l for k in ["advanced", "expert"]):
        level = "Advanced"
    topic = None
    triggers = ["i want to learn", "want to learn", "learn", "study", "master", "explore"]
    for t in triggers:
        if t in l:
            idx = l.find(t)
            topic_part = ui[idx + len(t):].strip(" :,-.?")
            if topic_part:
                topic = " ".join(topic_part.split()[:6])
            break
    return topic, level


def _format_learning_path_cards(topic: str, level: str, courses: list) -> List[str]:
    topic_clean = topic.title() if topic else "Topic"

    intro_lines = []
    intro_lines.append("1. Introduction")
    intro_lines.append(f"1.1 {topic_clean} is an excellent subject to dive into. It builds practical skills that are widely applicable.")
    intro_lines.append("1.2 As your Knowledge Navigator Agent and Academic Advisor, I searched the web for high-quality, beginner-friendly courses and structured them into a logical learning path tailored for a smooth start.")
    intro_card = "\n".join(intro_lines)

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
    lp_lines = []
    lp_lines.append(f"2. Learning Path: {topic_clean} Fundamentals")
    for idx, p in enumerate(phases, start=1):
        lp_lines.append(f"2.{idx} {p['phase']}")
        lp_lines.append(f"2.{idx}.1 Focus: {p['focus']}")
        lp_lines.append(f"2.{idx}.2 Key Topics to Master: {p['key_topics']}")
        lp_lines.append(f"2.{idx}.3 Estimated Duration: {p['duration']}")
        lp_lines.append("")
    learning_path_card = "\n".join(lp_lines).strip()

    phase_one = [c for c in courses if c.get("phase") == "Phase I"]
    candidates = phase_one or sorted(courses, key=lambda x: x.get("rating", 0), reverse=True)
    top3 = sorted(candidates, key=lambda x: x.get("rating", 0), reverse=True)[:3]

    top_lines = []
    top_lines.append("3. Top 3 Courses to Start Your Journey")
    if not top3:
        top_lines.append("3.1 No courses were found. You can try refining the query or enabling Google CSE keys for better results.")
    else:
        for i, c in enumerate(top3, start=1):
            name = c.get("name", "Unknown")
            platform = c.get("platform", "Unknown")
            focus = (c.get("focus") or c.get("key_topics") or "").replace("\n", " ")
            price = c.get("price", "Varies")
            rating = f"{float(c.get('rating')):.1f}" if c.get("rating") else "N/A"
            url = c.get("url", "N/A")
            top_lines.append(f"3.{i} Course Name: {name}")
            top_lines.append(f"3.{i}.1 Platform: {platform}")
            top_lines.append(f"3.{i}.2 Key Focus: {focus}")
            top_lines.append(f"3.{i}.3 Price (USD): {price}")
            top_lines.append(f"3.{i}.4 Rating: {rating}")
            top_lines.append(f"3.{i}.5 Link: {url}")
            top_lines.append("")
    top_courses_card = "\n".join(top_lines).strip()

    next_lines = []
    next_lines.append("4. Next Steps")
    if top3:
        next_lines.append(f"4.1 Recommendation: Start with \"{top3[0].get('name')}\" for a strong foundation.")
        next_lines.append("4.2 Study focus: Work through core concepts in Phase I and complete small practice exercises after each module.")
        next_lines.append("4.3 Would you like to filter results to free resources only, include hands-on projects/notebooks, or search for a specific platform?")
    else:
        next_lines.append("4.1 I couldn't identify clear Phase I courses. Try broadening the search or enabling API keys for more results.")
    next_steps_card = "\n".join(next_lines).strip()

    return [intro_card, learning_path_card, top_courses_card, next_steps_card]


def main():
    if not GEMINI_API_KEY:
        logging.warning("GEMINI_API_KEY not set. LLM features may not work. Live web search still functions (DuckDuckGo).")

    # KnowledgeNavigatorAgent is available (fallback or full). If import fails earlier, an exception would have been raised.
    try:
        agent = KnowledgeNavigatorAgent()
    except Exception as e:
        logging.error(f"Failed to initialize KnowledgeNavigatorAgent: {e}")
        agent = None

    memory = ConversationMemory()

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

        topic, level = _extract_topic_and_level(user_input)
        if topic:
            if not level:
                level = memory.user_level
            try:
                courses = search_online_courses(topic, level=level, max_results=12)
            except Exception as e:
                logging.error(f"search_online_courses error: {e}")
                courses = []
            if courses:
                cards = _format_learning_path_cards(topic, level, courses)
                for idx, card in enumerate(cards, start=1):
                    print(f"\nCard {idx}")
                    print("-" * 60)
                    print(card)
                    print("-" * 60)
                memory.add_message("user", user_input)
                memory.add_message("assistant", "\n\n".join(cards))
                continue
            else:
                print("No live course results found. Falling back to agent (if available).")

        if agent:
            try:
                response = agent.generate_response(user_input)
                print("\nAdvisor:")
                print(response)
                memory.add_message("user", user_input)
                memory.add_message("assistant", response)
            except Exception as e:
                logging.error(f"Agent generate_response error: {e}")
                print("Agent failed to generate a response. Try again or refine your query.")
        else:
            print("No agent available and no live search results. Try refining your query or set GEMINI_API_KEY.")


if __name__ == "__main__":
    main()
