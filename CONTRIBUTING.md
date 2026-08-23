# Contributing

Open Loops improves fastest through failures.

The best contribution is usually a small sanitized case showing a judgment the skill got wrong.

## Good contributions

- false positive the skill should have suppressed
- meaningful loop it missed
- completion evidence it failed to recognize
- ownership transfer it missed
- duplicate loops that should have merged
- bad timing
- bad ranking
- a source-scope mistake
- a clearer universal rule backed by an eval

## Privacy first

Never submit real private inbox, Slack, meeting, CRM, customer, or calendar content.

Before opening an issue or PR, replace

- names
- company names
- email addresses
- URLs
- exact amounts
- account identifiers
- confidential product details
- private document content

with synthetic placeholders.

Keep only the minimum structure required to reproduce the reasoning failure.

## Behavior changes require evals

If a PR changes classification, ranking, completion detection, ownership, or suppression behavior, add or update at least one case in `evals/cases.jsonl`.

Prefer a small failing fixture over a long explanation.

## Keep the public skill small

The public skill should contain universal procedure and baseline judgment.

Do not add

- company-specific priorities
- private data sources
- personal relationship rules
- secrets
- proprietary ranking heuristics learned from private deployments
- vendor-specific tool commands when a capability description is enough

## Pull request checklist

- [ ] The change addresses a real observed or benchmarked failure.
- [ ] The relevant eval case fails before the behavior change and passes after it.
- [ ] `SKILL.md` remains focused and under the Agent Skills size guidance.
- [ ] Detailed material is in `references/` when it does not belong on every run.
- [ ] No secrets or private source material are included.
- [ ] External actions remain approval-gated.
- [ ] `python3 scripts/validate_repo.py` passes.
- [ ] `python3 evals/validate_triggers.py` passes.
- [ ] `python3 evals/validate_cases.py` passes.

## Design rule

Copy structural lessons from other agent skills. Do not copy someone else's domain judgment and call it a method.
