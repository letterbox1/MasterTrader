---
id: P1-T067
kind: task
title: Run the Phase 1 exit demo
phase: 1
type: VERIFY
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T043, P1-T055, P1-T056, P1-T057, P1-T058, P1-T059, P1-T060, P1-T061, P1-T062, P1-T063, P1-T064, P1-T065, P1-T066, P1-T020, P1-T026, P1-T027, P1-T028]
requirements: [R1.01, R1.02, R1.03, R1.04, R1.05, R1.06, R1.07, R1.08, R1.09, R1.10, R1.11, R1.12, R1.13, R1.14, R1.15, R1.N1, R1.N2, R1.N3]
roadmap_todos: [T1.60, T1.61, T1.62, T1.63, T1.64, T1.80]
modules: [M1, M16, M17, M15]
dashboards: [D07, D02]
branch: p1/P1-T067-phase-1-exit-demo
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/roadmap/README.md, docs/04-plan-of-action.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P1-T067 · Run the Phase 1 exit demo

## Goal / expected outcome

In one recorded session, every Phase 1 exit criterion is demonstrated live and evidenced, all P1 tasks are done or cancelled, no S1/S2 bug is open, and `PHASE.md` exit boxes are ticked.

## Context & references

- Roadmap: requirements [R1.01](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.02](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.03](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.04](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.05](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.06](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.07](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.08](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.09](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.10](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.11](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.12](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.13](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.14](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.15](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.N1](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.N2](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.N3](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.60](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets), [T1.61](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets), [T1.62](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets), [T1.63](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets), [T1.64](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets), [T1.80](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Exit criteria: [phase 1 §6 exit criteria](../../../docs/roadmap/phase-1-data-and-monitoring.md#6-exit-criteria-demo) · PHASE.md exit checklist (`tracking/phase-1/PHASE.md`) · evidence from P1-T056…T066
- Depends on (this phase): P1-T043, P1-T055, P1-T056, P1-T057, P1-T058, P1-T059, P1-T060, P1-T061, P1-T062, P1-T063, P1-T064, P1-T065, P1-T066, P1-T020, P1-T026, P1-T027, P1-T028

## Requirements

- Demo 1: Grafana and D02 show live prices at every timeframe from ticks to 1D for crypto, FX/metals and ETFs, plus daily futures and macro (re-run P1-T061 live)
- Demo 2: spread/funding/swap panels populated; reconciliation clean on practice accounts (P1-T064 evidence + a live `data.recon.run`)
- Demo 3: kill a feed → `stale` in < 2 s on D07 and the alert arrives on Telegram, email and ntfy (live, timed)
- Demo 4: 06 §3 open checks recorded pass/fail (P1-T056)
- Also show: RBA F11 and ABS CPI loaded with pit queries (P3 prerequisite), EDGAR filings, venue health panel, storage projection from the soak, provenance/retention report
- Evidence pack under `reports/exit/P1/` (screen recording link, timings, report index)

## ToDo

- [ ] Prepare the demo script and check every dependency's report exists
- [ ] Run the demo with you watching; time demo 3
- [ ] Tick PHASE.md exit criteria and confirm no open S1/S2 bugs
- [ ] Update roadmap README status via `./kanban build` (run by the main agent)
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Re-run the e2e suites from P1-T057, P1-T061 and P1-T060 as part of the demo

### Scenarios

- Given any demo step fails, when it happens, then a P1 bug is filed with severity and the demo is re-run after the fix

### Stress / failure injection

- Demo 3 is the live failure injection; load evidence comes from P1-T062

## Acceptance criteria

- [ ] All four roadmap exit criteria demonstrated and evidenced
- [ ] All P1 tasks done/cancelled; no open S1/S2 bugs; PHASE.md exit boxes ticked
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Market hours: schedule when US equities, FX and crypto are all open (e.g. Tuesday 00:30–06:00 Sydney time)

## Cardinal rules (do NOT)

- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT put Telegram text into any model input, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)); the bot only sends alerts.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.60, T1.61, T1.62, T1.63, T1.64, T1.80 once every task traced to it in PHASE.md is done; note P1-T067 next to it.
- `docs/roadmap/README.md`: phase 1 marked done (generated block via `./kanban build`)
- `docs/04-plan-of-action.md` Phase 1: tick deliverables

## Branch & PR

- Branch: `p1/P1-T067-phase-1-exit-demo`
- PR title: `P1-T067: Run the Phase 1 exit demo`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T067` run

## Progress log

- 2026-10-21 00:00 · planner · created
