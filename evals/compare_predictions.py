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
parser.add_argument(
    "--include-personal-overrides",
    action="store_true",
    help="Apply reviewer-specific calibration. Use only when both tested conditions received the matching personal preferences.",
)
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
    if not item.get("case_id") or item.get("scenario_id"):
        continue
    if item.get("scope", "universal") == "personal" and not args.include_personal_overrides:
        continue
    reviews[item["case_id"]] = item


def predictions(path: Path):
    result = {}
    for item in load_jsonl(path):
        result[item["case_id"]] = item
    return result


baseline = predictions(args.baseline)
skill = predictions(args.skill)
selected = [cid for cid in cases if cid in baseline or cid in skill]


def obligation_groups(case, review):
    open_items = list(case["expected"]["open"])
    suppressed_items = list(case["expected"]["suppressed"])
    primary_anchors = {item["anchor"] for item in open_items + suppressed_items}
    groups = []
    for item in open_items:
        aliases = {item["anchor"]}
        aliases.update(a for a in item.get("related", []) if a not in primary_anchors)
        groups.append({"anchor": item["anchor"], "aliases": aliases, "label": "main", "state": item.get("state")})
    for item in suppressed_items:
        aliases = {item["anchor"]}
        aliases.update(a for a in item.get("related", []) if a not in primary_anchors)
        groups.append({"anchor": item["anchor"], "aliases": aliases, "label": "suppress", "state": None})
    if review:
        if len(groups) != 1:
            raise SystemExit(f"human-reviewed case {case['id']} must have exactly one scored obligation")
        groups[0]["label"] = review["label"]
    return groups


def pred_map(item):
    result = {}
    if not item:
        return result
    for bucket in ("main", "watching"):
        for entry in item.get(bucket, []):
            anchor = entry.get("anchor")
            if anchor:
                result[anchor] = {"bucket": bucket, "state": entry.get("state")}
    return result


def group_prediction(group, mapping):
    matches = [(a, mapping[a]) for a in group["aliases"] if a in mapping]
    if any(v["bucket"] == "main" for _, v in matches):
        label = "main"
    elif any(v["bucket"] == "watching" for _, v in matches):
        label = "watching"
    else:
        label = "suppress"
    state = next((v.get("state") for _, v in matches if v["bucket"] == "main" and v.get("state")), "")
    used = ",".join(a for a, _ in matches)
    return label, state, used, max(0, len(matches) - 1)


def short_source(case, anchor):
    event = next((x for x in case["sources"] if x.get("id") == anchor), None)
    if not event:
        return ""
    text = str(event.get("text", "")).replace("|", "\\|").replace("\n", " ")
    return text if len(text) <= 68 else text[:65] + "..."


print("# Prediction comparison")
print()
print(f"Cases in report: {len(selected)}")
print("Calibration: universal + personal" if args.include_personal_overrides else "Calibration: universal only")
print()
print("| Case | Obligation | Accepted anchors | Gold | Baseline | Open Loops | Baseline state | Open Loops state | Baseline used | Open Loops used | Evidence |")
print("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")

baseline_exact = 0
skill_exact = 0
row_count = 0
base_duplicates = 0
skill_duplicates = 0
case_diffs = []

for cid in selected:
    case = cases[cid]
    groups = obligation_groups(case, reviews.get(cid))
    base = pred_map(baseline.get(cid))
    sk = pred_map(skill.get(cid))
    covered = set().union(*(g["aliases"] for g in groups)) if groups else set()
    case_changed = False

    for group in groups:
        b, bs, bu, bd = group_prediction(group, base)
        s, ss, su, sd = group_prediction(group, sk)
        base_duplicates += bd
        skill_duplicates += sd
        if b == group["label"]:
            baseline_exact += 1
        if s == group["label"]:
            skill_exact += 1
        row_count += 1
        if b != s or bs != ss:
            case_changed = True
        aliases = ",".join(sorted(group["aliases"]))
        print(
            f"| {cid} | {group['anchor']} | {aliases} | {group['label']} | {b} | {s} | "
            f"{bs} | {ss} | {bu} | {su} | {short_source(case, group['anchor'])} |"
        )

    # Surface predictions on context-only anchors as explicit extra rows.
    for anchor in sorted((set(base) | set(sk)) - covered):
        b = base.get(anchor, {}).get("bucket", "suppress")
        s = sk.get(anchor, {}).get("bucket", "suppress")
        bs = base.get(anchor, {}).get("state", "") or ""
        ss = sk.get(anchor, {}).get("state", "") or ""
        if b == "suppress":
            baseline_exact += 1
        if s == "suppress":
            skill_exact += 1
        row_count += 1
        if b != s or bs != ss:
            case_changed = True
        print(f"| {cid} | extra:{anchor} | {anchor} | suppress | {b} | {s} | {bs} | {ss} | {anchor if b != 'suppress' else ''} | {anchor if s != 'suppress' else ''} | {short_source(case, anchor)} |")

    if case_changed:
        case_diffs.append(cid)

print()
print("## Summary")
print()
print(f"- Obligation/context rows: {row_count}")
print(f"- Baseline exact disposition matches: {baseline_exact}/{row_count}")
print(f"- Open Loops exact disposition matches: {skill_exact}/{row_count}")
print(f"- Baseline duplicate evidence-anchor predictions: {base_duplicates}")
print(f"- Open Loops duplicate evidence-anchor predictions: {skill_duplicates}")
print(f"- Cases where baseline and Open Loops differ: {', '.join(case_diffs) if case_diffs else 'none'}")
print()
print("Related evidence anchors can represent the same real-world obligation unless that anchor is itself a separately scored obligation. Inspect obligation-level differences before changing SKILL.md.")
