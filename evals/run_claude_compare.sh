#!/usr/bin/env bash
set -euo pipefail

SMOKE="${SMOKE:-}"
LIMIT="${LIMIT:-0}"
CONDITION="${CONDITION:-both}"
RESCORE_ONLY="${RESCORE_ONLY:-0}"
REUSE_HARD="${REUSE_HARD:-0}"
HARD_DIR="${HARD_DIR:-/tmp/open-loops-hard-smoke}"
HARD_CASES="case_010,case_017,case_026,case_036,case_037,case_042,case_043,case_046,case_049,case_060,case_062,case_064"

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
  CASE_ARGS=(--case-ids "$HARD_CASES")
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
if [[ "$REUSE_HARD" != "0" && "$REUSE_HARD" != "1" ]]; then
  echo "REUSE_HARD must be 0 or 1" >&2
  exit 2
fi
if [[ "$REUSE_HARD" == "1" ]]; then
  if [[ -n "$SMOKE" || "$LIMIT" != "0" || "$RESCORE_ONLY" != "0" || "$CONDITION" != "both" ]]; then
    echo "REUSE_HARD=1 requires a full CONDITION=both run with no SMOKE, LIMIT, or RESCORE_ONLY" >&2
    exit 2
  fi
  CASE_ARGS=(--exclude-case-ids "$HARD_CASES")
fi

BASELINE="$OUT_DIR/claude-baseline.jsonl"
SKILL="$OUT_DIR/claude-open-loops.jsonl"

if [[ "$REUSE_HARD" == "1" ]]; then
  HARD_BASELINE="$HARD_DIR/claude-baseline.jsonl"
  HARD_SKILL="$HARD_DIR/claude-open-loops.jsonl"
  HARD_BASELINE_RAW="$HARD_DIR/claude-baseline.jsonl.raw"
  HARD_SKILL_RAW="$HARD_DIR/claude-open-loops.jsonl.raw"
  for required in "$HARD_BASELINE" "$HARD_SKILL" "$HARD_BASELINE_RAW" "$HARD_SKILL_RAW"; do
    if [[ ! -f "$required" ]]; then
      echo "REUSE_HARD=1 requires existing hard-smoke file: $required" >&2
      exit 2
    fi
  done

  REM_BASELINE="$OUT_DIR/claude-baseline.remaining.jsonl"
  REM_SKILL="$OUT_DIR/claude-open-loops.remaining.jsonl"

  python3 evals/run_claude_blind.py \
    --condition baseline \
    --out "$REM_BASELINE" \
    "${MODEL_ARGS[@]}" \
    "${CASE_ARGS[@]}"

  python3 evals/run_claude_blind.py \
    --condition skill \
    --out "$REM_SKILL" \
    "${MODEL_ARGS[@]}" \
    "${CASE_ARGS[@]}"

  python3 evals/merge_prediction_sets.py --out "$BASELINE" "$HARD_BASELINE" "$REM_BASELINE"
  python3 evals/merge_prediction_sets.py --out "$SKILL" "$HARD_SKILL" "$REM_SKILL"
  python3 evals/merge_prediction_sets.py --out "$BASELINE.raw" "$HARD_BASELINE_RAW" "$REM_BASELINE.raw"
  python3 evals/merge_prediction_sets.py --out "$SKILL.raw" "$HARD_SKILL_RAW" "$REM_SKILL.raw"

  if [[ "$(wc -l < "$BASELINE" | tr -d ' ')" != "64" || "$(wc -l < "$SKILL" | tr -d ' ')" != "64" ]]; then
    echo "merged full benchmark must contain exactly 64 predictions per condition" >&2
    exit 2
  fi
elif [[ "$RESCORE_ONLY" == "0" ]]; then
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
