# questionnaire.py
QUESTIONNAIRE = {
  "questions": [
    {
      "id": "use_case",
      "question": "What will you mainly use the laptop for?",
      "type": "single-choice",
      "options": [
        "Internet, movies, and office work",
        "College or school work, coding, and studying",
        "Gaming or watching high-quality videos",
        "Designing, video editing, or creative work",
        "Other"
      ]
    },
    {
      "id": "budget",
      "question": "How much do you want to spend?",
      "type": "single-choice",
      "options": [
        "Low (₹35K–50K)",
        "Medium (₹55K–75K)",
        "High (₹80K–1.2L)",
        "Premium (₹1.3L+)",
        "Not sure"
      ]
    },
    {
      "id": "processor",
      "question": "Processor / Speed preference",
      "type": "single-choice",
      "options": [
        "Basic (Intel i3 / Ryzen 3)",
        "Balanced (Intel i5 / Ryzen 5)",
        "Fast (Intel i7 / Ryzen 7)"
      ]
    },
    {
      "id": "ram",
      "question": "RAM / Memory preference",
      "type": "single-choice",
      "options": ["8GB", "16GB", "32GB+"]
    },
    {
      "id": "storage",
      "question": "Storage preference",
      "type": "single-choice",
      "options": ["SSD", "SSD + Extra HDD"]
    },
    {
      "id": "gpu",
      "question": "Graphics preference",
      "type": "single-choice",
      "options": ["Normal", "Dedicated"]
    },
    {
      "id": "screen_size",
      "question": "Screen size preference",
      "type": "single-choice",
      "options": ["Small (14\")", "Medium (15–16\")", "Other"]
    },
    {
      "id": "screen_quality",
      "question": "Screen quality / resolution",
      "type": "single-choice",
      "options": ["Normal (Full HD)", "High quality (2K / 4K)"]
    },
    {
      "id": "weight",
      "question": "Laptop weight preference",
      "type": "single-choice",
      "options": ["Light (<1.6 kg)", "Medium (1.6–2.5 kg)", "Heavy (>2.5 kg)"]
    },
    {
      "id": "battery",
      "question": "Battery life preference",
      "type": "single-choice",
      "options": ["5–6 hours minimum", "6–10 hours preferred", "Not important"]
    },
    {
      "id": "aesthetics",
      "question": "Do you care about how it looks?",
      "type": "single-choice",
      "options": ["Yes, stylish laptop", "Doesn’t matter"]
    },
    {
      "id": "ports",
      "question": "Ports & connectivity (USB, HDMI, headphones, etc.)",
      "type": "single-choice",
      "options": ["Need many ports", "A few ports are enough", "Don’t care"]
    },
    {
      "id": "security",
      "question": "Security features",
      "type": "multi-choice",
      "options": ["Webcam 1080p", "Fingerprint or face login", "Don’t care"]
    },
    {
      "id": "priorities",
      "question": "What matters most to you?",
      "type": "multi-choice",
      "options": [
        "Speed / Performance",
        "Portability / Light weight",
        "Battery life",
        "Screen quality",
        "Keyboard comfort / typing",
        "Price / Value for money"
      ]
    },
    {
      "id": "brand",
      "question": "Do you have any brand preference?",
      "type": "multi-choice",
      "options": ["Dell", "HP", "Lenovo", "ASUS", "Acer", "Apple", "No preference"]
    },
    {
      "id": "other_requirements",
      "question": "Anything else you want? (Touchscreen, stylus, foldable, color, etc.)",
      "type": "text"
    }
  ]
}

def ask_questionnaire(questions):
    answers = {}
    for q in questions:
        print("\n" + q["question"])
        if q["type"] in ["single-choice", "multi-choice"]:
            for i, option in enumerate(q["options"], 1):
                print(f"{i}. {option}")
        if q["type"] == "single-choice":
            while True:
                try:
                    choice = int(input("Enter choice number: ").strip())
                    if 1 <= choice <= len(q["options"]):
                        answers[q["id"]] = q["options"][choice - 1]
                        break
                    else:
                        print("Invalid choice. Try again.")
                except ValueError:
                    print("Enter a number.")
        elif q["type"] == "multi-choice":
            print("Enter numbers separated by comma (e.g., 1,3):")
            while True:
                inp = input("Your choice(s): ").strip()
                try:
                    indices = [int(x) for x in inp.split(",") if x.strip().isdigit()]
                    valid_indices = [i for i in indices if 1 <= i <= len(q["options"])]
                    if valid_indices:
                        answers[q["id"]] = [q["options"][i - 1] for i in valid_indices]
                        break
                    else:
                        print("Invalid choice(s). Try again.")
                except ValueError:
                    print("Enter numbers separated by commas.")
        elif q["type"] == "text":
            ans = input("Your answer: ").strip()
            answers[q["id"]] = ans
    return answers
