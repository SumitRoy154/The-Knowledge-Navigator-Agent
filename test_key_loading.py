from config import GEMINI_API_KEY
print(f"API Key Loaded: {bool(GEMINI_API_KEY)}")
print(f"Key length: {len(GEMINI_API_KEY) if GEMINI_API_KEY else 0} characters")
