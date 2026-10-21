---
id: P1-T031
kind: task
title: Add the session-aware stale-feed check (< 2 s)
phase: 1
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T030, P1-T009]
requirements: [R1.10, R1.N1]
roadmap_todos: [T1.27]
modules: [M16]
dashboards: [D07]
branch: p1/P1-T031-dq-check-stale-feed
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

# P1-T031 · Add the session-aware stale-feed check (< 2 s)

## Goal / expected outcome

A stale feed is marked `stale` on `dq.status` within 2 s, using connection-level signals (socket closed, heartbeat missed) and per-instrument session-aware timeouts, with fault-injection tests that prove the SLO.

## Context & references

- Roadmap: requirements [R1.10](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.N1](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.27](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M16](../../../docs/03-build-spec.md#m16-live-cost--data-quality-monitor--mt_monitor-always-on-autonomous) (DQ checks table) · flow [02 §8 F1](../../../docs/02-v1-architecture.md#8-end-to-end-flows) step 5 · subjects [02 §6](../../../docs/02-v1-architecture.md#6-messaging-nats) · degraded modes [02 §9.3](../../../docs/02-v1-architecture.md#93-degraded-modes) · UI [D07 Data & Quality](../../../docs/ui/dashboards/D07-data-quality.md) Quality tab
- SLO: [02 §9.2](../../../docs/02-v1-architecture.md#92-observability--slos) (feed staleness detection → strategy paused < 2 s); R1.N1; exit criterion 3 ([phase 1 §6 exit criteria](../../../docs/roadmap/phase-1-data-and-monitoring.md#6-exit-criteria-demo))
- Ambiguity on where the 2 s starts: P1-B001
- Depends on (this phase): P1-T030, P1-T009

## Requirements

- Two layers: (1) connection-level: on socket close, missed venue heartbeat/ping, or `feed_status=disconnected` → all instruments of that feed `stale` immediately (target < 500 ms); (2) per-instrument: no message for `timeout(instrument, venue, session)` → `stale`
- Timeouts learned per instrument × hour-of-week (p99.9 inter-arrival × factor, min 2 s, configurable) and zero outside sessions (`exchange_calendars` / FX weekend / crypto 24/7)
- Metric `mt_dq_stale_detect_seconds` = detection time − last message time (histogram) and `mt_dq_stale_publish_seconds` = publish − detection
- SLO alert: p99 of (kill → `stale` published) > 2 s over 1 h → `alert.warning.slo_stale`

## ToDo

- [ ] Implement both layers and the learned-timeout job (nightly, from Parquet inter-arrival stats)
- [ ] Fault-injection tests: kill socket, blackhole TCP, stop publishing one symbol, venue maintenance
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Fault injection (CI, fake venues): kill the socket → `stale` published within 2 s in 100/100 runs (assert p100 < 2 s)
- Fault injection: TCP blackhole (no FIN) → detected via heartbeat miss within heartbeat interval + 2 s (documented separately per venue)
- Unit: no stale outside sessions; timeouts never below 2 s floor

### Scenarios

- Given BTCUSDT on Binance stops sending while the socket stays open, when its learned timeout (e.g. 3 s) passes, then it is `stale` within one 250 ms evaluation tick
- Given US market closed, when Alpaca symbols are silent, then nothing is stale
- Given the feed resumes, when 3 healthy evaluations pass, then status returns to `ok` and the incident resolves

### Stress / failure injection

- Chaos: randomly kill 1 of 5 crypto feeds every 2 min for 1 h; every kill detected < 2 s, zero false stales on the others

## Acceptance criteria

- [ ] Socket-kill → `stale` p100 < 2 s in the CI fault-injection suite
- [ ] SLO metrics exported and graphed
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Very illiquid instruments: per-instrument timeout may exceed 2 s by design; the < 2 s SLO applies to connection-level staleness (record this in P1-B001's resolution)
- Clock step: timers use monotonic time

## Cardinal rules (do NOT)

- Do NOT UPDATE or DELETE WORM rows (`audit.*`); resolutions and corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT let any path loosen DQ thresholds, risk or alert routing without C3 (Telegram + TOTP + cool-down); tightening is C1.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.27 once every task traced to it in PHASE.md is done; note P1-T031 next to it.
- `docs/02-v1-architecture.md` §9.2: state exactly what the 2 s measures
- `docs/03-build-spec.md` §M16: document the two-layer stale rule

## Branch & PR

- Branch: `p1/P1-T031-dq-check-stale-feed`
- PR title: `P1-T031: Add the session-aware stale-feed check (< 2 s)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T031` run

## Progress log

- 2026-10-21 00:00 · planner · created
