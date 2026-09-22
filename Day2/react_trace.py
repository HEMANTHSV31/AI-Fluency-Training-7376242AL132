import json
from config import client, MODEL, banner

def check_book_availability(book_title: str) -> str:
    """Checks the database if a book is available to borrow."""
    print(f"  [Action] --> Checking availability for: '{book_title}'")
    db = {
        "ai fundamentals": "Available",
        "machine learning 101": "Checked Out",
        "deep learning mastery": "Available"
    }
    status = db.get(book_title.lower(), "Not Found")
    return f"Book '{book_title}' status: {status}"

tools = [
    {
        "type": "function",
        "function": {
            "name": "check_book_availability",
            "description": "Checks the database if a book is available to borrow.",
            "parameters": {
                "type": "object",
                "properties": {
                    "book_title": {
                        "type": "string",
                        "description": "The title of the book, e.g., AI Fundamentals"
                    }
                },
                "required": ["book_title"]
            }
        }
    }
]

def agent(query, max_steps=8):
    messages = [
        {"role": "system", "content": "You are a helpful ReAct agent. You think about what to do, take actions using tools, and observe the results before returning the final answer."},
        {"role": "user", "content": query}
    ]
    
    for step in range(max_steps):
        print(f"\n--- Step {step + 1} ---")
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0.0
        )
        
        response_message = response.choices[0].message
        
        if response_message.tool_calls:
            print("  [Thought] --> The model decided to use a tool.")
            messages.append(response_message)
            
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                if function_name == "check_book_availability":
                    result = check_book_availability(function_args.get("book_title"))
                else:
                    result = f"Error: Unknown tool {function_name}"
                    
                print(f"  [Observation] --> {result}")
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": result
                })
        else:
            return response_message.content
            
    return "Agent hit max steps without finding an answer."

if __name__ == "__main__":
    banner("REACT AGENT TRACE")
    QUESTION = "Is the book 'AI Fundamentals' currently available in the library database? Also, if I borrow it and the return limit is 14 days, how many weeks is that?"
    print("QUESTION:", QUESTION, "\n")
    print("--- the agent's actions and observations ---")
    answer = agent(QUESTION, max_steps=8)
    print("\nFINAL ANSWER:", answer)