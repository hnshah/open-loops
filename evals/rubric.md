# Eval rubric

Use binary invariants first, then a small number of judgment dimensions.

## Three output buckets

Human calibration uses three labels.

- **Main** — strong enough to compete for scarce space in the primary Open Loops list now.
- **Watching / Probably fine** — meaningful latent state worth preserving or showing outside the main list, but not important or actionable enough to compete for a primary slot now.
- **Suppress** — should not be retained as meaningful open-loop state for this scan.

This distinction matters. A candidate can be real enough to remember without being important enough to interrupt the user now.

`evals/human-reviewed.jsonl` records reviewed labels plus a `scope`.

- `universal` reviews calibrate the generic public skill.
- `personal` reviews apply only when the evaluated condition received the matching reviewer preference.

A personal judgment must not silently become generic benchmark gold.

## The scored object is the obligation

The benchmark scores one real-world obligation once.

An expected primary `anchor` and its non-conflicting `related` evidence IDs are acceptable evidence aliases for that obligation. If a related ID is itself a separately scored expected anchor, it remains separate.

Choosing a different accepted evidence alias is not an error. Surfacing multiple aliases for the same obligation is a duplicate.

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

Pass when each expected obligation receives the correct Main, Watching, or Suppress disposition regardless of which accepted evidence alias the model uses as its anchor.

### Completion detection

Pass when later evidence that closes, cancels, delegates, supersedes, obsoletes, or makes an action window useless prevents the old actionable loop from being surfaced.

### Ownership and state

Pass when the state reflects the current kind of unresolved work.

- `I owe` for an explicit user commitment or assignment
- `Response expected` for an unanswered inbound question/request
- `Waiting on` for another party's outstanding deliverable when no stronger blocker applies
- `Dependency` when consequential work is explicitly blocked on the prerequisite
- `Follow-up` only after the timing condition has arrived
- `Prepare` only with explicit preparation evidence

### Duplicate collapse

Pass when multiple references to one real-world obligation become one surfaced loop. Multiple accepted evidence aliases surfaced as separate loops count as a duplicate.

### Timing

Pass when future obligations are not promoted too early and overdue or imminent obligations are not surfaced too late. A concrete future obligation may belong in Watching before it becomes actionable.

A deadline-bound action whose only useful window has already passed may be obsolete rather than an active Main loop.

### Calendar discipline

Pass when routine calendar presence alone does not create inferred preparation work.

### Evidence discipline

Pass when the surfaced loop can point to an accepted evidence anchor and does not claim a broader resolution search than the available sources support.

A claimed completion in an inaccessible destination should preserve uncertainty rather than being asserted as definitely open or closed.

## Ranking-scenario invariants

### Disposition accuracy

Pass when each candidate is assigned to Main, Watching, or Suppress correctly for the calibration scope being tested.

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

How often does the skill correctly recognize that an apparent commitment has already closed or become obsolete?

### Duplicate rate

How often does one real-world obligation appear more than once?

### Miss rate

What meaningful loops did the user know about that the skill failed to find?

### Watching calibration

How often does the system correctly preserve lower-priority, ambiguous, future, or unverifiable state without promoting it into the primary list?

### Ranking agreement

How closely does the ordering of Main candidates match human judgment in mixed candidate sets?

### Correction count

How many user corrections are needed before the brief becomes useful?

## No metric theater

Do not publish a precision number from synthetic fixtures as if it represents real inbox performance.

A public quality claim should state the host, model, source mix, evaluation set, calibration scope, and grading method.
