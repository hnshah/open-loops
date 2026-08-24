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
    for state in sorted(CANONICAL_STATES, key=len, reverse=True):
        prefix = state.lower()
        if lowered.startswith(prefix) and len(lowered) > len(prefix):
            next_char = lowered[len(prefix)]
            if re.match(r"[\s:—-]", next_char):
                return state
    return None


def load_jsonl(path):
    out = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.strip():
            out.append(json.loads(raw))
    return out


parser = argparse.ArgumentParser()
parser.add_argument("predictions", type=Path)
parser.add_argument(
    "--only-predicted",
    action="store_true",
    help="Score only case IDs present in the prediction file. Use for smoke tests or deliberate subsets.",
)
parser.add_argument(
    "--include-personal-overrides",
    action="store_true",
    help="Apply reviewer-specific human calibration in addition to universal calibration. Use only when the tested condition was given the matching personal preferences.",
)
args = parser.parse_args()

if not args.predictions.exists():
    raise SystemExit(f"predictions file not found: {args.predictions}")

cases = {item["id"]: item for item in load_jsonl(CASES_PATH)}

reviews = {}
for item in load_jsonl(REVIEW_PATH):
    if not item.get("case_id") or item.get("scenario_id"):
        continue
    scope = item.get("scope", "universal")
    if scope == "personal" and not args.include_personal_overrides:
        continue
    reviews[item["case_id"]] = item

preds = {}
for line_no, item in enumerate(load_jsonl(args.predictions), 1):
    cid = item.get("case_id")
    if not cid:
        raise SystemExit(f"missing case_id on prediction item {line_no}")
    if cid not in cases:
        raise SystemExit(f"unknown prediction case_id {cid} on item {line_no}")
    if cid in preds:
        raise SystemExit(f"duplicate prediction for {cid} on item {line_no}")
    preds[cid] = item

if args.only_predicted and not preds:
    raise SystemExit("--only-predicted requires at least one prediction")

scored_case_ids = [cid for cid in cases if cid in preds] if args.only_predicted else list(cases)


def obligation_groups(case, review):
    open_items = list(case["expected"]["open"])
    suppressed_items = list(case["expected"]["suppressed"])
    primary_anchors = {item["anchor"] for item in open_items + suppressed_items}
    groups = []

    for item in open_items:
        aliases = {item["anchor"]}
        aliases.update(a for a in item.get("related", []) if a not in primary_anchors)
        groups.append({
            "anchor": item["anchor"],
            "aliases": aliases,
            "label": "main",
            "state": item.get("state"),
        })

    for item in suppressed_items:
        aliases = {item["anchor"]}
        aliases.update(a for a in item.get("related", []) if a not in primary_anchors)
        groups.append({
            "anchor": item["anchor"],
            "aliases": aliases,
            "label": "suppress",
            "state": None,
        })

    if review:
        if len(groups) != 1:
            raise SystemExit(
                f"human-reviewed case {case['id']} must have exactly one scored obligation, "
                f"found {[g['anchor'] for g in groups]}"
            )
        groups[0]["label"] = review["label"]

    return groups


def prediction_map(case, pred):
    if pred is None:
        return {}
    result = {}
    valid_sources = {x["id"] for x in case["sources"]}
    for bucket in ("main", "watching"):
        items = pred.get(bucket, [])
        if not isinstance(items, list):
            raise SystemExit(f"{case['id']}: {bucket} must be a list")
        for item in items:
            anchor = item.get("anchor")
            if anchor not in valid_sources:
                raise SystemExit(f"{case['id']}: unknown predicted anchor {anchor!r}")
            if anchor in result:
                raise SystemExit(f"{case['id']}: anchor predicted more than once: {anchor}")
            result[anchor] = {"bucket": bucket, "state": item.get("state")}
    return result


def group_prediction(group, pred_map):
    matches = [(anchor, pred_map[anchor]) for anchor in group["aliases"] if anchor in pred_map]
    if any(item["bucket"] == "main" for _, item in matches):
        label = "main"
    elif any(item["bucket"] == "watching" for _, item in matches):
        label = "watching"
    else:
        label = "suppress"
    return label, matches


