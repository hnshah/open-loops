#!/usr/bin/env python3
from pathlib import Path
import argparse
import json
import re

ROOT = Path(__file__).resolve().parent
CASES_PATH = ROOT / "cases.jsonl"
REVIEW_PATH = ROOT / "human-reviewed.jsonl"
CANONICAL_STATES = (
    "I owe",
    "Waiting on",
    "Response expected",
    "Decision",
    "Follow-up",
    "Prepare",
    "Dependency",
    "Watching",
)


def canonicalize_state(value):
    if not isinstance(value, str):
        return None
    text = value.strip()
    lowered = text.lower()
    for state in CANONICAL_STATES:
        if lowered == state.lower():
            return state
    # Treat obvious descriptive expansions such as "I owe the deck" as the
    # same semantic category while scoring exact enum compliance separately.
    for state in sorted(CANONICAL_STATES, key=len, reverse=True):
        prefix = state.lower()
        if lowered.startswith(prefix) and len(lowered) > len(prefix):
            next_char = lowered[len(prefix)]
            if re.match(r"[\s:—-]", next_char):
                return state
    return None


parser = argparse.ArgumentParser()
parser.add_argument("predictions", type=Path)
parser.add_argument(
    "--only-predicted",
    action="store_true",
    help="Score only case IDs present in the prediction file. Use for smoke tests or deliberate subsets.",
)
args = parser.parse_args()

pred_path = args.predictions
if not pred_path.exists():
    raise SystemExit(f"predictions file not found: {pred_path}")

cases = {}
for raw in CASES_PATH.read_text(encoding="utf-8").splitlines():
    if raw.strip():
        case = json.loads(raw)
        cases[case["id"]] = case

# Independent case-level human calibration only. Scenario-specific ranking judgments
# remain in the ranking benchmark and must not silently override independent labels.
case_review = {}
for raw in REVIEW_PATH.read_text(encoding="utf-8").splitlines():
    if not raw.strip():
        continue
    item = json.loads(raw)
    if item.get("case_id") and not item.get("scenario_id"):
        case_review[item["case_id"]] = item["label"]

preds = {}
for line_no, raw in enumerate(pred_path.read_text(encoding="utf-8").splitlines(), 1):
    if not raw.strip():
        continue
    item = json.loads(raw)
    cid = item.get("case_id")
    if not cid:
        raise SystemExit(f"missing case_id on prediction line {line_no}")
    if cid not in cases:
        raise SystemExit(f"unknown prediction case_id {cid} on line {line_no}")
    if cid in preds:
        raise SystemExit(f"duplicate prediction for {cid} on line {line_no}")
    preds[cid] = item

if args.only_predicted and not preds:
    raise SystemExit("--only-predicted requires at least one prediction")

if args.only_predicted:
    scored_case_ids = [cid for cid in cases if cid in preds]
else:
    scored_case_ids = list(cases)

main_tp = main_fp = main_fn = 0
retained_tp = retained_fp = retained_fn = 0
disposition_ok = disposition_total = 0
state_semantic_ok = state_total = 0
state_schema_ok = state_schema_total = 0
missing_cases = []

for cid in scored_case_ids:
    case = cases[cid]

    gold = {}
    expected_by_anchor = {}
    for item in case["expected"]["open"]:
        gold[item["anchor"]] = "main"
        expected_by_anchor[item["anchor"]] = item
    for item in case["expected"]["suppressed"]:
        gold[item["anchor"]] = "suppress"
        expected_by_anchor.setdefault(item["anchor"], item)

    if cid in case_review:
        anchors = list(gold)
        if len(anchors) != 1:
            raise SystemExit(f"human-reviewed case {cid} must have exactly one scored anchor, found {anchors}")
        gold[anchors[0]] = case_review[cid]

    pred = preds.get(cid)
    if pred is None:
        missing_cases.append(cid)
        pred_main = set()
        pred_watching = set()
    else:
        pred_main = {x.get("anchor") for x in pred.get("main", []) if x.get("anchor")}
        pred_watching = {x.get("anchor") for x in pred.get("watching", []) if x.get("anchor")}
        if pred_main & pred_watching:
            raise SystemExit(f"{cid}: anchor predicted in both main and watching")

    valid_sources = {x["id"] for x in case["sources"]}
    unknown = (pred_main | pred_watching) - valid_sources
    if unknown:
        raise SystemExit(f"{cid}: unknown predicted anchors {sorted(unknown)}")

    gold_main = {a for a, label in gold.items() if label == "main"}
    gold_retained = {a for a, label in gold.items() if label in {"main", "watching"}}
    pred_retained = pred_main | pred_watching

    main_tp += len(pred_main & gold_main)
    main_fp += len(pred_main - gold_main)
    main_fn += len(gold_main - pred_main)

    retained_tp += len(pred_retained & gold_retained)
    retained_fp += len(pred_retained - gold_retained)
    retained_fn += len(gold_retained - pred_retained)

    for anchor, label in gold.items():
        disposition_total += 1
        if anchor in pred_main:
            predicted_label = "main"
        elif anchor in pred_watching:
            predicted_label = "watching"
        else:
            predicted_label = "suppress"
        if predicted_label == label:
            disposition_ok += 1

    if pred is not None:
        for item in pred.get("main", []):
            anchor = item.get("anchor")
            expected_state = expected_by_anchor.get(anchor, {}).get("state")
            raw_state = item.get("state")
            if anchor in gold_main and raw_state and expected_state:
                state_total += 1
                if canonicalize_state(raw_state) == expected_state:
                    state_semantic_ok += 1
                state_schema_total += 1
                if raw_state in CANONICAL_STATES:
                    state_schema_ok += 1


def ratio(num, den, empty=1.0):
    return num / den if den else empty

main_precision = ratio(main_tp, main_tp + main_fp)
main_recall = ratio(main_tp, main_tp + main_fn)
main_f1 = ratio(2 * main_precision * main_recall, main_precision + main_recall, empty=0.0)
retained_precision = ratio(retained_tp, retained_tp + retained_fp)
retained_recall = ratio(retained_tp, retained_tp + retained_fn)
disposition_acc = ratio(disposition_ok, disposition_total)
active_overrides = sum(1 for cid in scored_case_ids if cid in case_review)

print(f"available cases: {len(cases)}")
print(f"scored cases: {len(scored_case_ids)}")
print(f"predicted cases: {len(preds)}")
print(f"human-reviewed overrides in scored set: {active_overrides}")
print("scope: predicted subset only" if args.only_predicted else "scope: full benchmark")
print(f"main precision: {main_precision:.3f}")
print(f"main recall: {main_recall:.3f}")
print(f"main f1: {main_f1:.3f}")
print(f"retained precision (main + watching): {retained_precision:.3f}")
print(f"retained recall (main + watching): {retained_recall:.3f}")
print(f"disposition accuracy: {disposition_acc:.3f}")
if state_total:
    print(f"state category accuracy on matched main predictions: {state_semantic_ok / state_total:.3f}")
if state_schema_total:
    print(f"state schema adherence on matched main predictions: {state_schema_ok / state_schema_total:.3f}")
if missing_cases:
    print(f"missing case predictions: {len(missing_cases)}")
