# Completion detection

Open Loops is a state reconstruction skill. Candidate extraction is not enough.

Use this reference before deciding that an apparent obligation remains open.

## Resolution procedure

For each candidate

1. Identify the obligation event.
2. State the expected resolution in plain language.
3. Search forward in time from the obligation event.
4. Check the same thread first.
5. Check other authorized sources when closure could plausibly occur there.
6. Determine whether the original obligation is still current.
7. Preserve uncertainty when source scope is incomplete.

## Strong closure signals

Examples

- the promised file, link, answer, or action appears later
- the recipient acknowledges receipt
- the user says it is done
- the requester withdraws the request
- the project is cancelled
- the deadline or expectation is explicitly moved
- another person accepts ownership
- a later decision supersedes the old commitment
- the meeting or event no longer exists and context confirms it was cancelled

## Cross-source closure

An obligation may start in one source and close in another.

Examples

- promise made in Slack, file sent by email
- question asked in email, answered during meeting notes
- task created in a meeting, marked complete in the project system

If the relevant second source is authorized, search it before surfacing the loop.

If it is not available, do not pretend the search was complete. Mention the limited resolution scope when it affects confidence.

## Claimed completion outside the visible scope

A statement such as "sent it to your operations inbox" is evidence of a claimed completion, but it is not proof of receipt when that destination is outside the authorized source set.

In that situation

- do not call the obligation definitely closed
- do not ignore the completion claim and call it definitely open
- preserve the unresolved verification state as `Watching` when it still matters
- state which destination or source could not be checked

If later authorized evidence confirms receipt, close the loop.

## Delegation

Delegation changes ownership.

Example

```text
Mon
You  "I'll handle the pricing analysis."

Tue
You  "Jane is taking the pricing analysis from here."
```

Do not surface `I owe pricing analysis` after the later transfer. If the user still owns oversight and that matters, surface the oversight obligation only when supported by context.

## Supersession

Later instructions can replace earlier ones.

Example

```text
Mon
"Let's finish the report Friday."

Wed
"Skip the report. We are cancelling the project."
```

The old report commitment is closed as obsolete.

## Expired action windows

Some obligations are only useful before a specific event.

Example

```text
Tue
"I'll review the candidate packet before Thursday's debrief."

Thu
Candidate debrief occurs.

Sat
No evidence confirms whether the review happened.
```

Do not keep the old review as an actionable loop merely because completion is unverified. If the action can no longer achieve its intended purpose, treat it as obsolete. Surface a new follow-up only if later evidence creates one, such as a request to revisit the candidate decision.

## Partial completion

Do not close a loop because one subpart happened if the original expected result remains incomplete.

Example

- promised "deck and pricing appendix"
- later sent only the deck

The loop may remain open for the appendix.

## Silence is not closure

Do not infer completion from time passing.

## No same-thread reply is not proof of openness

If authorized sources make cross-source closure plausible, search them.

## Staleness

Old unresolved text is not automatically an active obligation.

Look for project cancellation, changed priorities, later decisions, role changes, expired action windows, or other evidence that makes the candidate obsolete.

When staleness is ambiguous, suppress or mark `Watching` rather than reviving dead work aggressively.
