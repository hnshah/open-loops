# Eval rubric

Use binary invariants first, then a small number of judgment dimensions.

## Per-case invariants

### Obligation classification

Pass when the expected open anchors are surfaced and expected suppressed anchors are not promoted.

### Completion detection

Pass when later evidence that closes, cancels, delegates, supersedes, or obsoletes an obligation prevents the old loop from being surfaced.

### Ownership

Pass when `I owe`, `Waiting on`, and other states reflect the current owner after later evidence.

### Duplicate collapse

Pass when multiple references to one real-world obligation become one surfaced loop.

### Timing

Pass when future obligations are not surfaced too early and overdue or imminent obligations are not surfaced too late.

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

### Correction count

How many user corrections are needed before the brief becomes useful?

## No metric theater

Do not publish a precision number from synthetic fixtures as if it represents real inbox performance.

A public quality claim should state the host, model, source mix, evaluation set, and grading method.
