# ADR 0001 — State reconstruction, not task extraction

**Status:** Accepted

## Context

Action-item extraction identifies beginnings. Open Loops must decide whether an underlying obligation remains unresolved after later evidence.

## Decision

Every surfaced candidate must go through a forward closure search before promotion.

## Consequences

- completion detection is a first-class eval family
- cross-source evidence matters
- same-thread silence is not proof of openness
- source limitations must preserve uncertainty
- later valid evidence wins over older obligation text
