---
title: Architecture
type: architecture
status: in-progress
tags:
  - architecture
  - c
created: {{date}}
updated: {{date}}
---

# Architecture

> Document verified architecture. Mark unknowns instead of guessing.

## System Summary

`{{brief description of the program and its main flow}}`

## Module Map

| Module / file | Responsibility | Public interface | Dependencies |
| --- | --- | --- | --- |
| `{{module}}` | `{{responsibility}}` | `{{header/API}}` | `{{dependencies}}` |

## Data Flow

Describe how inputs move through the program, how state changes, and how results are produced.

## Ownership and Lifetime

Record important allocation, ownership, borrowing, lifetime, and cleanup rules.

## Invariants

- `{{invariant}}` — evidence/source: `{{file_or_test}}`

## Error Handling

Document error propagation, return codes, cleanup behavior, and failure modes.

## Concurrency

Record threads, synchronization, shared state, and relevant assumptions. If there is no concurrency, state that this has been checked.

## Open Questions

- [ ] `{{question_to_investigate}}`

## Related Decisions

- Link relevant notes in [[Decision Index]].
