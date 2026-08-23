#!/usr/bin/env python3
from pathlib import Path
import json
import sys

CASES_PATH = Path(__file__).with_name("cases.jsonl")

if len(sys.argv) != 2:
    print("usage: python3 evals/score_predictions.py predictions.jsonl")
    sys.exit(2)

pred_path = Path(sys.argv[1])
if not pred_path.exists():
    print(f"predictions file not found: {pred_path}")
    sys.exit(2)

cases = {}
for raw in CASES_PATH.read_text(encoding="utf-8").splitlines():
    if raw.strip():
        c = json.loads(raw)
        cases[c["id"]] = c

preds = {}
for line_no, raw in enumerate(pred_path.read_text(encoding="utf-8").splitlines(), 1):
    if not raw.strip():
        continue
    p = json.loads(raw)
    cid = p.get("case_id")
    if cid in preds:
        raise SystemExit(f"duplicate prediction for {cid} on line {line_no}")
    preds[cid] = p

TP = FP = FN = 0
state_ok = state_total = 0
missing_cases = []

for cid, case in cases.items():
    pred = preds.get(cid)
    if pred is None:
        missing_cases.append(cid)
        expected_open = {x["anchor"] for x in case["expected"]["open"]}
        FN += len(expected_open)
        continue
    expected = {x["anchor"]: x for x in case["expected"]["open"]}
    predicted_items = pred.get("open", [])
    predicted_anchors = [x.get("anchor") for x in predicted_items if x.get("anchor")]
    predicted_set = set(predicted_anchors)
    expected_set = set(expected)
    TP += len(predicted_set & expected_set)
    FP += len(predicted_set - expected_set)
    FN += len(expected_set - predicted_set)
    for item in predicted_items:
        anchor = item.get("anchor")
        if anchor in expected and item.get("state"):
            state_total += 1
            if item["state"] == expected[anchor].get("state"):
                state_ok += 1
    # Repeating an anchor is a duplicate overproduction error.
    FP += max(0, len(predicted_anchors) - len(predicted_set))

precision = TP / (TP + FP) if TP + FP else 1.0
recall = TP / (TP + FN) if TP + FN else 1.0
f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
state_acc = state_ok / state_total if state_total else None

print(f"cases: {len(cases)}")
print(f"predicted cases: {len(preds)}")
print(f"true positives: {TP}")
print(f"false positives: {FP}")
print(f"false negatives: {FN}")
print(f"precision: {precision:.3f}")
print(f"recall: {recall:.3f}")
print(f"f1: {f1:.3f}")
if state_acc is not None:
    print(f"state accuracy on matched predictions: {state_acc:.3f}")
if missing_cases:
    print(f"missing case predictions: {len(missing_cases)}")
