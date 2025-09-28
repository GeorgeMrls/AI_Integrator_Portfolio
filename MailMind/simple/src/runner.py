from pathlib import Path
import sys
import json
from datetime import datetime
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("Missing OPENAI_API_KEY in your .env")
    sys.exit(1)

client = OpenAI(api_key=OPENAI_API_KEY)
MODEL = "gpt-4o-mini"

ROOT = Path(__file__).resolve().parents[1]
SAMPLES_DIR = ROOT / "samples"
OUTPUTS_DIR = ROOT / "outputs"
TEMPLATE_PATH = Path(__file__).resolve().parent / "prompt_template.txt"

def call_llm(prompt_text: str) -> dict:
    """Sends the filled prompt to the LLM and expects a strict JSON object back.
    Returns a Python dict (parsed), or a safe fallback dict on error."""

    try:
        resp = client.chat.completions.create(
            model = MODEL,
            messages=[
                {"role": "system", "content": "You are a careful JSON-only email triage assistant."},
                {"role": "user", "content": prompt_text},
            ],
            temperature=0.2,
            response_format={"type":"json_object"},
        )
        content = resp.choices[0].message.content  # JSON string
        return json.loads(content)  # dict
    except Exception as e:
        # Safe fallback if model returns bad JSON or any error occurs
        return {
            "schema_version": "v1",
            "id": "unknown",
            "category": "other",
            "priority": "medium",
            "action": "route",
            "confidence": 0.0,
            "key_points": [],
            "draft_reply": "",
            "error": f"{type(e).__name__}: {e}"
        }


def main() -> int:
    # Ensure folders exist
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    # List sample
    sample_files = sorted(SAMPLES_DIR.glob("*.json"))
    print(f"Found {len(sample_files)} sample(s) in {SAMPLES_DIR}")
    for p in sample_files:
        print(" -", p.name)

    # Quick template presence check
    if not TEMPLATE_PATH.exists():
        print(f"Template not found at: {TEMPLATE_PATH}")
        return 1
    print ("Template found ✅")

    if not sample_files:
        print("OMG, 😱 no files in here.")
        return 1
    first_sample = sample_files[0]
    try: data = json.loads(first_sample.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"Failed to read JSON from {first_sample.name}: {e}")
        return 1
    
    sample_id = data.get("id", "unknown")
    subject = data.get("subject", "")
    body = data.get("body", "")

    #Load the prompt template as text
    template_text = TEMPLATE_PATH.read_text(encoding="utf-8")

    #Fill placeholders {{id}}, {{subject}}, {{body}}
    filled_prompt = (
        template_text
        .replace("{{id}}", str(sample_id))
        .replace("{{subject}}", subject)
        .replace("{{body}}", body)
    )

    # Print a tiny preview (my age - 36 characters)

    preview_len = 36
    preview = filled_prompt[:preview_len].replace("\n", " ")
    print(f"\n=== Prompt preview ({preview_len} chars) ===")
    print(preview + ("..." if len(filled_prompt) > preview_len else ""))
    print("===== This is the end =====\n")
    
    # loop all samples and write JSONL Log
    run_id = datetime.now().strftime("run_%Y-%m-%d_%H-%M-%S")
    log_path = OUTPUTS_DIR / f"{run_id}.jsonl"

    with log_path.open("w", encoding="utf-8") as f:
        for sample_path in sample_files:
            try:
                record = json.loads(sample_path.read_text(encoding="utf-8"))
            except Exception as e:
                print(f"[{sample_path.name}] JSON read error: {e}")
                continue

            sid = record.get("id", sample_path.stem)
            subj = record.get("subject", "")
            bod = record.get("body", "")

            # reuse the same template_text you loaded earlier
            filled = (
                template_text
                .replace("{{id}}", str(sid))
                .replace("{{subject}}", subj)
                .replace("{{body}}", bod)
            )

            llm_output = call_llm(filled)

            out_record = {
                "input": record,
                "prompt": filled,
                "output": llm_output,
                "meta": {
                    "run_id": run_id,
                    "schema_version": "v1",
                    "timestamp": datetime.now().isoformat(timespec="seconds")
                }
            }

            f.write(json.dumps(out_record, ensure_ascii=False) + "\n")
            print(f"[{sid}] prompt ready (len={len(filled)} chars)")
        
            cat = llm_output.get("category", "other")
            pri = llm_output.get("priority", "medium")
            act = llm_output.get("action", "route")
            conf = llm_output.get("confidence", 0.0)
            print(f"[{sid}] category={cat} priority={pri} action={act} conf={conf}")



    print(f"\nAll prompts written to {log_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())