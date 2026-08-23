# Open Loops evals

The benchmark tests a harder question than action-item extraction.

> **Does a meaningful obligation remain unresolved after later evidence is considered?**

The cases are synthetic and designed to expose state-reconstruction failures.

## Primary metric

**Precision@5** is the main product quality metric for real scans.

A technically valid but low-value result can still be noise, so real-world testing should also track Importance@5.

The repository does not claim a current benchmark score. Fixture counts and suite metadata live in `benchmark-manifest.json`.

## Human-reviewed gold calibration

`human-reviewed.jsonl` records explicit human judgments on ambiguous benchmark cases.

Calibration uses three labels:

- `main` — deserves a primary Open Loops slot now
- `watching` — preserve outside the primary list as Watching or Probably fine
- `suppress` — do not retain as meaningful open-loop state for this scan

The original synthetic fixture remains useful as the authored hypothesis. When a human-reviewed label differs, the reviewed label is the current gold product judgment. This keeps disagreements inspectable instead of silently rewriting history.

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
- ranking and importance

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

`anchor` points to the source event that created the underlying obligation. For duplicate cases, an expected open loop may also include `related` source IDs.

## Validate the fixtures

```bash
python3 evals/validate_cases.py
```

## Score structured predictions

A host adapter can write predictions as JSONL.

```json
{"case_id":"case_001","open":[{"anchor":"m1","state":"I owe","rank":1}]}
```

Then run

```bash
python3 evals/score_predictions.py predictions.jsonl
```

The deterministic scorer measures obligation classification, state accuracy, false positives, misses, and duplicate overproduction when the prediction format includes repeated anchors.

It does not pretend to solve subjective importance grading or Watching calibration. Human or rubric-judge review is still needed for ranking quality, secondary-state placement, and next-step usefulness.

## Real-world dogfood protocol

1. Run on one real source and a seven-day lookback.
2. Grade the top five manually.
3. Record every false positive, miss, wrong owner, wrong completion judgment, bad rank, and bad Watching decision.
4. Sanitize each failure into the smallest synthetic case.
5. Re-run the same case after every behavior change.
6. Add cross-source access only after single-source precision is acceptable.
7. Add routine execution only after several one-time runs are useful.

Every important failure should become an eval before it becomes another paragraph of instructions.

## Host/model validation

Use [`HOST_MATRIX.md`](HOST_MATRIX.md) to record configurations that have actually been tested. Use [`REAL_WORLD_SCORECARD.md`](REAL_WORLD_SCORECARD.md) for manual dogfood grading.

The benchmark methodology and reporting standard are documented in [`../docs/benchmark-methodology.md`](../docs/benchmark-methodology.md).
