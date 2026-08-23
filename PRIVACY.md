# Privacy

Open Loops is designed to work over sensitive work communication, so the default data posture is intentionally simple.

## No telemetry

This repository contains no analytics, tracking, remote logging, or data collection code.

The skill itself does not transmit source content anywhere.

Any data access comes from the agent runtime and the work sources the user has already authorized. Those systems have their own privacy and retention policies.

## Local learning

If the user chooses to persist feedback locally, store generalized correction rules rather than raw message content whenever possible.

Suggested private path

```text
.open-loops/feedback.jsonl
```

Do not commit that file.

## Public contributions

Never open an issue or PR with raw private work data.

Sanitize failures into synthetic cases before contributing them.

## Source minimization

The skill should quote or expose only the evidence needed to justify a surfaced loop. It should not dump entire private threads into the result.
