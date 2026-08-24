# Reuse a validated hard smoke in the full Claude run

If the 12-case hard smoke was run with the same Claude model selector, blind prompt, and skill version intended for the full comparison, those frozen predictions can be reused instead of paying to rerun them.

Run the remaining 52 cases for both conditions and merge them with the existing hard-smoke outputs:

```bash
OUT_DIR=/tmp/open-loops-full-v021 \
REUSE_HARD=1 \
CLAUDE_MODEL=opus \
bash evals/run_claude_compare.sh
```

By default, the wrapper reuses frozen files from `/tmp/open-loops-hard-smoke`. Override that with `HARD_DIR=/path/to/hard-smoke`.

Requirements:

- both hard-smoke prediction files and raw-output files must still exist
- the hard baseline must still be valid for the current baseline prompt and model
- the hard skill run must use the same skill version intended for the full comparison
- `REUSE_HARD=1` cannot be combined with `SMOKE`, `LIMIT`, `RESCORE_ONLY`, or a single-condition run

The wrapper runs only the other 52 cases per condition, merges the two non-overlapping sets, verifies that each merged prediction file contains 64 cases, then scores and compares the full benchmark.

This saves 24 Claude calls while preserving the same 64-case comparison when the frozen hard-smoke conditions are genuinely reusable.
