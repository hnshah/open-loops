# FAQ

## Is Open Loops a task manager?

No. It reconstructs unresolved obligations from work activity. A task manager stores explicit tasks.

## Why not extract every action item?

Because exhaustive inferred task lists become noise. Open Loops optimizes for the few unresolved items that deserve attention.

## Why is completion detection so important?

Detecting “I'll send the deck” is easy. Determining whether the deck was later sent, cancelled, delegated, superseded, or made obsolete is the harder and more valuable problem.

## Does it need multiple sources?

No. One source can be useful. Multiple sources improve closure detection when obligations cross systems.

## What if a loop was completed somewhere the agent cannot access?

The agent should preserve uncertainty and state the resolution-scope limitation when it materially affects trust.

## Does it send follow-ups automatically?

No. The default boundary is inspect, analyze, and prepare. External writes require explicit approval.

## Can it draft the follow-up?

Yes. Preparation is part of the intended action ladder.

## Does it keep my work data?

The repository itself collects no telemetry. What a specific host stores depends on that host. See [`../PRIVACY.md`](../PRIVACY.md).

## Can it remember my preferences?

If the runtime supports durable local memory or files and you want it to, repeated corrections can become personal judgment rules. Those rules should stay separate from the universal public skill.

## Why is there a `Probably fine` section?

To make uncertainty visible without polluting the main list. It should contain at most a few ambiguous candidates, not become a shadow task list.

## What does `Watching` mean?

A possible loop exists, but it is not actionable or certain enough to promote yet. For example, someone promised something tomorrow and tomorrow has not passed.

## Why not use a numerical priority score?

A fake formula can create false precision. The current method uses qualitative judgment until real evidence shows a numerical model improves ranking.

## What is the main success metric?

Whether people choose to run it again. Precision@5 and Importance@5 are the core quality metrics underneath that behavior.

## Can a team use it?

The public method is person-centric, but the state-reconstruction pattern may generalize. Team loops are an adjacent job, not part of the current core.

## Can it scan public promises or social posts?

That is possible in principle, but it is outside the current default source model and should not silently broaden the skill.

## Why are the public evals synthetic?

Private inboxes and chats should not become a public benchmark. Real failures should be sanitized into minimal synthetic cases.

## Is the benchmark proof that the skill works?

No. The public fixtures are a regression suite. Real host/model/source tests are required for performance claims.

## Why include plugin manifests if the core is a skill?

Distribution conventions differ. The manifests are thin wrappers around one canonical skill package, not separate implementations.

## Why keep the skill narrow?

Narrow jobs have clearer triggers, clearer success criteria, better evals, and a better chance of becoming trusted delegated responsibilities.

## What should I contribute?

The most valuable contribution is usually a sanitized failure case that forces the method to improve.
