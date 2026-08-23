#!/usr/bin/env python3
from pathlib import Path
import json
import sys

PATH = Path(__file__).with_name("triggers.jsonl")
errors = []
seen = set()
positive = negative = 0

for line_no, raw in enumerate(PATH.read_text(encoding="utf-8").splitlines(), 1):
    if not raw.strip():
        continue
    try:
        item = json.loads(raw)
    except json.JSONDecodeError as e:
        errors.append(f"line {line_no}: invalid JSON: {e}")
        continue
    for field in ["id", "text", "should_trigger", "reason"]:
        if field not in item:
            errors.append(f"line {line_no}: missing {field}")
    iid = item.get("id")
    if iid in seen:
        errors.append(f"line {line_no}: duplicate id {iid}")
    seen.add(iid)
    if not isinstance(item.get("should_trigger"), bool):
        errors.append(f"line {line_no}: should_trigger must be boolean")
    elif item["should_trigger"]:
        positive += 1
    else:
        negative += 1
    if not str(item.get("text", "")).strip():
        errors.append(f"line {line_no}: empty text")

if positive < 10:
    errors.append(f"only {positive} positive trigger cases; expected at least 10")
if negative < 8:
    errors.append(f"only {negative} negative trigger cases; expected at least 8")

if errors:
    print("Trigger validation failed")
    for e in errors:
        print(f"- {e}")
    sys.exit(1)

print(f"Trigger cases are valid: {positive + negative}")
print(f"- should trigger: {positive}")
print(f"- should not trigger: {negative}")
