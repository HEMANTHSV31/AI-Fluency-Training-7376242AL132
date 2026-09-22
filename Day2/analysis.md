# Reasoning and Acting: Comparing Direct Prompting, Chain-of-Thought, and ReAct

## 1. Scenario: Library Book Tracking
For this analysis, I have chosen a **Library Book Tracking** scenario. This scenario involves questions that require multi-step arithmetic, logical deductions based on dates, and questions that require fetching real-time data from a mock library database.

**The three questions used in this scenario are:**
1. **Multi-step arithmetic:** "If I borrow 3 books on Monday, return 1 on Wednesday, and the total borrowing limit is 5 books, how many more books can I borrow right now?"
2. **Logic / Ordering:** "John was born 5 years before the book 'AI Fundamentals' was published. If the book was published in 2015, how old will John be in 2030?"
3. **External Information:** "Is the book 'AI Fundamentals' currently available in the library database? Also, if I borrow it and the return limit is 14 days, how many weeks is that?"

---

## 3.1 Explanation of each approach

### Direct Prompting
- **What it can answer:** Simple factual questions that are widely known and exist in its training data, or extremely simple math equations.
- **What it cannot answer:** Complex multi-step reasoning problems (it often jumps to the wrong conclusion) and questions requiring real-time or private external data (like our library database).
- **Tool usage:** It does not use tools. It cannot decide to call one.
- **How it arrives at a final answer:** It takes the user's prompt and immediately generates the most statistically likely response based on its internal weights. There is no visible reasoning or scratchpad used.
- **Limitations on this scenario:** For the third question (checking book availability), it either hallucinates an answer or apologizes for not having access to the library system. For the math questions, if the math is complex enough, it may hallucinate the final number because it didn't take the time to calculate intermediate steps.

### Chain-of-Thought (CoT)
- **What it can answer:** Complex multi-step math, logic puzzles, and reasoning questions.
- **What it cannot answer:** Questions requiring external data.
- **Tool usage:** It does not use tools.
- **How it arrives at a final answer:** The system prompt forces the model to think step-by-step. It breaks the problem down, writes out intermediate calculations (e.g., "Step 1: Calculate current borrowed books. 3 - 1 = 2"), and uses its own generated output as context for the next step before arriving at the `Final Answer:`.
- **Limitations on this scenario:** While it brilliantly solves the math and logic questions about borrowing limits and John's age by breaking them down, it still fails completely on the third question. No amount of "thinking step-by-step" can tell it whether 'AI Fundamentals' is currently checked out of the database.

### ReAct Agent (Reasoning + Acting)
- **What it can answer:** Both complex reasoning tasks AND questions requiring real-time external data.
- **Tool usage:** Yes. It is provided with a list of available tools (e.g., `check_book_availability`) and their JSON schemas. It uses its "Thought" step to realize it lacks information, outputs a JSON tool call, waits for the observation, and then continues.
- **How it arrives at a final answer:** It loops through a cycle:
  1. **Thought:** "I need to know if the book is available."
  2. **Action:** `check_book_availability("AI Fundamentals")`
  3. **Observation:** "Available"
  4. **Thought:** "Now I need to calculate how many weeks 14 days is."
  5. **Action:** (Internal math reasoning: 14 / 7 = 2)
  6. **Final Answer:** "The book is available, and 14 days is 2 weeks."
- **Limitations on this scenario:** It is slower and more expensive because it requires multiple API calls back and forth to the LLM. It can also get stuck in loops if the tool returns unexpected errors.

---

## 3.2 Comparison table

| Basis for comparison | Direct prompting | Chain-of-Thought | ReAct agent |
| :--- | :--- | :--- | :--- |
| **Reasoning depth** | Very shallow. Jumps straight to the answer. | High. Explores intermediate steps thoroughly. | High. Explores steps and incorporates new data. |
| **Tool usage** | None. | None. | Yes, can call external functions autonomously. |
| **Reliability on multi-step questions** | Low. Prone to hallucinating math results. | High. Breaking it down drastically reduces errors. | High. Can reason through steps and verify facts. |
| **Transparency (can you see how it got the answer?)** | No. Only the final output is visible. | Yes. The entire thought process is printed. | Yes. Thoughts, Actions, and Observations are logged. |
| **Speed / cost** | Very fast / Lowest cost (1 API call). | Slower / Medium cost (more tokens generated). | Slowest / Highest cost (multiple API calls). |
| **Consistency across repeated runs** | Moderate. May flip-flop on math answers. | High. Step-by-step logic stabilizes the output. | High. Tool usage guarantees factual consistency. |

---

## 3.3 Self-consistency observation

I ran the `self_consistency.py` script on the first question ("If I borrow 3 books on Monday, return 1 on Wednesday...") 5 times with a high temperature (`0.8`). 

**Observation:**
Because the temperature was high, the wording of the intermediate steps varied wildly between runs. Some runs used algebraic variables (x = 3 - 1), while others used plain English sentences. However, because Chain-of-Thought forces the logic to be sound, the final calculated number ("3") was extremely consistent.

- **Majority Answer:** 3
- **Was it correct?** Yes (5 limit - (3 borrowed - 1 returned) = 3).
- **If temperature was 0:** The exact same wording and steps would be generated every single time, rendering self-consistency redundant but guaranteeing the most statistically probable path.

---

## 3.4 Suitability analysis

For this Library Book Tracking scenario, the **ReAct agent** is the most suitable approach. 

As shown in the comparison table, while CoT has high reasoning depth and reliability, it entirely lacks the ability to check the library database. A library system is useless if it cannot tell you whether a book is actually on the shelf. The ReAct agent combines the step-by-step math reasoning of CoT (to calculate return dates and borrowing limits) with the crucial ability to trigger the `check_book_availability` tool, making it the only approach capable of handling the full scope of user queries in this scenario.

---

## 3.5 Conclusion

Choosing the right approach depends entirely on the problem domain to optimize for cost, speed, and capability:

1. **Direct Prompting** is the most appropriate choice for simple text transformations (summarization, translation) or answering general knowledge questions. It is fast, cheap, and requires no complex orchestration.
2. **Chain-of-Thought** is the best choice for closed-domain math, logic puzzles, coding algorithms, and complex reasoning where all the necessary facts are already present in the prompt. It provides high accuracy without the latency and cost of a full agent loop.
3. **ReAct Agents** are the only appropriate choice when a task requires interacting with the outside world—such as querying a private database, browsing the web, or triggering actions (like sending an email). They are slower and more expensive, but they bridge the gap between static LLM knowledge and dynamic real-world execution.
