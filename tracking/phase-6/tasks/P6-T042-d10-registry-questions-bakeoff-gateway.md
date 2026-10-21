---
id: P6-T042
kind: task
title: D10 Registry, Decision questions, Bake-off and Gateway tabs
phase: 6
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T009, P6-T018, P6-T026, P6-T029, P6-T030]
requirements: [R6.40, R6.12, R6.14, R6.07]
roadmap_todos: [T6.29]
modules: [M15, M21]
dashboards: [D10]
branch: p6/P6-T042-d10-registry-questions-bakeoff-gateway
pr: ""
doc_sync: [docs/ui/dashboards/D10-models-memory.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P6-T042 · D10 Registry, Decision questions, Bake-off and Gateway tabs

## Goal / expected outcome

D10's governance tabs are live: Registry (tier A/B/gateway models with calibration, latency vs SLO, lineage, status), Decision questions (versions, thresholds, abstain/flip rates, proposals), Bake-off (reports incl. Kev and FinMMEval), Gateway (spend vs budget, fallbacks), with promote/rollback/bake-off/question/budget actions at the right confirmation levels.

## Context & references

- Roadmap: [R6.40](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.12](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.14](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.07](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.29
- UI: [D10](../../../docs/ui/dashboards/D10-models-memory.md) (tabs, actions, acceptance) · [DESIGN §6.8](../../../DESIGN.md#68-test-matrix-every-screen-must-pass)
- API: [02 §7.1](../../../docs/02-v1-architecture.md#71-queries-rest-read) (`/models/*`)
- Depends on (this phase): P6-T009, P6-T018, P6-T026, P6-T029, P6-T030

## Requirements

- Registry detail: reliability diagram, confusion matrix, drift (Evidently), lineage (teacher runs + outcomes), gate results; out-of-SLO models flagged red.
- Actions: `models.promote` (C2; C3 for auto consumers, gate results shown), `models.rollback` (C1), `models.bakeoff.run` (C1), `lab.validate.run` kind=distill (C1), `models.question.update` (C1 new version; veto threshold lowering C3), budget adjust (`system.settings.update`: raise C3, lower C1).
- Provenance filter count (rows excluded with `train_ok=false`) shown on dataset/lineage views.
- Responsive per D10 tiers; viewport matrix.

## ToDo

- [ ] Tabs + detail panels.
- [ ] Action sheets with gate result previews.
- [ ] Playwright tests + viewport matrix.
- [ ] Docs.

## Verification

### Tests
- Playwright: promotion blocked with reason when a gate fails; budget raise prompts C3.
- Viewport matrix.

### Scenarios
- Given a candidate failing the ECE gate, when Promote is pressed, then the sheet shows the failing gate and no command is sent.
- Given a production model out of latency SLO, then its row is red.

### Stress / failure injection
- Registry with 500 model versions paginates (cursor) with p95 API < 300 ms.

## Acceptance criteria

- [ ] D10 acceptance 1–3 pass.
- [ ] Viewport matrix green.

## Exceptions & edge cases

- MLflow down: registry shows cached metadata with a stale badge.

## Cardinal rules (do NOT)

- Do NOT offer any promotion path that skips gates.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order and on-chain move goes through M11.
- Do NOT loosen anything (risk, LLM budgets, treasury policy, allow-list, autonomous mode, mandates) without C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/ui/dashboards/D10-models-memory.md`: implemented tabs; Kev in Bake-off list.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.29 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T042-d10-registry-questions-bakeoff-gateway`
- PR title: `P6-T042: D10 Registry, Decision questions, Bake-off and Gateway tabs`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T042` run

## Progress log

- 2026-10-21 00:00 · planner · created
