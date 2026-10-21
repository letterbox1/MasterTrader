---
id: P2-T163
kind: task
title: Verify viewport matrix + axe on D01, D03, D04, D05 and approvals
phase: 2
type: VERIFY
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T142, P2-T143, P2-T144, P2-T145, P2-T146, P2-T147, P2-T148, P2-T149]
requirements: [R2.50]
roadmap_todos: [T2.68]
modules: [M15]
dashboards: [D01, D03, D04, D05]
branch: p2/P2-T163-verify-viewport-matrix-axe
pr: ""
doc_sync: [DESIGN.md, docs/ui/README.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T163 · Verify viewport matrix + axe on D01, D03, D04, D05 and approvals

## Goal / expected outcome

All part-B routes (`/`, `/strategies`, `/strategies/new`, `/strategies/:id`, `/lab`, `/lab/backtests/:id`, `/lab/experiments/:id`, `/execution` incl. approvals sheet) pass the full DESIGN.md §6.8 matrix and axe with zero serious/critical violations, as a required CI job. D06 is verified by part A.

## Context & references

- Roadmap: [R2.50](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.68 (D06 portion in part A (P2-T001–T099))
- [DESIGN §6.8](../../../DESIGN.md#68-test-matrix-every-screen-must-pass) · [DESIGN §9 accessibility](../../../DESIGN.md#9-accessibility) · [mob §2 phone flows](../../../docs/ui/mobile-and-telegram.md)

## Requirements

- Viewports: every size in §6.8 (2560×1440 … 240×320) incl. foldable cover 280×653 and phone landscape 568×320.
- Per viewport: no horizontal page scroll (`scrollWidth <= innerWidth`), no clipped/overlapping text or controls, kill switch + mode visible within one tap, touch targets ≥ 44 px on touch, contrast per §2, no fixed element covering content, 200% zoom reflow at 320 CSS px.
- axe: 0 serious/critical; kill switch reachable within 2 tabs of the top bar; focus order follows visual order.
- Phone flows ≤ 3 taps (HALT, approve, check safety, see P&L, close a position) scripted.
- Screenshots stored as CI artefacts; job required for merge on `apps/web`.

## ToDo

- [ ] Extend the P0 Playwright matrix config with the part-B routes and fixtures
- [ ] Script phone flows
- [ ] Fix or file bug items for violations
- [ ] Make the job required

## Verification

### Tests
- Playwright matrix + axe across all routes and viewports.

### Scenarios
- Given 240×320, then the Cockpit shows Safety and Needs-you and the HALT button without horizontal scroll.
- Given 568×320 landscape, then the rail replaces the bottom nav and charts fill height.

### Stress / failure injection
- Run with 4× CPU throttling to catch layout shifts during live updates.

## Acceptance criteria

- [ ] 0 matrix failures across all part-B routes
- [ ] 0 serious/critical axe violations
- [ ] Job required in CI

## Exceptions & edge cases

- Monaco editor on phones is read-only; axe exemptions must be justified per rule in the config.

## Cardinal rules (do NOT)

- Do NOT add blanket axe rule exclusions or skip viewports to get green.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `DESIGN.md` §6.8: note any new automated checks.
- `docs/ui/README.md`: routes covered by the matrix.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.68 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T163-verify-viewport-matrix-axe`
- PR title: `P2-T163: Verify viewport matrix + axe on D01, D03, D04, D05 and approvals`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T163` run · Playwright viewport matrix + axe green

## Progress log

- 2026-10-21 00:00 · planner · created
