---
id: P0-B015
kind: gap
title: Roadmap README USER register drops 'Object Lock' from T0.04
phase: 0
type: DOC
status: done
priority: low
size: XS
severity: S4
owner: agent
claimed_by: ""
depends_on: []
requirements: [R0.N4, R0.07]
roadmap_todos: [T0.04]
modules: []
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p0/P0-B015-roadmap-readme-t004-drift
pr: ""
doc_sync: [docs/roadmap/README.md]
doc_sync_status: done
found_in: docs/roadmap/README.md §6 (T0.04 row)
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P0-B015 · Roadmap README USER register drops 'Object Lock' from T0.04

## Goal / expected outcome

The docs agree and the implementing tasks have one unambiguous answer. Suggested fix: Regenerate or edit the register row from the phase doc (the register may be a generated block — fix at the generator if so).

## Context & references

- Found in: `docs/roadmap/README.md §6 (T0.04 row)`
- Related: P0-T006

## Requirements

- **Steps to reproduce:** Compare T0.04 in the phase doc ('with Object Lock … or rest-server --append-only … → R0.N4, R0.07') with the README §6 register row.
- **Expected:** Same wording and requirement links.
- **Actual:** README row omits Object Lock / append-only and R0.07.
- **Impact:** Low: a reader of the register may open a mutable bucket, breaking WORM anchoring.
- **Suggested fix:** Regenerate or edit the register row from the phase doc (the register may be a generated block — fix at the generator if so).

## ToDo

- [x] Decision taken: 17 §D P0-B015 (ratified in 17 §E)
- [x] Docs updated so they agree: roadmap README §6 user-action register T0.04 row (Object Lock / append-only, R0.N4, R0.07) matches the phase doc
- [x] Affected P0 task files reference the resolution: P0-T006
- [x] Regression check owned: doc check: the register row equals the phase-doc ToDo

## Verification

### Tests
- Doc check: grep the listed docs for the conflicting statements; none remain after the fix.

### Scenarios
- Given a developer reads any of the listed docs, then they reach the same answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Listed docs carry the 17 §D P0-B015 decision and agree (checked in the alignment wave, 2026-10-22)
- [x] Implementation owned by: n/a (doc only; P0-T006 is the USER action)
- [x] Root cause noted in the progress log

## Exceptions & edge cases

- If the user decides differently from the suggestion, the affected tasks are updated before they start.

## Cardinal rules (do NOT)

- Do NOT close without updating every listed doc.
- Do NOT edit WORM records to 'fix' data; append a correction instead.

## Doc sync on completion

- `docs/roadmap/README.md`: reconcile as described.

## Branch & PR

- Branch: `p0/P0-B015-roadmap-readme-t004-drift`
- PR title: `P0-B015: fix roadmap README USER register drops 'Object Lock' from T0.04`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-B015` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by 17 §D P0-B015; docs checked: roadmap README §6 user-action register T0.04 row (Object Lock / append-only, R0.N4, R0.07) matches the phase doc. Root cause: the register row was copied before the phase doc gained the Object Lock wording. Implementation owned by n/a (doc only; P0-T006 is the USER action).
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D P0-B015); docs updated: roadmap README §6 user-action register T0.04 row (Object Lock / append-only, R0.N4, R0.07) matches the phase doc; implementation owned by n/a (doc only; P0-T006 is the USER action)
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
