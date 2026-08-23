#!/usr/bin/env python3
from pathlib import Path
import json

PATH = Path(__file__).with_name("cases.jsonl")

for raw in PATH.read_text(encoding="utf-8").splitlines():
    if not raw.strip():
        continue
    case = json.loads(raw)
    blind = {
        "case_id": case["id"],
        "category": case["category"],
        "as_of": case["as_of"],
        "sources": case["sources"],
    }
    if case.get("notes"):
        # Notes can contain grading hints, so never export them into a blind run.
        pass
    print(json.dumps(blind, separators=(",", ":"), ensure_ascii=False))
