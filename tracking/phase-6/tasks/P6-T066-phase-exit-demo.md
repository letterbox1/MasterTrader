---
id: P6-T066
kind: task
title: Phase 6 exit demo
phase: 6
type: VERIFY
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T052, P6-T053, P6-T054, P6-T055, P6-T056, P6-T057, P6-T058, P6-T059, P6-T060, P6-T061, P6-T062, P6-T063, P6-T064, P6-T065, P6-T043, P6-T044, P6-T045, P6-T032, P6-T010, P6-T034, P6-T067, P6-T069, P6-T070]
requirements: [R6.01, R6.05, R6.10, R6.12, R6.20, R6.21, R6.22, R6.24, R6.40]
roadmap_todos: []
modules: [M8, M9, M10, M21, M22]
dashboards: [D09, D10, D18]
tools: [git, uv, docker, pnpm, playwright]
mcp: []
env: []
services: [mt-api, agents, anvil, telegram-bot-api]
branch: p6/P6-T066-phase-exit-demo
pr: ""
doc_sync: [tracking/phase-6/PHASE.md, docs/roadmap/phase-6-ai-models-treasury.md]
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

# P6-T066 · Phase 6 exit demo

## Goal / expected outcome

Every Phase 6 exit criterion is demonstrated live and recorded: (1) analysis of any instrument → sourced Signal with provenance in D09; (2) an anomaly explained on Telegram; (3) the bake-off report names a production tier-B model or keeps SemIf with calibration evidence; (4) idle stables allocated within the allow-list after the cost gate with the reserve holding.

## Context & references

- Roadmap: [R6.01](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.05](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.10](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.12](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.20](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.21](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.22](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.24](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.40](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo none (supporting item)
- [roadmap §6 exit criteria](../../../docs/roadmap/phase-6-ai-models-treasury.md#6-exit-criteria-demo) · Roadmap §5 deliverables
- All VERIFY items in this phase
- Depends on (this phase): P6-T052, P6-T053, P6-T054, P6-T055, P6-T056, P6-T057, P6-T058, P6-T059, P6-T060, P6-T061, P6-T062, P6-T063, P6-T064, P6-T065, P6-T043, P6-T044, P6-T045, P6-T032, P6-T010, P6-T034 (your approved treasury policy), P6-T067 (sample runs), P6-T069 (port check), P6-T070 (live keys)

## Requirements

- Live demo on the host in paper/fork mode, recorded (screenshots + ids).
- Re-check: no open S1/S2 bugs in phase 6; all tasks done/cancelled; optional items decided.
- Tick the exit criteria in PHASE.md with evidence links.

## ToDo

- [ ] Demo 1: D09 → analysis of a tester-chosen instrument → Signal with provenance.
- [ ] Demo 2: seeded anomaly → Telegram brief.
- [ ] Demo 3: open the signed-off bake-off report (P6-T059) and the registry entry.
- [ ] Demo 4: allocate idle test stables on fork under your approved policy (P6-T034) → gate allow → position within caps; reserve ≥ min.
- [ ] Link the evidence of P6-T067 (sample runs), P6-T069 (port check) and P6-T070 (live key check).
- [ ] Confirm no open S1/S2 bugs; tick PHASE.md exit boxes.

## Verification

### Tests
- Re-run of the CI suites (pit, provenance, prompt-injection, WORM) green on the demo commit.

### Scenarios
- Given the demo checklist, when each step runs, then evidence ids are logged here.

### Stress / failure injection
- n/a: covered by P6-T058, P6-T064.

## Acceptance criteria

- [ ] All four exit criteria demonstrated with evidence.
- [ ] PHASE.md exit criteria ticked.
- [ ] No open S1/S2 bugs.

## Exceptions & edge cases

- If a criterion fails, open a bug and re-run that step after the fix.

## Cardinal rules (do NOT)

- Do NOT demo with live money.
- Do NOT touch live money or live keys; keys stay trade-only, IP-locked, withdrawals disabled (live is gated to P7).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order and on-chain move goes through M11.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `tracking/phase-6/PHASE.md`: exit criteria ticked with evidence links.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick the matching ToDo (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T066-phase-exit-demo`
- PR title: `P6-T066: Phase 6 exit demo`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T066` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (exit demo now also depends on P6-T034, P6-T067, P6-T069, P6-T070 (new T6.66/T6.73 and the live check); run fields)
