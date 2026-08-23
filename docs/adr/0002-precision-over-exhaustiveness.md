# ADR 0002 — Precision over exhaustiveness

**Status:** Accepted

## Context

An exhaustive inferred task list creates more cognitive load and quickly teaches users to ignore the system.

## Decision

Default to 3–5 high-confidence important loops and cap normal output at 10 unless the user explicitly asks for more.

## Consequences

- weak candidates are suppressed or placed in `Watching` / `Probably fine`
- importance is part of correctness
- an empty main list is valid
- Precision@5 and Importance@5 matter more than extraction count
