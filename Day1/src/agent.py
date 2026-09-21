import os
import sys
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

def load_data():
    """Helper to load the JSON database."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, "..", "data", "tickets.json")
    with open(data_path, "r") as f:
        return json.load(f)

def get_ticket_status(ticket_id: str) -> str:
    """Returns the status, priority, and notes of a specific ticket by its ID (e.g., T-1001)."""
    print(f"  [Agent Tool Execution] --> Called get_ticket_status('{ticket_id}')")
    tickets = load_data()
    for t in tickets:
        if t["ticket_id"].upper() == ticket_id.upper():
            return f"Ticket {ticket_id}: Status='{t['status']}', Priority='{t['priority']}', Notes='{t['notes']}'"
    return f"Ticket {ticket_id} not found."

def get_all_tickets() -> str:
    """Returns the entire database of all open and closed tickets as a JSON string. Use this to count tickets or find specific patterns."""
    print("  [Agent Tool Execution] --> Called get_all_tickets()")
    return json.dumps(load_data())

def main():
    """Run the AI Agent (LLM + Tools + Loop)."""
    if len(sys.argv) < 2:
        print("Usage: python agent.py \"<your question>\"")
        sys.exit(1)
        
    query = sys.argv[1]
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "paste_your_api_key_here_inside_the_quotes":
        print("Error: GEMINI_API_KEY is missing or not configured in .env file.")
        sys.exit(1)
        
    client = genai.Client(api_key=api_key)
    
    print(f"--- AI AGENT (LLM + TOOLS) ---")
    print(f"User Query: '{query}'\n")
    print("Agent is reasoning and deciding which tools to use...")
    
    try:
        chat = client.chats.create(
            model='gemini-3.6-flash',
            config=types.GenerateContentConfig(
                tools=[get_ticket_status, get_all_tickets],
                temperature=0.0
            )
        )
        
        response = chat.send_message(
            f"You are an intelligent support agent. Use your tools to answer this user's query accurately based on our private database: {query}"
        )
        print("\nFinal Agent Response:")
        print(response.text)
        
    except Exception as e:
        print(f"API Error: {e}")

if __name__ == "__main__":
    main()
