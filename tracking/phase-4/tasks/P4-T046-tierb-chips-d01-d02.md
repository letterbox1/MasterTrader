---
id: P4-T046
kind: task
title: Tier B chips on D01/D02 and calendar/event overlays on D02 charts
phase: 4
type: BUILD
status: backlog
priority: medium
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T043, P4-T029]
requirements: [R4.13, R4.12]
roadmap_todos: [T4.29]
modules: [M21, M5, M3]
dashboards: [D01, D02]
branch: p4/P4-T046-tierb-chips-d01-d02
pr: ""
doc_sync: [docs/ui/dashboards/D02-markets.md, docs/ui/dashboards/D01-cockpit.md, docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P4-T046 · Tier B chips on D01/D02 and calendar/event overlays on D02 charts

## Goal / expected outcome

D01 'Signals & decisions' lists tier-B decisions (question, probability, model version) alongside strategy signals; D02 quadrant cards show a tier-B regime chip, the instrument detail shows `TierBScore` probabilities with model version + 'uncalibrated' badge, and `PriceChart` overlays calendar/event markers and shaded blackout windows; 'Ask decision model' (`models.tierb.ask`) works from D02.

## Context & references

- Roadmap: [R4.13, R4.12](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.29](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- UI: [D01](../../../docs/ui/dashboards/D01-cockpit.md) · [D02](../../../docs/ui/dashboards/D02-markets.md) (tier-B and intel overlays in Phase 4)
- Cross-phase: P2 D01, P1 D02.

## Requirements

- Stage-1 scores carry an 'uncalibrated' badge until P4-T048 thresholds exist.
- WS `tierb`, `cal`, `evt` subscriptions throttled per DESIGN rules (≤ 4 Hz charts).
- No Telegram-derived chips on D01/D02.

## ToDo

- [ ] `TierBScore` + regime chip components.
- [ ] D01/D02 integrations.
- [ ] PriceChart overlay layer for `cal`/`evt`/blackouts.
- [ ] Playwright + axe.

## Verification

### Tests
- Playwright: seeded tier-B decision appears on D01 and D02 within 1 s of WS message.
- Visual regression of overlays at sm/md/xl.

### Scenarios
- Given decision-svc down, then chips show degraded state without breaking the cards.

### Stress / failure injection
- n/a: covered by the viewport matrix in P4-T059.

## Acceptance criteria

- [ ] Chips + overlays render per spec on all tiers
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, viewport matrix + axe)

## Exceptions & edge cases

- Instruments without tier-B coverage show no chip (not 'neutral').

## Cardinal rules (do NOT)

- Do NOT present uncalibrated probabilities as calibrated.
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/ui/dashboards/D02-markets.md`: mark tier-B/intel overlays implemented
- `docs/ui/dashboards/D01-cockpit.md`: tier-B rows in Signals & decisions
- `docs/roadmap/phase-4-intel.md`: tick T4.29 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T046-tierb-chips-d01-d02`
- PR title: `P4-T046: Tier B chips on D01/D02 and calendar/event overlays on D02 charts`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T046` run

## Progress log

- 2026-10-21 00:00 · planner · created
