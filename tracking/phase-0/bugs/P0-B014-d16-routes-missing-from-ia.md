---
id: P0-B014
kind: gap
title: D16 routes `/system/security` and `/system/backups` are missing from the IA table
phase: 0
type: DOC
status: ready
priority: low
size: XS
severity: S4
owner: agent
claimed_by: ""
depends_on: []
requirements: [R0.11]
roadmap_todos: [T0.26]
modules: []
dashboards: []
branch: p0/P0-B014-d16-routes-missing-from-ia
pr: ""
doc_sync: [docs/ui/README.md]
doc_sync_status: n/a
found_in: docs/ui/README.md §1
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P0-B014 · D16 routes `/system/security` and `/system/backups` are missing from the IA table

## Goal / expected outcome

The docs agree and the implementing tasks have one unambiguous answer. Suggested fix: Add the two routes to ui §1.

## Context & references

- Found in: `docs/ui/README.md §1`
- Related: P0-T052, P0-T051
- [D16 System](../../../docs/ui/dashboards/D16-system.md)

## Requirements

- **Steps to reproduce:** Compare ui §1 D16 row routes with D16-system.md routes.
- **Expected:** Same route list in both.
- **Actual:** ui §1 lists `/system`, `/system/audit`, `/system/settings`; D16 also has `/system/security`, `/system/backups`.
- **Impact:** Low: nav/palette may omit two pages.
- **Suggested fix:** Add the two routes to ui §1.

## ToDo

- [ ] Confirm the decision with the user (or take the suggested fix if no objection)
- [ ] Update the listed docs so they agree
- [ ] Update the affected P0 task files' Context if the decision differs from the suggestion
- [ ] Add/adjust a regression check where one is possible (see Verification)

## Verification

### Tests
- Doc check: grep the listed docs for the conflicting statements; none remain after the fix.

### Scenarios
- Given a developer reads any of the listed docs, then they reach the same answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [ ] Listed docs updated and consistent
- [ ] Affected tasks reference the resolution
- [ ] Root cause (how the drift happened) noted in the progress log

## Exceptions & edge cases

- If the user decides differently from the suggestion, the affected tasks are updated before they start.

## Cardinal rules (do NOT)

- Do NOT close without updating every listed doc.
- Do NOT edit WORM records to 'fix' data; append a correction instead.

## Doc sync on completion

- `docs/ui/README.md`: reconcile as described.

## Branch & PR

- Branch: `p0/P0-B014-d16-routes-missing-from-ia`
- PR title: `P0-B014: fix d16 routes `/system/security` and `/system/backups` are missing from the IA table`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-B014` run

## Progress log

- 2026-10-21 00:00 · planner · opened
