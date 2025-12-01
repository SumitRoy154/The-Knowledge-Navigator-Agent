from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Local imports
from config import GEMINI_API_KEY

# This is a separate, dedicated LLM instance for this tool.
# It's a good practice to isolate tool-specific LLMs if they have different prompts or settings.
_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.7
)

_prompt = ChatPromptTemplate.from_template(
    """You are an expert academic advisor. A user wants to learn about '{topic}'.
    Create a concise, structured learning roadmap with these sections:
    
    1.  Brief Introduction (1-2 sentences)
    2.  Learning Phases (2-3 phases max):
        - Phase Name
        - Key Topics (3-5 bullet points)
        - Why It Matters (1 sentence)
    
    Keep it direct, practical, and focused on essential learning objectives.
    Avoid lengthy explanations or background information.
    """
)

# This is the LangChain Expression Language (LCEL) chain for this tool.
roadmap_chain = _prompt | _llm | StrOutputParser()

def generate_learning_roadmap(topic: str):
    """Generates a structured, multi-phase learning roadmap for a given topic."""
    return roadmap_chain.invoke({"topic": topic})
