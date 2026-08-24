#!/usr/bin/env python3
import json
from pathlib import Path
import tempfile

from run_claude_blind import normalize_prediction, load_existing_predictions, keep_completed_raw_records

case = {
    "case_id": "case_test",
    "sources": [
        {"id": "m1", "text": "one"},
        {"id": "m2", "text": "two"},
    ],
}

pred = normalize_prediction(
    {"case_id": "case_test", "main": [{"anchor": "m1", "state": "I owe"}], "watching": ["m2"]},
    case,
)
assert pred == {
    "case_id": "case_test",
    "main": [{"anchor": "m1", "state": "I owe"}],
    "watching": [{"anchor": "m2"}],
}

with tempfile.TemporaryDirectory() as td:
    root = Path(td)
    out = root / "pred.jsonl"
    raw = root / "pred.jsonl.raw"
    out.write_text(
        json.dumps({"case_id": "case_001", "main": [], "watching": []}) + "\n"
        + json.dumps({"case_id": "case_002", "main": [], "watching": []}) + "\n",
        encoding="utf-8",
    )
    raw.write_text(
        json.dumps({"case_id": "case_001", "returncode": 0}) + "\n"
        + json.dumps({"case_id": "case_002", "returncode": 0}) + "\n"
        + json.dumps({"case_id": "case_003", "returncode": 1}) + "\n",
        encoding="utf-8",
    )

    existing = load_existing_predictions(out)
    assert set(existing) == {"case_001", "case_002"}
    keep_completed_raw_records(raw, set(existing))
    remaining_raw = [json.loads(line) for line in raw.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert [item["case_id"] for item in remaining_raw] == ["case_001", "case_002"]

print("Claude runner helper tests passed")
