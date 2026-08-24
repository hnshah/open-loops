#!/usr/bin/env bash
set -euo pipefail

SMOKE="${SMOKE:-}"
LIMIT="${LIMIT:-0}"

if [[ -z "${OUT_DIR:-}" ]]; then
  if [[ "$SMOKE" == "hard" ]]; then
    OUT_DIR="/tmp/open-loops-hard-smoke"
  else
    OUT_DIR="/tmp/open-loops-benchmark"
  fi
fi
mkdir -p "$OUT_DIR"

MODEL_ARGS=()
if [[ -n "${CLAUDE_MODEL:-}" ]]; then
  MODEL_ARGS=(--model "$CLAUDE_MODEL")
fi

CASE_ARGS=()
SCORE_ARGS=()
if [[ "$SMOKE" == "hard" ]]; then
  if [[ "$LIMIT" != "0" ]]; then
    echo "SMOKE=hard cannot be combined with LIMIT" >&2
    exit 2
  fi
  CASE_ARGS=(--case-ids "case_010,case_017,case_026,case_036,case_037,case_042,case_043,case_046,case_049,case_060,case_062,case_064")
  SCORE_ARGS=(--only-predicted)
elif [[ -n "$SMOKE" ]]; then
  echo "unknown SMOKE set: $SMOKE" >&2
  exit 2
elif [[ "$LIMIT" != "0" ]]; then
  CASE_ARGS=(--limit "$LIMIT")
  SCORE_ARGS=(--only-predicted)
fi

BASELINE="$OUT_DIR/claude-baseline.jsonl"
SKILL="$OUT_DIR/claude-open-loops.jsonl"

python3 evals/run_claude_blind.py \
  --condition baseline \
  --out "$BASELINE" \
  "${MODEL_ARGS[@]}" \
  "${CASE_ARGS[@]}"

python3 evals/run_claude_blind.py \
  --condition skill \
  --out "$SKILL" \
  "${MODEL_ARGS[@]}" \
  "${CASE_ARGS[@]}"

echo
echo "=== BASELINE ==="
python3 evals/score_calibrated.py "$BASELINE" "${SCORE_ARGS[@]}"

echo
echo "=== OPEN LOOPS ==="
python3 evals/score_calibrated.py "$SKILL" "${SCORE_ARGS[@]}"

echo
echo "=== PER-CASE COMPARISON ==="
python3 evals/compare_predictions.py "$BASELINE" "$SKILL"

echo
echo "Predictions and raw outputs are in $OUT_DIR"
