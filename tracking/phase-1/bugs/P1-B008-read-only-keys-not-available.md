---
id: P1-B008
kind: gap
title: Read-only keys are not available at OANDA, IG, Alpaca or IBKR paper
phase: 1
type: DOC
status: backlog
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R1.12]
roadmap_todos: []
modules: []
dashboards: []
branch: p1/P1-B008-read-only-keys-not-available
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/07-security-notes.md]
doc_sync_status: n/a
found_in: docs/roadmap/phase-1-data-and-monitoring.md T1.02; docs/07-security-notes.md §3
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P1-B008 · Read-only keys are not available at OANDA, IG, Alpaca or IBKR paper

## Goal / expected outcome

07 §3 states the compensating control for full-scope practice credentials (GET-only HTTP allow-list in `mt_monitor`, practice/paper hosts only, separate secrets entries)

## Context & references

- Found in: T1.02 asks for **read-only** keys; [07 §3](../../../docs/07-security-notes.md#3-broker--exchange-keys) says keys are trade-only scoped; OANDA personal tokens, IG API keys, Alpaca paper keys and IBKR logins are not scope-limited
- Related items: P1-T002, P1-T041, P1-T042

## Requirements

- **Where:** T1.02 asks for **read-only** keys; [07 §3](../../../docs/07-security-notes.md#3-broker--exchange-keys) says keys are trade-only scoped; OANDA personal tokens, IG API keys, Alpaca paper keys and IBKR logins are not scope-limited
- **Expected:** 07 §3 states the compensating control for full-scope practice credentials (GET-only HTTP allow-list in `mt_monitor`, practice/paper hosts only, separate secrets entries)
- **Actual:** The requirement cannot be met as written for four of six venues
- **Suggested fix:** Amend T1.02 and 07 §3: read-only where offered (Binance/Bybit testnets), GET-only client enforcement elsewhere (tested in P1-T041/T042)
- **Impact:** False sense of safety if unaddressed (severity S3)

## ToDo

- [ ] Edit T1.02 and 07 §3
- [ ] Update the affected P1 task files if the decision changes their requirements

## Verification

### Tests

- Doc review: the edited sections agree with each other and with the affected task files

### Scenarios

- Given a developer picks up the related task cold, when they read the fixed docs, then there is exactly one interpretation

### Stress / failure injection

- n/a: documentation gap

## Acceptance criteria

- [ ] Docs updated and consistent
- [ ] Root cause and decision noted in the progress log

## Exceptions & edge cases

- Until fixed, related tasks follow the interim rule stated in their own files

## Cardinal rules (do NOT)

- Do NOT resolve by silently picking a number in code; the decision lands in the docs first
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: apply the fix above
- `docs/07-security-notes.md`: apply the fix above

## Branch & PR

- Branch: `p1/P1-B008-read-only-keys-not-available`
- PR title: `P1-B008: Read-only keys are not available at OANDA, IG, Alpaca or IBKR paper`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-B008` run

## Progress log

- 2026-10-21 00:00 · planner · opened
