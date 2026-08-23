#!/usr/bin/env python3
from pathlib import Path
import argparse
import shutil
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "open-loops"
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
DIST = ROOT / "dist"
OUT = DIST / f"open-loops-skill-v{VERSION}.zip"

parser = argparse.ArgumentParser()
parser.add_argument("--check", action="store_true", help="Build into a temporary path and verify package contents")
args = parser.parse_args()

if not SKILL_DIR.exists():
    raise SystemExit("missing skills/open-loops")

out = OUT
if args.check:
    out = ROOT / f".open-loops-package-check-{VERSION}.zip"

out.parent.mkdir(parents=True, exist_ok=True)
if out.exists():
    out.unlink()

with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as zf:
    for path in sorted(SKILL_DIR.rglob("*")):
        if path.is_file():
            arc = Path("open-loops") / path.relative_to(SKILL_DIR)
            zf.write(path, arc)

with zipfile.ZipFile(out) as zf:
    names = set(zf.namelist())
    required = {"open-loops/SKILL.md"}
    missing = required - names
    if missing:
        raise SystemExit(f"package missing: {sorted(missing)}")
    if any(name.endswith("README.md") for name in names):
        raise SystemExit("package unexpectedly contains README.md")

if args.check:
    out.unlink(missing_ok=True)
    print("Skill package check passed")
else:
    print(out.relative_to(ROOT))
