# Human ranking stability — Batch 4

Reviewed: 2026-08-22

This batch reverses presentation order for six previously reviewed pairwise comparisons to test whether the preference survives side order and small wording changes.

## Results

| Stability pair | Original preference | Reversed presentation | Stable? |
| --- | --- | --- | --- |
| Partner memo vs investor introduction | Partner memo | Partner memo | Yes |
| Customer QBR preparation vs production API-key blocker | Customer QBR preparation | Customer QBR preparation | Yes |
| Low-stakes reply due today vs high-consequence decision due in three days | Low-stakes reply due today | Low-stakes reply due today | Yes |
| Customer non-urgent product question vs investor introduction | Customer question | Customer question | Yes |
| Overdue customer promise vs internal pricing blocker | Customer promise | Customer promise | Yes |
| Customer security answer vs overdue candidate references | Customer security answer | Customer security answer | Yes |

**Stability result: 6/6 preferences survived side reversal.**

This is human calibration, not model performance. It supports treating these six pairwise judgments as stable enough to use as calibration fixtures. It does not establish a universal ranking formula.

## Stable signals supported by this batch

- Near-term customer-facing obligations are strong attention candidates.
- An owned obligation can outrank a waiting-on item even when the waiting-on item is overdue.
- Immediacy can outrank larger consequence when the larger-consequence item is still several days away.
- Severe operational blockers can outrank weaker internal blockers.
- A concrete owned deliverable can outrank a relationship-response item.

The mixed-list benchmark still matters because pairwise stability does not imply that all preferences compose into one context-free total order.
