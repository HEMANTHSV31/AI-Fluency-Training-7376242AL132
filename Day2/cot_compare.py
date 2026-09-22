

from config import client, MODEL, banner

QUESTIONS = [
    # 1. Multi-step arithmetic
    "If I borrow 3 books on Monday, return 1 on Wednesday, and the total borrowing limit is 5 books, how many more books can I borrow right now?",
    # 2. Logic / Ordering
    "John was born 5 years before the book 'AI Fundamentals' was published. If the book was published in 2015, how old will John be in 2030?",
    # 3. Requires Tool (External info)
    "Is the book 'AI Fundamentals' currently available in the library database?",
]

DIRECT_PROMPT = "You are a helpful assistant. Give only the final answer. Do not explain."

COT_PROMPT = ("You are a helpful assistant. Solve the problem step by step. "
              "Number each step and show the calculation in that step. "
              "After the steps, write the last line exactly as: Final Answer: <answer>")

def ask(system_prompt, question):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": system_prompt},
                  {"role": "user", "content": question}],
        temperature=0,
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    banner("CHAIN-OF-THOUGHT COMPARISON")
    for number, question in enumerate(QUESTIONS, start=1):
        print("=" * 72)
        print(f"QUESTION {number}: {question}\n")
        print("--- WITHOUT CoT ---")
        print(ask(DIRECT_PROMPT, question), "\n")
        print("--- WITH CoT ---")
        print(ask(COT_PROMPT, question), "\n")