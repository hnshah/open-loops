# Benchmark methodology

Open Loops is useful only if it is trusted.

The benchmark therefore evaluates state reconstruction and judgment, not raw extraction volume.

## Benchmark question

> Given source activity over time, does a meaningful obligation remain unresolved as of the evaluation time, and does it deserve scarce attention now?

A case can require the model to identify an obligation, find later closure, infer ownership, merge duplicates, respect timing, choose a disposition, and rank importance.

## Public benchmark units

The public suite has three fixture types.

### Trigger fixtures

Tests whether the skill should activate for a request.

Positive examples cover the owned job. Near-neighbor negatives cover adjacent jobs such as generic task extraction, project planning, inbox cleanup, and unrelated requests.

### State-reconstruction cases

Synthetic timelines with one or more source events and expected open/suppressed outcomes.

Cases should be small enough to understand by inspection and difficult enough that naive extraction fails.

### Ranking scenarios

Mixed sets of already-understood candidate cases used to test judgment under a constrained attention budget.

A ranking scenario separates three decisions:

1. **Disposition** — Main, Watching, or Suppress.
2. **Ranking** — order among Main candidates.
3. **Display** — which Main candidates fit inside the current top-k limit.

This matters because a rank-six Main candidate is not the same thing as a Watching candidate. The former is strong enough to compete for the primary list but happens to sit below the current cutoff. The latter is intentionally held outside the primary competition for now.

`evals/ranking-scenarios.jsonl` stores human-reviewed mixed candidate sets. `evals/human-reviewed.jsonl` stores the underlying calibration judgments.

## Human calibration before model scoring

Do not assume synthetic gold labels are correct merely because they were written first.

Before treating subjective cases as benchmark truth:

1. present ambiguous cases without their expected answers
2. collect a human disposition judgment
3. compare it to the synthetic label
4. record disagreements rather than silently rewriting history
5. update the current calibration gold where appropriate

For ranking, ask the reviewer to order a mixed candidate set under a fixed display limit and separately mark Watching or Suppress candidates.

This surfaces the user's actual attention policy instead of forcing all unresolved work into a binary open/closed frame.

## Primary real-world metrics

### Precision@5

Of the five highest-ranked surfaced loops, how many does the user agree are real unresolved obligations?

This is the primary quality metric because false alarms destroy the habit.

### Importance@5

Of the top five, how many actually deserve the user's attention?

A technically open but trivial item can still be product noise.

### Completion detection accuracy

How often does the system correctly recognize that an apparent obligation has already been satisfied, cancelled, delegated, superseded, rescheduled, or made obsolete?

### Duplicate rate

How often does one real-world obligation appear more than once?

### Miss rate

What important loops did the user know about that the system failed to surface?

### Watching calibration

How often does the system preserve latent state without spending scarce primary attention on it too early?

### Ranking agreement

For mixed candidate sets, measure top-k overlap and pairwise ordering agreement among Main candidates.

Do not turn ranking agreement into fake universal importance. It is evidence about how well the system matches a reviewed attention policy.

### Action usefulness

Was the proposed next step and preparation offer actually useful?

## Why there is no single magic score

Several dimensions are partly subjective.

Importance depends on the user. Source access changes what can be proven. A host with email only should not be compared naively against a host with email, Slack, calendar, and files.

Publish enough context to make a result interpretable.

## Host/model result record

A credible benchmark report should include:

- repo version or commit
- host and model
- source scope
- fixture set version
- whether the skill was explicitly invoked or auto-triggered
- temperature or equivalent control if exposed
- number of independent runs
- structured prediction format
- human grading protocol for importance
- human calibration source for ranking scenarios
- known limitations

Use [`../evals/HOST_MATRIX.md`](../evals/HOST_MATRIX.md) as the public record of validated configurations.

## Baseline comparison

When possible, compare:

1. the same model and tools without the skill
2. the same model and tools with Open Loops

That isolates skill lift from model capability.

## Do not leak private data into the benchmark

Real failures should be reduced to synthetic cases.

Preserve only the reasoning structure required to reproduce the error. Replace names, companies, URLs, exact amounts, identifiers, and confidential content.

## Avoid benchmark theater

Do not:

- count structurally valid fixtures as model accuracy
- publish a precision number from one curated inbox run
- tune against the entire public suite and present it as held-out performance
- compare hosts with radically different source access without disclosure
- treat rank > display limit as equivalent to Watching
- turn subjective importance judgments into fake decimal precision

The benchmark exists to make the method falsifiable and regression-safe. It is not marketing decoration.
