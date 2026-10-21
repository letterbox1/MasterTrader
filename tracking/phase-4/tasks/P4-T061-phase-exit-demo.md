---
id: P4-T061
kind: task
title: Phase 4 exit demo
phase: 4
type: VERIFY
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T050, P4-T051, P4-T052, P4-T053, P4-T054, P4-T055, P4-T056, P4-T057, P4-T058, P4-T059, P4-T060]
requirements: [R4.14, R4.10, R4.03]
roadmap_todos: []
modules: [M2, M3, M5, M6, M9, M21, M11]
dashboards: [D08, D06, D01, D02]
branch: p4/P4-T061-phase-exit-demo
pr: ""
doc_sync: [docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P4-T061 · Phase 4 exit demo

## Goal / expected outcome

A recorded demo runs every Phase 4 exit criterion: (1) a morning Telegram brief arrives with sourced items, events mapped to assets and today's blackouts; (2) a calendar blackout pauses an affected paper strategy; (3) the Telegram-text gate test passes — plus evidence links for all VERIFY items, all tasks done/cancelled and no open S1/S2 bugs, after which PHASE.md exit boxes are ticked.

## Context & references

- Roadmap: §6 Exit criteria · [R4.14, R4.10, R4.03](../../../docs/roadmap/phase-4-intel.md#3-requirements)
- Evidence: P4-T047/T060 (brief), P4-T052 (blackout), P4-T050 (gate), P4-T051/T053/T054/T055/T056/T057/T058/T059 (other verifies).
- Phase file: `tracking/phase-4/PHASE.md`.

## Requirements

- Demo on the real stack in paper mode; screen recording + Telegram screenshot saved under `docs/demos/phase-4/` (no secrets visible).
- Each exit criterion has a pass/fail line with an evidence link.
- Board check: `./kanban validate --phase 4` 0 errors; no open S1/S2 bugs.

## ToDo

- [ ] Trigger `/brief` and capture the scheduled brief of the day.
- [ ] Run `ops/demo/blackout_nfp.sh` (paper) and capture D06/D08.
- [ ] Run the gate suite and attach the report.
- [ ] Collect VERIFY evidence links into `docs/demos/phase-4/README.md`.
- [ ] Tick PHASE.md exit criteria.

## Verification

### Tests
- Re-run P4-T050 and P4-T052 suites as part of the demo.

### Scenarios
- Given any criterion fails, then the demo stops, a bug is filed and the phase stays open.

### Stress / failure injection
- n/a: demo; stress evidence comes from P4-T058.

## Acceptance criteria

- [ ] Exit criterion 1 shown (brief with sourced items, mapped events, blackouts)
- [ ] Exit criterion 2 shown (paper strategy paused by blackout)
- [ ] Exit criterion 3 shown (gate suite green)
- [ ] All P4 tasks done/cancelled; no open S1/S2 bugs
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- If the GPU isn't available, demo on CPU mode and note it (SemIf relevance-only).

## Cardinal rules (do NOT)

- Do NOT demo against live accounts.
- Do NOT tick exit boxes without evidence links.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT touch live money (P7 gates); keys stay trade-only, IP-locked, withdrawals disabled.
- Do NOT commit secrets or paste them into chats, issues or logs; they live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/roadmap/phase-4-intel.md`: tick §6 exit criteria with evidence links

## Branch & PR

- Branch: `p4/P4-T061-phase-exit-demo`
- PR title: `P4-T061: Phase 4 exit demo`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T061` run

## Progress log

- 2026-10-21 00:00 · planner · created
