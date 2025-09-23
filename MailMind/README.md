# EmailTriageAI

This project demonstrates two approaches for building an **AI-powered email triage and auto-reply system**.

## Modes

1) **Simple Mode**
   - One-shot LLM call per email sample.
   - Ideal for POCs and demos.

2) **Pro Mode**
   - Modular architecture: parser, classifier, templatizer, dispatcher, logger.
   - Suitable for production-level integration with Zapier/n8n, CRMs, Slack.

Each subfolder (`simple/` and `pro/`) contains its own README with setup & usage instructions.