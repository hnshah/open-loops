#!/usr/bin/env python3
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "open-loops"
SKILL = SKILL_DIR / "SKILL.md"
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip() if (ROOT / "VERSION").exists() else None
errors = []

required_root = [
    "README.md", "VERSION", "LICENSE", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md",
    "GOVERNANCE.md", "SECURITY.md", "PRIVACY.md", "CHANGELOG.md",
    "skills/open-loops/SKILL.md", "evals/triggers.jsonl", "evals/cases.jsonl",
    "evals/rubric.md", "evals/benchmark-manifest.json", "docs/README.md",
    "schemas/source-event.schema.json", "schemas/open-loop.schema.json",
    ".claude-plugin/plugin.json", ".codex-plugin/plugin.json",
]
for rel in required_root:
    if not (ROOT / rel).exists():
        errors.append(f"missing required file: {rel}")

skill_version = None
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
        version_match = re.search(r"^\s*version:\s*[\"']?([^\n\"']+)", fm, re.M)
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
        if version_match:
            skill_version = version_match.group(1).strip()

    for target in re.findall(r"`((?:references|assets)/[^`]+)`", text):
        if not (SKILL_DIR / target).exists():
            errors.append(f"broken packaged reference: {target}")

if VERSION and skill_version and VERSION != skill_version:
    errors.append(f"VERSION {VERSION} does not match SKILL metadata version {skill_version}")

for rel in [".claude-plugin/plugin.json", ".claude-plugin/marketplace.json", ".codex-plugin/plugin.json", ".agents/plugins/marketplace.json", "evals/benchmark-manifest.json"]:
    p=ROOT/rel
    if not p.exists():
        continue
    try:
        obj=json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        errors.append(f"invalid JSON {rel}: {e}")
        continue
    if rel.endswith("plugin.json") and obj.get("version") != VERSION:
        errors.append(f"{rel} version {obj.get('version')} does not match VERSION {VERSION}")

for p in (ROOT/"schemas").glob("*.json") if (ROOT/"schemas").exists() else []:
    try:
        json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        errors.append(f"invalid schema JSON {p.relative_to(ROOT)}: {e}")

# Validate repository-local Markdown links. Ignore anchors, web URLs, and mail links.
md_link_re = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
for path in ROOT.rglob("*.md"):
    if ".git" in path.parts:
        continue
    text=path.read_text(encoding="utf-8")
    for raw in md_link_re.findall(text):
        target=raw.split("#",1)[0].strip()
        if not target or target.startswith(("http://","https://","mailto:")):
            continue
        resolved=(path.parent/target).resolve()
        try:
            resolved.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"link escapes repository in {path.relative_to(ROOT)}: {raw}")
            continue
        if not resolved.exists():
            errors.append(f"broken local link in {path.relative_to(ROOT)}: {raw}")

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
print(f"version: {VERSION}")
print(f"SKILL.md lines: {len(SKILL.read_text(encoding='utf-8').splitlines())}")
