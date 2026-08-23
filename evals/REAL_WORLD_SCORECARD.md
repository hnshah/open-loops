# Real-world scorecard

Use this sheet when dogfooding a real scan. Keep private source content out of the public repo.

## Run metadata

```text
Date:
Repo commit:
Host / model:
Lookback window:
Authorized sources:
Resolution-scope limitations:
Explicit or implicit skill invocation:
```

## Grade the top five

For each surfaced item mark one:

```text
TP-important
TP-unimportant
false-positive
already-completed
duplicate
wrong-owner
wrong-timing
bad-next-step
```

Then record:

```text
Important missed loops:
Anything genuinely forgotten:
Worst result:
Source where closure actually existed, if missed:
```

## Derived metrics

```text
Precision@5 = real open loops in top five / surfaced top five
Importance@5 = important real loops in top five / surfaced top five
Duplicate rate = duplicate surfaced items / surfaced items
```

Do not publish private examples. Convert each meaningful failure into a sanitized synthetic fixture.
