## What changed

Describe the behavior, documentation, eval, portability, or tooling change.

## Why

Link the observed failure, benchmark case, or concrete user need.

## Validation

- [ ] I added or updated an eval if behavior changed.
- [ ] I did not include private work data, credentials, or secrets.
- [ ] External writes remain approval-gated.
- [ ] `python3 scripts/validate_repo.py` passes.
- [ ] `python3 scripts/check_portability.py` passes.
- [ ] `python3 evals/validate_triggers.py` passes.
- [ ] `python3 evals/validate_cases.py` passes.
- [ ] `python3 scripts/package_skill.py --check` passes.
- [ ] I did not add an unearned performance claim.

## Failure class

If this fixes agent behavior, choose the closest class:

- detection false positive
- detection false negative
- resolution false positive
- resolution false negative
- ownership error
- timing error
- importance error
- duplicate error
- source error
- action error
- personalization error
- other
