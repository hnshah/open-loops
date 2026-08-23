# Blind model run

This protocol measures model behavior without exposing benchmark gold labels to the model.

## Why blind runs matter

The public fixtures contain expected answers for deterministic scoring. A model that can read those answers is not being evaluated.

A valid blind run must give the model only:

- the Open Loops skill package being tested
- the case ID
- the `as_of` time
- the source events
- the required prediction format

It must not receive `expected`, human-reviewed labels, ranking gold, pairwise preferences, or scorer output before producing predictions.

## Export the blind state-reconstruction set

```bash
python3 evals/export_blind_cases.py > /tmp/open-loops-blind-cases.jsonl
```

Each line contains a case with the `expected` field removed.

## Required prediction format

For each case, return one JSON object:

```json
{"case_id":"case_001","main":[{"anchor":"m1","state":"I owe"}],"watching":[],"suppress":[]}
```

Rules:

- `main` contains unresolved obligations that deserve primary-list eligibility now.
- `watching` contains meaningful latent state that should stay outside the primary list for now.
- `suppress` contains source anchors that should not be retained as meaningful open-loop state.
- Include only source IDs present in the case.
- Do not invent source IDs.
- Do not include prose outside the JSON object when running a machine-scored benchmark.

The legacy `open` prediction format remains supported by `score_predictions.py` for the original binary fixtures. Three-bucket runs should use the newer scorer once all reviewed gold labels are available.

## Run procedure

1. Start a fresh model context.
2. Install or provide the exact skill version under test.
3. Do not expose the repository `evals/` directory to the model if the harness can isolate it.
4. Feed blind cases in a fixed order or a recorded randomized order.
5. Use one prediction per case.
6. Save the raw model output unchanged.
7. Record host, model, model version, skill commit, source scope, temperature or equivalent setting, and run timestamp.
8. Score only after the complete prediction file is frozen.

## Recommended first comparison

Run two conditions with the same model:

### Baseline

Model receives the case and output schema, but not `SKILL.md` or its references.

### Open Loops

Model receives the same case plus the installed Open Loops skill.

The difference is more informative than a standalone accuracy number because it isolates skill lift from model capability.

## Claude-first protocol

For the first external benchmark, use a fresh Claude context for each condition. Keep the model version, temperature setting, case order, and output schema identical between baseline and Open Loops.

Do not let Claude inspect `cases.jsonl`, `human-reviewed.jsonl`, `ranking-scenarios.jsonl`, or `pairwise-preferences.jsonl` directly. Export the blind set first.

## Human review

After deterministic scoring, manually inspect:

- false positives
- false negatives
- ownership mistakes
- closure mistakes
- Watching vs Main mistakes on reviewed cases
- top-five ranking quality in mixed scenarios
- next-step usefulness on real scans

Every meaningful failure should be reduced to a sanitized regression fixture before changing the skill.
