# Demo

This example is synthetic. It exists to make the product contract inspectable without using private data.

## Source activity

### Email

`e1` Thursday 9:12 AM

You to Sarah

> I'll send you the revised launch brief tomorrow.

`e2` Friday 3:40 PM

Alex to you and Priya

> Hiten, meet Priya. Priya is evaluating this now.

`e3` Friday 3:51 PM

Priya to you

> Great to meet you. Are you free Tuesday afternoon?

`e4` Friday 5:18 PM

You to Marco

> I'll send the numbers tonight.

`e5` Friday 7:02 PM

You to Marco

> Here are the numbers.

Attachment `numbers.xlsx`

### Calendar

`c1` Monday 10:00 AM

Customer review Tuesday 11:00 AM

### Team chat

`s1` Monday 10:14 AM

Taylor to you

> For tomorrow's review, can you bring the churn breakdown?

`s2` Monday 2:00 PM

Jordan to you

> We should grab coffee sometime.

## Expected reconstruction

### Sarah

Anchor `e1` created an explicit promise. No later evidence in the checked sources shows delivery. Surface.

### Priya

`e2` created the introduction. `e3` created a direct scheduling question. No reply was found. Surface.

### Marco

`e4` created a promise. `e5` plus the attachment closes it. Suppress.

### Customer review

`c1` establishes the upcoming event. `s1` explicitly creates preparation work. Surface.

### Jordan

`s2` is weak social language without a concrete next step. Suppress by default.

## Expected output

```markdown
# Open Loops

## 1. Send Sarah the revised launch brief

**State**
I owe

**Why this is open**
You told Sarah Thursday that you would send the revised launch brief Friday. No later evidence of delivery was found in the checked sources.

**Next step**
Send the latest revision or update Sarah on timing.

**I can help**
Locate the latest brief and prepare the message.

**Evidence**
Email e1, Thursday 9:12 AM

**Resolution checked**
Later email and team chat activity in the authorized scope.

## 2. Respond to Priya's introduction

**State**
Response expected

**Why this is open**
Priya replied to the introduction with a direct scheduling question. No response was found.

**Next step**
Reply with availability.

**Evidence**
Email e3, Friday 3:51 PM

## 3. Prepare the churn breakdown for tomorrow's customer review

**State**
Prepare

**Why this is open**
The customer review is tomorrow and Taylor explicitly asked you to bring the churn breakdown.

**Next step**
Gather the current churn data and prepare a review-ready view.

**Evidence**
Calendar c1 and team chat s1

## Probably fine

- Marco numbers. Closed by e5 and the attachment.
- Coffee with Jordan. Too weak and unconcretized to treat as a commitment.
```
