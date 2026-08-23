# Source adapter contract

The core skill does not require a specific API.

This document defines an optional normalized contract for runners, host adapters, and test harnesses that want to feed source activity into Open Loops consistently.

The contract is deliberately small. It describes evidence, not a new productivity database.

## Capability discovery

An adapter should be able to report which of these capabilities are available.

```text
search_messages
read_thread
read_calendar
read_meeting_notes
search_files
read_project_records
```

A host may expose more. Open Loops should reason in capability terms rather than vendor tool names.

## Normalized source event

Use [`../schemas/source-event.schema.json`](../schemas/source-event.schema.json) when a runner needs a portable event shape.

Important fields:

- `id` — stable within the scan
- `type` — email, chat, calendar, meeting note, file, project record, or other
- `timestamp` — source timestamp with timezone
- `author` and `participants` when known
- `thread_id` when messages belong to a thread
- `title` and/or `text`
- `source_ref` — a deep link, opaque host identifier, or safe locator
- `attachments` — metadata only unless the host authorizes reading content

Do not flatten away source identity. Evidence provenance is part of the product.

## Ordering

Adapters should preserve source timestamps and avoid silently reordering events by ingestion time.

For recurring runs, a host may keep a cursor, but a cursor must not prevent searching backwards or forwards when a candidate requires resolution evidence outside the incremental window.

## Resolution scope

Every scan should know what it was actually able to check.

Example:

```json
{
  "messages": ["email", "slack"],
  "calendar": true,
  "meeting_notes": false,
  "files": true,
  "project_records": false
}
```

The agent does not need to show this object verbatim. It should mention limitations when they materially affect certainty.

## Identity

Do not assume display names uniquely identify people.

A host adapter may provide stable person IDs internally. Public outputs should use human-readable names or roles where appropriate and avoid leaking raw identifiers.

## Attachments and files

An attachment sent after a promise can be powerful completion evidence.

Adapters should expose enough metadata to establish that a file or link was actually sent. Reading the file body is only necessary when resolution depends on its contents and the user has authorized that access.

## Side effects

Source adapters used by the core scan should be read-oriented.

If a host also exposes send, create, update, delete, schedule, or publish capabilities, those remain outside the default scan and must respect the approval boundary in the skill.

## Failure behavior

When a source is unavailable or an auth scope expires:

1. continue with remaining sources if useful
2. record the missing resolution scope
3. lower certainty where appropriate
4. do not claim exhaustive closure search
5. do not ask the user to reconnect a source unless that access is genuinely required for the requested result
