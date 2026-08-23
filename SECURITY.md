# Security

Agent skills can influence tool use and can become part of a software supply chain. Treat installation like installing code or an extension, even when the core artifact is Markdown.

## This repository

Open Loops v0.1.0 is instruction-first.

- It contains no runtime network code.
- It contains no credential handling code.
- It does not require secrets.
- It does not pre-approve tools through `allowed-tools`.
- It requires explicit approval before consequential external actions.

The repository scripts are maintainer-side validators for the public files and eval fixtures.

## User source access

The skill uses only sources already authorized through the host agent runtime.

It should not

- request broader permissions merely to improve recall
- copy credentials into prompts or files
- bypass a connector's normal authorization flow
- use an unapproved alternate source when one source fails

## External side effects

Sending, publishing, scheduling, deleting, and external record mutation require explicit user approval.

See `skills/open-loops/references/approval-boundaries.md`.

## Reporting a security issue

Please do not publish exploitable details in a public issue.

Report privately to the repository owner through GitHub's security reporting features when available.
