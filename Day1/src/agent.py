import os
import sys
import json
from dotenv import load_dotenv
from groq import Groq

env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))
load_dotenv(env_path)

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
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "gsk_xxxxxxxxxxxxxxxxxxxx":
        print("Error: GROQ_API_KEY is missing or not configured in .env file.")
        sys.exit(1)
        
    client = Groq(api_key=api_key)
    
    print(f"--- AI AGENT (LLM + TOOLS) ---")
    print(f"User Query: '{query}'\n")
    print("Agent is reasoning and deciding which tools to use...")
    
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_ticket_status",
                "description": "Returns the status, priority, and notes of a specific ticket by its ID (e.g., T-1001).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticket_id": {
                            "type": "string",
                            "description": "The ticket ID, e.g., T-1001"
                        }
                    },
                    "required": ["ticket_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_all_tickets",
                "description": "Returns the entire database of all open and closed tickets as a JSON string. Use this to count tickets or find specific patterns.",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            }
        }
    ]
    
    messages = [
        {"role": "system", "content": "You are an intelligent support agent. Use your tools to answer this user's query accurately based on our private database."},
        {"role": "user", "content": query}
    ]
    
    try:
        response = client.chat.completions.create(
            model=os.getenv("MODEL", "openai/gpt-oss-120b"),
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0.0
        )
        
        response_message = response.choices[0].message
        
        if response_message.tool_calls:
            messages.append(response_message)
            
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                if function_name == "get_ticket_status":
                    result = get_ticket_status(function_args.get("ticket_id"))
                elif function_name == "get_all_tickets":
                    result = get_all_tickets()
                else:
                    result = f"Error: Unknown tool {function_name}"
                    
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": result
                })
                
            second_response = client.chat.completions.create(
                model=os.getenv("MODEL", "openai/gpt-oss-120b"),
                messages=messages,
                temperature=0.0
            )
            print("\nFinal Agent Response:")
            print(second_response.choices[0].message.content)
        else:
            print("\nFinal Agent Response:")
            print(response_message.content)
            
    except Exception as e:
        print(f"API Error: {e}")

if __name__ == "__main__":
    main()
