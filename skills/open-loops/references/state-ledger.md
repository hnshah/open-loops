# State ledger

A ledger is optional. One-time scans do not require it.

Use persistence only when the runtime supports durable local state and the user wants continuity.

Suggested fields:

```text
id
summary
owner
counterparty
created
source
status
expected_resolution
due
importance
confidence
last_checked
resolution_evidence
```

Suggested states:

- candidate
- open
- waiting
- watching
- prepared
- resolved
- dismissed
- obsolete

Treat persisted state as a hypothesis cache. Recheck evidence before carrying an item forward indefinitely.

Never store credentials or full private source bodies merely to maintain the ledger. Prefer source references and minimal summaries when the host can re-read authorized evidence later.
