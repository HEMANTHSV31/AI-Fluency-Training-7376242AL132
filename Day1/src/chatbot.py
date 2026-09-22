import os
import sys
from dotenv import load_dotenv
from groq import Groq

env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))
load_dotenv(env_path)

def main():
    """Run the plain chatbot (no data access)."""
    if len(sys.argv) < 2:
        print("Usage: python chatbot.py \"<your question>\"")
        sys.exit(1)
        
    query = sys.argv[1]
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "gsk_xxxxxxxxxxxxxxxxxxxx":
        print("Error: GROQ_API_KEY is missing or not configured in .env file.")
        sys.exit(1)
        
    client = Groq(api_key=api_key)
    
    print(f"--- PLAIN CHATBOT ---")
    print(f"User Query: '{query}'\n")
    print("Thinking (without any access to private data)...\n")
    
    try:
        response = client.chat.completions.create(
            model=os.getenv("MODEL", "openai/gpt-oss-120b"),
            messages=[
                {"role": "system", "content": "You are a helpful customer support assistant."},
                {"role": "user", "content": f"Please answer this query: {query}"}
            ]
        )
        print("Response:")
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"API Error: {e}")

if __name__ == "__main__":
    main()
