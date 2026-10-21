---
id: P0-T000
kind: task
title: Short imperative title
phase: 0
type: BUILD
status: backlog
priority: medium
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: []
requirements: []
roadmap_todos: []
modules: []
dashboards: []
branch: p0/P0-T000-short-slug
pr: ""
doc_sync: []
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P0-T000 · Short imperative title

## Goal / expected outcome

One or two sentences: what exists or is true when this is done, and why it matters for the phase exit criteria.

## Context & references

- Roadmap: [R0.xx](../../../docs/roadmap/phase-0-foundations.md) · ToDo T0.xx
- Spec: [03 §x](../../../docs/03-build-spec.md) · Architecture: [02 §x](../../../docs/02-v1-architecture.md)
- Related items: P0-T0xx

## Requirements

- Functional: …
- Non-functional (latency, security, storage, licence): …

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

- Branch: `p0/P0-T000-short-slug`
- PR title: `P0-T000: Short imperative title`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T000` run

## Progress log

- 2026-10-21 00:00 · planner · created
