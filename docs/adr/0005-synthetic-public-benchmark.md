# ADR 0005 — Synthetic public benchmark

**Status:** Accepted

## Context

Real inboxes, chats, meeting notes, calendars, and CRM records contain private and company-sensitive information.

## Decision

The public benchmark uses synthetic fixtures. Real-world failures are reduced to the smallest sanitized case that preserves the reasoning structure.

## Consequences

- the repo does not need invasive telemetry
- contributors can improve failure coverage without donating private corpora
- benchmark cases are inspectable
- aggregate real-world performance claims require a separate explicit protocol
