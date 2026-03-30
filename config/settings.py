import os
from dotenv import load_dotenv

load_dotenv()

USE_OLLAMA = os.getenv("USE_OLLAMA", "true").lower() == "true"

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral:7b")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")