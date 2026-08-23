#!/usr/bin/env python3
from pathlib import Path
import json
import sys

PATH = Path(__file__).with_name("cases.jsonl")
errors = []
seen_cases = set()
category_counts = {}
case_count = 0

for line_no, raw in enumerate(PATH.read_text(encoding="utf-8").splitlines(), 1):
    if not raw.strip():
        continue
    case_count += 1
    try:
        case = json.loads(raw)
    except json.JSONDecodeError as e:
        errors.append(f"line {line_no}: invalid JSON: {e}")
        continue
    for field in ["id", "category", "as_of", "sources", "expected"]:
        if field not in case:
            errors.append(f"line {line_no}: missing {field}")
    cid = case.get("id")
    if cid in seen_cases:
        errors.append(f"line {line_no}: duplicate case id {cid}")
    seen_cases.add(cid)
    cat = case.get("category")
    category_counts[cat] = category_counts.get(cat, 0) + 1
    sources = case.get("sources", [])
    if not isinstance(sources, list) or not sources:
        errors.append(f"line {line_no}: sources must be a non-empty list")
        continue
    source_ids = [s.get("id") for s in sources]
    if len(source_ids) != len(set(source_ids)):
        errors.append(f"line {line_no}: duplicate source ids")
    if any(not sid for sid in source_ids):
        errors.append(f"line {line_no}: every source needs an id")
    expected = case.get("expected", {})
    for bucket in ["open", "suppressed"]:
        if bucket not in expected or not isinstance(expected[bucket], list):
            errors.append(f"line {line_no}: expected.{bucket} must be a list")
            continue
        for item in expected[bucket]:
            anchor = item.get("anchor")
            if anchor not in source_ids:
                errors.append(f"line {line_no}: {bucket} anchor {anchor!r} not found in sources")
            for rid in item.get("related", []):
                if rid not in source_ids:
                    errors.append(f"line {line_no}: related source {rid!r} not found")
            for rid in item.get("resolution_evidence", []):
                if rid not in source_ids:
                    errors.append(f"line {line_no}: resolution source {rid!r} not found")

if case_count < 50:
    errors.append(f"benchmark has only {case_count} cases; expected at least 50")

if errors:
    print("Eval validation failed")
    for e in errors:
        print(f"- {e}")
    sys.exit(1)

print(f"Eval cases are valid: {case_count}")
for cat in sorted(category_counts):
    print(f"- {cat}: {category_counts[cat]}")
