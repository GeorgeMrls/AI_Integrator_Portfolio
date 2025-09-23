# EmailTriageAI — Pro Mode

**Goal:** Production-style modular architecture with dedicated stages:
- `parser` → text cleaning/normalization
- `classifier` → LLM structured output (category, priority, action, key_points)
- `templatizer` → ready-made replies filled into approved templates
- `dispatcher` → send via Gmail API or webhook to Zapier/n8n/CRMs/Slack
- `logger` → full audit trail (raw → parsed → classified → dispatched)

## Folders
- `config/` → settings (YAML) & `templates/` for reply texts.
- `src/` → modules & main orchestrator.
- `tests/samples/` → example inputs for evaluation.
- `outputs/` → logs, runs, metrics.

## Installation (when code is added)
1. Create `.env` (LLM key, webhook secrets).
2. Fill in `config/` (policies, routing rules).
3. Run `python -m src.main`.

## Extensions
- Zapier/n8n webhooks (HMAC, idempotency, retries).
- Metrics & evaluation per stage.
- A/B testing templates, localization, GDPR data minimization.