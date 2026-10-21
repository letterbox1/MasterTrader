---
id: P6-T041
kind: task
title: D09 Agents & Decisions UI
phase: 6
type: BUILD
status: backlog
priority: high
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T008, P6-T013, P6-T015]
requirements: [R6.40, R6.01]
roadmap_todos: [T6.29]
modules: [M15, M8, M9, M10, M21]
dashboards: [D09]
branch: p6/P6-T041-d09-agents-ui
pr: ""
doc_sync: [docs/ui/dashboards/D09-agents.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P6-T041 · D09 Agents & Decisions UI

## Goal / expected outcome

`/agents` and `/agents/runs/:id` are live: New analysis (with budget estimate), Runs list, Signals, tier-B decision stream, Outcome scorecard, Anomaly explanations, and the debate detail with stage timeline, `AgentTurn`s, `ConsensusBar`, final signal card, evidence (`ProvenanceList`), memory used and settlement — across the full viewport matrix.

## Context & references

- Roadmap: [R6.40](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.01](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.29
- UI: [D09](../../../docs/ui/dashboards/D09-agents.md) (layouts, widgets, actions, acceptance) · [ui components](../../../docs/ui/components.md) · [DESIGN §6.8](../../../DESIGN.md#68-test-matrix-every-screen-must-pass)
- API: [02 §7.1](../../../docs/02-v1-architecture.md#71-queries-rest-read) · [02 §7.3](../../../docs/02-v1-architecture.md#73-real-time-websocket-apiv1ws)
- Exit: [roadmap §6 exit criteria](../../../docs/roadmap/phase-6-ai-models-treasury.md#6-exit-criteria-demo) item 1
- Depends on (this phase): P6-T008, P6-T013, P6-T015

## Requirements

- Widgets and data sources exactly as D09 tables; actions `agents.run_analysis` (C1 with budget), `models.tierb.ask` (C0), `journal.note.add` (C0), schedule via `system.settings.update` (C1).
- Acceptance from D09: numbers link to provenance; unsourced numbers flagged; cost/model visible on every run; budget-exhausted runs show local fallback; settlement only after horizon.
- Responsive tiers: ≥ 2xl three columns; xl–md stacked; ≤ ph tabs; debate detail timeline/drawer/thread per tier.
- Live updates via WS `agents.run`, `signals`, `tierb`, `notifications` with seq gap re-sync.

## ToDo

- [ ] Routes, components (`AgentTurn`, `ConsensusBar`, `TierBScore`, `ProvenanceList`) per ui/components.
- [ ] New analysis sheet with budget estimate.
- [ ] Scorecard charts (reliability diagram).
- [ ] Playwright tests incl. viewport matrix.
- [ ] Docs.

## Verification

### Tests
- Playwright: start analysis → run appears → detail shows stages and provenance.
- Viewport matrix 240 → 2560 px (DESIGN §6.8) overflow/overlap checks.
- Component tests for unsourced-number flag.

### Scenarios
- Given a finished run, when opening the detail on a 360×780 phone, then turns are grouped by stage and sources open in a sheet.
- Given a run's horizon hasn't ended, then no settlement panel is shown.

### Stress / failure injection
- Stream 100 tier-B decisions/s on WS: UI throttles to ≤ 1 Hz table updates, no jank > 100 ms.

## Acceptance criteria

- [ ] D09 acceptance criteria 1–3 pass in Playwright.
- [ ] Viewport matrix green.
- [ ] CI green.

## Exceptions & edge cases

- Agents service down: runs list shows last state + banner; New analysis disabled with reason.

## Cardinal rules (do NOT)

- Do NOT call services directly from the UI; only `mt_api`.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order and on-chain move goes through M11.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/ui/dashboards/D09-agents.md`: mark implemented; note any field changes.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.29 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T041-d09-agents-ui`
- PR title: `P6-T041: D09 Agents & Decisions UI`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T041` run

## Progress log

- 2026-10-21 00:00 · planner · created
