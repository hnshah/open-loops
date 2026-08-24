#!/usr/bin/env bash
set -euo pipefail

SMOKE="${SMOKE:-}"
LIMIT="${LIMIT:-0}"
CONDITION="${CONDITION:-both}"
RESCORE_ONLY="${RESCORE_ONLY:-0}"

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

case "$CONDITION" in
  both|baseline|skill) ;;
  *)
    echo "CONDITION must be both, baseline, or skill" >&2
    exit 2
    ;;
esac

if [[ "$RESCORE_ONLY" != "0" && "$RESCORE_ONLY" != "1" ]]; then
  echo "RESCORE_ONLY must be 0 or 1" >&2
  exit 2
fi

BASELINE="$OUT_DIR/claude-baseline.jsonl"
SKILL="$OUT_DIR/claude-open-loops.jsonl"

if [[ "$RESCORE_ONLY" == "0" ]]; then
  if [[ "$CONDITION" == "both" || "$CONDITION" == "baseline" ]]; then
    python3 evals/run_claude_blind.py \
      --condition baseline \
      --out "$BASELINE" \
      "${MODEL_ARGS[@]}" \
      "${CASE_ARGS[@]}"
  fi

  if [[ "$CONDITION" == "both" || "$CONDITION" == "skill" ]]; then
    python3 evals/run_claude_blind.py \
      --condition skill \
      --out "$SKILL" \
      "${MODEL_ARGS[@]}" \
      "${CASE_ARGS[@]}"
  fi
fi

if [[ -f "$BASELINE" ]]; then
  echo
  echo "=== BASELINE ==="
  python3 evals/score_calibrated.py "$BASELINE" "${SCORE_ARGS[@]}"
else
  echo
  echo "No baseline prediction file at $BASELINE"
fi

if [[ -f "$SKILL" ]]; then
  echo
  echo "=== OPEN LOOPS ==="
  python3 evals/score_calibrated.py "$SKILL" "${SCORE_ARGS[@]}"
else
  echo
  echo "No Open Loops prediction file at $SKILL"
fi

if [[ -f "$BASELINE" && -f "$SKILL" ]]; then
  echo
  echo "=== PER-CASE COMPARISON ==="
  python3 evals/compare_predictions.py "$BASELINE" "$SKILL"
fi

echo
echo "Predictions and raw outputs are in $OUT_DIR"
