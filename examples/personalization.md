# Example — Personalization after correction

Universal reasoning and personal importance should stay separate.

## Run one

The agent surfaces:

1. Respond to a customer escalation
2. Follow up on a recruiting candidate
3. Confirm an internal lunch
4. Respond to an investor introduction

The user says:

```text
Customers should almost always outrank internal scheduling.
Recruiting candidates matter a lot to me.
Do not treat casual internal meal coordination as an important loop unless someone is blocked.
```

## What should change

The next run should:

- preserve the universal fact that all real obligations still need correct open/closed classification
- rank customer and recruiting items higher for this user
- suppress or demote trivial internal meal coordination

## What should not change

The skill should not rewrite universal ontology so that lunches are never obligations for anyone.

Personal rules belong in the user's durable layer when supported, not in the public skill.
