# MailMind – Simple Mode

This project demonstrates a **basic AI-powered email triage & auto-reply system** using OpenAI’s API.  
It processes sample emails in JSON, generates structured outputs (category, priority, action, draft reply), and logs everything in `.jsonl` format.

---

## 📂 Project Structure

MailMind/
└── simple/
├── samples/              # Example input emails in JSON
├── outputs/              # LLM responses written as JSONL logs
├── src/
│   ├── runner.py         # Main script (loop + LLM call)
│   └── prompt_template.txt # Template prompt for the LLM
└── README.md             # You are here

---

## ⚙️ Setup

1. **Clone repository & move into folder**
   git clone <your_repo_url>
   cd MailMind/simple


2.	**Create virtual environment**
    python3.12 -m venv mailvenv
    source mailvenv/bin/activate


3.	**Install dependencies**
    pip install python-dotenv openai


4.	**Set environment variables**
    Create a .env file inside MailMind/:
        OPENAI_API_KEY=your_api_key_here


## ▶️ Running

python src/runner.py

*Expected console output:*

Found 6 sample(s) in .../samples
 - 001_sales.json
 - 002_complaint.json
 ...
Template found ✅

=== Prompt preview (36 chars) ===
You are an AI email triage assistant...
===== This is the end =====

[001_sales] category=sales priority=high action=reply conf=0.9
[002_complaint] category=complaint priority=high action=reply conf=0.9
...
All prompts written to .../outputs/run_YYYY-MM-DD_HH-MM-SS.jsonl

# 📄 Output Format

{
  "input": {
    "id": "001_sales",
    "subject": "Inquiry about product X",
    "body": "Hello, I'm interested in..."
  },
  "prompt": "...full prompt text...",
  "output": {
    "schema_version": "v1",
    "id": "001_sales",
    "category": "sales",
    "priority": "high",
    "action": "reply",
    "confidence": 0.9,
    "key_points": ["interested in product X"],
    "draft_reply": "Hello, thank you for your interest in..."
  },
  "meta": {
    "run_id": "run_2025-09-28_19-36-57",
    "timestamp": "2025-09-28T19:36:57",
    "schema_version": "v1"
  }
}


# Feel free to play with more categories, connected it with an email, create branch here and play together. 