# Example — Calendar + messages

Calendar events become preparation loops only when context supports real preparation.

## Sources

```text
Calendar, Tue 10:00
QBR with Acme

Chat, Mon 15:14
For tomorrow's Acme QBR, can you bring the churn breakdown by segment?

Calendar, Thu 17:00
Coffee with Maya
```

## Expected result

Surface one `Prepare` loop for the churn breakdown before the QBR.

Do not infer elaborate preparation for the coffee event without supporting evidence.

This case tests that the agent combines sources without treating every calendar event as work.
