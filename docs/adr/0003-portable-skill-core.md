# ADR 0003 — Portable skill core, thin host adapters

**Status:** Accepted

## Context

Agent hosts expose different connectors, MCP servers, tool names, plugin manifests, and installation paths.

## Decision

Keep universal reasoning in one canonical Agent Skill. Treat host-specific metadata and adapters as thin shells that map available capabilities to the same method.

## Consequences

- no vendor-specific tool names in universal judgment rules when capability language is enough
- plugin manifests may exist without becoming separate implementations
- source adapters should report evidence scope rather than change ontology
- portability regressions are testable repository failures
