#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent
CASES_PATH = ROOT / "cases.jsonl"
RANKING_PATH = ROOT / "ranking-scenarios.jsonl"

cases = {}
for raw in CASES_PATH.read_text(encoding="utf-8").splitlines():
    if raw.strip():
        case = json.loads(raw)
        cases[case["id"]] = case

errors = []
scenario_count = 0
seen = set()

for line_no, raw in enumerate(RANKING_PATH.read_text(encoding="utf-8").splitlines(), 1):
    if not raw.strip():
        continue
    scenario_count += 1
    try:
        scenario = json.loads(raw)
    except json.JSONDecodeError as exc:
        errors.append(f"line {line_no}: invalid JSON: {exc}")
        continue

    sid = scenario.get("id")
    if not sid:
        errors.append(f"line {line_no}: missing id")
    elif sid in seen:
        errors.append(f"line {line_no}: duplicate scenario id {sid}")
    seen.add(sid)

    candidates = scenario.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        errors.append(f"line {line_no}: candidates must be a non-empty list")
        continue
    if len(candidates) != len(set(candidates)):
        errors.append(f"line {line_no}: duplicate candidate ids")
    for cid in candidates:
        if cid not in cases:
            errors.append(f"line {line_no}: unknown case id {cid}")

    display_limit = scenario.get("display_limit")
    if not isinstance(display_limit, int) or display_limit < 1:
        errors.append(f"line {line_no}: display_limit must be a positive integer")

    expected = scenario.get("expected", {})
    main_order = expected.get("main_order", [])
    displayed = expected.get("displayed", [])
    watching = expected.get("watching", [])
    suppress = expected.get("suppress", [])

    for name, bucket in [("main_order", main_order), ("displayed", displayed), ("watching", watching), ("suppress", suppress)]:
        if not isinstance(bucket, list):
            errors.append(f"line {line_no}: expected.{name} must be a list")
            continue
        if len(bucket) != len(set(bucket)):
            errors.append(f"line {line_no}: duplicate ids in expected.{name}")
        for cid in bucket:
            if cid not in candidates:
                errors.append(f"line {line_no}: {cid} in expected.{name} is not a candidate")

    if isinstance(display_limit, int) and displayed != main_order[:display_limit]:
        errors.append(f"line {line_no}: expected.displayed must equal the first display_limit items of main_order")

    if set(main_order) & set(watching):
        errors.append(f"line {line_no}: main_order and watching overlap")
    if set(main_order) & set(suppress):
        errors.append(f"line {line_no}: main_order and suppress overlap")
    if set(watching) & set(suppress):
        errors.append(f"line {line_no}: watching and suppress overlap")

    classified = set(main_order) | set(watching) | set(suppress)
    if classified != set(candidates):
        missing = set(candidates) - classified
        extra = classified - set(candidates)
        if missing:
            errors.append(f"line {line_no}: unclassified candidates: {sorted(missing)}")
        if extra:
            errors.append(f"line {line_no}: unexpected classified candidates: {sorted(extra)}")

if scenario_count < 1:
    errors.append("ranking benchmark has no scenarios")

if errors:
    print("Ranking validation failed")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print(f"Ranking scenarios are valid: {scenario_count}")
