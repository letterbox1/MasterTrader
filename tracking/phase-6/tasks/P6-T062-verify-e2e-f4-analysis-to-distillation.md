---
id: P6-T062
kind: task
title: End-to-end F4: analysis → Signal → D09 → settlement → teacher log → candidate
phase: 6
type: VERIFY
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T041, P6-T042, P6-T013, P6-T031]
requirements: [R6.01, R6.04, R6.14, R6.40]
roadmap_todos: []
modules: [M8, M9, M21, M15]
dashboards: [D09, D10]
tools: [git, uv, pnpm, playwright]
mcp: []
env: []
services: [agents, hindsight, mt-api, prefect]
branch: p6/P6-T062-verify-e2e-f4-analysis-to-distillation
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/roadmap/phase-6-ai-models-treasury.md]
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

# P6-T062 · End-to-end F4: analysis → Signal → D09 → settlement → teacher log → candidate

## Goal / expected outcome

The whole F4 flow works on the real stack: you ask for an analysis of an arbitrary instrument in D09, get a sourced Signal with provenance, it settles after its horizon with a reflection in Hindsight, and the next nightly flow uses it in a registered candidate (visible in D10 lineage).

## Context & references

- Roadmap: [R6.01](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.04](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.14](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.40](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo none (supporting item)
- Flow: [02 F4](../../../docs/02-v1-architecture.md#8-end-to-end-flows) · [D09](../../../docs/ui/dashboards/D09-agents.md) · [D10](../../../docs/ui/dashboards/D10-models-memory.md) · [roadmap §6 exit criteria](../../../docs/roadmap/phase-6-ai-models-treasury.md#6-exit-criteria-demo) item 1
- Related: P6-T067 (sample runs, T6.66); this item covers the full F4 flow through settlement and distillation
- Depends on (this phase): P6-T041, P6-T042, P6-T013, P6-T031

## Requirements

- Instruments: one crypto, one FX, one equity, one chosen at random by the tester.
- Short horizon (1 day) for the test so settlement happens in-window.
- Evidence: run ids, signal ids, settlement ids, memory ids, candidate model id with lineage.

## ToDo

- [ ] Run four analyses via D09.
- [ ] Wait for settlement; verify reflections in D10 Memory.
- [ ] Verify the nightly candidate lineage includes these runs.
- [ ] Record ids in the progress log.

## Verification

### Tests
- Playwright E2E (recorded LLM) for the D09 part in CI; real run once on the host.

### Scenarios
- Given 'Analyse XAUUSD', then D09 shows stages, a Signal with ≥ 3 provenance items, cost and model; next day settlement and reflection appear.

### Stress / failure injection
- Run four analyses concurrently: all complete; budgets respected.

## Acceptance criteria

- [ ] Four runs complete with provenance.
- [ ] Settlements and reflections present.
- [ ] Candidate lineage includes them.

## Exceptions & edge cases

- Instrument without fundamentals: fundamentals analyst reports unavailable; still a valid run.

## Cardinal rules (do NOT)

- Do NOT hand-edit DB rows to make the flow pass.
- Do NOT UPDATE or DELETE WORM rows (`audit.*`, `journal.*`, policy changes); corrections are new rows referencing the original (15 §2).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order and on-chain move goes through M11.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/02-v1-architecture.md` F4: note verified.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick the matching ToDo (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T062-verify-e2e-f4-analysis-to-distillation`
- PR title: `P6-T062: End-to-end F4: analysis → Signal → D09 → settlement → teacher log → candidate`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T062` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (sample runs moved to P6-T067 (T6.66); run fields)
