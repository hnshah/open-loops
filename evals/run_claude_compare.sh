#!/usr/bin/env bash
set -euo pipefail

OUT_DIR="${OUT_DIR:-/tmp/open-loops-benchmark}"
LIMIT="${LIMIT:-0}"
mkdir -p "$OUT_DIR"

MODEL_ARGS=()
if [[ -n "${CLAUDE_MODEL:-}" ]]; then
  MODEL_ARGS=(--model "$CLAUDE_MODEL")
fi

LIMIT_ARGS=()
SCORE_ARGS=()
if [[ "$LIMIT" != "0" ]]; then
  LIMIT_ARGS=(--limit "$LIMIT")
  SCORE_ARGS=(--only-predicted)
fi

BASELINE="$OUT_DIR/claude-baseline.jsonl"
SKILL="$OUT_DIR/claude-open-loops.jsonl"

python3 evals/run_claude_blind.py \
  --condition baseline \
  --out "$BASELINE" \
  "${MODEL_ARGS[@]}" \
  "${LIMIT_ARGS[@]}"

python3 evals/run_claude_blind.py \
  --condition skill \
  --out "$SKILL" \
  "${MODEL_ARGS[@]}" \
  "${LIMIT_ARGS[@]}"

echo
echo "=== BASELINE ==="
python3 evals/score_calibrated.py "$BASELINE" "${SCORE_ARGS[@]}"

echo
echo "=== OPEN LOOPS ==="
python3 evals/score_calibrated.py "$SKILL" "${SCORE_ARGS[@]}"

echo
echo "Predictions and raw outputs are in $OUT_DIR"
