---
id: P0-B001
kind: gap
title: Trading halt on audit verify mismatch has no defined mechanism or clear command
phase: 0
type: DOC
status: done
priority: high
size: S
severity: S2
owner: agent
claimed_by: ""
depends_on: []
requirements: [R0.07]
roadmap_todos: [T0.23]
modules: []
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p0/P0-B001-verify-halt-mechanism-undefined
pr: ""
doc_sync: [docs/15-bots-hitl-and-worm-audit.md, docs/02-v1-architecture.md, docs/03-build-spec.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: done
found_in: docs/15-bots-hitl-and-worm-audit.md §2.2 (Verification)
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P0-B001 · Trading halt on audit verify mismatch has no defined mechanism or clear command

## Goal / expected outcome

The docs agree and the implementing tasks have one unambiguous answer. Suggested fix: Adopt `risk_state.trading_halt` (reason, incident_id) + `risk.halt.clear` (C3); add it to 02 §6/§7.2, 03 M11 pre-trade checks and the P2 roadmap as a cross-phase requirement.

## Context & references

- Found in: `docs/15-bots-hitl-and-worm-audit.md §2.2 (Verification)`
- Related: P0-T038, P0-T055
- [15 §2.2 layers](../../../docs/15-bots-hitl-and-worm-audit.md#22-layers)
- [02 §7.2 commands](../../../docs/02-v1-architecture.md#72-commands-rest-write)

## Requirements

- **Steps to reproduce:** Read 15 §2.2 'halt new trading', 02 §6 KV list and 02 §7.2 command catalogue.
- **Expected:** A named state (e.g. NATS KV `risk_state.trading_halt`) that M11 honours, distinct from the kill switch (which cancels and may flatten), plus a C3 command to clear it.
- **Actual:** 15 §2.2 says verify mismatch halts new trading (default on) but no doc says how: no KV key, no NATS subject, no clear command (`risk.halt.clear` is absent from 02 §7.2), and P2's M11 requirements don't mention honouring it.
- **Impact:** Without a contract, P0 sets a flag nobody reads and P2 may not block orders on a broken audit trail.
- **Suggested fix:** Adopt `risk_state.trading_halt` (reason, incident_id) + `risk.halt.clear` (C3); add it to 02 §6/§7.2, 03 M11 pre-trade checks and the P2 roadmap as a cross-phase requirement.

## ToDo

- [x] Decision taken: 17 §A P0-B001 (ratified in 17 §E)
- [x] Docs updated so they agree: 16 §2.11 + §3.3; 15 §2.2 (integrity response) + §2.4; 02 §5.1 (KV `audit.integrity`), §7.2 (`audit.integrity.ack` C3), §9.3; 03 M11 pre-trade + M17; 07 §6, §8; roadmap P0 R0.12/T0.27 and P2 R2.58/T2.39/T2.71
- [x] Affected P0 task files reference the resolution: P0-T038, P0-T035, P0-T046, P0-T050, P0-T052, P0-T055, P0-T061, P0-T069
- [x] Regression check owned: P0-T069 integrity drill and the P0-T038 `integrity_gate` golden tests

## Verification

### Tests
- Doc check: grep the listed docs for the conflicting statements; none remain after the fix.

### Scenarios
- Given a developer reads any of the listed docs, then they reach the same answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Listed docs carry the 17 §A P0-B001 decision and agree (checked in the alignment wave, 2026-10-22)
- [x] Implementation owned by: P0-T038 (KV status, `mt_risk.integrity_gate`, ack), P0-T069 (drill); P2 T2.39 calls the gate inline
- [x] Root cause noted in the progress log

## Exceptions & edge cases

- If the user decides differently from the suggestion, the affected tasks are updated before they start.

## Cardinal rules (do NOT)

- Do NOT close without updating every listed doc.
- Do NOT edit WORM records to 'fix' data; append a correction instead.

## Doc sync on completion

- `docs/15-bots-hitl-and-worm-audit.md`: reconcile as described.
- `docs/02-v1-architecture.md`: reconcile as described.
- `docs/03-build-spec.md`: reconcile as described.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: reconcile as described.

## Branch & PR

- Branch: `p0/P0-B001-verify-halt-mechanism-undefined`
- PR title: `P0-B001: fix trading halt on audit verify mismatch has no defined mechanism or clear command`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-B001` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by 17 §A P0-B001; docs checked: 16 §2.11 + §3.3; 15 §2.2 (integrity response) + §2.4; 02 §5.1 (KV `audit.integrity`), §7.2 (`audit.integrity.ack` C3), §9.3; 03 M11 pre-trade + M17; 07 §6, §8; roadmap P0 R0.12/T0.27 and P2 R2.58/T2.39/T2.71. Root cause: 15 §2.2 said 'halt new trading' before any doc defined a state, consumer or clear command. Implementation owned by P0-T038 (KV status, `mt_risk.integrity_gate`, ack), P0-T069 (drill); P2 T2.39 calls the gate inline.
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §A P0-B001); docs updated: 16 §2.11 + §3.3; 15 §2.2 (integrity response) + §2.4; 02 §5.1 (KV `audit.integrity`), §7.2 (`audit.integrity.ack` C3), §9.3; 03 M11 pre-trade + M17; 07 §6, §8; roadmap P0 R0.12/T0.27 and P2 R2.58/T2.39/T2.71; implementation owned by P0-T038 (KV status, `mt_risk.integrity_gate`, ack), P0-T069 (drill); P2 T2.39 calls the gate inline
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:05 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
