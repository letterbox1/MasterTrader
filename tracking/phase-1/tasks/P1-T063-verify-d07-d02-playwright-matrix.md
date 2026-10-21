---
id: P1-T063
kind: task
title: Verify D07 and D02 acceptance across the viewport matrix
phase: 1
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T048, P1-T049, P1-T050, P1-T051]
requirements: [R1.15]
roadmap_todos: [T1.32]
modules: [M15]
dashboards: [D07, D02]
branch: p1/P1-T063-verify-d07-d02-playwright-matrix
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/ui/dashboards/D07-data-quality.md, docs/ui/dashboards/D02-markets.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P1-T063 · Verify D07 and D02 acceptance across the viewport matrix

## Goal / expected outcome

A single Playwright run covers D07, D02 (matrix and detail) and the notification centre across every DESIGN §6.8 viewport with axe, plus each dashboard's acceptance criteria, and the result is stored as phase evidence.

## Context & references

- Roadmap: requirements [R1.15](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.32](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- [DESIGN §6.8](../../../DESIGN.md#68-test-matrix-every-screen-must-pass) (viewports and pass criteria) · [D07 Data & Quality](../../../docs/ui/dashboards/D07-data-quality.md) acceptance 1–3 · [D02 Markets](../../../docs/ui/dashboards/D02-markets.md) acceptance 1 and 3 (ticket acceptance 2 belongs to P2)
- Depends on (this phase): P1-T048, P1-T049, P1-T050, P1-T051

## Requirements

- Viewports: all of DESIGN §6.8 (desktop 2560×1440 → floor 240×320, portrait + landscape, foldables)
- Pass criteria per viewport: no horizontal scroll, no clipped/overlapping controls, kill switch visible within one tap, touch targets per §6.7, contrast, no fixed element covering content, 200% zoom reflow at 320 px
- D07: stale within 2 s of detection, paid feed blocked, quota warning before throttle; D02: timeframe switch < 500 ms cached; ticket sheet fits 320×568 (disabled in P1)
- Screenshots + axe report under `reports/verify/P1-T063/`

## ToDo

- [ ] Assemble the suite from the per-screen tests and add missing acceptance checks
- [ ] Run on CI and store the report
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Playwright suite as listed

### Scenarios

- Given the 280×653 foldable cover viewport, when D07 loads, then segmented tabs and feed cards render without horizontal scroll

### Stress / failure injection

- n/a: UI verification; load is P1-T062

## Acceptance criteria

- [ ] Suite green on all viewports; report stored
- [ ] CI green (lint, types, tests, Playwright viewport matrix 240→2560 px per DESIGN §6.8, axe)

## Exceptions & edge cases

- Flaky timing tests are fixed, not retried into green

## Cardinal rules (do NOT)

- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.32 once every task traced to it in PHASE.md is done; note P1-T063 next to it.
- `docs/ui/dashboards/D07-data-quality.md` and `docs/ui/dashboards/D02-markets.md`: mark acceptance criteria verified

## Branch & PR

- Branch: `p1/P1-T063-verify-d07-d02-playwright-matrix`
- PR title: `P1-T063: Verify D07 and D02 acceptance across the viewport matrix`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T063` run · viewport matrix + axe green

## Progress log

- 2026-10-21 00:00 · planner · created
