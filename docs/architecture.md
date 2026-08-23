# Architecture

Open Loops is designed as a portable reasoning layer first.

It should work anywhere an agent can inspect at least one authorized work source. Tool names, APIs, connectors, MCP servers, browsers, and local runtimes are implementation details.

## Layers

```text
┌─────────────────────────────────────────────┐
│ User request / routine trigger              │
├─────────────────────────────────────────────┤
│ Open Loops skill                            │
│ ontology + completion + ranking + evidence  │
├─────────────────────────────────────────────┤
│ Capability adapter layer                    │
│ messages / threads / calendar / files / PM  │
├─────────────────────────────────────────────┤
│ Authorized host tools                       │
│ connector / MCP / browser / API / filesystem│
├─────────────────────────────────────────────┤
│ Work sources                                │
└─────────────────────────────────────────────┘
```

Optional persistence sits beside the reasoning layer and stores validated loop state or user-specific corrections. It is not required for a one-time scan.

## 1. Skill layer

The portable skill owns universal judgment.

- what qualifies as an open loop
- what does not qualify
- how to generate candidates
- how to search for closure
- how to determine ownership
- how to merge duplicates
- how to rank
- how to expose evidence and uncertainty
- where external-action approval is required

The skill should not contain credentials, vendor-specific private setup, or personal ranking rules.

## 2. Capability adapter layer

Adapters answer a small set of capability questions:

- Can I search messages?
- Can I read full thread history?
- Can I read upcoming calendar events?
- Can I read meeting notes?
- Can I search files?
- Can I inspect project or CRM-like records?

The agent uses whichever capabilities exist and records the actual resolution scope.

See [`source-adapter-contract.md`](source-adapter-contract.md) for an optional normalization contract.

## 3. State-reconstruction layer

This is the technical center.

For each candidate the agent identifies an expected resolution, searches later evidence, determines current ownership and state, and retains uncertainty when the observable world is incomplete.

See [`state-reconstruction.md`](state-reconstruction.md).

## 4. Ranking and presentation

The output is intentionally bounded.

Ranking considers obligation strength, open-state confidence, consequence, urgency, dependency, relationship significance supported by context, recency, preparation burden, and learned user preferences.

The agent does not expose a fake numerical score unless a future benchmark demonstrates that one improves quality.

## 5. Optional persistence

A recurring implementation may maintain a ledger with states such as:

- candidate
- open
- waiting
- watching
- prepared
- resolved
- dismissed
- obsolete

Persistence should improve continuity, not become a new source of stale truth. Every carried-forward loop should still be eligible for closure checks.

The reference schema is [`../schemas/ledger-record.schema.json`](../schemas/ledger-record.schema.json).

## External actions

Open Loops separates seeing work from acting on the outside world.

Read, analyze, gather, and prepare by default. Sending messages, publishing, scheduling, deleting, or mutating external records requires explicit approval.

That boundary lets the repository test judgment before it asks users to trust execution.
