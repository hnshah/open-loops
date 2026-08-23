# Multi-source completion

The hardest Open Loops cases begin in one system and end in another.

This synthetic example demonstrates why the skill searches for closure rather than treating every commitment as a task.

## Source activity

### Slack

`s1` Monday 9:10 AM

You to team

> I will send Nina the pricing appendix after lunch.

`s2` Monday 11:30 AM

Nina to you

> Can you also include the annual plan table?

### Email

`e1` Monday 2:18 PM

You to Nina

> Pricing appendix attached. I included the annual plan table too.

Attachment `pricing-appendix.pdf`

`e2` Monday 2:31 PM

Nina to you

> Perfect, thank you.

## Wrong behavior

```text
Send Nina the pricing appendix.
```

A task extractor sees `s1` and stops.

## Correct behavior

Do not surface the loop.

The commitment began in Slack and closed in email. `e1` contains the expected deliverable and `e2` acknowledges receipt.

## Degraded behavior with Slack-only access

If email is not authorized, the skill may treat the loop as medium-confidence open or suppress it depending on importance. It must say that resolution was checked only in Slack.

It must not claim that no closure exists anywhere.
