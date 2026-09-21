# Analysis: Plain Chatbot vs. Rule-Based Workflow vs. AI Agent

**Name:** Hemanth SV  
**Roll Number:** 7376242AL132  

## 1. Scenario: Enterprise Support Ticket Triage

I chose a private-data scenario based on an Enterprise Support Ticket System. A local JSON file (`tickets.json`) acts as the database containing sensitive ticket details like statuses and priorities. The goal is to answer a manager's test query: *"What is the status of ticket T-1004 and how many high priority tickets do we currently have?"*

---

## 3.1 Explanation of Each Approach

### Approach 1: Plain Chatbot
The plain chatbot relies entirely on its pre-trained knowledge. It has no access to the private `tickets.json` database. It requires zero tools or rules—just an LLM API connection. When asked about ticket T-1004, it forwards the prompt to the LLM. Since it cannot see the actual data, it either hallucinates a response or apologizes for its lack of access, making it useless for internal data queries.

### Approach 2: Rule-Based Workflow
The rule-based workflow has full local access to `tickets.json` and loads it into memory. It does not use an LLM. Instead, it relies on strict, hardcoded Regex and `if/else` rules. When it receives a query, it checks for a perfectly matching pattern. Its biggest limitation is rigidity: it fails on compound or slightly altered questions (like our test query) unless a specific rule was manually coded for that exact phrasing. 

### Approach 3: AI Agent (LLM + Tools + Loop)
The AI agent uses an LLM, tools, and a reasoning loop. It accesses the `tickets.json` database indirectly through Python functions like `get_ticket_status()`. For our test query, the agent enters a loop: it reasons it needs two pieces of information, calls the first tool for T-1004, observes the result, and calls the second tool to count priorities. Finally, it synthesizes a natural language answer. While highly capable, it is slightly slower due to network calls and can face API rate limits.

---

## 3.2 Comparison Table

| Basis for comparison | Plain chatbot | Rule-based workflow | AI agent |
| :--- | :--- | :--- | :--- |
| **Flexibility** | Extremely High | Extremely Low | Very High |
| **Decision-making** | Entirely by the LLM | Hardcoded by developer | Dynamic (LLM decides tools) |
| **Tool usage** | None | None | High (Uses Python tools) |
| **Private-data access**| **None** | **Full** (Direct) | **Full** (Via Tools) |
| **Multi-step task handling** | Poor | Poor | Excellent (Reasoning loop) |
| **Automation** | Low | High (For narrow tasks) | High (For complex tasks) |
| **Reliability** | Low (Hallucinates) | High (But brittle) | Medium-High |

---

## 3.3 Suitability Analysis

The **AI Agent** is unequivocally the best approach for this scenario. The plain chatbot fails due to lack of data access. The rule-based workflow fails because managers ask highly varied, complex questions that cannot be covered by rigid regex rules. The AI agent provides the perfect balance: it uses the LLM's natural language comprehension for flexibility while securely retrieving absolute facts via its tools.

---

## 3.4 Conclusion

* **Use a Plain Chatbot when:** You need general knowledge, brainstorming, or text summarization without requiring strict factual accuracy or private data.
* **Use a Rule-Based Workflow when:** The task is highly repetitive, mission-critical, and inputs are perfectly structured (e.g., parsing a specific CSV). 
* **Use an AI Agent when:** Dealing with unstructured natural language, accessing private APIs/databases, and requiring multi-step reasoning to bridge the gap between human language and complex internal systems.
