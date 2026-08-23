#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "open-loops"
errors = []

if (SKILL_DIR / "README.md").exists():
    errors.append("skill package should not contain README.md")

for path in SKILL_DIR.rglob("*"):
    if not path.is_file():
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    if re.search(r"/(Users|home)/[^/]+/", text):
        errors.append(f"absolute user path in {path.relative_to(ROOT)}")
    if "C:\\\\" in text or re.search(r"[A-Za-z]:\\\\", text):
        errors.append(f"Windows absolute path in {path.relative_to(ROOT)}")

skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
for target in re.findall(r"`((?:references|assets)/[^`]+)`", skill):
    if not (SKILL_DIR / target).exists():
        errors.append(f"missing packaged reference: {target}")

# Core judgment should use capability language rather than hard-coded private tool names.
for forbidden in ["gmail.search", "slack.search", "linear.search", "notion.search"]:
    if forbidden in skill.lower():
        errors.append(f"hard-coded host tool name in SKILL.md: {forbidden}")

if errors:
    print("Portability check failed")
    for e in errors:
        print(f"- {e}")
    sys.exit(1)

print("Portability check passed")
