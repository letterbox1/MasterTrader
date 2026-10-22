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
depends_on: [P1-T004, P0-T029, P0-T030, P0-T035]
requirements: [R1.10, R1.17]
roadmap_todos: [T1.27]
modules: [M16]
dashboards: [D07]
tools: [git, uv, docker]
mcp: []
env: []
services: [nats, postgres]
branch: p1/P1-T030-dq-service-core
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/03-build-spec.md, docs/02-v1-architecture.md]
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

# P1-T030 · Build the mt_monitor DQ service core

## Goal / expected outcome

`monitor` runs a streaming DQ engine on NATS with rolling state per (venue, instrument), a pluggable checks registry, a status machine publishing `dq.status.{venue}.{symbol}` (`ok | degraded | stale | closed | bad`) and KV `feed_status`, WORM incidents in `audit.dq_event`, and incident acknowledgements as separate WORM rows in `audit.dq_ack`.

## Context & references

- Roadmap: requirements [R1.10](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.27](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M16](../../../docs/03-build-spec.md#m16-live-cost--data-quality-monitor--mt_monitor-always-on-autonomous) (DQ checks table) · flow [02 §8 F1](../../../docs/02-v1-architecture.md#8-end-to-end-flows) step 5 · subjects [02 §6](../../../docs/02-v1-architecture.md#6-messaging-nats) · degraded modes [02 §9.3](../../../docs/02-v1-architecture.md#93-degraded-modes) · UI [D07 Data & Quality](../../../docs/ui/dashboards/D07-data-quality.md) Quality tab
- WORM: [15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many) (DQ events are WORM; 15 §2.4 tests apply to every phase adding a WORM table)
- Downstream: from P2, M11 checks data age inline on every order (R2.58) and pauses affected bots on `stale`/`bad` (R2.16); the monitor's status is the pause signal, not the only guard ([16 §2.2](../../../docs/16-configuration-and-safety-model.md#22-data-freshness-what-stale-means))
- Decisions: [17 §A](../../../docs/17-decisions-register.md#a-s2-items-all-resolved) P1-B001 (data age, ≤ 250 ms p99) · [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P1-B018 (ack = a new `audit.dq_ack` row), P0-B002/P1-B009 (C3 via the break-glass CLI until Telegram C3 in P2) · [17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer) canonical audit names
- Cross-phase prerequisites (depends_on): P0-T029 (WORM privileges/triggers), P0-T030 (hash chain), P0-T035 (C1/C3 classification and break-glass approval)
- Depends on (this phase): P1-T004

## Requirements

- Package `mt_monitor.dq`: `InstrumentState` (last msg times, last seq, rolling median/MAD, spreads, recv-exchange deltas), `Check` interface (`on_message`, `on_tick(now)`), registry from `config/dq_checks.yaml` (check, scope, thresholds, severity)
- Status per instrument stream: `ok | degraded | stale | closed | bad` + reasons + current data age; `closed` for closed sessions (never stale); worst-of rule across checks; hysteresis (default 3 consecutive ok evaluations, configurable) applies to recovery only, so entering `stale`/`bad` is never delayed
- Publish on every status change to `dq.status.{venue}.{symbol}` and KV `feed_status`; periodic re-publish every 5 s
- Incident lifecycle: open/update/resolve rows appended to `audit.dq_event` (check, instrument, venue, observed, threshold and the layer that set it, auto-action, started_at, resolved_at via a new row with `supersedes_id`); also `alert.{severity}.dq` through the one fan-out. Acknowledgement (`data.incident.ack`, C0) appends an `audit.dq_ack` row referencing the incident; the incident row is never updated
- Timing: deadline-driven timers per stream (fire at last receive + threshold) plus a 50 ms safety sweep, so `stale` is published ≤ 250 ms p99 after a data-age threshold is crossed (R1.N1, R1.17)
- Thresholds are configurable defaults from [16 §2.2](../../../docs/16-configuration-and-safety-model.md#22-data-freshness-what-stale-means) held in settings (`config/dq_checks.yaml` seeds them, never constants in code): tighten = C1, loosen = C3 via `system.settings.update`; until Telegram C3 lands in P2, C3 completes via the break-glass CLI (`mtctl approve <id>` + TOTP), audited. Every change is a versioned WORM row
- Heartbeat `sys.heartbeat.monitor` (dead-man input in P2)

## ToDo

- [ ] Implement state store, check registry, status machine with hysteresis and publisher
- [ ] Migrations for `audit.dq_event` and `audit.dq_ack` under the WORM layer (owner `worm_owner`, INSERT/SELECT grants, hash chain trigger from P0)
- [ ] Incident writer with supersede semantics and alert publishing
- [ ] A fault-injection harness `mt_monitor.testing.FaultInjector` (drop, delay, corrupt, skew, reorder) reused by P1-T031…T036 and P1-T057
- [ ] Write the tests listed under Verification
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Unit: worst-of status, hysteresis, re-publish cadence
- WORM (15 §2.4): app-role UPDATE/DELETE/TRUNCATE on `audit.dq_event` and `audit.dq_ack` fails; hash chain verifies after 1k incidents and acks
- Unit: an ack writes one `audit.dq_ack` row referencing the incident and leaves the incident row byte-identical
- Integration: injected fault → incident open row → resolve row; KV and subject match

### Scenarios

- Given a check flips ok→bad→ok within 1 s, when hysteresis is 3 evaluations, then one incident opens and closes once (no flapping alerts)
- Given the monitor restarts, when it comes back, then statuses start `unknown`, recover from live data, and open incidents are reconciled (resolved rows appended if healthy)

### Stress / failure injection

- Load: 500 instruments × 50 msgs/s through the engine; evaluation loop p99 < 50 ms; CPU < 1 core

## Acceptance criteria

- [ ] `dq.status.*` published for every streaming instrument; incidents in `audit.dq_event` and acks in `audit.dq_ack` pass the WORM suite
- [ ] Fault-injection harness available to later checks
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Postgres down: statuses still publish to NATS; incident rows buffer in JetStream (default bound 1 GB or 24 h, [16 §3.3](../../../docs/16-configuration-and-safety-model.md#33-records-the-write-path-vs-the-integrity-check)) and flush later (02 §9.3)
- NATS down: monitor cannot see data → everything `unknown`; dead-man in P2 handles it

## Cardinal rules (do NOT)

- Do NOT UPDATE or DELETE WORM rows (`audit.*`); resolutions and corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT let any path loosen DQ thresholds, risk or alert routing without C3 (Telegram + TOTP + cool-down; in P1 via the break-glass CLI `mtctl approve` + TOTP); tightening is C1.
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
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (status incl. closed; audit.dq_ack acks (P1-B018); ≤ 250 ms reaction via deadline timers (P1-B001); thresholds as 16 §2.2 defaults, C3 via break-glass (P1-B009); P0 WORM/C-level deps)
