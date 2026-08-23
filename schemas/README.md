# Schemas

These JSON Schemas are optional integration contracts for runners, adapters, persistence, and eval tooling.

They are not required for an agent to use the skill directly.

- `source-event.schema.json` — normalized evidence event
- `open-loop.schema.json` — structured surfaced loop
- `ledger-record.schema.json` — optional recurring-state record
- `feedback.schema.json` — local correction record
- `prediction.schema.json` — structured benchmark prediction

The schemas deliberately avoid credentials, raw private storage conventions, and vendor-specific tool names.
