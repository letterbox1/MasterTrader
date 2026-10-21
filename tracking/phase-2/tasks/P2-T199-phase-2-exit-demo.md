---
id: P2-T199
kind: task
title: Phase 2 exit demo
phase: 2
type: VERIFY
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T133, P2-T160, P2-T161, P2-T162, P2-T163, P2-T164, P2-T165, P2-T166, P2-T167, P2-T168, P2-T180]
requirements: [R2.01, R2.06, R2.40, R2.42, R2.43, R2.45, R2.47, R2.48, R2.50, R2.51, R2.N1]
roadmap_todos: []
modules: [M0, M7, M11, M12, M15, M21]
dashboards: [D01, D03, D04, D05, D06]
branch: p2/P2-T199-phase-2-exit-demo
pr: ""
doc_sync: [docs/roadmap/README.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T199 · Phase 2 exit demo

## Goal / expected outcome

A recorded, end-to-end demonstration of every Phase 2 exit criterion, run from the web UI and the phone, with evidence links for each, after which PHASE.md's exit boxes can be ticked.

## Context & references

- Roadmap: [§6 exit criteria](../../../docs/roadmap/phase-2-strategies-risk-lab.md#6-exit-criteria-demo)
- Evidence also required from part A (P2-T001–T099): kill drill from the phone (T2.06/T2.61), C3 loosening with TOTP + cool-down (T2.07/T2.62-series), Telegram approval of an approve-mode order (T2.33/T2.69), risk golden tests (T2.60), D06 matrix
- Part-B evidence: P2-T133, T160–T168, T180

## Requirements

- Exit 1: create a strategy from a template, from code and by 'describe it'; backtest with measured costs (snapshot id shown); the validation report shows all harness sections (P2-T166 run live, not recorded).
- Exit 2: run it on paper behind M11; an approve-mode (HITL) order is approved from Telegram and the web queue reflects it < 1 s (part A Telegram + P2-T149).
- Exit 3: kill drill passes from the phone (cancels < 1 s) and a C3 loosening needs TOTP + cool-down (part A evidence linked).
- Exit 4: the P1 paper clock has started (P2-T180 timestamps shown in D03).
- Also shown: latency results (P2-T162), parity report (P2-T161), seeded-bug catch (P2-T160), sandbox containment (P2-T165), MTB goldens (P2-T133), viewport matrix + axe (P2-T163 + part A D06).
- No open S1/S2 bugs in Phase 2; all Phase 2 tasks done/cancelled.

## ToDo

- [ ] Prepare a demo script listing each criterion and its evidence link
- [ ] Run the demo (desktop + phone); record screen captures
- [ ] Collect part-A evidence links
- [ ] Tick PHASE.md exit criteria (main agent merge) and update roadmap README via `./kanban build`

## Verification

### Tests
- Re-run of the E2E nightly suites immediately before the demo (all green).

### Scenarios
- Given any criterion fails during the demo, then the demo stops, a bug item is filed with severity, and the demo is repeated after the fix.

### Stress / failure injection
- Kill drill performed while a validation job and a sweep are running (lab load must not slow kill → cancels beyond 1 s).

## Acceptance criteria

- [ ] Exit criterion 1 demonstrated with evidence
- [ ] Exit criterion 2 demonstrated with evidence
- [ ] Exit criterion 3 demonstrated with evidence (part A)
- [ ] Exit criterion 4 demonstrated with evidence
- [ ] No open S1/S2 bugs in phase 2

## Exceptions & edge cases

- Gateway outage on demo day: describe-it uses local-advisor fallback and that is stated in the evidence.

## Cardinal rules (do NOT)

- Do NOT demo with recorded/stubbed services where the criterion requires the real path (M11, Telegram, kill).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT let any UI/API path loosen risk, enable autonomous mode or turn the kill switch off without C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT touch live money; keys are trade-only, IP-locked, withdrawals disabled; live waits for the P7 gates.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/roadmap/README.md`: regenerated status block via `./kanban build` (main agent).
- `docs/roadmap/phase-2-strategies-risk-lab.md`: note the result in the progress of the matching exit criterion.

## Branch & PR

- Branch: `p2/P2-T199-phase-2-exit-demo`
- PR title: `P2-T199: Phase 2 exit demo`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T199` run · Playwright viewport matrix + axe green

## Progress log

- 2026-10-21 00:00 · planner · created
