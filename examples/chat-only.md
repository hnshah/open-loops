# Example — Chat only

Chat is where weak social language and casual brainstorming create many false positives.

## Activity

```text
10:03  Jordan
We should grab coffee sometime.

10:11  You
Yeah definitely.

11:42  Priya
Can you post the launch decision in this channel before 3?

11:44  You
Yep, will do.

13:05  Team
Maybe we should explore a lighter onboarding flow next quarter.

14:32  You
Decision is to ship variant B. Details here: [link]
```

## Expected result

Suppress all three candidate-looking threads:

- coffee is weak social language with no concrete follow-up
- onboarding is speculative ideation
- launch decision was completed before 3

The correct main list can be empty.
