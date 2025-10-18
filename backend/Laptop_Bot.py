import os
import sys
import re
import json
from dotenv import load_dotenv
import google.generativeai as genai
from tabulate import tabulate
from questionnaire import QUESTIONNAIRE, ask_questionnaire


# Always load keys.env from the same directory as this script
dotenv_path = os.path.join(os.path.dirname(__file__), "keys.env")
load_dotenv(dotenv_path)

# Get API key
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY not found in keys.env")

# Configure Gemini
genai.configure(api_key=API_KEY)
# Fast & cheap
model = genai.GenerativeModel("gemini-2.5-flash")

# OR, more powerful
# model = genai.GenerativeModel("gemini-2.5-pro")

# OR, always track latest
# model = genai.GenerativeModel("gemini-pro-latest")


PROMPT = """You are a Laptop Recommendation Assistant.
DONOT give the response in table format, but in list format.
Return ONLY valid JSON (no prose, no markdown fences). Schema:
{
  "query": string,
  "currency": "INR",
  "items": [
    {
      "model": string,
      "cpu": string,
      "ram": string,
      "storage": string,
      "gpu": string,
      "display": string,
      "battery": string,
      "price_inr": string,
      "why": string
    }
  ],
  "summary": {
    "best_overall": string,
    "notes": string
  }
}

Rules:
- If budget/location is mentioned, filter accordingly (assume India if unspecified).
- If unsure about a spec or price, write "Unknown".
- List atleast 5 relevant laptops.
- Model name strictly should be the first to be mentioned.
"""

def build_prompt(user_query: str) -> str:
    return PROMPT + f'\nUser Query: "{user_query}"\nJSON:'

def extract_json(txt: str):
    m = re.search(r'(\{.*\}|\[.*\])', txt, re.DOTALL)
    return m.group(1) if m else txt

def answers_to_query(answers: dict) -> str:
    query_parts = []
    for k, v in answers.items():
        if isinstance(v, list):
            query_parts.append(f"{k}: {', '.join(v)}")
        else:
            query_parts.append(f"{k}: {v}")
    return " ; ".join(query_parts)

# def run_query(q: str):
#     resp = model.generate_content(build_prompt(q))
#     raw = resp.text or ""
#     js = extract_json(raw).strip()
#     try:
#         data = json.loads(js)
#     except Exception:
#         print("Raw model output:\n", raw)
#         return
#     items = data.get("items", [])
#     if not items:
#         print("No items returned.\nRaw:", data)
#         return
#     table = []
#     for it in items:
#         table.append([
#             it.get("model", ""),
#             it.get("cpu", ""),
#             it.get("ram", ""),
#             it.get("storage", ""),
#             it.get("gpu", ""),
#             it.get("display", ""),
#             it.get("battery", ""),
#             it.get("price_inr", ""),
#             it.get("why", "")
#         ])
#     headers = ["Model", "CPU", "RAM", "Storage", "GPU", "Display", "Battery", "Price", "Why"]
#     print(tabulate(table, headers=headers, tablefmt="github"))
#     summary = data.get("summary", {})
#     if summary:
#         print("\nBest Overall:", summary.get("best_overall", ""))
#         print("Notes:", summary.get("notes", ""))

# def run_query(q: str):
#     resp = model.generate_content(build_prompt(q))
#     raw = resp.text or ""
#     js = extract_json(raw).strip()
#     try:
#         data = json.loads(js)
#     except Exception:
#         print("Raw model output:\n", raw)
#         return
    
#     # Pretty-print JSON output
#     print("\nLaptop Recommendations:")
#     print(json.dumps(data, indent=2))

def run_query(q: str, return_json=False):
    resp = model.generate_content(build_prompt(q))
    raw = resp.text or ""
    js = extract_json(raw).strip()
    try:
        data = json.loads(js)
    except Exception:
        return {"error": "Failed to parse model output", "raw": raw}
    
    if return_json:
        return data
    print("\nLaptop Recommendations:")
    print(json.dumps(data, indent=2))


# if __name__ == "__main__":
#     if len(sys.argv) > 1:
#         run_query(" ".join(sys.argv[1:]))
#     else:
#         print("Laptop Bot ready. Type your query (or 'q' to quit).")
#         while True:
#             try:
#                 q = input("> ").strip()
#             except EOFError:
#                 break
#             if not q or q.lower() in {"q", "Q", "quit", "Quit", "exit", "Exit"}:
#                 break
#             run_query(q)

# if __name__ == "__main__":
#     print("Laptop Bot using Questionnaire\n")
#     user_answers = ask_questionnaire(QUESTIONNAIRE["questions"])
#     query_str = answers_to_query(user_answers)
#     print("\nThanks! Searching for the best laptops based on your preferences...\n")
#     run_query(query_str)

if __name__ == "__main__":
    print("Laptop Bot using Questionnaire\n")

    # Step 1: Run questionnaire once
    user_answers = ask_questionnaire(QUESTIONNAIRE["questions"])
    query_str = answers_to_query(user_answers)
    
    # Step 2: Show processing message
    print("\nThanks! Searching for the best laptops based on your preferences...\n")
    run_query(query_str)
    
    # Step 3: Allow user to modify or refine query in a loop
    print("\nYou can now modify the query or add more preferences (type 'q' to quit).")
    while True:
        try:
            user_input = input("> ").strip()
        except EOFError:
            break
        
        if not user_input or user_input.lower() in {"q", "quit", "exit"}:
            break
        
        # Append new input to original query or replace completely
        updated_query = query_str + " ; " + user_input
        print("\nSearching with updated preferences...\n")
        run_query(updated_query)