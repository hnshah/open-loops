# Eval rubric

Use binary invariants first, then a small number of judgment dimensions.

## Three output buckets

Human calibration uses three labels.

- **Main** — strong enough to compete for scarce space in the primary Open Loops list now.
- **Watching / Probably fine** — meaningful latent state worth preserving or showing outside the main list, but not important or actionable enough to compete for a primary slot now.
- **Suppress** — should not be retained as meaningful open-loop state for this scan.

This distinction matters. A candidate can be real enough to remember without being important enough to interrupt the user now.

`evals/human-reviewed.jsonl` records reviewed labels. When a reviewed label differs from the original synthetic fixture, treat the human-reviewed judgment as the current gold interpretation for product calibration.

## Main eligibility is not the display cutoff

Classify disposition before applying the list-size limit.

A candidate can be **Main** and rank sixth even when the default brief displays only five items. That candidate remains main-eligible and should surface if the user expands the list or higher-ranked items close.

Do **not** relabel a main-eligible item as Watching merely because it falls below the current top-k display cutoff.

The evaluation therefore separates:

1. **disposition** — Main, Watching, or Suppress
2. **ranking** — order among Main candidates
3. **display** — the first `k` Main candidates shown in the current brief

`evals/ranking-scenarios.jsonl` contains multi-candidate ranking sets where these distinctions can be tested directly.

## Per-case invariants

### Obligation classification

Pass when the expected main-list anchors are classified as Main, watching candidates are kept out of the main list, and suppressed anchors are not promoted.

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

## Ranking-scenario invariants

### Disposition accuracy

Pass when each candidate is assigned to Main, Watching, or Suppress correctly.

### Top-k selection

Pass when the displayed list is the first `k` items from the gold Main ranking.

### Pairwise ordering

For every pair of gold Main candidates, credit the system when the higher-ranked candidate appears above the lower-ranked candidate.

This is more informative than pretending importance has a universal numeric score.

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

How often does the system correctly preserve lower-priority, ambiguous, or future state without promoting it into the primary list?

### Ranking agreement

How closely does the ordering of Main candidates match human judgment in mixed candidate sets?

### Correction count

How many user corrections are needed before the brief becomes useful?

## No metric theater

Do not publish a precision number from synthetic fixtures as if it represents real inbox performance.

A public quality claim should state the host, model, source mix, evaluation set, and grading method.
