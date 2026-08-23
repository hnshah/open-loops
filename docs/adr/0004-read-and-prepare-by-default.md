# ADR 0004 — Read and prepare by default

**Status:** Accepted

## Context

The first product risk is bad judgment. Allowing surprise external actions would compound that risk and make failures harder to inspect.

## Decision

The default action ladder stops at finding, explaining, and preparing. Sending, publishing, scheduling, deleting, or mutating external records requires explicit approval.

## Consequences

- the system can still be useful before autonomous execution
- trust can increase gradually
- routines do not weaken the approval boundary
- tests can isolate judgment quality from side-effect safety
