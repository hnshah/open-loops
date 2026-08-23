---
name: open-loops
description: Finds important unresolved commitments, requests, decisions, dependencies, follow-ups, and preparation work across authorized work sources. Use when the user asks what they owe, what others owe them, what needs follow-up, what may have been forgotten, what remains unresolved, or what is at risk of falling through the cracks. Not for generic task extraction, project planning, or inbox zero.
license: MIT
compatibility: Requires access to at least one authorized work source such as email, chat, calendar, meeting notes, files, or a project system.
metadata:
  author: hnshah
  version: "0.2.0"
---

# Open Loops

Find the few important pieces of unfinished work that deserve attention now.

## Critical laws

1. **Evidence before inference.** Do not surface a loop without source evidence.
2. **Search for closure before surfacing.** Task extraction is only candidate generation. Check later evidence first.
3. **Precision over exhaustiveness.** Prefer 3-5 high-confidence loops. Default maximum is 10.
4. **Current state wins.** Completion, cancellation, delegation, supersession, rescheduling, or obsolescence closes or changes the original candidate.
5. **One obligation, one loop.** Merge duplicate references across threads and sources.
6. **Do not invent work.** Weak social language, FYIs, ideas, and naturally concluded exchanges are not obligations by default.
7. **Importance is part of correctness.** Do not crowd the top list with trivial but technically unresolved items.
8. **Uncertainty is useful.** Preserve medium-confidence items as `Watching` or `Probably fine` instead of overstating certainty.
9. **Quiet is valid.** If no important loops remain open, say so.
10. **No consequential external action without approval.** You may inspect, analyze, gather, and prepare. Sending, publishing, scheduling, deleting, or mutating external records requires explicit approval.

Before a full scan, read these references only when needed.

- Read `references/what-is-an-open-loop.md` when classification is ambiguous.
- Read `references/completion-detection.md` before judging whether a candidate is still open, especially when later messages or multiple sources exist.
- Read `references/evidence-rules.md` when evidence is partial, contradictory, or hard to link.
- Read `references/judgment-rules.md` when ranking or suppression is difficult.
- Read `references/source-capabilities.md` when choosing tools or degrading to a smaller source scope.
- Read `references/feedback-and-learning.md` when the user corrects a result or asks the skill to remember preferences.
- Read `references/approval-boundaries.md` before any step that could create an external side effect.
- Read `references/routine-mode.md` when the user asks to repeat the scan or turn it into a routine.
- Read `references/state-ledger.md` when the runtime supports durable state and continuity would help.

## Default scope

Unless the user specifies otherwise

- look back 7 days
- inspect the next 7 days of upcoming events if calendar access exists
- use only sources already authorized by the user
- return 3-5 high-confidence loops
- allow expansion up to 10 on request
- take no external write actions

Do not ask setup questions you can answer from the available runtime. Ask only for missing information that is required to proceed.

## Workflow

### 1. Establish the evidence scope

Identify which authorized capabilities are available.

Useful capabilities include

- searching messages
- reading message or thread history
- reading calendar
- reading meeting notes
- searching files
- reading project or CRM-like systems

Record the actual resolution scope internally. If only one source is available, continue with that source and lower confidence when closure could plausibly exist elsewhere.

### 2. Gather obligation candidates

Search the lookback window for evidence of

- promises and commitments
- assignments
- direct requests
- questions requiring response
- deadlines
- decisions waiting to be made
- dependencies
- introductions
- concrete future follow-ups
- upcoming preparation

Candidate generation is broad. Surfacing is narrow.

### 3. Reconstruct current state

For every candidate, determine the expected resolution and search forward from the obligation event to the current time.

Look for evidence that the item was

- completed
- answered
- cancelled
- withdrawn
- superseded
- delegated
- declined
- rescheduled
- acknowledged as received
- made obsolete

Search all available authorized sources when cross-source closure is plausible.

Do not infer that silence means completion. Do not infer that no same-thread reply means the item is still open if another available source could contain closure.

