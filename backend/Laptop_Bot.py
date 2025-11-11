import os
import re
import json
from dotenv import load_dotenv
import google.generativeai as genai
from tabulate import tabulate
from questionnaire import QUESTIONNAIRE, ask_questionnaire

dotenv_path = os.path.join(os.path.dirname(__file__), "keys.env")
load_dotenv(dotenv_path)

# --- First Gemini Bot ---
API_KEY = os.getenv("API_KEY_FIRST")
if not API_KEY:
    raise ValueError("API_KEY_FIRST not found in keys.env")

genai.configure(api_key=API_KEY)
# model = genai.GenerativeModel("gemini-2.5-pro")
model = genai.GenerativeModel("gemini-2.5-flash-lite")

# --- Second Gemini Bot ---
API_KEY_SECOND = os.getenv("API_KEY_SECOND")
if not API_KEY_SECOND:
    raise ValueError("API_KEY_SECOND not found in keys.env")

# No separate client; we'll reconfigure before using it.
details_model_name = "gemini-2.5-flash-lite"
# details_model_name = "gemini-2.5-flash"
# details_model_name = "gemini-flash-latest"


# ------------------ PROMPTS ------------------
PROMPT = """You are a Laptop Recommendation Assistant.
DONOT give the response in table format, but in list format.
Return ONLY valid JSON (no prose, no markdown fences). Schema:
{
  "query": string,
  "currency": "INR",
  "items": [
    {
        "model": string,
        "price_inr": string,
        "why": string
    }
  ]
}

Compulsory Rules:
- Keep the search limited to lenovo laptops only and as for model, give me the series name only.
- If budget is mentioned, filter accordingly assuming that India is the location.
- If unsure about a spec or price, give us the predicted value for the model (donot include lenovo in model name).
- List top 5 relevant laptops.
- Model name strictly should be the first to be mentioned.
- In "price_inr", give approximate price in INR.
- In "why", briefly explain why this laptop matches the query in the simplest terms.
- In "why", the range of the words should be between 20 to 25 words.
"""

DETAILS_PROMPT = """You are a Laptop Specification Expert.
You will receive a list of laptop model names.
For each model, return detailed specs in JSON format with this schema:
{
  "model": string,
  "cpu": string,
  "ram": string,
  "storage": string,
  "gpu": string,
  "display": string,
  "battery": string,
}

Compulsory Rules:
- If unsure about a spec or price, give us the predicted value for the model.
"""

# ------------------ UTILS ------------------
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

# ------------------ MAIN BOT ------------------
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

    # items = data.get("items", [])
    # if items:
    #     fetch_laptop_details(items)

def fetch_laptop_details(items, return_json=False):
    models = [it.get("model") for it in items if it.get("model")]
    if not models:
        print("No laptop models found to fetch details for.")
        return
    
    print("\nFetching detailed specifications for each model...\n")
    query = DETAILS_PROMPT + "\nModels:\n" + "\n".join(models) + "\nJSON:"
    
    genai.configure(api_key=API_KEY_SECOND)
    details_model = genai.GenerativeModel(details_model_name)

    resp = details_model.generate_content(query)
    raw = resp.text or ""
    js = extract_json(raw).strip()
    try:
        details_data = json.loads(js)
    except Exception:
        print("Error parsing details response.\nRaw output:\n", raw)
        return
    
    if return_json:
        return details_data
    
    print("\nDetailed Laptop Specifications:")
    print(json.dumps(details_data, indent=2))

# ------------------ ENTRY ------------------
if __name__ == "__main__":
    print("Laptop Bot using Questionnaire\n")

    user_answers = ask_questionnaire(QUESTIONNAIRE["questions"])
    query_str = answers_to_query(user_answers)
    
    print("\nThanks! Searching for the best laptops based on your preferences...\n")
    run_query(query_str)
    
    print("\nYou can now modify the query or add more preferences (type 'q' to quit).")
    while True:
        try:
            user_input = input("> ").strip()
        except EOFError:
            break
        
        if not user_input or user_input.lower() in {"q", "quit", "exit"}:
            break
        
        updated_query = query_str + " ; " + user_input
        print("\nSearching with updated preferences...\n")
        run_query(updated_query)