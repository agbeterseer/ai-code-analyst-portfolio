import os
from dotenv import load_dotenv

load_dotenv()

ENABLE_HALLUCINATION_CHECK = os.getenv("ENABLE_HALLUCINATION_CHECK", "false").lower() == "true"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
