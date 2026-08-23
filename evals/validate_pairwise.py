#!/usr/bin/env python3
from pathlib import Path
import json
import sys

PATH = Path(__file__).with_name("pairwise-preferences.jsonl")
errors = []
seen = set()
count = 0

for line_no, raw in enumerate(PATH.read_text(encoding="utf-8").splitlines(), 1):
    if not raw.strip():
        continue
    count += 1
    try:
        item = json.loads(raw)
    except json.JSONDecodeError as exc:
        errors.append(f"line {line_no}: invalid JSON: {exc}")
        continue

    pid = item.get("id")
    if not pid:
        errors.append(f"line {line_no}: missing id")
    elif pid in seen:
        errors.append(f"line {line_no}: duplicate id {pid}")
    seen.add(pid)

    for side in ["left", "right"]:
        value = item.get(side)
        if not isinstance(value, dict):
            errors.append(f"line {line_no}: {side} must be an object")
            continue
        for field in ["key", "text"]:
            if not value.get(field):
                errors.append(f"line {line_no}: {side}.{field} is required")

    if item.get("preferred") not in {"left", "right", "tie"}:
        errors.append(f"line {line_no}: preferred must be left, right, or tie")

    if not item.get("dimension"):
        errors.append(f"line {line_no}: dimension is required")

    reviewer_count = item.get("reviewer_count")
    if not isinstance(reviewer_count, int) or reviewer_count < 1:
        errors.append(f"line {line_no}: reviewer_count must be a positive integer")

if count < 1:
    errors.append("pairwise benchmark has no preferences")

if errors:
    print("Pairwise validation failed")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print(f"Pairwise preferences are valid: {count}")
