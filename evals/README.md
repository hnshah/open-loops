# Open Loops evals

The benchmark tests a harder question than action-item extraction.

> **Does a meaningful obligation remain unresolved after later evidence is considered, and does it deserve scarce attention now?**

The cases are synthetic and designed to expose state-reconstruction and ranking failures.

## Primary metric

**Precision@5** is the main product quality metric for real scans.

A technically valid but low-value result can still be noise, so real-world testing should also track Importance@5 and ranking agreement.

The repository does not claim a current model benchmark score. Fixture counts and suite metadata live in `benchmark-manifest.json`.

## Eval families

- trigger and near-neighbor routing
- explicit obligations
- completion detection
- cancellation and supersession
- delegation and ownership
- waiting on others
- response-required requests
- ambiguous social language
- follow-up timing
- preparation work
- duplicate collapse
- stale obligations
- cross-source resolution
- partial evidence
- disposition and ranking
- pairwise attention preferences
- side-reversal stability

## Trigger fixtures

`triggers.jsonl` contains positive and near-neighbor negative requests for testing whether the skill activates on the job it owns and stays out of adjacent jobs.

Validate them with

```bash
python3 evals/validate_triggers.py
```

A host-specific eval runner should measure false positives and false negatives separately.

## State-reconstruction case format

Each line of `cases.jsonl` is one independent synthetic case.

Core fields

```json
{
  "id": "case_001",
  "category": "explicit_promise",
  "as_of": "2026-08-22T12:00:00Z",
  "sources": [
    {
      "id": "m1",
      "type": "email",
      "timestamp": "2026-08-20T09:00:00Z",
      "author": "you",
      "text": "I'll send the deck tomorrow."
    }
  ],
  "expected": {
    "open": [
      {
        "anchor": "m1",
        "state": "I owe",
        "priority": "high"
      }
    ],
    "suppressed": []
  }
}
```

`anchor` points to the primary source event for the obligation. `related` source IDs are supporting evidence for the same real-world obligation unless a related source ID is itself a separately scored expected anchor.

The calibrated scorer operates at the **obligation level**, not the raw evidence-anchor level. A model may anchor one obligation to any accepted evidence alias without being penalized for choosing a different but valid source event. Surfacing multiple aliases for the same obligation is tracked separately as a duplicate.

## Human-reviewed calibration

`human-reviewed.jsonl` records blind human review of ambiguous cases and mixed ranking sets.

Calibration uses three dispositions:

- `main`
- `watching`
- `suppress`

Each human judgment also has a calibration scope:

- `universal` — product reasoning that should apply to the generic public skill, such as a future follow-up remaining in Watching until it is due.
- `personal` — a reviewer-specific preference, such as keeping casual coffee language visible as relationship state.

Generic baseline-vs-skill model runs apply only universal overrides. Personal overrides should be scored only when both tested conditions received the matching personal preferences. This prevents the benchmark from penalizing a generic skill for failing to know a reviewer-specific rule it was never given.

A reviewed judgment can differ from the original synthetic expectation. The disagreement stays visible rather than being silently erased.

## Ranking scenarios

`ranking-scenarios.jsonl` combines existing cases into mixed candidate sets under a fixed display limit.

It separates:

1. Main / Watching / Suppress disposition
2. order among Main candidates
3. the top-k Main candidates that fit in the brief

This distinction is important. A Main candidate ranked sixth is still Main even when the current display limit is five. It should not be mislabeled Watching just because the interface is intentionally short.

Validate ranking scenarios with

```bash
python3 evals/validate_rankings.py
```

## Pairwise attention calibration

`pairwise-preferences.jsonl` isolates two candidates at a time and asks which deserves attention first.

Pairwise review helps identify which dimensions actually drive ranking, such as urgency, ownership, customer significance, dependency severity, and external expectation.

It also exposes an important failure mode in benchmark design: **human ranking may be context-dependent rather than a perfectly stable global ordering.**

A pairwise answer can conflict with the ordering of analogous items inside a larger mixed set. Preserve that conflict. Do not silently force transitivity or convert one judgment into a universal weight.

The benchmark should use pairwise calibration to form hypotheses and test ranking stability, not to pretend one reviewer has revealed a permanent mathematical priority function.

Batch 4 reversed the presentation order of six earlier pairwise comparisons. All six preferences survived the reversal. See [`stability-batch-4.md`](stability-batch-4.md).

Validate pairwise fixtures with

```bash
python3 evals/validate_pairwise.py
```

## Blind model runs

Never evaluate a model by handing it `cases.jsonl` with the expected answers intact.

Export a gold-free case set with

```bash
python3 evals/export_blind_cases.py > /tmp/open-loops-blind-cases.jsonl
```

Then run the model in a fresh context and freeze its predictions before scoring.

The recommended first comparison is the same model under two conditions:

1. baseline without the skill
2. Open Loops with the exact skill version installed

See [`BLIND_RUN.md`](BLIND_RUN.md) for the full protocol, including Claude-first isolation requirements.

## Validate the fixtures

```bash
python3 evals/validate_cases.py
```

## Score structured predictions

For the current three-bucket benchmark, a host adapter writes predictions as JSONL.

```json
{"case_id":"case_001","main":[{"anchor":"m1","state":"I owe"}],"watching":[]}
```

Score a complete generic run with

```bash
python3 evals/score_calibrated.py predictions.jsonl
```

Score a smoke subset with

```bash
python3 evals/score_calibrated.py predictions.jsonl --only-predicted
```

Only use reviewer-specific calibration when the evaluated model actually received those personal preferences:

```bash
python3 evals/score_calibrated.py predictions.jsonl --include-personal-overrides
```

The calibrated scorer measures Main precision/recall/F1, retained-state precision/recall, disposition accuracy, semantic state accuracy, exact state-schema adherence, duplicate evidence-anchor predictions, and orphan predictions.

`score_predictions.py` remains the legacy binary scorer for the original `open` prediction shape.

Neither deterministic scorer pretends to solve subjective ranking quality. Human or rubric-judge review is still needed for ranking and next-step usefulness.

## Real-world dogfood protocol

1. Run on one real source and a seven-day lookback.
2. Grade the top five manually.
3. Record every false positive, miss, wrong owner, wrong completion judgment, and bad rank.
4. Sanitize each failure into the smallest synthetic case.
5. Re-run the same case after every behavior change.
6. Add cross-source access only after single-source precision is acceptable.
7. Add routine execution only after several one-time runs are useful.

Every important failure should become an eval before it becomes another paragraph of instructions.

## Host/model validation

Use [`HOST_MATRIX.md`](HOST_MATRIX.md) to record configurations that have actually been tested. Use [`REAL_WORLD_SCORECARD.md`](REAL_WORLD_SCORECARD.md) for manual dogfood grading.

The benchmark methodology and reporting standard are documented in [`../docs/benchmark-methodology.md`](../docs/benchmark-methodology.md).
