# Eval rubric

Use binary invariants first, then a small number of judgment dimensions.

## Three output buckets

Human calibration uses three labels.

- **Main** — deserves scarce space in the primary Open Loops list now.
- **Watching / Probably fine** — meaningful latent state worth preserving or showing outside the main list, but not strong or actionable enough to consume a primary slot.
- **Suppress** — should not be retained as meaningful open-loop state for this scan.

This distinction matters. A candidate can be real enough to remember without being important enough to interrupt the user now.

`evals/human-reviewed.jsonl` records reviewed labels. When a reviewed label differs from the original synthetic fixture, treat the human-reviewed judgment as the current gold interpretation for product calibration.

## Per-case invariants

### Obligation classification

Pass when the expected main-list anchors are surfaced, watching candidates are kept out of the main list, and suppressed anchors are not promoted.

### Completion detection

Pass when later evidence that closes, cancels, delegates, supersedes, or obsoletes an obligation prevents the old loop from being surfaced.

### Ownership

Pass when `I owe`, `Waiting on`, and other states reflect the current owner after later evidence.

### Duplicate collapse

Pass when multiple references to one real-world obligation become one surfaced loop.

### Timing

Pass when future obligations are not promoted too early and overdue or imminent obligations are not surfaced too late. A concrete future obligation may still belong in Watching before it becomes actionable.

### Evidence discipline

Pass when the surfaced loop can point to the obligation anchor and does not claim a broader resolution search than the available sources support.

## Real-scan quality dimensions

Score 0, 1, or 2.

### Importance

0 - trivial or distracting

1 - real but not clearly important

2 - the user would care if it were forgotten

### Open-state confidence

0 - weak or contradicted

1 - plausible but source scope is incomplete

2 - strong obligation plus strong closure search

### Next-step usefulness

0 - wrong or generic

1 - reasonable

2 - specific and immediately useful

## Product-level metrics

### Precision@5

Of the five highest-ranked surfaced loops, how many are real open loops?

### Importance@5

Of the five highest-ranked surfaced loops, how many does the user actually care about?

### Completion detection accuracy

How often does the skill correctly recognize that an apparent commitment has already closed?

### Duplicate rate

How often does one real-world obligation appear more than once?

### Miss rate

What meaningful loops did the user know about that the skill failed to find?

### Watching calibration

How often does the system correctly preserve ambiguous or future state without promoting it into the primary list?

### Correction count

How many user corrections are needed before the brief becomes useful?

## No metric theater

Do not publish a precision number from synthetic fixtures as if it represents real inbox performance.

A public quality claim should state the host, model, source mix, evaluation set, and grading method.
