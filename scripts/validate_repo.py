#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "open-loops"
SKILL = SKILL_DIR / "SKILL.md"

errors = []

required_root = [
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "PRIVACY.md",
    "CHANGELOG.md",
    "skills/open-loops/SKILL.md",
    "evals/triggers.jsonl",
    "evals/cases.jsonl",
    "evals/rubric.md",
]
for rel in required_root:
    if not (ROOT / rel).exists():
        errors.append(f"missing required file: {rel}")

if SKILL.exists():
    text = SKILL.read_text(encoding="utf-8")
    lines = text.splitlines()
    if len(lines) > 500:
        errors.append(f"SKILL.md is {len(lines)} lines; keep it at or below 500")
    if not text.startswith("---\n"):
        errors.append("SKILL.md must start with YAML frontmatter")
    parts = text.split("---", 2)
    if len(parts) < 3:
        errors.append("SKILL.md frontmatter is not closed")
    else:
        fm = parts[1]
        name_match = re.search(r"^name:\s*([^\n]+)$", fm, re.M)
        desc_match = re.search(r"^description:\s*([^\n]+)$", fm, re.M)
        if not name_match:
            errors.append("frontmatter missing name")
        else:
            name = name_match.group(1).strip().strip('"')
            if name != SKILL_DIR.name:
                errors.append(f"name {name!r} must match parent directory {SKILL_DIR.name!r}")
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
                errors.append(f"invalid skill name: {name}")
            if len(name) > 64:
                errors.append("skill name exceeds 64 characters")
        if not desc_match:
            errors.append("frontmatter missing one-line description")
        else:
            desc = desc_match.group(1).strip().strip('"')
            if not desc or len(desc) > 1024:
                errors.append(f"description length invalid: {len(desc)}")
            if "Use when" not in desc:
                errors.append("description should include explicit 'Use when' routing text")

    # Resolve Markdown links that point inside the skill package.
    for target in re.findall(r"\]\((references/[^)#]+)\)", text):
        if not (SKILL_DIR / target).exists():
            errors.append(f"broken skill reference: {target}")

# Basic secret smell check. This is not a security scanner.
secret_patterns = [
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
]
for path in ROOT.rglob("*"):
    if not path.is_file() or ".git" in path.parts:
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    for pat in secret_patterns:
        if pat.search(text):
            errors.append(f"possible secret-like token in {path.relative_to(ROOT)}")

if errors:
    print("Repository validation failed")
    for e in errors:
        print(f"- {e}")
    sys.exit(1)

print("Repository is valid")
print(f"SKILL.md lines: {len(SKILL.read_text(encoding='utf-8').splitlines())}")
