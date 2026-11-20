---
id: P1-T078
kind: task
title: mt-connectors crate skeleton: HTTP client, quotas, provenance, pit writer, fixture harness
phase: 1
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: []
requirements: []
roadmap_todos: []
modules: []
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p1/P1-T078-mt-connectors-crate-skeleton-http-client-quotas-
pr: ""
doc_sync: []
doc_sync_status: n/a
found_in: ""
created: 2026-11-20
updated: 2026-11-20
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P1-T078 · mt-connectors crate skeleton: HTTP client, quotas, provenance, pit writer, fixture harness

## Goal / expected outcome

One or two sentences: what exists or is true when this is done, and why it matters for the phase exit criteria.

## Context & references

- Roadmap: [R0.xx](../../../docs/roadmap/phase-0-foundations.md) · ToDo T0.xx
- Spec: [03 §x](../../../docs/03-build-spec.md) · Architecture: [02 §x](../../../docs/02-v1-architecture.md)
- Related items: P0-T0xx

## Requirements

- Functional: …
- Non-functional (latency, security, storage, licence): …
- Tools & access: listed in the front matter (`tools`, `mcp`, `env` names, `services`); `./kanban preflight <ID>` checks them before start.

## ToDo

- [ ] Step 1 …
- [ ] Write tests (see Verification)
- [ ] Update docs listed under Doc sync

## Verification

### Tests
- Unit: …
- Integration: …

### Scenarios
- Given … when … then …

### Stress / failure injection
- … (or "n/a: reason")

## Acceptance criteria

- [ ] …
- [ ] CI green (lint, types, tests, `pit` check, viewport matrix where UI)

## Exceptions & edge cases

- …

## Cardinal rules (do NOT)

- Do NOT bypass `mt_api` / the risk manager / the `pit` API.
- Do NOT commit secrets; do NOT weaken a test to make it pass.
- …

## Doc sync on completion

- `docs/…`: what changes.

## Branch & PR

- Branch: `p1/P1-T078-mt-connectors-crate-skeleton-http-client-quotas-`
- PR title: `P1-T078: mt-connectors crate skeleton: HTTP client, quotas, provenance, pit writer, fixture harness`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T078` run

## Progress log

- 2026-11-20 01:08 · cloud:vm:be04b6ae61f8 · created
