---
id: P7-T050
kind: task
title: Reconciliation fault injection: disconnects, partial fills, phantom positions
phase: 7
type: VERIFY
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T025, P7-T026, P7-T027]
requirements: [R7.09]
roadmap_todos: [T7.23]
modules: [M16, M12, M18]
dashboards: [D07, D05]
tools: [git, uv, docker, toxiproxy]
mcp: []
env: []
services: [postgres, nats]
branch: p7/P7-T050-verify-recon-fault-injection
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-7-prove-and-go-live.md]
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

# P7-T050 · Reconciliation fault injection: disconnects, partial fills, phantom positions

## Goal / expected outcome

A fault-injection suite proves the three-way reconciliation and unconfirmed-state logic under realistic failures, producing the 'recon report' that verifies R7.09.

## Context & references

- Roadmap: [R7.09 · ToDo T7.23](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [03 M16](../../../docs/03-build-spec.md#m16-live-cost--data-quality-monitor--mt_monitor-always-on-autonomous) · [02 §9.3](../../../docs/02-v1-architecture.md#93-degraded-modes) · Roadmap R7.09 'Verified by: recon report'
- Related: P7-T025, P7-T026, P7-T027

## Requirements

- Faults: WS drop during a partial fill; REST 5xx on submit with a later fill; engine crash between submit and ack; journal consumer lag 10 min; STP cancel; fee rounding; phantom engine position; missing resting stop; venue maintenance window; exit-node tunnel down.
- Expected: each fault ends in a confirmed account with zero unexplained breaks, or a break that alerts immediately, becomes unexplained if no journal event matches within 24 h, and then halts everything (16 §2.9, clock-injected).
- Output: a recon report (HTML) summarising each fault, detection time and resolution — attached to the progress log.

## ToDo

- [ ] Fault injector (toxiproxy for network, venue mock for 5xx/partial fills).
- [ ] Cases in `tests/sim/test_recon_faults.py`.
- [ ] Generate and attach the recon report.

## Verification

### Tests
- Sim suite with one test per fault; detection time asserted ≤ one recon interval (60 s positions/orders, 5 min balances, [16 §2.9](../../../docs/16-configuration-and-safety-model.md#29-reconciliation)) + 30 s.

### Scenarios
- Given an engine crash between submit and ack, when the engine restarts, then the venue order is adopted (no duplicate) and the account is confirmed after recon.

### Stress / failure injection
- Run with 10 sub-accounts concurrently and 5% random packet loss for 1 h: no duplicate orders, no missed breaks.

## Acceptance criteria

- [ ] All fault cases pass; recon report attached.
- [ ] No duplicate orders across all runs.

## Exceptions & edge cases

- toxiproxy must never be in the production compose file.

## Cardinal rules (do NOT)

- Do NOT inject faults against live accounts.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.
- Do NOT update or delete WORM rows; corrections are new rows with `supersedes_id` (15 §2).

## Doc sync on completion

- `docs/03-build-spec.md` M16: link the recon fault suite.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.23 when this item is done.

## Branch & PR

- Branch: `p7/P7-T050-verify-recon-fault-injection`
- PR title: `P7-T050: Reconciliation fault injection: disconnects, partial fills, phantom positions`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T050` run · evidence (redacted, no secrets) linked in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (cadence and 24 h rule per 16 §2.9; tunnel-down fault)
