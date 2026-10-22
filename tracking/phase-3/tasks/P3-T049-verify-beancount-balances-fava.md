---
id: P3-T049
kind: task
title: Beancount export balances and Fava opens it
phase: 3
type: VERIFY
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T035, P3-T009]
requirements: [R3.10]
roadmap_todos: [T3.63]
modules: [M18]
dashboards: [D15]
tools: [git, uv]
mcp: []
env: []
services: [journal, fava, caddy]
branch: p3/P3-T049-verify-beancount-balances-fava
pr: ""
doc_sync: [docs/roadmap/phase-3-journal-and-tax.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P3-T049 · Beancount export balances and Fava opens it

## Goal / expected outcome

The Beancount export of the real paper-trading period passes `bean-check`, its balances equal journal and recon balances per account/asset, its capital-gain totals match the engine's CGT schedule, and Fava (sidecar) opens it over Tailscale.

## Context & references

- Roadmap: [R3.10, T3.63](../../../docs/roadmap/phase-3-journal-and-tax.md) · export P3-T035 · sidecar P3-T009

## Requirements

- `bean-check` exit 0.
- Per account/asset closing balance = journal holdings (exact) = last recon `ok` row.
- Sum of realised gains in Beancount (via `bean-query`) = engine CGT schedule totals (AUD, exact to the cent).
- Fava loads at `/fava/` within 60 s.

## ToDo

- [ ] Export the paper period
- [ ] Run `bean-check` and comparison queries (script `tools/journal/compare_beancount.py`)
- [ ] Open Fava; screenshot; record results

## Verification

### Tests

- Comparison script output = zero differences.

### Scenarios

- Given an introduced discrepancy in a scratch export, when compared, then the script reports it (negative test).

### Stress / failure injection

- n/a: one-off verification

## Acceptance criteria

- [ ] Zero differences
- [ ] Fava opens; screenshot in PR

## Exceptions & edge cases

- Fava version pinned; renders lot costs.

## Cardinal rules (do NOT)

- Do NOT hand-edit the exported ledger to make it balance.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.63 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T049-verify-beancount-balances-fava`
- PR title: `P3-T049: Beancount export balances and Fava opens it`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T049` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (no decision changes; tools/services filled)
