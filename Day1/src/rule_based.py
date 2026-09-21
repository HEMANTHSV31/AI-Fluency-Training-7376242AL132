import json
import sys
import re
import os

def load_data():
    """Load the mock database of tickets."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, "..", "data", "tickets.json")
    
    with open(data_path, "r") as f:
        return json.load(f)

def main():
    """Run the rule-based workflow (No LLM)."""
    if len(sys.argv) < 2:
        print("Usage: python rule_based.py \"<your question>\"")
        sys.exit(1)
        
    query = sys.argv[1].lower()
    tickets = load_data()
    
    print(f"--- RULE-BASED WORKFLOW ---")
    print(f"User Query: '{sys.argv[1]}'\n")
    print("Processing using hardcoded Regex and If-Else rules...\n")
    
    status_match = re.search(r"status of.*(t-\d{4})", query)
    if status_match:
        ticket_id = status_match.group(1).upper()
        for ticket in tickets:
            if ticket["ticket_id"] == ticket_id:
                print("Response:")
                print(f"The status of ticket {ticket_id} is '{ticket['status']}'.")
                return
        print("Response:\nTicket not found.")
        return
        
    if "how many" in query and "high priority" in query:
        count = sum(1 for t in tickets if t["priority"].lower() == "high")
        print("Response:")
        print(f"There are currently {count} high priority tickets.")
        return
        
    print("Response:")
    print("I'm sorry, I am a rule-based bot and I don't understand that query. I can only check the status of a specific ticket ID or count high priority tickets.")

if __name__ == "__main__":
    main()
