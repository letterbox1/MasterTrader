---
id: P2-T062
kind: task
title: Viewport matrix and axe on D06 and the D03 Bots tab
phase: 2
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T041, P2-T042, P2-T043, P0-T053]
requirements: [R2.50]
roadmap_todos: [T2.68]
modules: [M15]
dashboards: [D06, D03]
tools: [pnpm, playwright]
mcp: []
env: []
services: []
branch: p2/P2-T062-verify-viewport-axe-d06-bots
pr: ""
doc_sync: [docs/ui/dashboards/D06-risk.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T062 · Viewport matrix and axe on D06 and the D03 Bots tab

## Goal / expected outcome

D06 (all tabs incl. the Stress placeholder), the D03 Bots tab and the D03 `/strategies/settings` page pass the DESIGN §6.8 Playwright viewport matrix (240 → 2560 px, portrait + landscape, 200% zoom) and axe checks; D01/D03 (non-bot)/D04/D05 are P2-T163's share of T2.68.

## Context & references

- Roadmap: [R2.50](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.68 (D06 + Bots tab part)
- Test matrix: [DESIGN §6.8](../../../DESIGN.md#68-test-matrix-every-screen-must-pass) · [mob §2 phone flows](../../../docs/ui/mobile-and-telegram.md#2-phone-flows-must-be--3-taps-from-a-cold-open)
- Cross-phase (`depends_on`): Playwright matrix harness + axe (P0-T053, T0.64).

## Requirements

- Every viewport in §6.8 incl. 280×653 and 568×320: no horizontal scroll, no overlap, kill switch + mode visible within one tap, touch targets, contrast, 200% zoom reflow.
- axe: 0 serious/critical violations.
- HALT ≥ 56 px on touch viewports; HALT flow ≤ 3 taps from cold open (mob §2).

## ToDo

- [ ] Add routes to the matrix config
- [ ] Fix violations in the owning tasks' code
- [ ] Attach report
- [ ] Record results (numbers, run IDs, screenshots) in the progress log and tick the roadmap ToDo box

## Verification

### Tests
- Playwright matrix + axe in CI.

### Scenarios
- Given 240×320, when D06 Overview loads, then the kill card is first and fully visible without horizontal scroll.

### Stress / failure injection
- n/a: layout tests.

## Acceptance criteria

- [ ] Matrix + axe green for D06 tabs and Bots tab

## Exceptions & edge cases

- Charts in landscape-short fill height (mob §2).

## Cardinal rules (do NOT)

- Do NOT exclude a viewport to get green.
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.

## Doc sync on completion

- `docs/ui/dashboards/D06-risk.md`: note matrix pass.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.68 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T062-verify-viewport-axe-d06-bots`
- PR title: `P2-T062: Viewport matrix and axe on D06 and the D03 Bots tab`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T062` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (Stress placeholder and D03 settings page in the matrix; cross-phase harness dep)
