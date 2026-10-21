---
id: P7-T010
kind: task
title: Professional-advice register linked to venue-registry blocks
phase: 7
type: BUILD
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: []
requirements: [R7.13]
roadmap_todos: [T7.07]
modules: [M19, M11]
dashboards: [D13, D06, D15]
branch: p7/P7-T010-pro-advice-register
pr: ""
doc_sync: [docs/12-policy-and-compliance.md, docs/ui/dashboards/D13-tasks-curation.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-T010 · Professional-advice register linked to venue-registry blocks

## Goal / expected outcome

Every 12 §6 advice item exists as a `PRO_ADVICE` task with state `open | answered | deferred`, and any venue/product linked to an item that is not `answered` is forced to `blocked`/`read_only` in `ops.venue_registry` with reason `pending_advice:<task_id>`.

## Context & references

- Roadmap: [R7.13 · ToDo T7.07](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [12 §6](../../../docs/12-policy-and-compliance.md#6-professional-advice-triggers-tracked-as-tasks-in-d13--d15) · [12 §2](../../../docs/12-policy-and-compliance.md#2-venue-access-registry) (status + reason) · [D13](../../../docs/ui/dashboards/D13-tasks-curation.md) (`PRO_ADVICE` task type) · [D15](../../../docs/ui/dashboards/D15-tax.md) (Questions tab)
- Cross-phase: P5 curation task queue (`curation.task`), P0 T0.22 `ops.venue_registry`, P2 T2.22 registry check in M11.
- Related: P7-T002, P7-T003, P7-T011 (preflight reads this register)

## Requirements

- Seed migration creates idempotently: lawyer ×3 (spot-token manipulation reach, Hyperliquid, private/non-commercial boundary), tax ×2 (investor vs trader; 2027 CGT reform), venue ×4 (AUSTRAC by ABN; OKX AU derivatives; venue conduct/STP/rate-limit terms; FP Markets algo clauses).
- New table `curation.pro_advice_link(task_id, venue, product, created_at)` (WORM: insert-only; unlinking = new row with `supersedes_id`).
- Registry guard: `venue.registry.update` to `allowed` for a linked product is rejected while the task is `open`/`deferred`; tightening is always allowed (C1).
- `deferred` requires `reason` and `revisit_on`; a Prefect flow re-opens deferred items on `revisit_on` and posts a Telegram task.
- Query `/tasks?type=PRO_ADVICE` returns state, links and revisit date; counted by preflight.

## ToDo

- [ ] Alembic migration: `curation.pro_advice_link` + WORM grants/triggers (reuse the P0 WORM helper).
- [ ] Seed data module `packages/mt_curation/seeds/pro_advice.py` with the 9 items and default links (Hyperliquid perps/HLP, OKX AU perps, FP Markets CFDs).
- [ ] Registry guard in `packages/mt_api/commands/venue.py`: reject `allowed` while linked advice not `answered` (problem+json `pending_advice`).
- [ ] Prefect flow `pro_advice_revisit` (daily).
- [ ] D13 task detail: state selector (answered/deferred), reason, revisit date, linked products list.
- [ ] Tests (below); update docs.

## Verification

### Tests
- Unit: state machine open → answered/deferred → open (revisit); deferred without reason rejected.
- Integration: linked product cannot be set `allowed` (command returns 409 `pending_advice`); unlinked product can (C3 path).
- Migration test: seed is idempotent (run twice → 9 items).

### Scenarios
- Given Hyperliquid is linked to an open item, when you submit `venue.registry.update allowed`, then it is rejected with the task id.
- Given an item is deferred to 2027-01-15, when that date passes, then the item re-opens and a Telegram task arrives.
- Given the item is answered, when you then allow the product, then the normal C3 flow runs.

### Stress / failure injection
- n/a: low-volume admin data; covered by unit/integration tests.

## Acceptance criteria

- [ ] 9 `PRO_ADVICE` items seeded and visible in D13.
- [ ] Registry guard blocks `allowed` for linked products until answered.
- [ ] CI green (lint, types, tests).

## Exceptions & edge cases

- Residency change: every item re-opens for the new jurisdiction (hook on `tax.residency.add`).
- Item answered 'no': keep product blocked; the guard only opens the C3 path, it never allows automatically.

## Cardinal rules (do NOT)

- Do NOT store advice documents in git; only encrypted-store references.
- Do NOT update or delete WORM rows; corrections are new rows with `supersedes_id` (15 §2).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT let loosening risk, autonomous mode or a capital step apply without C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/12-policy-and-compliance.md` §6: note the register and the `pending_advice` block reason.
- `docs/ui/dashboards/D13-tasks-curation.md`: PRO_ADVICE state fields.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.07 when this item is done.

## Branch & PR

- Branch: `p7/P7-T010-pro-advice-register`
- PR title: `P7-T010: Professional-advice register linked to venue-registry blocks`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T010` run

## Progress log

- 2026-10-21 00:00 · planner · created
