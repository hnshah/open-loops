# State reconstruction

Open Loops treats unfinished work as a temporal state-reconstruction problem.

Task extraction asks:

> Did a sentence create a possible action?

Open Loops asks:

> Given everything we are allowed to inspect after that event, what is the current state of the underlying obligation?

## The state transition

```text
obligation event
    ↓
expected resolution
    ↓
search later evidence
    ↓
completion / cancellation / delegation / supersession / reschedule / no closure
    ↓
current owner + current state
    ↓
importance judgment
    ↓
surface, watch, or suppress
```

## 1. Find the obligation event

Candidate events include promises, requests, assignments, direct questions, deadlines, introductions, decisions, follow-ups, dependencies, and preparation signals.

Candidate generation should be permissive. Promotion should be conservative.

## 2. Define the expected resolution

The same wording can imply different endings.

| Event | Expected resolution |
| --- | --- |
| “I'll send the deck tomorrow.” | Deck or equivalent deliverable sent, commitment withdrawn, delegated, or made obsolete |
| “Can you approve this?” | Approval, rejection, delegation, cancellation, or explicit decision that approval is unnecessary |
| “Let's reconnect after launch.” | A later follow-up when the triggering condition has occurred |
| “I'll introduce you to Priya.” | Introduction made or commitment withdrawn |
| Customer review tomorrow + “bring churn breakdown” | Preparation completed or event changed/cancelled |

Without an expected resolution, an agent cannot search intelligently for closure.

## 3. Search forward, not only inside the original thread

Closure can appear as:

- an attachment sent later
- a link shared in another channel
- explicit “done” language
- recipient acknowledgement
- another person taking ownership
- a new deadline
- request withdrawal
- project cancellation
- evidence the underlying work happened elsewhere

The search scope should follow available authorized capabilities. Same-thread search is a useful first pass, not a proof of openness.

## 4. Apply current-state precedence

Later valid evidence beats older obligation text.

A practical precedence rule is:

1. verified completion
2. verified cancellation or obsolescence
3. verified ownership transfer
4. verified reschedule or changed expectation
5. still-open evidence
6. uncertainty

This is not a claim that every source is equally trustworthy. Evidence quality still matters.

## 5. Separate ownership from existence

An obligation can still exist after it stops belonging to the user.

Examples:

- “I'll handle it.” → later “Jane is taking this.”
- User asks a vendor for a contract → user is waiting, not owing.
- A manager asks a teammate to own an item → user may need to track it, but it is not an `I owe` item.

Ownership errors are especially damaging because they turn useful memory into fake work.

## 6. Deduplicate the real-world obligation

Messages are evidence. They are not the unit of output.

Three messages about the same promised deck should become one loop with an evidence trail, not three tasks.

## 7. Preserve partial observability

Open Loops often cannot inspect every system where closure might have happened.

When source access is partial:

- run on the available evidence
- lower certainty when missing sources plausibly contain closure
- state the resolution scope when it materially affects trust
- never convert “I could not find it here” into “it definitely did not happen”

## 8. Quiet is a valid result

If every candidate closes, becomes obsolete, or stays too ambiguous, the correct output can be an empty main list.

The system should not manufacture work to make the scan feel productive.

## The difficult cases

The benchmark intentionally concentrates on cases where reasonable models disagree:

- soft social language
- partial completion
- cross-source closure
- implied preparation
- timing before a follow-up is due
- delegation without explicit “you no longer own this” wording
- stale obligations after project changes
- multiple messages describing one underlying obligation

These are the cases that separate open-loop reconstruction from generic action-item extraction.