main_tp = main_fp = main_fn = 0
retained_tp = retained_fp = retained_fn = 0
disposition_ok = disposition_total = 0
state_semantic_ok = state_total = 0
state_schema_ok = state_schema_total = 0
duplicate_alias_predictions = 0
orphan_predictions = 0
missing_cases = []
active_overrides = 0

for cid in scored_case_ids:
    case = cases[cid]
    review = reviews.get(cid)
    if review:
        active_overrides += 1
    groups = obligation_groups(case, review)
    pred = preds.get(cid)
    if pred is None:
        missing_cases.append(cid)
    pred_map = prediction_map(case, pred)
    covered_aliases = set().union(*(g["aliases"] for g in groups)) if groups else set()

    for group in groups:
        gold = group["label"]
        predicted, matches = group_prediction(group, pred_map)
        duplicate_alias_predictions += max(0, len(matches) - 1)

        if predicted == "main" and gold == "main":
            main_tp += 1
        elif predicted == "main" and gold != "main":
            main_fp += 1
        elif predicted != "main" and gold == "main":
            main_fn += 1

        gold_retained = gold in {"main", "watching"}
        pred_retained = predicted in {"main", "watching"}
        if pred_retained and gold_retained:
            retained_tp += 1
        elif pred_retained and not gold_retained:
            retained_fp += 1
        elif not pred_retained and gold_retained:
            retained_fn += 1

        disposition_total += 1
        if predicted == gold:
            disposition_ok += 1

        if gold == "main" and predicted == "main" and group.get("state"):
            main_matches = [item for _, item in matches if item["bucket"] == "main"]
            with_state = [item for item in main_matches if item.get("state")]
            if with_state:
                raw_state = with_state[0]["state"]
                state_total += 1
                if canonicalize_state(raw_state) == group["state"]:
                    state_semantic_ok += 1
                state_schema_total += 1
                if raw_state in CANONICAL_STATES:
                    state_schema_ok += 1

    # A surfaced source anchor that is not part of any scored obligation/evidence
    # group is a genuine extra prediction. Context-only source events are otherwise
    # ignored when the model leaves them alone.
    for anchor, item in pred_map.items():
        if anchor in covered_aliases:
            continue
        orphan_predictions += 1
        disposition_total += 1
        if item["bucket"] == "main":
            main_fp += 1
        retained_fp += 1


def ratio(num, den, empty=1.0):
    return num / den if den else empty

main_precision = ratio(main_tp, main_tp + main_fp)
main_recall = ratio(main_tp, main_tp + main_fn)
main_f1 = ratio(2 * main_precision * main_recall, main_precision + main_recall, empty=0.0)
retained_precision = ratio(retained_tp, retained_tp + retained_fp)
retained_recall = ratio(retained_tp, retained_tp + retained_fn)
disposition_acc = ratio(disposition_ok, disposition_total)

print(f"available cases: {len(cases)}")
print(f"scored cases: {len(scored_case_ids)}")
print(f"predicted cases: {len(preds)}")
print(f"human-reviewed overrides in scored set: {active_overrides}")
print("calibration: universal + personal" if args.include_personal_overrides else "calibration: universal only")
print("scope: predicted subset only" if args.only_predicted else "scope: full benchmark")
print(f"main precision: {main_precision:.3f}")
print(f"main recall: {main_recall:.3f}")
print(f"main f1: {main_f1:.3f}")
print(f"retained precision (main + watching): {retained_precision:.3f}")
print(f"retained recall (main + watching): {retained_recall:.3f}")
print(f"disposition accuracy: {disposition_acc:.3f}")
print(f"duplicate evidence-anchor predictions: {duplicate_alias_predictions}")
print(f"orphan predictions: {orphan_predictions}")
if state_total:
    print(f"state category accuracy on matched main predictions: {state_semantic_ok / state_total:.3f}")
if state_schema_total:
    print(f"state schema adherence on matched main predictions: {state_schema_ok / state_schema_total:.3f}")
if missing_cases:
    print(f"missing case predictions: {len(missing_cases)}")
