#!/usr/bin/env python3
"""Run the synthetic Open Loops cases through Claude Code without exposing gold labels.

This harness intentionally starts a fresh `claude -p` process per case and runs it
inside a temporary directory that does not contain the eval answer key.

Conditions:
- baseline: case only
- skill: case plus a copy of skills/open-loops; prompt tells Claude to read SKILL.md

The `skill` condition measures instruction lift. Trigger/auto-invocation behavior should
be tested separately in a host-level compatibility run.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "evals" / "cases.jsonl"
SKILL_PATH = ROOT / "skills" / "open-loops"


def blind_cases():
    for raw in CASES_PATH.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        case = json.loads(raw)
        yield {
            "case_id": case["id"],
            "as_of": case["as_of"],
            "sources": case["sources"],
        }


def extract_json(text: str) -> dict:
    stripped = text.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        stripped = "\n".join(lines).strip()
    try:
        value = json.loads(stripped)
        if isinstance(value, dict):
            return value
    except json.JSONDecodeError:
        pass
    start = stripped.find("{")
    end = stripped.rfind("}")
    if start >= 0 and end > start:
        value = json.loads(stripped[start : end + 1])
        if isinstance(value, dict):
            return value
    raise ValueError("Claude output did not contain one parseable JSON object")


def normalize_prediction(value: dict, case: dict) -> dict:
    cid = case["case_id"]
    if value.get("case_id") != cid:
        raise ValueError(f"expected case_id {cid}, got {value.get('case_id')!r}")

    source_ids = {event["id"] for event in case["sources"]}
    result = {"case_id": cid, "main": [], "watching": []}

    for bucket in ("main", "watching"):
        items = value.get(bucket, [])
        if not isinstance(items, list):
            raise ValueError(f"{bucket} must be a list")
        seen = set()
        for item in items:
            if not isinstance(item, dict):
                raise ValueError(f"every {bucket} item must be an object")
            anchor = item.get("anchor")
            if anchor not in source_ids:
                raise ValueError(f"unknown anchor {anchor!r} in {bucket}")
            if anchor in seen:
                raise ValueError(f"duplicate anchor {anchor!r} in {bucket}")
            seen.add(anchor)
            normalized = {"anchor": anchor}
            if item.get("state"):
                normalized["state"] = item["state"]
            result[bucket].append(normalized)

    overlap = {x["anchor"] for x in result["main"]} & {x["anchor"] for x in result["watching"]}
    if overlap:
        raise ValueError(f"anchors cannot be both main and watching: {sorted(overlap)}")
    return result


def make_prompt(case: dict, condition: str) -> str:
    skill_instruction = ""
    if condition == "skill":
        skill_instruction = (
            "Before judging the case, read skills/open-loops/SKILL.md in the current directory "
            "and follow it. Read its referenced files only when its instructions call for them.\n\n"
        )

    payload = json.dumps(case, ensure_ascii=False, indent=2)
    return f"""You are running one blind Open Loops benchmark case.

{skill_instruction}Use only the source events in the case. Do not browse, search for outside facts, or inspect files outside the current directory.

Decide which source anchor, if any, represents an unresolved obligation that belongs in the primary Open Loops list now. Put meaningful latent state that should be retained but not promoted now in `watching`. Anything omitted from both buckets is treated as suppressed for scoring.

Return exactly one JSON object and no prose:
{{"case_id":"{case['case_id']}","main":[{{"anchor":"m1","state":"I owe"}}],"watching":[]}}

Use only source IDs that appear in the case. `main` and `watching` may be empty. Do not invent an obligation merely to fill a bucket.

CASE
{payload}
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--condition", choices=["baseline", "skill"], required=True)
    parser.add_argument("--out", required=True, help="prediction JSONL output path")
    parser.add_argument("--raw-out", help="optional raw Claude output JSONL path")
    parser.add_argument("--model", help="optional Claude Code model selector")
    parser.add_argument("--limit", type=int, default=0, help="run only the first N cases; 0 means all")
    args = parser.parse_args()

    if shutil.which("claude") is None:
        print("claude executable not found on PATH", file=sys.stderr)
        return 2
    if args.condition == "skill" and not SKILL_PATH.exists():
        print(f"skill directory not found: {SKILL_PATH}", file=sys.stderr)
        return 2

    cases = list(blind_cases())
    if args.limit:
        cases = cases[: args.limit]

    out_path = Path(args.out)
    raw_path = Path(args.raw_out) if args.raw_out else out_path.with_suffix(out_path.suffix + ".raw")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    raw_path.parent.mkdir(parents=True, exist_ok=True)

    with out_path.open("w", encoding="utf-8") as pred_file, raw_path.open("w", encoding="utf-8") as raw_file:
        for index, case in enumerate(cases, 1):
            with tempfile.TemporaryDirectory(prefix="open-loops-blind-") as temp_dir:
                temp = Path(temp_dir)
                if args.condition == "skill":
                    target = temp / "skills" / "open-loops"
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copytree(SKILL_PATH, target)

                cmd = ["claude", "-p", make_prompt(case, args.condition)]
                if args.model:
                    cmd.extend(["--model", args.model])

                proc = subprocess.run(
                    cmd,
                    cwd=temp,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                raw_record = {
                    "case_id": case["case_id"],
                    "returncode": proc.returncode,
                    "stdout": proc.stdout,
                    "stderr": proc.stderr,
                }
                raw_file.write(json.dumps(raw_record, ensure_ascii=False) + "\n")
                raw_file.flush()

                if proc.returncode != 0:
                    print(f"{case['case_id']}: Claude exited {proc.returncode}; see {raw_path}", file=sys.stderr)
                    return proc.returncode or 1
                try:
                    prediction = normalize_prediction(extract_json(proc.stdout), case)
                except Exception as exc:
                    print(f"{case['case_id']}: {exc}; see {raw_path}", file=sys.stderr)
                    return 1

                pred_file.write(json.dumps(prediction, ensure_ascii=False) + "\n")
                pred_file.flush()
                print(f"[{index}/{len(cases)}] {case['case_id']}", file=sys.stderr)

    print(f"wrote {len(cases)} predictions to {out_path}")
    print(f"wrote raw outputs to {raw_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
