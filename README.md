# Open Loops

[![validate](https://github.com/hnshah/open-loops/actions/workflows/validate.yml/badge.svg)](https://github.com/hnshah/open-loops/actions/workflows/validate.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Find the important things that are about to fall through the cracks.**

Your work creates commitments everywhere.

You tell someone you will send something. A customer asks a question. Someone promises to follow up. A meeting creates an action. An introduction waits for a response. A decision stays unresolved.

Most of it never becomes a task.

Open Loops gives an agent one job. Find the important things that still need to happen.

It searches the work sources you authorize, reconstructs unfinished commitments, checks whether they were resolved, and returns the few things most likely to matter. Every surfaced loop includes evidence.

> **Task extraction finds beginnings. Open Loops checks whether they ended.**

## The difference

A weak agent turns communication into a giant task list.

Open Loops is deliberately conservative.

- It searches for evidence of completion before surfacing anything.
- It prefers five high-confidence loops over fifty possible tasks.
- It merges duplicate references to the same real-world obligation.
- It distinguishes what you owe, what you are waiting on, responses, decisions, dependencies, follow-ups, and preparation.
- It treats weak social language and naturally concluded conversations as noise unless context makes them important.
- It does not take external actions without approval.

The intended reaction is simple.

> **I actually forgot about that.**

## Start here

- **Try it:** install the skill and run the seven-day scan below.
- **Understand the idea:** read [`docs/why-open-loops.md`](docs/why-open-loops.md).
- **Understand the technical center:** read [`docs/state-reconstruction.md`](docs/state-reconstruction.md).
- **Implement a host adapter:** read [`docs/architecture.md`](docs/architecture.md) and [`docs/source-adapter-contract.md`](docs/source-adapter-contract.md).
- **Test it:** read [`docs/benchmark-methodology.md`](docs/benchmark-methodology.md) and [`docs/testing-protocol.md`](docs/testing-protocol.md).
- **Contribute a failure:** use the issue templates or [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Try it

Install the skill, give your agent access to at least one real work source, then ask

```text
Find my important open loops from the last seven days.
Use only sources I have authorized.
Do not take external actions.
```

Review the top five. Correct anything it got wrong. Run it again.

That correction loop is part of the product.

## Install

### With the Skills CLI

```bash
npx skills add hnshah/open-loops --skill open-loops
```

The repository uses the standard flat `skills/<name>/SKILL.md` layout so cross-agent installers can discover it directly.

### Claude Code

```bash
cp -R skills/open-loops ~/.claude/skills/open-loops
```

### Codex and other `.agents` compatible runtimes

```bash
cp -R skills/open-loops ~/.agents/skills/open-loops
```

### Claude.ai or another upload-based host

Zip the `skills/open-loops` directory and upload that skill folder through the host's skill UI.

Create a clean installable zip with `python3 scripts/package_skill.py`.

See [`docs/compatibility.md`](docs/compatibility.md) for the portability model, host wrappers, and validation standard.

## What the skill does

```text
source activity
    ↓
obligation candidates
    ↓
search forward for resolution
    ↓
deduplicate into real-world loops
    ↓
rank by importance + urgency + open-state confidence
    ↓
3-5 evidence-backed open loops
```

The core technical idea is **state reconstruction**.

For every candidate, the skill asks two separate questions.

1. What happened that might have created an obligation?
2. What happened later that may have closed, changed, delegated, cancelled, or superseded it?

Only then does it decide whether the loop is still open.

## Example

Synthetic source activity

```text
Thu 9:12 AM  You → Sarah
"I'll send you the revised launch brief tomorrow."

Fri 3:40 PM  Alex → You, Priya
"Hiten, meet Priya. Priya is evaluating this now."

Fri 3:51 PM  Priya → You
"Great to meet you. Are you free Tuesday afternoon?"

Fri 5:18 PM  You → Marco
"I'll send the numbers tonight."

Fri 7:02 PM  You → Marco
"Here are the numbers." [attachment]

Mon 10:00 AM  Calendar
Customer review tomorrow

Mon 10:14 AM  Team chat
"For tomorrow's review, can you bring the churn breakdown?"

Mon 2:00 PM  Jordan → You
"We should grab coffee sometime."
```

Open Loops should surface something like

```markdown
# Open Loops

## 1. Send Sarah the revised launch brief

**Why this is open**
You said Thursday that you would send the revision Friday. No later evidence of delivery was found in the authorized sources.

**Next step**
Send the latest revision or update Sarah on timing.

**I can help**
Locate the latest brief and prepare the message.

**Evidence**
Thu 9:12 AM, message to Sarah

## 2. Respond to Priya's introduction

**Why this is open**
Priya replied to the introduction with a direct scheduling question. No response was found.

**Next step**
Reply with availability.

## 3. Prepare the churn breakdown for tomorrow's customer review

**Why this is open**
The calendar event is tomorrow and the team explicitly asked you to bring the churn breakdown.

**Next step**
Gather the current churn numbers and prepare the review-ready view.

## Probably fine

- Marco numbers. Closed by the later message and attachment.
- Coffee with Jordan. Too weak to treat as a real commitment.
```

The example is intentionally small. See [`examples/demo.md`](examples/demo.md) for the full evidence trail and [`examples/multi-source.md`](examples/multi-source.md) for cross-source closure.

## What counts as an open loop

Open Loops looks for seven kinds of unresolved work.

| Type | Meaning |
| --- | --- |
| I owe | You made an explicit or strongly implied commitment. |
| Waiting on | Someone else committed to deliver something and it has not arrived. |
| Response expected | A question, introduction, approval, escalation, or request reasonably needs your response. |
| Decision unresolved | The conversation reached a real decision point without evidence of a decision. |
| Follow-up | The exchange created a concrete later interaction. |
| Preparation | An upcoming event plus supporting evidence implies work before it happens. |
| Dependency | Progress is blocked on an expected action or missing information. |

It does **not** try to convert every sentence into work.

## Product laws

These are the opinions that make the skill useful.

1. **Evidence before inference.** Every surfaced loop must be traceable to source evidence.
2. **Search for closure.** A candidate is not an open loop until later evidence has been checked.
3. **Precision over exhaustiveness.** Weak candidates stay out of the main list.
4. **Current state over old text.** Later completion, cancellation, delegation, or supersession wins.
5. **One obligation, one loop.** Multiple references collapse into one item.
6. **Importance matters.** A technically real but trivial loop can still be noise.
7. **Uncertainty is useful.** Medium-confidence items can sit in `Probably fine` or `Watching` instead of polluting the top list.
8. **Quiet is valid.** If nothing important remains open, say so.
9. **Prepare freely. Write externally only with approval.** Drafts, research, and preparation are allowed. Sending, publishing, scheduling, deleting, and external mutation require approval.

## Source model

Open Loops does not require a specific vendor or API. It works from capabilities.

Useful capabilities include

- search messages
- read thread history
- read calendar
- read meeting notes
- search files
- inspect project systems

If only one source is available, the skill still runs. It reports the resolution scope so the user knows what could and could not be checked.

See [`references/source-capabilities.md`](skills/open-loops/references/source-capabilities.md).

## Feedback and learning

After a run, correct it in plain language.

```text
1 matters a lot.
2 is already done.
Never surface casual coffee messages.
Anything involving a customer should rank higher.
```

When the runtime supports local files or durable memory, the skill can turn repeated corrections into a small personal rule layer. The public skill keeps universal rules separate from personal judgment.

The repository collects no telemetry.

See [`PRIVACY.md`](PRIVACY.md) and [`references/feedback-and-learning.md`](skills/open-loops/references/feedback-and-learning.md).

## Evals first

This repo treats evals as product code.

The initial public benchmark covers

- explicit promises
- completed promises
- cancelled and superseded commitments
- delegated ownership
- waiting on someone else
- response-required requests
- ambiguous social language
- concrete follow-ups
- upcoming preparation
- duplicate references
- stale obligations
- cross-source completion
- timing errors
- ownership errors

Run the repository checks

```bash
python3 scripts/validate_repo.py
python3 evals/validate_triggers.py
python3 evals/validate_cases.py
```

The benchmark is intentionally synthetic. Do not submit private inbox or Slack data. If you find a failure, sanitize it into the smallest possible case.

See [`evals/README.md`](evals/README.md), [`docs/benchmark-methodology.md`](docs/benchmark-methodology.md), and the currently unclaimed [`evals/HOST_MATRIX.md`](evals/HOST_MATRIX.md).

## Contributing failures

The fastest way to improve Open Loops is to contribute what it got wrong.

Use the issue templates for

- false positive
- missed loop
- ranking failure
- completion failure

Replace names, companies, links, exact amounts, and sensitive details with synthetic placeholders before submitting.

Every behavior change should add or update an eval case.

See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## What this is not

Open Loops is not

- a task manager
- inbox zero
- a universal productivity agent
- an AI chief of staff
- a system that sends messages on its own
- an excuse to turn every conversation into a task

The public wedge stays narrow on purpose.

## Repository structure

```text
open-loops/
├── README.md
├── VERSION
├── AGENTS.md
├── GOVERNANCE.md
├── CODE_OF_CONDUCT.md
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
├── PRIVACY.md
├── .claude-plugin/              # thin distribution metadata
├── .codex-plugin/               # thin distribution metadata
├── .agents/plugins/             # thin cross-agent metadata
├── skills/
│   └── open-loops/
│       ├── SKILL.md             # canonical behavior
│       ├── agents/
│       │   └── openai.yaml
│       ├── references/          # progressive-disclosure judgment rules
│       └── assets/              # routine, brief, feedback, ledger templates
├── docs/                        # public method and architecture
│   └── adr/                     # durable product decisions
├── schemas/                     # optional adapter / runner contracts
├── evals/                       # triggers, state cases, rubric, scorecards
├── examples/                    # single- and multi-source walkthroughs
└── scripts/                     # validation, portability, packaging
```

The skill is the product behavior. The rest of the repository makes that behavior understandable, testable, portable, and safe to improve.

## Documentation map

The README is the front door. The deeper method lives in [`docs/`](docs/README.md), including architecture, state reconstruction, source adapters, benchmarking, testing, routine mode, portability, the agent-job framework, FAQ, roadmap, and architecture decision records.

Structured integration contracts live in [`schemas/`](schemas/README.md).

## What is not proven yet

The repository is deliberately explicit about the remaining unknowns.

- Trigger behavior still needs paired testing across the specific hosts and models people actually use.
- Cross-source completion quality depends on the resolution scope exposed by each runtime.
- Personalization quality depends on whether the runtime can persist user corrections safely.
- Routine ownership should come only after repeated one-time scans prove useful.
- The synthetic benchmark is a regression suite, not evidence of real-inbox precision.

Every real failure should become a sanitized fixture before the public method gets more complicated.

## Status

**v0.2.0 is still an experiment.**

The public question is whether an agent can reliably reconstruct important unfinished work with enough precision that people choose to run it again.

No performance number is claimed yet. The benchmark exists so future claims can be earned.

## License

MIT
