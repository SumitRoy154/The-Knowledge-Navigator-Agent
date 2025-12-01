import os
import sys
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Get the API key and strip any surrounding whitespace and quotes
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip('"\'')

if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY not found. Please set it in the .env file.", file=sys.stderr)
    sys.exit(1)

# Verify the key length (should be 39 characters for a valid key)
if len(GEMINI_API_KEY) != 39 or not GEMINI_API_KEY.startswith('AIza'):
    print(f"Warning: The API key format appears to be invalid. Expected 39 characters starting with 'AIza', got {len(GEMINI_API_KEY)} characters.", file=sys.stderr)
