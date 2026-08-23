# Routine mode

Use recurring execution only after one-time scans are already useful.

## Default routine

1. Start from the previous successful run if persistent state exists.
2. Recheck carried-forward high-confidence loops for closure.
3. Inspect new activity since the last run.
4. Add new candidates and search forward for resolution.
5. Merge duplicates with carried-forward items.
6. Return no more than five items that deserve attention now.
7. Keep the approval boundary unchanged.

Use `../assets/routine-instructions.md` as a reusable starting prompt when the host supports routines.

A routine may prepare work, but it must not send, publish, schedule, delete, or mutate external records without explicit approval.
