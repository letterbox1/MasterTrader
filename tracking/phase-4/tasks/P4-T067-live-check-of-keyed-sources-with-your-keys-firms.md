---
id: P4-T067
kind: task
title: Live check of keyed sources with your keys (FIRMS, ACLED, Finnhub, CryptoPanic, Myfxbook)
phase: 4
type: VERIFY
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
branch: p4/P4-T067-live-check-of-keyed-sources-with-your-keys-firms
pr: ""
doc_sync: []
doc_sync_status: n/a
found_in: ""
created: 2026-10-22
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P4-T067 · Live check of keyed sources with your keys (FIRMS, ACLED, Finnhub, CryptoPanic, Myfxbook)

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

- Branch: `p4/P4-T067-live-check-of-keyed-sources-with-your-keys-firms`
- PR title: `P4-T067: Live check of keyed sources with your keys (FIRMS, ACLED, Finnhub, CryptoPanic, Myfxbook)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T067` run

## Progress log

- 2026-10-22 01:53 · cloud:vm:be04b6ae61f8 · created
