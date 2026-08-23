# Governance

Open Loops is intentionally opinionated. The repository optimizes for a small set of product laws rather than maximum feature coverage.

## Source of truth

The canonical public behavior lives in:

1. `skills/open-loops/SKILL.md`
2. the skill's `references/`
3. `evals/cases.jsonl` and `evals/triggers.jsonl`
4. architecture decisions in `docs/adr/`

README prose is explanatory. Evals and the skill define behavior.

## Decision rules

A behavior change should usually satisfy all of these:

- it addresses a real failure or a clearly missing class of failure
- it preserves evidence-first state reconstruction
- it improves precision, completion detection, ownership, timing, deduplication, or ranking
- it does not broaden Open Loops into generic task management
- it keeps external writes approval-gated
- it adds or updates an eval when behavior changes

## Maintainer responsibility

Maintainers decide releases, resolve conflicting product laws, review security-sensitive changes, and keep the public skill portable.

The repository does not promise to accept every useful idea. Some ideas belong in host adapters, private personalization, or adjacent projects instead of the universal skill.

## Release standard

A release should not ship until:

- repository validation passes
- trigger fixtures validate
- state-reconstruction fixtures validate
- package creation succeeds
- skill metadata and plugin manifests agree on the version
- new behavior has regression coverage
- documentation does not claim unmeasured performance

See [`docs/roadmap.md`](docs/roadmap.md) for the learning order.
