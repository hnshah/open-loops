# Source capabilities

Open Loops is capability-driven rather than vendor-driven.

Use whatever authorized tools the runtime exposes.

## Capability A

Search messages.

Useful for candidate discovery and cross-thread closure.

## Capability B

Read a thread or conversation history.

Useful for reconstructing sequence and local resolution.

## Capability C

Read calendar.

Useful for deadlines, upcoming events, and preparation loops.

A calendar event by itself is usually not enough to infer preparation work. Pair it with supporting evidence.

## Capability D

Read meeting notes or transcripts.

Useful for assignments, decisions, follow-ups, and context that may close a message-based loop.

## Capability E

Search files.

Useful for checking whether a promised artifact exists or locating material needed for the next step.

Existence of a file does not always prove it was delivered. Distinguish creation from delivery.

## Capability F

Read project, CRM, or ticket systems.

Useful when an explicit work system can confirm ownership, status, or completion.

## Graceful degradation

### One source available

Run the scan. Be precise about what was checked.

### Several sources available

Use cross-source resolution when it can materially change open-state judgment.

### A source fails or is unauthorized

Do not retry through an unapproved route. Do not log in, request credentials, or broaden permissions without the user.

Continue with available sources if the result can still be useful. State the limitation when it affects confidence.

### No source available

Do not pretend to run Open Loops. Ask the user to authorize or provide at least one source, or offer to analyze only materials they explicitly supply in the current conversation.

## Tool neutrality

Do not hardcode vendor-specific tool names into the universal method.

A host may provide the same capability through connectors, MCP, browser use, filesystem access, direct APIs, or native tools. The reasoning contract remains the same.
