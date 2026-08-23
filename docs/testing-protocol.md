# Testing protocol

Testing should move from controlled state reconstruction to messy real work in deliberate stages.

## Controlled test 1 — Email only

Goal: determine whether the skill finds unresolved obligations from seven days of email without flooding the user.

Review:

- top-five precision
- completion detection
- direct questions requiring response
- waiting-on items
- duplicate threads

## Controlled test 2 — Chat only

Goal: test casual language, threads, assignments, and weak social phrases.

Watch especially for false positives from “we should,” “maybe,” “sometime,” brainstorming, jokes, and concluded exchanges.

## Controlled test 3 — Calendar + messages

Goal: test preparation inference.

A calendar event alone should not create elaborate speculative work. Supporting message evidence can.

## Controlled test 4 — Cross-source completion

Create the obligation in one source and resolve it in another.

Examples:

- promise in Slack, deliverable in email
- question in email, answer in meeting notes
- preparation request in chat, artifact in files

The expected result is one reconstructed loop or a correctly suppressed closed loop, not duplicate source-level tasks.

## Controlled test 5 — Personalization

1. Run a fixed window.
2. Correct at least five judgments.
3. Persist only clearly durable personal rules if the host supports it and the user wants that.
4. Re-run the same window.
5. Measure whether the changed judgments improve without breaking universal cases.

If run two is not meaningfully better, routine use will be hard to sustain.

## Dogfood protocol

Start with one real source.

For every top result, classify it as:

- correct and important
- correct but unimportant
- already completed
- false positive
- duplicate
- wrong owner
- wrong timing
- bad next step

Then record anything important that was missed.

Turn every meaningful failure into the smallest synthetic eval before adding another general rule.

## Outside tester protocol

Give testers as little instruction as possible.

1. Install Open Loops.
2. Authorize one real source.
3. Ask: `Find my important open loops from the last seven days.`
4. Review the top five.
5. Correct the agent.
6. Run it again.
7. If it remains useful, try it daily for one week.

### After run one

Ask:

- Did it find something you had genuinely forgotten?
- How many of the top five were real?
- Which result was worst?
- What did it miss?

### After day seven

Ask:

- Are you still using it?
- Did you turn it into a routine?
- Did it cause you to complete anything meaningful?
- What would make you stop using it?
- What responsibility would you give the agent next?

## Test the job before the routine

Do not schedule Open Loops because recurring agents are fashionable.

A routine should run a proven scan. Repetition amplifies both usefulness and noise.
