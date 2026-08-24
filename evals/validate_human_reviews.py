#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent
REVIEW_PATH = ROOT / "human-reviewed.jsonl"
CASES_PATH = ROOT / "cases.jsonl"

case_ids = {
    json.loads(raw)["id"]
    for raw in CASES_PATH.read_text(encoding="utf-8").splitlines()
    if raw.strip()
}

errors = []
seen = set()
count = 0

for line_no, raw in enumerate(REVIEW_PATH.read_text(encoding="utf-8").splitlines(), 1):
    if not raw.strip():
        continue
    count += 1
    try:
        item = json.loads(raw)
    except json.JSONDecodeError as exc:
        errors.append(f"line {line_no}: invalid JSON: {exc}")
        continue

    cid = item.get("case_id")
    if cid not in case_ids:
        errors.append(f"line {line_no}: unknown case_id {cid!r}")

    if item.get("label") not in {"main", "watching", "suppress"}:
        errors.append(f"line {line_no}: label must be main, watching, or suppress")

    if item.get("scope") not in {"universal", "personal"}:
        errors.append(f"line {line_no}: scope must be universal or personal")

    if not item.get("reviewed_at"):
        errors.append(f"line {line_no}: reviewed_at is required")

    reviewer_count = item.get("reviewer_count")
    if not isinstance(reviewer_count, int) or reviewer_count < 1:
        errors.append(f"line {line_no}: reviewer_count must be a positive integer")

    key = (item.get("scenario_id"), cid)
    if key in seen:
        errors.append(f"line {line_no}: duplicate review key {key}")
    seen.add(key)

if count < 1:
    errors.append("human review file has no records")

if errors:
    print("Human review validation failed")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print(f"Human reviews are valid: {count}")
