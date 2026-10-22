---
id: P0-B014
kind: gap
title: D16 routes `/system/security` and `/system/backups` are missing from the IA table
phase: 0
type: DOC
status: done
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
tools: []
mcp: []
env: []
services: []
branch: p0/P0-B014-d16-routes-missing-from-ia
pr: ""
doc_sync: [docs/ui/README.md]
doc_sync_status: done
found_in: docs/ui/README.md §1
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
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

- [x] Decision taken: 17 §D P0-B014 (ratified in 17 §E)
- [x] Docs updated so they agree: ui README §1 D16 row lists `/system`, `/system/audit`, `/system/settings`, `/system/security`, `/system/backups`, matching D16
- [x] Affected P0 task files reference the resolution: P0-T050, P0-T052
- [x] Regression check owned: P0-T053 runs the matrix on all five D16 routes

## Verification

### Tests
- Doc check: grep the listed docs for the conflicting statements; none remain after the fix.

### Scenarios
- Given a developer reads any of the listed docs, then they reach the same answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Listed docs carry the 17 §D P0-B014 decision and agree (checked in the alignment wave, 2026-10-22)
- [x] Implementation owned by: P0-T050 (route stubs), P0-T052
- [x] Root cause noted in the progress log

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
- 2026-10-22 00:00 · aligner · resolved by 17 §D P0-B014; docs checked: ui README §1 D16 row lists `/system`, `/system/audit`, `/system/settings`, `/system/security`, `/system/backups`, matching D16. Root cause: D16 gained routes after the IA table was written. Implementation owned by P0-T050 (route stubs), P0-T052.
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D P0-B014); docs updated: ui README §1 D16 row lists `/system`, `/system/audit`, `/system/settings`, `/system/security`, `/system/backups`, matching D16; implementation owned by P0-T050 (route stubs), P0-T052
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
