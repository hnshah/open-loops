# Open Loops documentation

The repository has three layers.

1. **The skill** — the portable operating procedure an agent loads.
2. **The proof system** — evals, schemas, examples, and validation.
3. **The public method** — the reasoning, architecture, test protocol, and design decisions around the skill.

## Start here

| You are | Read |
| --- | --- |
| Trying Open Loops | [`../README.md`](../README.md), then [`compatibility.md`](compatibility.md) |
| Evaluating the idea | [`why-open-loops.md`](why-open-loops.md), then [`state-reconstruction.md`](state-reconstruction.md) |
| Building a host adapter | [`architecture.md`](architecture.md), then [`source-adapter-contract.md`](source-adapter-contract.md) |
| Running tests | [`benchmark-methodology.md`](benchmark-methodology.md), then [`testing-protocol.md`](testing-protocol.md) |
| Turning it into a routine | [`routine-mode.md`](routine-mode.md) |
| Contributing | [`../CONTRIBUTING.md`](../CONTRIBUTING.md), [`../evals/README.md`](../evals/README.md) |
| Understanding design choices | [`adr/`](adr/) |

## Core docs

- [`why-open-loops.md`](why-open-loops.md) — why unfinished work is a state problem rather than a task-extraction problem
- [`state-reconstruction.md`](state-reconstruction.md) — the technical reasoning model for beginnings, endings, ownership, and uncertainty
- [`architecture.md`](architecture.md) — portable layers and boundaries
- [`source-adapter-contract.md`](source-adapter-contract.md) — optional normalized event and capability contract for host implementers
- [`benchmark-methodology.md`](benchmark-methodology.md) — what to measure and how not to fool yourself
- [`testing-protocol.md`](testing-protocol.md) — controlled tests, dogfood, and outside-user protocol
- [`routine-mode.md`](routine-mode.md) — continuity, ledger states, and recurring scans
- [`compatibility.md`](compatibility.md) — install surfaces and portability expectations
- [`agent-job-framework.md`](agent-job-framework.md) — why Open Loops is a useful example of a durable agent job
- [`faq.md`](faq.md) — practical questions
- [`roadmap.md`](roadmap.md) — learning order rather than feature theater

## Architecture decisions

ADRs record the product laws that should not drift casually.

- [`adr/0001-state-reconstruction-not-task-extraction.md`](adr/0001-state-reconstruction-not-task-extraction.md)
- [`adr/0002-precision-over-exhaustiveness.md`](adr/0002-precision-over-exhaustiveness.md)
- [`adr/0003-portable-skill-core.md`](adr/0003-portable-skill-core.md)
- [`adr/0004-read-and-prepare-by-default.md`](adr/0004-read-and-prepare-by-default.md)
- [`adr/0005-synthetic-public-benchmark.md`](adr/0005-synthetic-public-benchmark.md)
