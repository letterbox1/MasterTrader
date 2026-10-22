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
depends_on: [P1-T004, P1-T005, P0-T029, P0-T030]
requirements: [R1.12]
roadmap_todos: [T1.29]
modules: [M16]
dashboards: [D07]
tools: [git, uv, docker]
mcp: []
env: []
services: [nats, postgres]
branch: p1/P1-T041-recon-framework-crypto-testnets
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/03-build-spec.md]
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

# P1-T041 · Reconcile balances and positions on crypto testnets

## Goal / expected outcome

A reconciliation framework compares our records with each venue's own: positions and open orders every 60 s, balances every 5 min, and a full reconciliation at end of day (Sydney) (defaults, configurable, [16 §2.9](../../../docs/16-configuration-and-safety-model.md#29-reconciliation)); mismatches become WORM incidents in `audit.recon` and `recon.{venue}` messages. First adapters: Binance and Bybit testnets via ccxt with read-only keys, built and tested keyless against recorded fixtures (the live run is P1-T074).

## Context & references

- Roadmap: requirements [R1.12](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.29](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M16](../../../docs/03-build-spec.md#m16-live-cost--data-quality-monitor--mt_monitor-always-on-autonomous) (Reconciliation: 60 s / 5 min / EOD defaults; an unexplained mismatch is an incident) · [07 §3](../../../docs/07-security-notes.md#3-broker--exchange-keys)
- Defaults: [16 §2.9](../../../docs/16-configuration-and-safety-model.md#29-reconciliation) (cadence, tolerance, explained vs unexplained) · decisions [17 §C](../../../docs/17-decisions-register.md#c-defaults-that-were-n-or-unspecified) P7-B007, [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P1-B008 (read-only keys where the testnet offers them)
- Build first, keys last ([17 §E](../../../docs/17-decisions-register.md#e-ratification-2026-10-22)): keyless here (fixtures/mocks); live reconciliation with your keys (P1-T002) is P1-T074 (T1.67)
- Cross-phase prerequisites (depends_on): P0-T029, P0-T030 (WORM layer for `audit.recon`)
- Depends on (this phase): P1-T004, P1-T005

## Requirements

- `mt_monitor.recon`: `ReconAdapter` (fetch balances, positions, open orders) and a comparator: position quantities must match exactly; balances within 0.01% or dust (dust from instrument precision) (defaults, [16 §2.9](../../../docs/16-configuration-and-safety-model.md#29-reconciliation))
- "Ours" in P1 = last confirmed venue snapshot plus `audit.fill`/`audit.position_snapshot` when they exist (empty until P2)
- Schedule (configurable defaults): positions and open orders every 60 s, balances every 5 min, full reconciliation at end of day Sydney time (00:05 Australia/Sydney, DST-aware); `data.recon.run` (C1) triggers on demand
- Results appended to `audit.recon` (WORM: run, venue, scope, asset, ours, theirs, diff, status `matched | explained | unexplained | unreachable`) and published on `recon.{venue}`; a mismatch is `explained` only when matched to a known journal event within 24 h (the journal arrives in P3, so every P1 mismatch is `unexplained`); unexplained → `alert.warning.recon`, escalating to `alert.critical.recon` at 24 h (the halt itself is M11's, from P2)
- HTTP allow-list: only GET/read endpoints; any write method raises before sending

## ToDo

- [ ] Implement framework, comparator, `audit.recon` (WORM) and publisher
- [ ] ccxt adapters for Binance and Bybit testnets, tested against recorded/mocked responses (no keys in CI)
- [ ] Write the tests listed under Verification
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Unit: comparator tolerances (exact positions, 0.01% balances); dust ignored; sign conventions
- Unit: the scheduler runs positions/open orders every 60 s and balances every 5 min (SimClock), and the full run at Sydney end of day across DST
- Integration: mocked venue with an injected 0.01 BTC difference → mismatch incident; clean → `ok`
- Security: adapter attempting `create_order` raises before network (test)
- WORM: `audit.recon` passes the 15 §2.4 tests

### Scenarios

- Given the venue API times out, when recon runs, then status `unreachable` (not mismatch) and retry next cycle
- Given a manual deposit on testnet, when recon runs, then mismatch → you confirm via D07 and a new baseline row is appended (no edits)

### Stress / failure injection

- Fault: venue returns 500 for 1 h; recon backs off and reports `unreachable`, no retry storm

## Acceptance criteria

- [ ] Against fixtures, clean recon runs at the default cadence (60 s / 5 min / EOD) and an injected mismatch raises an `unexplained` incident; the live run is P1-T074
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Testnet resets wipe balances: detected as mass mismatch; flagged `venue_reset` with guidance in the runbook (P1-T055)

## Cardinal rules (do NOT)

- Do NOT UPDATE or DELETE WORM rows (`audit.*`); resolutions and corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT use keys with withdrawal rights, or without an IP allow-list where the venue supports one; practice/testnet/paper only, no live money before the P7 gates.
- Do NOT place, modify or cancel orders from this code; P1 is read-only toward venues (orders arrive in P2 through M11).
- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file (kept outside the repo) mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
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
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (16 §2.9 cadence/tolerance/explained rule (P1-B017, P7-B007); keyless build, live run split to P1-T074 (T1.67); deps trimmed; P0 WORM deps)
