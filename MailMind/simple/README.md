# EmailTriageAI — Simple Mode

**Goal:** Minimal complexity. For each sample (in `samples/`), a **single** LLM call produces:
- `category`, `priority`, `action`
- `key_points`
- `draft_reply` (ready-to-send text)
- `confidence`

## Folders
- `samples/` — input test files (e.g. `001_sales.json`).
- `src/` — the runner code (to be added).
- `outputs/` — logs/results of each run (JSONL).

## Steps (when code is added)
1. Configure `.env` (API key).
2. Run `python src/runner.py` — processes all samples.
3. Review results in the console & in `outputs/`.

## Notes
- Gmail API is not used here, only local samples.
- Optionally, a webhook dispatcher to Zapier/n8n can be added for demo flows.