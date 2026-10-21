---
id: P6-T013
kind: task
title: Decision settlement and reflection jobs
phase: 6
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T007, P6-T012]
requirements: [R6.04, R6.14]
roadmap_todos: [T6.21]
modules: [M9, M8, M21]
dashboards: [D09]
branch: p6/P6-T013-settlement-reflection-jobs
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/02-v1-architecture.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P6-T013 · Decision settlement and reflection jobs

## Goal / expected outcome

After each Signal's horizon a Prefect flow settles it (realised return, alpha vs benchmark, barrier hits) via `pit`, writes an `audit.decision_settlement` row, has the agent write a reflection, and retains episode + lesson to Hindsight; this is the outcome-labelled teacher log for distillation.

## Context & references

- Roadmap: [R6.04](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.14](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.21
- Spec: [02 F4](../../../docs/02-v1-architecture.md#8-end-to-end-flows) steps 3–4 · [03 M9](../../../docs/03-build-spec.md#m9-memory--rag--mt_memory) (settlement + reflection, teacher logs into `decisions`) · [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design) (labels corrected against realised outcomes: forward returns / barrier hits) · [research: TradingAgents/FinRobot](../../../docs/research/agents-tradingagents-finrobot.md) (TradingAgents 5-day settlement + reflection)
- UI: [D09](../../../docs/ui/dashboards/D09-agents.md) Settlement panel, Outcome scorecard
- Depends on (this phase): P6-T007, P6-T012

## Requirements

- Settlement flow (Prefect, every 15 min): select runs with `settlement_due_at ≤ now` and no settlement row.
- Outcome via `pit(as_of=settlement_time)`: forward return over horizon, alpha vs the instrument's benchmark (manifest/asset-class default), triple-barrier hit (upper/lower/time) with barriers from the Signal or volatility default, hit/miss vs direction, P&L if traded (join fills).
- `audit.decision_settlement` WORM row referencing `run_id`/`signal_id`; never update the run.
- Reflection: gateway role `memory` (budgeted) writes a short reflection; stored with the settlement; Hindsight retain into `decisions` (episode) and `strategies` (lesson) with `created_at` = settlement time.
- Scorecard metrics endpoint `GET /agents/runs?settled=1&metrics=1`: hit rate, Brier, reliability bins, by role/model/horizon.
- Settlement never visible in views with as_of before the horizon end (D09 acceptance 3).

## ToDo

- [ ] Prefect flow `settle_decisions` + `reflect_decision` in `mt_memory.settlement`.
- [ ] Outcome calculators (forward return, alpha, triple barrier) with unit tests.
- [ ] Reflection prompt in the prompt registry.
- [ ] Scorecard aggregation query.
- [ ] Tests; docs.

## Verification

### Tests
- Unit: triple-barrier and alpha calculators (golden series).
- Integration: a recorded run with 1-day horizon settles once; rerun of the flow is idempotent.
- PIT: settlement uses only bars ≤ settlement time (pit mock asserts).

### Scenarios
- Given a long Signal on BTCUSDT with 5d horizon and +3% realised, then settlement shows hit=true, alpha vs benchmark, and a reflection memory exists.
- Given bars are missing at horizon end (DQ gap), then settlement waits (max 24 h) then settles `status=unsettleable` with reason.
- Given the `memory` budget is exhausted, then settlement still writes the numeric row and the reflection falls back to local or is queued.

### Stress / failure injection
- Backlog of 5,000 due settlements after downtime: flow processes in batches without double-settling; runtime < 30 min.

## Acceptance criteria

- [ ] Every due Signal gets exactly one settlement row.
- [ ] Reflections retained with correct timestamps.
- [ ] Scorecard endpoint returns metrics.

## Exceptions & edge cases

- Instrument delisted/rugged: settle at last available price and flag (survivorship-free).
- Flat Signals: settle as abstentions (no hit/miss) but keep for calibration.

## Cardinal rules (do NOT)

- Do NOT backdate settlement or reflection memories to the decision time.
- Do NOT UPDATE or DELETE WORM rows (`audit.*`, `journal.*`, policy changes); corrections are new rows referencing the original (15 §2).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order and on-chain move goes through M11.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md` §4.3: settlement label definitions.
- `docs/02-v1-architecture.md` F4: settlement table name.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.21 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T013-settlement-reflection-jobs`
- PR title: `P6-T013: Decision settlement and reflection jobs`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T013` run

## Progress log

- 2026-10-21 00:00 · planner · created
