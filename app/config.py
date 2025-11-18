import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise RuntimeError("GITHUB_TOKEN is required in environment or .env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is required in environment or .env")

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

# Local timezone offset (e.g., Cairo = +2)
TZ_OFFSET_HOURS = int(os.getenv("TZ_OFFSET_HOURS", "2"))
