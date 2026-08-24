# Blind model run

This protocol measures model behavior without exposing benchmark gold labels or grading hints to the model.

## Why blind runs matter

The public fixtures contain expected answers and semantic case categories for deterministic analysis. A model that can read those fields is not being evaluated.

A valid blind run must give the model only:

- the Open Loops skill package being tested, when testing the skill condition
- the case ID
- the `as_of` time
- the source events
- the required prediction format

It must not receive `expected`, `category`, fixture notes, human-reviewed labels, ranking gold, pairwise preferences, or scorer output before producing predictions.

## Export the blind state-reconstruction set

```bash
python3 evals/export_blind_cases.py > /tmp/open-loops-blind-cases.jsonl
```

Each line contains only `case_id`, `as_of`, and `sources`.

## Required prediction format

For each case, return one JSON object:

```json
{"case_id":"case_001","main":[{"anchor":"m1","state":"I owe"}],"watching":[]}
```

Rules:

- `main` contains unresolved obligations that deserve primary-list eligibility now.
- `watching` contains meaningful latent state that should stay outside the primary list for now.
- Anything omitted from both buckets is treated as suppressed for scoring.
- Include only source IDs present in the case.
- Do not invent source IDs.
- Do not include prose outside the JSON object when running a machine-scored benchmark.

The benchmark scores **real-world obligations**, not raw source-event IDs. When several source events are accepted evidence for the same obligation, choosing any one accepted alias is valid. Surfacing several aliases separately is a duplicate.

## Fastest Claude-first comparison

The repository includes a wrapper that runs conditions and scores them.

### Representative hard smoke set

Before spending a full 128 Claude calls, run the curated 12-case hard smoke set:

```bash
SMOKE=hard CLAUDE_MODEL=opus bash evals/run_claude_compare.sh
```

The set spans cross-source completion, cancellation, ownership transfer, response expectations, ambiguous social language, follow-up timing, preparation, routine calendar noise, dependency blocking, and partial evidence. It intentionally favors judgment cases over easy explicit promises.

Hard-smoke outputs are written under `/tmp/open-loops-hard-smoke` by default.

### Rescore frozen outputs without new model calls

When benchmark semantics change, do not rerun the model just to get new scores. Reuse the frozen prediction files:

```bash
RESCORE_ONLY=1 SMOKE=hard bash evals/run_claude_compare.sh
```

This re-scores any existing baseline and Open Loops files in `/tmp/open-loops-hard-smoke` and prints the per-case comparison without calling Claude.

### Rerun only the skill condition

After changing Open Loops behavior, keep a valid frozen baseline and rerun only the skill condition:

```bash
CONDITION=skill SMOKE=hard CLAUDE_MODEL=opus bash evals/run_claude_compare.sh
```

The wrapper preserves the existing baseline file, replaces the Open Loops prediction file with the new run, then scores and compares both. Use a different `OUT_DIR` instead if you need to preserve multiple skill versions side by side.

### Simple first-N smoke test

For harness debugging only:

```bash
LIMIT=5 CLAUDE_MODEL=opus bash evals/run_claude_compare.sh
```

The first five fixtures are not representative of the benchmark and should not be used to estimate skill lift.

### Full comparison

```bash
CLAUDE_MODEL=opus bash evals/run_claude_compare.sh
```

Claude Code accepts `opus` as an alias for the latest Opus model. Pin a full model name instead when you need an immutable published result.

The full wrapper writes predictions and raw outputs under `/tmp/open-loops-benchmark` by default. Override with `OUT_DIR=/path/to/results`.

Set `CONDITION=baseline` or `CONDITION=skill` when only one side needs a fresh run. The default is `CONDITION=both`.

## Claude Code harness

The underlying isolated runner starts one fresh `claude -p` process per case in a temporary directory that does not contain the answer key.

Baseline:

```bash
python3 evals/run_claude_blind.py \
  --condition baseline \
  --out /tmp/open-loops-claude-baseline.jsonl
```

Open Loops instruction condition:

```bash
python3 evals/run_claude_blind.py \
  --condition skill \
  --out /tmp/open-loops-claude-skill.jsonl
```

Pass `--model <your-Claude-Code-model-selector>` to pin a model explicitly. Use `--limit N` for a first-N harness test or `--case-ids case_010,case_017,...` for a deliberate subset. Do not combine them.

The skill condition copies only `skills/open-loops` into the isolated directory and instructs Claude to read `SKILL.md` and its references as needed. This measures instruction lift. Host auto-invocation and trigger routing are separate evals.

## Score the calibrated run

```bash
python3 evals/score_calibrated.py /tmp/open-loops-claude-baseline.jsonl
python3 evals/score_calibrated.py /tmp/open-loops-claude-skill.jsonl
```

For deliberate subsets, add `--only-predicted` so unrun cases are not counted as misses.

Generic model comparisons apply **universal human calibration only**. Reviewer-specific personal preferences are excluded because neither condition received them.

Only when both evaluated conditions were explicitly given the matching personal preferences should you add:

```bash
--include-personal-overrides
```

The calibrated scorer reports:

- Main precision
- Main recall
- Main F1
- retained-state precision and recall for Main + Watching
- disposition accuracy
- duplicate evidence-anchor predictions
- orphan predictions
- semantic state-category accuracy
- exact state-enum adherence

Scenario-specific ranking judgments do not silently overwrite independent case labels.

## Compare the two frozen prediction files

After both conditions are complete, inspect the obligation-level differences:

```bash
python3 evals/compare_predictions.py \
  /tmp/open-loops-hard-smoke/claude-baseline.jsonl \
  /tmp/open-loops-hard-smoke/claude-open-loops.jsonl
```

The report shows accepted evidence aliases, disposition, state, which source anchor each condition used, and duplicate evidence-anchor predictions.

## Run procedure

1. Pin the repo commit and Claude model.
2. Run the representative hard smoke set.
3. Inspect prediction differences and any gold disagreements.
4. Fix benchmark errors before changing skill behavior.
5. Turn real skill failures into regression cases before editing instructions.
6. Re-score frozen outputs after benchmark-only changes.
7. Rerun only the condition whose behavior changed when the other frozen condition is still valid.
8. Run all 64 baseline cases.
9. Run all 64 skill cases with the same model and settings.
10. Preserve the raw output files generated by the harness.
11. Freeze both prediction files before looking at gold or scores.
12. Score baseline and skill.
13. Manually inspect every disagreement that matters.

## Recommended first comparison

Compare the same Claude model under two conditions:

### Baseline

Model receives the case and output schema, but no Open Loops skill files.

### Open Loops

Model receives the same case plus the exact `skills/open-loops` package.

The difference is more informative than a standalone score because it isolates skill lift from model capability.

## Claude-first isolation requirements

For the first external benchmark, keep the model version, case order, output schema, and exposed evidence identical between baseline and Open Loops.

Do not let Claude inspect `cases.jsonl`, `human-reviewed.jsonl`, `ranking-scenarios.jsonl`, `pairwise-preferences.jsonl`, `stability-batch-4.md`, or any scorer before its predictions are frozen.

Do not apply personal benchmark gold unless both model conditions were given the same personal preference context.

## Human review

After deterministic scoring, manually inspect:

- false positives
- false negatives
- ownership/state mistakes
- closure mistakes
- timing mistakes
- duplicate loops
- Watching vs Main mistakes on universally calibrated cases
- top-five ranking quality in mixed scenarios when personal ranking is being tested
- next-step usefulness on real scans

Every meaningful failure should become a sanitized regression fixture or human calibration record before changing the skill.
