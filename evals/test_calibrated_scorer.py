#!/usr/bin/env python3
from pathlib import Path
import json
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
SCORER = ROOT / "score_calibrated.py"


def score(items, *extra):
    with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False, encoding="utf-8") as f:
        path = Path(f.name)
        for item in items:
            f.write(json.dumps(item) + "\n")
    try:
        proc = subprocess.run(
            [sys.executable, str(SCORER), str(path), "--only-predicted", *extra],
            text=True,
            capture_output=True,
            check=True,
        )
        return proc.stdout
    finally:
        path.unlink(missing_ok=True)


def require(output, text):
    if text not in output:
        raise AssertionError(f"expected {text!r} in scorer output:\n{output}")


# Generic scoring must not assume a reviewer-specific preference that the model
# was never given. case_037 is synthetic suppress, personal calibration Watching.
out = score([{"case_id": "case_037", "main": [], "watching": []}])
require(out, "calibration: universal only")
require(out, "human-reviewed overrides in scored set: 0")
require(out, "disposition accuracy: 1.000")

out = score(
    [{"case_id": "case_037", "main": [], "watching": []}],
    "--include-personal-overrides",
)
require(out, "calibration: universal + personal")
require(out, "human-reviewed overrides in scored set: 1")
require(out, "disposition accuracy: 0.000")

# case_060 is one dependency obligation supported by m2 with m1 as related
# evidence. Anchoring the loop to either evidence event should be accepted.
out = score([
    {"case_id": "case_060", "main": [{"anchor": "m1", "state": "Dependency"}], "watching": []}
])
require(out, "main precision: 1.000")
require(out, "main recall: 1.000")
require(out, "disposition accuracy: 1.000")
require(out, "duplicate evidence-anchor predictions: 0")
require(out, "state category accuracy on matched main predictions: 1.000")

# Surfacing two evidence aliases for the same real-world obligation is a
# duplicate, not two independent obligations.
out = score([
    {
        "case_id": "case_060",
        "main": [{"anchor": "m2", "state": "Dependency"}],
        "watching": [{"anchor": "m1"}],
    }
])
require(out, "disposition accuracy: 1.000")
require(out, "duplicate evidence-anchor predictions: 1")

# case_064 is universally calibrated to Watching. The later claimed-send event
# is related evidence for the same obligation and is a valid evidence anchor.
out = score([
    {"case_id": "case_064", "main": [], "watching": [{"anchor": "m2"}]}
])
require(out, "retained recall (main + watching): 1.000")
require(out, "disposition accuracy: 1.000")

print("Calibrated scorer tests passed")
