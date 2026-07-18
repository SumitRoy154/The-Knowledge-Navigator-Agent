import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field


# Local imports
from app.core.config import GEMINI_API_KEY, GEMINI_MODEL
from tools.course_finder import search_online_courses
from tools.roadmap_generator import generate_learning_roadmap

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- System Prompt Definition ---
SYSTEM_PROMPT = """
You are a concise, practical, and resourceful Academic Advisor named the Knowledge Navigator.
Your main goal is to help the user find the best available courses for their learning goal, then provide a clear, actionable learning path.

**Agent Workflow:**
1. When a user asks to learn a topic, FIRST use the `search_online_courses` tool to find the best courses for that topic.
2. Then use the `generate_learning_roadmap` tool to create a logical learning path (number of phases is up to you).
3. Synthesize both into a single, concise response.


**Response Structure:**
- Start with a brief, friendly introduction.
- Present the top recommended courses. For each course, always include:
    - Course name
    - Platform
    - Link to the course (MANDATORY)
    - Short reason for recommendation
- Present the learning path (phases as needed, each with phase name, key topics, and why it matters).
- Be concise and to the point. Avoid lengthy explanations.

**Constraint Rules:**
- NEVER invent or hallucinate course data. Only use the exact data returned by the `search_online_courses` tool.
- If the search tool returns no results, clearly state that no courses were found, but still present the learning path.
"""

# --- Pydantic Model for the Tool's Arguments ---
class CourseSearchArgs(BaseModel):
    topic: str = Field(description="The main subject or topic of the courses to search for.")
    max_price: float = Field(default=None, description="The maximum budget for the course in USD.")
    min_rating: float = Field(default=None, description="The minimum user rating for the course (e.g., 4.5).")

# --- Agent Class ---
class Agent:
    def __init__(self):
        # 1. Initialize the LLM (model configurable)
        self.llm = ChatGoogleGenerativeAI(
            model=GEMINI_MODEL,
            google_api_key=GEMINI_API_KEY,
            temperature=0.7
        )

        # 2. Define the custom tools
        tools = [
            StructuredTool.from_function(
                func=search_online_courses,
                name="search_online_courses",
                description="Searches for online courses based on topic, budget, and rating preferences.",
                args_schema=CourseSearchArgs
            ),
            StructuredTool.from_function(
                func=generate_learning_roadmap,
                name="generate_learning_roadmap",
                description="Generates a concise, actionable learning roadmap for a given topic.",
            )
        ]

        # 3. Create the Agent Prompt Template
        prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ])

        # 4. Create the Agent
        agent = create_tool_calling_agent(self.llm, tools, prompt)

        # 5. Create the Agent Executor
        self.executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            handle_parsing_errors=True
        )

    def format_response(self, response):
        """Format the agent's response to be clean and consistent."""
        if isinstance(response, list) and all(isinstance(item, dict) and 'course_name' in item for item in response):
            formatted = "\nHere are some recommended courses for you:\n"
            for i, course in enumerate(response, 1):
                formatted += f"\n{i}. {course['course_name']}"
                formatted += f"\n   Platform: {course['platform_name']}"
                formatted += f"\n   Price: {'Free' if course['price_usd'] == 0.0 else f'${course['price_usd']}'}"
                formatted += f"\n   Rating: {course['average_rating']}/5"
                formatted += f"\n   Duration: {course['duration_weeks']} weeks"
                formatted += f"\n   [Course Link]({course['course_url']})\n"
            return formatted

        if isinstance(response, str):
            import re
            response = re.sub(r'\x1b\[([0-9A-Za-z;?]?[0-9]*)*[m|K]?', '', response)
            lines = [line.strip() for line in response.split('\n') if line.strip()]
            return '\n'.join(lines)

        return str(response)

    def invoke(self, user_input: str, chat_history: list):
        """Invokes the agent with user input and chat history, returning the response."""
        logging.info(f"Invoking agent with input: '{user_input}' and history: {len(chat_history)} messages")
        try:
            response = self.executor.invoke({
                "input": user_input,
                "chat_history": [msg for msg in chat_history if not isinstance(msg, dict)]
            })

            full_response = response['output']
            formatted_response = self.format_response(full_response)

            chat_history.append({
                'user_input': user_input,
                'response': formatted_response
            })

            logging.info("Agent response formatted")
            return formatted_response

        except Exception as e:
            error_msg = f"I'm sorry, but I encountered an error: {str(e)}"
            logging.error(f"Error in agent invocation: {error_msg}")
            return error_msg
