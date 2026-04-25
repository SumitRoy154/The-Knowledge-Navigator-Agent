import os
from dotenv import load_dotenv

load_dotenv()

# Gemini API Key and Model
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

SYSTEM_PROMPT = """
You are the Knowledge Navigator Agent, an expert Academic Advisor specializing in curriculum design and personalized learning paths.
"""
