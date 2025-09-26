from pathlib import Path
import sys
import json
from datetime import datetime


ROOT = Path(__file__).resolve().parents[1]
SAMPLES_DIR = ROOT / "samples"
OUTPUTS_DIR = ROOT / "outputs"
TEMPLATE_PATH = Path(__file__).resolve().parent / "prompt_template.txt"

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
    run_id = datetime.now().strftime("run_%d/%m/%Y_%H%:M%:S")
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

        out_record = {
            "input": record,
            "prompt": filled,
            "meta": {
                "run_id": run_id,
                "schema_version": "v1",
                "timestamp": datetime.now().isoformat(timespec="seconds")
            }
        }

        f.write(json.dumps(out_record, ensure_ascii=False) + "\n")
        print(f"[{sid}] prompt ready (len={len(filled)} chars)")
    
    print(f"\nAll prompts written to {log_path}")
    return 0

    








if __name__ == "__main__":
    sys.exit(main())
    # Read the first sample JSON