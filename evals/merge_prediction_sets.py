#!/usr/bin/env python3
from pathlib import Path
import argparse
import json

parser = argparse.ArgumentParser(description="Merge non-overlapping benchmark JSONL files by case_id.")
parser.add_argument("--out", type=Path, required=True)
parser.add_argument("inputs", type=Path, nargs="+")
args = parser.parse_args()

records = {}
for path in args.inputs:
    if not path.exists():
        raise SystemExit(f"input file not found: {path}")
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        item = json.loads(raw)
        cid = item.get("case_id")
        if not cid:
            raise SystemExit(f"missing case_id in {path} line {line_no}")
        if cid in records:
            raise SystemExit(f"duplicate case_id across inputs: {cid}")
        records[cid] = item

args.out.parent.mkdir(parents=True, exist_ok=True)
with args.out.open("w", encoding="utf-8") as handle:
    for cid in sorted(records):
        handle.write(json.dumps(records[cid], ensure_ascii=False) + "\n")

print(f"merged {len(records)} records into {args.out}")
