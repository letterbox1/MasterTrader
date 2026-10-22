---
id: P4-T059
kind: task
title: D08 and tier-B overlays: Playwright viewport matrix and axe
phase: 4
type: VERIFY
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T044, P4-T045, P4-T046, P4-T062, P4-T065]
requirements: [R4.13]
roadmap_todos: []
modules: [M15]
dashboards: [D08, D01, D02]
tools: [pnpm, node>=20, git]
mcp: []
env: []
services: [mt-api]
branch: p4/P4-T059-verify-d08-viewport-axe
pr: ""
doc_sync: [docs/ui/dashboards/D08-intel.md, docs/roadmap/phase-4-intel.md]
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

# P4-T059 · D08 and tier-B overlays: Playwright viewport matrix and axe

## Goal / expected outcome

D08 (all tabs + document sheet + label mode) and the new D01/D02 tier-B/overlay elements and live positioning/nowcast widgets (P4-T065) pass the DESIGN.md §6.8 viewport matrix (240 → 2560 px, portrait + landscape) and axe with zero serious/critical violations; the feed stays smooth at 1,000+ items on the phone profile.

## Context & references

- Roadmap: [R4.13](../../../docs/roadmap/phase-4-intel.md#3-requirements) (verified by Playwright)
- Test matrix: [DESIGN §6.8](../../../DESIGN.md#68-test-matrix-every-screen-must-pass) · [D08 acceptance](../../../docs/ui/dashboards/D08-intel.md)

## Requirements

- Every tier from DESIGN §6.8; map only ≥ md; filters in a sheet on phones.
- Performance budget: feed scroll ≥ 50 fps median on the mid-phone profile with 1,000 items.

## ToDo

- [ ] Playwright specs per tier.
- [ ] axe checks.
- [ ] Performance trace capture.

## Verification

### Tests
- The Playwright + axe suite.

### Scenarios
- Given landscape-short phones, then the rail layout is used and no content is clipped.

### Stress / failure injection
- 1,000+ items virtualised feed performance trace.

## Acceptance criteria

- [ ] Viewport matrix green; axe 0 serious/critical
- [ ] Feed performance budget met
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, viewport matrix + axe)

## Exceptions & edge cases

- MapLibre WebGL unavailable in CI headless: test the list fallback and run the map check in headed CI.

## Cardinal rules (do NOT)

- Do NOT exclude tiers from the matrix.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/ui/dashboards/D08-intel.md`: acceptance: link the passing run
- `docs/roadmap/phase-4-intel.md`: note the item in §7 risks / progress

## Branch & PR

- Branch: `p4/P4-T059-verify-d08-viewport-axe`
- PR title: `P4-T059: D08 and tier-B overlays: Playwright viewport matrix and axe`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T059` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (label mode now P4-T062; added D02 widgets P4-T065)
