# Example — Cross-source closure

The obligation begins in chat and closes in email.

## Chat

```text
Mon 09:15  You → team
I'll send Alex the updated deck today.
```

## Email

```text
Mon 16:40  You → Alex
Subject: Updated deck

Here it is. [attachment: updated-deck.pdf]
```

## Expected result

Suppress the loop as completed.

A same-thread-only scanner would falsely surface it. Open Loops should search all authorized later evidence when cross-source closure is plausible.
