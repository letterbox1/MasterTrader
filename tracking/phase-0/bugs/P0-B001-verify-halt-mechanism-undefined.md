---
id: P0-B001
kind: gap
title: Trading halt on audit verify mismatch has no defined mechanism or clear command
phase: 0
type: DOC
status: ready
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
branch: p0/P0-B001-verify-halt-mechanism-undefined
pr: ""
doc_sync: [docs/15-bots-hitl-and-worm-audit.md, docs/02-v1-architecture.md, docs/03-build-spec.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: docs/15-bots-hitl-and-worm-audit.md §2.2 (Verification)
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
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

- [ ] Confirm the decision with the user (or take the suggested fix if no objection)
- [ ] Update the listed docs so they agree
- [ ] Update the affected P0 task files' Context if the decision differs from the suggestion
- [ ] Add/adjust a regression check where one is possible (see Verification)

## Verification

### Tests
- Doc check: grep the listed docs for the conflicting statements; none remain after the fix.

### Scenarios
- Given a developer reads any of the listed docs, then they reach the same answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [ ] Listed docs updated and consistent
- [ ] Affected tasks reference the resolution
- [ ] Root cause (how the drift happened) noted in the progress log

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
