---
id: P2-T063
kind: task
title: "Part A end-to-end flows on paper: F2 with HITL, F5 and F6"
phase: 2
type: VERIFY
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T021, P2-T029, P2-T039, P2-T043, P2-T051, P2-T054]
requirements: [R2.10, R2.20, R2.18, R2.19, R2.34]
roadmap_todos: [T2.60, T2.61]
modules: [M0, M11, M12, M15, M16]
dashboards: [D06, D03]
branch: p2/P2-T063-verify-part-a-e2e-flows
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T063 · Part A end-to-end flows on paper: F2 with HITL, F5 and F6

## Goal / expected outcome

One scripted run proves the Part A side of exit criteria 2 and 3: a template strategy on paper behind M11 produces a hitl approval approved from Telegram and filled, with TCA recorded; a C3 loosening needs TOTP + cool-down; the kill drill passes. Part B's phase-exit demo depends on this.

## Context & references

- Roadmap: exit criteria 2–3 (../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDos T2.60/T2.61
- Flows: [02 F2, F5, F6](../../../docs/02-v1-architecture.md#8-end-to-end-flows)
- Part B: phase exit demo item depends on this task.

## Requirements

- F2: trend template (P2-T008) on BTCUSDT sandbox/testnet, hitl mode → card on Telegram → Approve → M11 re-check → fill → `fill.*` → TCA cost event → visible in D06 events/limits and Grafana.
- F5: raise a limit from D06 → C3 Telegram approve + TOTP → cool-down → applied; a tighten applies immediately.
- F6: kill from phone → cancels < 1 s → OFF via C3 after cause cleared.
- Every step leaves audit rows with a common `trace_id` (fill → logs jump works in Grafana).

## ToDo

- [ ] Scenario script `ops/demo/part_a_flows.py`
- [ ] Run, capture evidence (screenshots, audit ids)
- [ ] Report in progress log
- [ ] Record results (numbers, run IDs, screenshots) in the progress log and tick the roadmap ToDo box

## Verification

### Tests
- The scripted scenario (repeatable).

### Scenarios
- As listed in Requirements.

### Stress / failure injection
- n/a: covered by the dedicated drills.

## Acceptance criteria

- [ ] F2, F5, F6 pass end to end with evidence
- [ ] Trace ids link audit to logs

## Exceptions & edge cases

- If the journal (P3) isn't present, `fill.*` is still published and asserted.

## Cardinal rules (do NOT)

- Do NOT stage evidence; run against the real paper path.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Loosening risk, autonomous mode and mandates are C3 (Telegram approve + TOTP + cool-down); protective exits never wait for approval.

## Doc sync on completion

- `docs/02-v1-architecture.md` §8: mark F2/F5/F6 as demonstrated (paper).
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.60, T2.61 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T063-verify-part-a-e2e-flows`
- PR title: `P2-T063: Part A end-to-end flows on paper: F2 with HITL, F5 and F6`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T063` run

## Progress log

- 2026-10-21 00:00 · planner · created
