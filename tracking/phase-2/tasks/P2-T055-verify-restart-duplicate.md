---
id: P2-T055
kind: task
title: "Restart-duplicate test: crash mid-order, no duplicates, reconcile"
phase: 2
type: VERIFY
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T027, P2-T023]
requirements: [R2.32]
roadmap_todos: [T2.62]
modules: [M12]
dashboards: []
branch: p2/P2-T055-verify-restart-duplicate
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T055 · Restart-duplicate test: crash mid-order, no duplicates, reconcile

## Goal / expected outcome

A chaos test crashes the engine at each point of the order lifecycle on testnet/sandbox and proves restarts never duplicate orders and always reconcile open orders/positions before trading resumes.

## Context & references

- Roadmap: [R2.32](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.62
- Spec: [03 M12](../../../docs/03-build-spec.md#m12-execution--mt_engine)
- Related: P2-T027, P2-B007.

## Requirements

- Crash points: after intent ledger write / before submit; after submit / before ack; after ack / before fill; during partial fill; during cancel.
- After restart: venue order count per intent = 1; local state = venue state; trading resumes only after `READY`.
- Run on sandbox (all points, 100 iterations) and Binance testnet + one custom adapter (OANDA) (each point × 5).

## ToDo

- [ ] Fault-injection hooks (env-guarded, disabled in prod builds)
- [ ] Chaos runner
- [ ] Assertions + report
- [ ] Record results (numbers, run IDs, screenshots) in the progress log and tick the roadmap ToDo box

## Verification

### Tests
- As above.

### Scenarios
- Given a crash after submit before ack, when the engine restarts, then it finds the order by client id and does not resubmit.

### Stress / failure injection
- 100 sandbox iterations per crash point.

## Acceptance criteria

- [ ] 0 duplicates across all iterations
- [ ] Resume only after reconciliation in every run

## Exceptions & edge cases

- Venue down at restart: venue stays 'unconfirmed'; test asserts hold, not resume.

## Cardinal rules (do NOT)

- Do NOT leave fault-injection hooks enabled outside test builds.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.

## Doc sync on completion

- `docs/03-build-spec.md` M12: link the chaos test.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.62 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T055-verify-restart-duplicate`
- PR title: `P2-T055: Restart-duplicate test: crash mid-order, no duplicates, reconcile`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T055` run

## Progress log

- 2026-10-21 00:00 · planner · created
