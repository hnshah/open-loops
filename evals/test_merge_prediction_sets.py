#!/usr/bin/env python3
from pathlib import Path
import json
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
SCRIPT = ROOT / "merge_prediction_sets.py"

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    a = root / "a.jsonl"
    b = root / "b.jsonl"
    out = root / "out.jsonl"
    a.write_text(json.dumps({"case_id": "case_002", "main": [], "watching": []}) + "\n", encoding="utf-8")
    b.write_text(json.dumps({"case_id": "case_001", "main": [], "watching": []}) + "\n", encoding="utf-8")
    subprocess.run([sys.executable, str(SCRIPT), "--out", str(out), str(a), str(b)], check=True, capture_output=True, text=True)
    merged = [json.loads(line) for line in out.read_text(encoding="utf-8").splitlines()]
    assert [item["case_id"] for item in merged] == ["case_001", "case_002"]

    dup = root / "dup.jsonl"
    dup.write_text(json.dumps({"case_id": "case_001"}) + "\n", encoding="utf-8")
    proc = subprocess.run([sys.executable, str(SCRIPT), "--out", str(out), str(b), str(dup)], capture_output=True, text=True)
    assert proc.returncode != 0
    assert "duplicate case_id" in (proc.stdout + proc.stderr)

print("merge prediction set tests passed")
