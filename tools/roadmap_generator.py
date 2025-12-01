
# --- Roadmap Generator Tool ---
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Local imports
from config import GEMINI_API_KEY, GEMINI_MODEL

# Dedicated LLM instance for roadmap generation (model configurable)
_llm = ChatGoogleGenerativeAI(
    model=GEMINI_MODEL,
    google_api_key=GEMINI_API_KEY,
    temperature=0.7
)

# Prompt template for roadmap generation
_prompt = ChatPromptTemplate.from_template(
    """
    You are an expert academic advisor. A user wants to learn about '{topic}'.
    Your main goal is to help the student find the best courses for their needs, then provide a concise, actionable learning path.

    Output structure:
    1. Top Courses: List the best available courses for this topic (include course name, platform, and a short reason for recommendation).
    2. Learning Path: Suggest a logical sequence or phases for mastering the topic. The number of phases is up to you—use as many as needed for clarity and effectiveness. For each phase, include:
       - Phase Name
       - Key Topics (2-4 bullet points)
       - Why It Matters (1 sentence)

    Requirements:
    - Be concise and to the point.
    - Use clear section headers (no markdown symbols).
    - Focus on practical, actionable steps.
    - Avoid lengthy explanations or background information.
    """
)

# LangChain Expression Language (LCEL) chain for roadmap generation
roadmap_chain = _prompt | _llm | StrOutputParser()

def generate_learning_roadmap(topic: str):
    """
    Generates a concise learning roadmap for a given topic, showing top courses first, then a logical learning path (phases as needed).
    Returns a string with clear headers and practical focus.
    """
    return roadmap_chain.invoke({"topic": topic})
