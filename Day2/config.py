import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from the root .env
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_dotenv(env_path)

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY is missing from .env")

MODEL = os.getenv("MODEL", "openai/gpt-oss-120b")

client = Groq(api_key=api_key)

def banner(title):
    print("*" * 80)
    print(f"** {title}")
    print("*" * 80)
