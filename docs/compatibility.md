# Compatibility

Open Loops has one canonical behavior package:

`skills/open-loops/`

Everything else in the repository is a thin distribution or host-compatibility layer.

The goal is to keep the method portable even when installation conventions differ.

## Skills CLI

```bash
npx skills add hnshah/open-loops --skill open-loops
```

## Claude Code

```bash
cp -R skills/open-loops ~/.claude/skills/open-loops
```

The repo also includes `.claude-plugin/` metadata for hosts that support plugin-style installation.

## Codex and `.agents` compatible runtimes

```bash
cp -R skills/open-loops ~/.agents/skills/open-loops
```

The repo includes `.codex-plugin/` and `.agents/plugins/` metadata as thin wrappers around the same `skills/` directory.

## Upload-based hosts

Zip `skills/open-loops/` and upload the folder through the host's skill UI.

Build a clean zip with:

```bash
python3 scripts/package_skill.py
```

## Other agent harnesses

If a harness supports Agent Skills or can instruct an agent to load a `SKILL.md`, point it at the canonical skill directory.

If the harness uses different tool names, do not fork the core judgment rules merely to match those names. Add a small adapter or host note that maps available capabilities to:

- search messages
- read thread history
- read calendar
- read meeting notes
- search files
- inspect project records

The reasoning layer should remain unchanged.

## Grok Bot and computer-using agents

The public skill was designed with persistent computer-using agents in mind. The safest test sequence is still one-time scans first, aggressive correction second, expanded source scope third, preparation fourth, and routine scheduling last.

Do not treat a persistent computer as permission to take external actions automatically.

## OpenClaw and local agents

Local agents are a natural fit because they can combine skill files, local state, and user-controlled connectors. Keep personal feedback and ledgers local unless the user explicitly chooses otherwise.

## Compatibility standard

A host is meaningfully compatible when it can:

1. discover or explicitly load the skill
2. access at least one authorized source
3. search later evidence for resolution
4. preserve source identity for evidence
5. avoid external writes without approval
6. return a bounded evidence-backed list

Installation success alone is not behavioral compatibility.

## Public validation matrix

See [`../evals/HOST_MATRIX.md`](../evals/HOST_MATRIX.md). The matrix stays empty until a configuration has actually been tested.