### 4. Determine ownership and state

Classify each remaining candidate into one of these user-facing states.

- **I owe**
- **Waiting on**
- **Response expected**
- **Decision**
- **Follow-up**
- **Prepare**
- **Dependency**
- **Watching**

If ownership moved to someone else, do not keep it as an `I owe` loop.

### 5. Deduplicate

Collapse multiple messages, threads, calendar notes, or documents that refer to the same real-world obligation.

Preserve the strongest evidence and any useful resolution-search trail.

### 6. Rank what matters

Rank qualitatively using

- obligation strength
- open-state confidence
- consequence if forgotten
- urgency or deadline
- whether someone is blocked
- relationship or customer significance supported by context
- recency
- preparation burden
- explicit user preferences learned from prior corrections

Do not expose a fake numeric score.

A real but low-value loop may be omitted from the main list.

### 7. Produce the brief

Default output

```markdown
# Open Loops

## 1. [Specific next obligation]

**State**
[I owe | Waiting on | Response expected | Decision | Follow-up | Prepare | Dependency]

**Why this is open**
[Short evidence-backed explanation of the original obligation and why no valid closure was found.]

**Next step**
[One concrete next action.]

**I can help**
[One preparation action the agent can take without external side effects. Omit if not useful.]

**Evidence**
[Source, timestamp, person/thread, link or source identifier when the runtime provides one.]

**Resolution checked**
[Briefly state what later evidence or source scope was checked when this materially affects trust.]
```

Keep the brief short. Evidence can be one line unless ambiguity requires more.

If helpful, finish with

```markdown
## Probably fine

- [1-3 ambiguous or intentionally suppressed candidates, each with a one-line reason]
```

Do not use `Probably fine` as a dumping ground for dozens of weak candidates.

### 8. Offer preparation, not surprise execution

For surfaced loops, you may offer or perform preparation that stays inside the authorized workspace, such as

- find the latest promised file
- draft a reply
- gather the answer to a question
- prepare a meeting brief
- identify calendar availability
- assemble supporting evidence

Stop before any external side effect unless the user explicitly approves it.

### 9. Learn from corrections

Treat corrections as high-value product data.

Examples

- `1 matters a lot`
- `2 is already done`
- `Never surface casual coffee messages`
- `Anything involving a customer should rank higher`

Apply the correction immediately. If the runtime supports durable memory or local files and the user wants the rule remembered, follow `references/feedback-and-learning.md`.

Keep universal reasoning rules separate from user-specific preferences.

### 10. Add continuity only after the scan earns it

Do not recommend or create recurring ownership merely because the host supports routines. Use `references/routine-mode.md` after several one-time runs are useful. If durable state is appropriate, keep it lightweight and follow `references/state-ledger.md`.

## Refuse or degrade cleanly

### No authorized source access

Explain that Open Loops needs at least one authorized work source. Do not fabricate a scan from conversation context alone unless the user explicitly asks to analyze only the current conversation.

### Partial source access

Run on what is available. State the resolution scope when it materially limits closure detection.

### No important loops found

Say that no high-confidence important open loops were found in the checked scope. Do not fill the answer with low-confidence guesses.

### Ambiguous candidate

Place it in `Watching` or `Probably fine`, or suppress it. Do not promote it merely to make the list longer.

### Completion cannot be verified

State the uncertainty and which source could not be checked. Do not claim closure or openness with false certainty.

### User asks for a generic task list

Open Loops may help identify unresolved obligations, but do not turn the skill into project planning or exhaustive task extraction. If the user wants all possible tasks, explain that this skill is optimized for high-precision unfinished work.

## Final quality check

Before returning a scan, verify

- every surfaced loop has evidence
- later closure was searched for
- completed or obsolete items are suppressed
- ownership is correct
- duplicates are merged
- the main list is ordered by likely importance, not message recency alone
- weak social niceties are not promoted without context
- external actions have not been taken without approval
- the output is short enough to act on
