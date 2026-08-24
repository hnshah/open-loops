# Benchmark methodology

Open Loops is useful only if it is trusted.

The benchmark therefore evaluates state reconstruction and judgment, not raw extraction volume.

## Benchmark question

> Given source activity over time, does a meaningful obligation remain unresolved as of the evaluation time, and does it deserve scarce attention now?

A case can require the model to identify an obligation, find later closure, infer ownership, merge duplicates, respect timing, choose a disposition, and rank importance.

## The scoring unit is the obligation

Open Loops reasons about real-world obligations, not arbitrary source-event IDs.

One obligation can be evidenced by several messages, notes, or calendar events. The benchmark therefore treats an expected `anchor` plus its non-conflicting `related` source IDs as acceptable evidence aliases for the same obligation.

If a related source ID is itself a separately scored expected anchor, it remains a separate obligation and is not an alias.

A model is not penalized merely for choosing a different valid evidence event as its primary anchor. Surfacing multiple evidence aliases as separate loops is measured as a duplicate instead.

This keeps the benchmark aligned with the product law: one obligation, one loop.

## Public benchmark units

The public suite has four fixture types.

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

### Pairwise attention preferences

`evals/pairwise-preferences.jsonl` isolates two candidates and asks which deserves attention first.

Use pairwise review to test hypotheses about ranking dimensions such as:

- urgency
- ownership
- external expectation
- customer significance
- dependency severity
- consequence
- preparation burden

Pairwise review is especially useful when a mixed ranking set contains several confounded dimensions.

## Human calibration before model scoring

Do not assume synthetic gold labels are correct merely because they were written first.

Before treating subjective cases as benchmark truth:

1. present ambiguous cases without their expected answers
2. collect a human disposition judgment
3. compare it to the synthetic label
4. record disagreements rather than silently rewriting history
5. classify the judgment as universal product reasoning or a personal preference
6. update the current calibration gold where appropriate

For ranking, ask the reviewer to order a mixed candidate set under a fixed display limit and separately mark Watching or Suppress candidates.

Then use pairwise comparisons to isolate the dimensions that may explain the ranking.

This surfaces the user's actual attention policy instead of forcing all unresolved work into a binary open/closed frame.

## Universal and personal calibration are different

A generic public skill cannot be expected to know a reviewer-specific preference it was never given.

Human-reviewed calibration therefore records a `scope`:

- **universal** — reasoning intended to apply to the generic product, such as not promoting a future follow-up before it is due
- **personal** — an individual preference, such as retaining casual coffee language as low-pressure relationship state

Generic baseline-vs-skill comparisons apply universal overrides only.

Personal overrides may be included only when both evaluated conditions received the matching personal preferences. Otherwise the benchmark would reward hidden knowledge instead of skill quality.

Ranking and pairwise calibration are generally personal unless a separate review establishes a universal rule.

## Ranking may be contextual

Do not assume one reviewer has a single stable global ordering over every possible obligation.

The same two analogous items can reverse order when judged inside a ten-item set versus directly against each other. That is useful evidence, not necessarily reviewer error.

Possible causes include:

- attention-budget effects
- framing and wording
- context supplied by neighboring candidates
- salience
- uncertainty about consequence
- genuine non-transitive or situational preferences

Preserve these conflicts in the benchmark.

Do not silently rewrite the earlier review, average the judgments into a fake scalar weight, or force transitivity merely to make the dataset tidy.

Instead:

1. flag the conflict
2. rerun the pair with wording and side order varied
3. test the pair inside a second mixed context
4. infer a durable rule only after repeated evidence agrees

A ranking policy should be learned as a set of tested behavioral tendencies, not invented as a universal mathematical score.

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

Evidence aliases for the same obligation should count as one loop. If a model surfaces multiple aliases separately, record that as a duplicate rather than pretending they are independent obligations.

### Miss rate

What important loops did the user know about that the system failed to surface?

### Watching calibration

How often does the system preserve latent state without spending scarce primary attention on it too early?

### Ranking agreement

For mixed candidate sets, measure top-k overlap and pairwise ordering agreement among Main candidates.

Do not turn ranking agreement into fake universal importance. It is evidence about how well the system matches a reviewed attention policy.

### Pairwise preference agreement

For direct comparisons, measure how often the system chooses the same candidate as the reviewed preference.

Report stability separately when repeated or rephrased comparisons exist.

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
- calibration scope used for scoring
- whether the skill was explicitly invoked or auto-triggered
- temperature or equivalent control if exposed
- number of independent runs
- structured prediction format
- human grading protocol for importance
- human calibration source for ranking scenarios
- pairwise calibration source when ranking preferences are tested
- known limitations

Use [`../evals/HOST_MATRIX.md`](../evals/HOST_MATRIX.md) as the public record of validated configurations.

## Baseline comparison

When possible, compare:

1. the same model and tools without the skill
2. the same model and tools with Open Loops

That isolates skill lift from model capability.

Do not apply hidden personal calibration to one of these conditions unless both receive the same preference context.

## Do not leak private data into the benchmark

Real failures should be reduced to synthetic cases.

Preserve only the reasoning structure required to reproduce the error. Replace names, companies, URLs, exact amounts, identifiers, and confidential content.

## Avoid benchmark theater

Do not:

- count structurally valid fixtures as model accuracy
- publish a precision number from one curated inbox run
- tune against the entire public suite and present it as held-out performance
- compare hosts with radically different source access without disclosure
- penalize a valid evidence alias as though it were a different obligation
- apply reviewer-specific calibration to a generic model that was never given the preference
- treat rank > display limit as equivalent to Watching
- force inconsistent human ranking judgments into a fake universal score
- turn subjective importance judgments into fake decimal precision

The benchmark exists to make the method falsifiable and regression-safe. It is not marketing decoration.
