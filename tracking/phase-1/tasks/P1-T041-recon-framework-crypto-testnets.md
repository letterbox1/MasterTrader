---
id: P1-T041
kind: task
title: Reconcile balances and positions on crypto testnets
phase: 1
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T005, P1-T030]
requirements: [R1.12]
roadmap_todos: [T1.29]
modules: [M16]
dashboards: [D07]
branch: p1/P1-T041-recon-framework-crypto-testnets
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/03-build-spec.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P1-T041 · Reconcile balances and positions on crypto testnets

## Goal / expected outcome

A reconciliation framework compares our recorded balances/positions with each venue's own records every N minutes and at end of day; mismatches become incidents. First adapters: Binance and Bybit testnets via ccxt read-only.

## Context & references

- Roadmap: requirements [R1.12](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.29](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M16](../../../docs/03-build-spec.md#m16-live-cost--data-quality-monitor--mt_monitor-always-on-autonomous) (Reconciliation: every N minutes and EOD; any mismatch is an incident) · [07 §3](../../../docs/07-security-notes.md#3-broker--exchange-keys)
- Keys: P1-T002; known gap on read-only scopes P1-B008; N is unspecified (P1-B017)
- Depends on (this phase): P1-T005, P1-T030

## Requirements

- `mt_monitor.recon`: `ReconAdapter` (fetch balances, positions, open orders) and a comparator with per-asset tolerances (dust thresholds from instrument precision)
- "Ours" in P1 = last confirmed venue snapshot plus `audit.fill`/`audit.position_snapshot` when they exist (empty until P2)
- Schedule: every 15 min (default N, configurable) and EOD at 00:05 UTC; `data.recon.run` command triggers on demand
- Results appended to `audit.recon` (WORM: run, venue, asset, ours, theirs, diff, status) and published on `recon.{venue}`; mismatch → `alert.warning.recon`
- HTTP allow-list: only GET/read endpoints; any write method raises before sending

## ToDo

- [ ] Implement framework, comparator, `audit.recon` (WORM) and publisher
- [ ] ccxt adapters for Binance and Bybit testnets
- [ ] Write the tests listed under Verification
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Unit: comparator tolerances; dust ignored; sign conventions
- Integration: mocked venue with an injected 0.01 BTC difference → mismatch incident; clean → `ok`
- Security: adapter attempting `create_order` raises before network (test)
- WORM: `audit.recon` passes the 15 §2.4 tests

### Scenarios

- Given the venue API times out, when recon runs, then status `unreachable` (not mismatch) and retry next cycle
- Given a manual deposit on testnet, when recon runs, then mismatch → you confirm via D07 and a new baseline row is appended (no edits)

### Stress / failure injection

- Fault: venue returns 500 for 1 h; recon backs off and reports `unreachable`, no retry storm

## Acceptance criteria

- [ ] Clean recon runs on both testnets every 15 min and at EOD; injected mismatch raises an incident
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Testnet resets wipe balances: detected as mass mismatch; flagged `venue_reset` with guidance in the runbook (P1-T055)

## Cardinal rules (do NOT)

- Do NOT UPDATE or DELETE WORM rows (`audit.*`); resolutions and corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT use keys with withdrawal rights or without an IP allow-list; practice/testnet/paper only, no live money before the P7 gates.
- Do NOT place, modify or cancel orders from this code; P1 is read-only toward venues (orders arrive in P2 through M11).
- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.29 once every task traced to it in PHASE.md is done; note P1-T041 next to it.
- `docs/03-build-spec.md` §M16: record N=15 min default and EOD time

## Branch & PR

- Branch: `p1/P1-T041-recon-framework-crypto-testnets`
- PR title: `P1-T041: Reconcile balances and positions on crypto testnets`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T041` run

## Progress log

- 2026-10-21 00:00 · planner · created
