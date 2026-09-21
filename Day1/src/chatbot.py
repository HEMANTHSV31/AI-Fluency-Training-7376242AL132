import os
import sys
from dotenv import load_dotenv
from google import genai

load_dotenv()

def main():
    """Run the plain chatbot (no data access)."""
    if len(sys.argv) < 2:
        print("Usage: python chatbot.py \"<your question>\"")
        sys.exit(1)
        
    query = sys.argv[1]
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "paste_your_api_key_here_inside_the_quotes":
        print("Error: GEMINI_API_KEY is missing or not configured in .env file.")
        sys.exit(1)
        
    client = genai.Client(api_key=api_key)
    
    print(f"--- PLAIN CHATBOT ---")
    print(f"User Query: '{query}'\n")
    print("Thinking (without any access to private data)...\n")
    
    try:
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=f"You are a helpful customer support assistant. Please answer this query: {query}"
        )
        print("Response:")
        print(response.text)
    except Exception as e:
        print(f"API Error: {e}")

if __name__ == "__main__":
    main()
