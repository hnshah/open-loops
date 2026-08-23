# Repository instructions

Open Loops is a narrow public Agent Skill for reconstructing important unfinished obligations from authorized work sources.

When changing this repository

- preserve the one-job boundary
- do not turn it into generic task extraction, inbox zero, project planning, or an AI chief of staff
- keep evidence-before-inference and closure detection above convenience
- prefer suppressing weak candidates over inflating output
- preserve explicit approval before consequential external actions
- add or update an eval for behavior changes
- keep `skills/open-loops/SKILL.md` concise and move detailed method into `references/`
- do not add secrets, private source data, telemetry, or company-specific judgment
- do not add deterministic runtime code unless a repeated failure proves instructions are insufficient

Run before proposing a change

```bash
python3 scripts/validate_repo.py
python3 evals/validate_triggers.py
python3 evals/validate_cases.py
```
