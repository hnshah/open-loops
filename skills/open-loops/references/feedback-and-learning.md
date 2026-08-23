# Feedback and learning

User corrections are the highest-value signal for personalizing Open Loops.

## Correction types

Useful labels include

- correct
- important
- unimportant
- already completed
- false positive
- duplicate
- missed loop
- bad ownership
- bad timing
- bad ranking

## Immediate behavior

When the user corrects a result

1. update the current scan
2. explain the changed judgment only when useful
3. apply the correction to similar items in the current run
4. do not argue with the user's personal definition of importance

## Durable personal rules

When the runtime supports memory or local files and the user wants the behavior remembered, convert repeated or explicit preferences into a compact personal rule.

Examples

```text
Customers rank above internal requests when urgency is similar.
Do not treat casual coffee language as a commitment.
Introductions with a reply from the introduced person always deserve a response check.
```

Do not store sensitive message content when a generalized rule is enough.

## Optional local feedback log

If the environment supports files and the user wants a local audit trail, use a private local path outside the public skill package, for example

```text
.open-loops/feedback.jsonl
```

Suggested record

```json
{
  "classification": "false_positive",
  "candidate_summary": "Follow up about coffee",
  "reason": "Casual social language was not a commitment",
  "rule_update": "Ignore casual coffee language unless later concretized"
}
```

Do not write private source excerpts into a feedback log unless the user explicitly wants that.

## Universal vs personal

Universal rules include

- explicit promises matter
- completion closes the loop
- duplicates merge
- evidence is required

Personal rules include

- which relationships matter most
- how aggressively to surface social follow-ups
- which projects rank highest
- whether certain request types are important

Keep these layers separable so personal corrections do not degrade the general method.
