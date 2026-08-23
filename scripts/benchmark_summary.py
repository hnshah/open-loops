#!/usr/bin/env python3
from collections import Counter
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

def load_jsonl(path):
    rows=[]
    for line in path.read_text(encoding="utf-8").splitlines():
        line=line.strip()
        if line:
            rows.append(json.loads(line))
    return rows

cases=load_jsonl(ROOT/"evals"/"cases.jsonl")
triggers=load_jsonl(ROOT/"evals"/"triggers.jsonl")
print(f"state cases: {len(cases)}")
for k,v in sorted(Counter(c.get("category","unknown") for c in cases).items()):
    print(f"  {k}: {v}")
print(f"trigger fixtures: {len(triggers)}")
for k,v in sorted(Counter(str(t.get("should_trigger")).lower() for t in triggers).items()):
    print(f"  {k}: {v}")
