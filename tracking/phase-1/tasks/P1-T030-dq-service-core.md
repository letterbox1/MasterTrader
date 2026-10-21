---
id: P1-T030
kind: task
title: Build the mt_monitor DQ service core
phase: 1
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T004, P1-T010]
requirements: [R1.10]
roadmap_todos: [T1.27]
modules: [M16]
dashboards: [D07]
branch: p1/P1-T030-dq-service-core
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/03-build-spec.md, docs/02-v1-architecture.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P1-T030 · Build the mt_monitor DQ service core

## Goal / expected outcome

`monitor` runs a streaming DQ engine on NATS with rolling state per (venue, instrument), a pluggable checks registry, a status machine publishing `dq.status.{venue}.{symbol}` and KV `feed_status`, and WORM incidents in `audit.dq_event`.

## Context & references

- Roadmap: requirements [R1.10](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.27](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M16](../../../docs/03-build-spec.md#m16-live-cost--data-quality-monitor--mt_monitor-always-on-autonomous) (DQ checks table) · flow [02 §8 F1](../../../docs/02-v1-architecture.md#8-end-to-end-flows) step 5 · subjects [02 §6](../../../docs/02-v1-architecture.md#6-messaging-nats) · degraded modes [02 §9.3](../../../docs/02-v1-architecture.md#93-degraded-modes) · UI [D07 Data & Quality](../../../docs/ui/dashboards/D07-data-quality.md) Quality tab
- WORM: [15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many) (DQ events are WORM; 15 §2.4 tests apply to every phase adding a WORM table)
- Downstream: P2 risk manager blocks orders on `stale`/`bad` (R2.16); M11 is told to pause affected strategies
- Depends on (this phase): P1-T004, P1-T010

## Requirements

- Package `mt_monitor.dq`: `InstrumentState` (last msg times, last seq, rolling median/MAD, spreads, recv-exchange deltas), `Check` interface (`on_message`, `on_tick(now)`), registry from `config/dq_checks.yaml` (check, scope, thresholds, severity)
- Status per instrument: `ok | degraded | stale | bad` + reasons; worst-of rule across checks; hysteresis (N consecutive ok evaluations before recovery) to avoid flapping
- Publish on every status change to `dq.status.{venue}.{symbol}` and KV `feed_status`; periodic re-publish every 5 s
- Incident lifecycle: open/update/resolve rows appended to `audit.dq_event` (check, instrument, venue, observed, threshold, started_at, resolved_at via a new row with `supersedes_id`); also `alert.{severity}.dq`
- Evaluation timer at 250 ms so timeout-based checks can meet the < 2 s SLO
- Threshold changes: tighten = C1, loosen = C3 via `system.settings.update` (until P1-B009 is resolved, loosening is a reviewed PR to `config/dq_checks.yaml`)
- Heartbeat `sys.heartbeat.monitor` (dead-man input in P2)

## ToDo

- [ ] Implement state store, check registry, status machine with hysteresis and publisher
- [ ] Migration for `audit.dq_event` under the WORM layer (owner `worm_owner`, INSERT/SELECT grants, hash chain trigger from P0)
- [ ] Incident writer with supersede semantics and alert publishing
- [ ] A fault-injection harness `mt_monitor.testing.FaultInjector` (drop, delay, corrupt, skew, reorder) reused by P1-T031…T036 and P1-T057
- [ ] Write the tests listed under Verification
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Unit: worst-of status, hysteresis, re-publish cadence
- WORM (15 §2.4): app-role UPDATE/DELETE/TRUNCATE on `audit.dq_event` fails; hash chain verifies after 1k incidents
- Integration: injected fault → incident open row → resolve row; KV and subject match

### Scenarios

- Given a check flips ok→bad→ok within 1 s, when hysteresis is 3 evaluations, then one incident opens and closes once (no flapping alerts)
- Given the monitor restarts, when it comes back, then statuses start `unknown`, recover from live data, and open incidents are reconciled (resolved rows appended if healthy)

### Stress / failure injection

- Load: 500 instruments × 50 msgs/s through the engine; evaluation loop p99 < 50 ms; CPU < 1 core

## Acceptance criteria

- [ ] `dq.status.*` published for every streaming instrument; incidents in `audit.dq_event` pass the WORM suite
- [ ] Fault-injection harness available to later checks
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Postgres down: statuses still publish to NATS; incident rows buffer in a bounded JetStream queue and flush later (02 §9.3)
- NATS down: monitor cannot see data → everything `unknown`; dead-man in P2 handles it

## Cardinal rules (do NOT)

- Do NOT UPDATE or DELETE WORM rows (`audit.*`); resolutions and corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT let any path loosen DQ thresholds, risk or alert routing without C3 (Telegram + TOTP + cool-down); tightening is C1.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.27 once every task traced to it in PHASE.md is done; note P1-T030 next to it.
- `docs/03-build-spec.md` §M16: link `config/dq_checks.yaml` and the status rules
- `docs/02-v1-architecture.md` §6: confirm `dq.status` payload fields

## Branch & PR

- Branch: `p1/P1-T030-dq-service-core`
- PR title: `P1-T030: Build the mt_monitor DQ service core`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T030` run

## Progress log

- 2026-10-21 00:00 · planner · created
