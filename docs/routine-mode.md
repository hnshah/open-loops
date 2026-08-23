# Routine mode

Routine mode is an advanced operating mode, not the starting point.

Use it only after several one-time scans have demonstrated acceptable precision for the user's source scope.

## Morning Open Loops

A useful default recurring job is:

```text
Review activity since the previous successful run.
Carry forward unresolved high-confidence loops.
Check whether carried-forward loops have closed.
Add newly discovered loops.
Return no more than five things that deserve attention today.
Do not send, edit, schedule, publish, or delete anything.
```

The skill includes a reusable version at [`../skills/open-loops/assets/routine-instructions.md`](../skills/open-loops/assets/routine-instructions.md).

## Continuity matters

A routine should not recompute the universe from scratch every morning.

It should maintain lightweight continuity while still rechecking old assumptions.

A carried-forward loop can become:

- resolved
- dismissed
- obsolete
- rescheduled
- delegated
- still open
- still waiting

## Suggested ledger

The optional ledger schema lives at [`../schemas/ledger-record.schema.json`](../schemas/ledger-record.schema.json).

Core fields:

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

```text
candidate
open
waiting
watching
prepared
resolved
dismissed
obsolete
```

## Do not let persistence become stale truth

Persistence is a hypothesis cache, not an oracle.

On each run:

1. recheck high-value carried-forward loops for closure
2. update timing and ownership
3. remove duplicates
4. preserve resolution evidence
5. expire or downgrade items whose context no longer supports attention

## Frequency

There is no universal correct cadence.

Daily is a reasonable experiment for communication-heavy work. Weekly may be better for lower-volume environments. Twice-daily scans may be useful for high-tempo roles but raise the cost of false positives.

Frequency should be earned by signal quality.

## External actions

Routine mode does not change the approval boundary.

It may prepare drafts, locate files, assemble research, or identify availability. It should not send, publish, schedule, delete, or mutate external records without explicit approval.
