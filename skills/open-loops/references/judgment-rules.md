# Judgment rules

Use this reference to decide disposition first, then rank real open loops.

The public skill intentionally avoids a fake universal scoring formula.

## Decide disposition before rank

Every unresolved candidate should first land in one of three buckets.

### Main

Strong enough to compete for scarce space in the primary Open Loops list now.

### Watching / Probably fine

Meaningful state worth preserving, but not important, actionable, certain, or timely enough to compete for a primary slot now.

Watching is not synonymous with uncertainty. A clearly real obligation can still be Watching when it is not due yet or when stronger items deserve attention first.

### Suppress

Not meaningful enough to retain as open-loop state for the current scan.

## Timing gates disposition

A concrete future follow-up can be real without being actionable yet.

- If the stated date or condition has arrived, it may become `Follow-up` in Main.
- If the date or condition has not arrived, keep it in `Watching` rather than promoting it early.
- If an action was useful only before a past event and can no longer achieve its intended result, treat it as obsolete unless later evidence creates a new obligation.

Do not confuse "real" with "needs attention now."

## Calendar evidence

Calendar presence is supporting evidence, not automatic preparation work.

A routine meeting, weekly sync, or other ordinary event with no explicit prep request should not create a `Prepare` loop. Suppress it by default.

Use `Prepare` only when another source or the event itself explicitly states preparation requirements.

## Main eligibility is separate from display size

After disposition, rank only the Main candidates.

If the brief displays five items and a Main candidate ranks sixth, it remains Main. It is simply below the current display cutoff.

Do not demote rank-six or rank-seven Main candidates into Watching merely because the UI is intentionally short.

This distinction lets the system carry forward strong obligations as higher-ranked items close without confusing priority with state.

## Ranking dimensions

Consider

### Obligation strength

How explicit is the commitment or expectation?

### Open-state confidence

How strong is the evidence that the loop remains unresolved after the closure search?

### Consequence

What happens if this is forgotten?

### Urgency

Is there a deadline, upcoming meeting, or timing expectation?

### Dependency

Is another person, customer, deal, launch, shipment, or project blocked?

Treat the severity of the blocked outcome as part of consequence. Not every internal blocker deserves the same attention as a shipping or customer blocker.

### Relationship significance

Does the available context show that the counterparty or situation matters?

Do not infer importance from fame, title, or status without context.

### External expectation

A direct promise, question, or near-term obligation to an external counterparty can deserve scarce attention even when resolving it is easy.

This is a useful signal, not a universal law. User corrections should determine how heavily it matters for a particular person.

### Ownership

Distinguish work the user personally owes from work the user is merely waiting to receive.

Both can matter, but a direct user-owned obligation often creates a stronger reason to interrupt because the next move is under the user's control.

Treat this as a tendency to test, not a hard-coded universal preference.

### Recency

Recent obligations often matter more, but recency alone should not outrank consequence.

### Preparation burden

Items requiring work before a near-term event deserve earlier attention than easy replies when delay would create risk.

## Rank contextually, not mechanically

The dimensions above do not combine into one permanent total order.

When several Main candidates are close, compare the strongest contenders directly rather than pretending a fixed numeric score can settle every case.

A direct pairwise judgment can disagree with the order those same kinds of items received inside a larger candidate set. Preserve that tension.

Do not immediately turn one comparison into a universal rule such as "customer always beats internal" or "urgency always beats consequence."

Instead look for repeated evidence across:

- different wording
- reversed left/right presentation
- different surrounding candidate sets
- repeated real runs

Only promote a preference into a durable personal rule after it proves stable enough to be useful.

## Priority pattern

A useful mental model is

```text
priority is driven by importance × open-state confidence × urgency
```

Then apply context around consequence, dependency, relationship significance, ownership, external expectation, and explicit user preferences.

Treat this as a reasoning aid, not a numeric score.

## Suppression and demotion rules

Usually suppress or demote

- weak social niceties
- generic "let's catch up sometime" language
- low-consequence requests with no time pressure
- routine calendar events without explicit preparation evidence
- old items that likely became obsolete
- deadline-bound actions whose useful window has passed
- repeated automated reminders
- conversations that naturally concluded
- items already resolved elsewhere
- technically unfinished but trivial details that would crowd out meaningful work

Prefer Watching over suppression when preserving the state may plausibly matter later.

## Personal rules

User corrections may override the defaults.

Examples

- customers rank above internal asks
- recruiting candidates always matter
- social follow-ups rarely matter
- casual relationship language should stay visible in Watching
- a specific project should always rank highly
- introductions should always receive a response

Keep these as a separate personal layer. Do not rewrite universal rules based on one person's preference.
