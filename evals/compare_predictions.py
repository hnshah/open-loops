#!/usr/bin/env python3
from pathlib import Path
import argparse
import json

ROOT = Path(__file__).resolve().parent
CASES_PATH = ROOT / "cases.jsonl"
REVIEW_PATH = ROOT / "human-reviewed.jsonl"

parser = argparse.ArgumentParser(description="Compare two Open Loops prediction files against calibrated gold.")
parser.add_argument("baseline", type=Path)
parser.add_argument("skill", type=Path)
args = parser.parse_args()


def load_jsonl(path: Path):
    out = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.strip():
            out.append(json.loads(raw))
    return out


cases = {item["id"]: item for item in load_jsonl(CASES_PATH)}
reviews = {}
for item in load_jsonl(REVIEW_PATH):
    if item.get("case_id") and not item.get("scenario_id"):
        reviews[item["case_id"]] = item["label"]


def predictions(path: Path):
    result = {}
    for item in load_jsonl(path):
        cid = item["case_id"]
        result[cid] = item
    return result


baseline = predictions(args.baseline)
skill = predictions(args.skill)
selected = [cid for cid in cases if cid in baseline or cid in skill]


def gold_for(cid: str):
    case = cases[cid]
    gold = {}
    expected_state = {}
    for item in case["expected"]["open"]:
        gold[item["anchor"]] = "main"
        if item.get("state"):
            expected_state[item["anchor"]] = item["state"]
    for item in case["expected"]["suppressed"]:
        gold[item["anchor"]] = "suppress"
    if cid in reviews:
        anchors = list(gold)
        if len(anchors) == 1:
            gold[anchors[0]] = reviews[cid]
    return gold, expected_state


def pred_map(item):
    result = {}
    states = {}
    if not item:
        return result, states
    for bucket in ("main", "watching"):
        for entry in item.get(bucket, []):
            anchor = entry.get("anchor")
            if anchor:
                result[anchor] = bucket
                if entry.get("state"):
                    states[anchor] = entry["state"]
    return result, states


def label_for(mapping, anchor):
    return mapping.get(anchor, "suppress")


def short_source(case, anchor):
    event = next((x for x in case["sources"] if x.get("id") == anchor), None)
    if not event:
        return ""
    text = str(event.get("text", "")).replace("|", "\\|").replace("\n", " ")
    return text if len(text) <= 72 else text[:69] + "..."


print("# Prediction comparison")
print()
print(f"Cases in report: {len(selected)}")
print()
print("| Case | Anchor | Gold | Baseline | Open Loops | Baseline state | Open Loops state | Evidence anchor |")
print("| --- | --- | --- | --- | --- | --- | --- | --- |")

baseline_exact = 0
skill_exact = 0
row_count = 0
case_diffs = []

for cid in selected:
    gold, expected_state = gold_for(cid)
    base_labels, base_states = pred_map(baseline.get(cid))
    skill_labels, skill_states = pred_map(skill.get(cid))
    anchors = list(dict.fromkeys([*gold.keys(), *base_labels.keys(), *skill_labels.keys()]))
    case_changed = False
    for anchor in anchors:
        g = gold.get(anchor, "suppress")
        b = label_for(base_labels, anchor)
        s = label_for(skill_labels, anchor)
        if b == g:
            baseline_exact += 1
        if s == g:
            skill_exact += 1
        row_count += 1
        if b != s:
            case_changed = True
        print(
            f"| {cid} | {anchor} | {g} | {b} | {s} | "
            f"{base_states.get(anchor, '')} | {skill_states.get(anchor, '')} | {short_source(cases[cid], anchor)} |"
        )
    if case_changed:
        case_diffs.append(cid)

print()
print("## Summary")
print()
print(f"- Anchor disposition rows: {row_count}")
print(f"- Baseline exact disposition matches: {baseline_exact}/{row_count}")
print(f"- Open Loops exact disposition matches: {skill_exact}/{row_count}")
print(f"- Cases where baseline and Open Loops differ: {', '.join(case_diffs) if case_diffs else 'none'}")
print()
print("Use this report to inspect differences before changing SKILL.md. A score drop is not enough evidence to tune behavior without identifying the concrete failure cases.")
