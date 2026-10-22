---
id: P1-T031
kind: task
title: Add the session-aware stale-feed check (data age, ≤ 250 ms reaction)
phase: 1
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T030, P1-T009]
requirements: [R1.10, R1.N1, R1.17]
roadmap_todos: [T1.27]
modules: [M16]
dashboards: [D07]
tools: [git, uv, docker]
mcp: []
env: []
services: [nats, postgres]
branch: p1/P1-T031-dq-check-stale-feed
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

# P1-T031 · Add the session-aware stale-feed check (data age, ≤ 250 ms reaction)

## Goal / expected outcome

The DQ monitor measures **data age** per instrument stream (now on the host monotonic clock − the time *we received* the last update) against the per-bot freshness thresholds (defaults 2 s fast / 60 s slow, configurable, session-aware, [16 §2.2](../../../docs/16-configuration-and-safety-model.md#22-data-freshness-what-stale-means)) and publishes `dq.status = stale` within ≤ 250 ms (p99) of a threshold being crossed, with fault-injection tests that prove it.

## Context & references

- Roadmap: requirements [R1.10](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.N1](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.17](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.27](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Definition: [16 §2.2](../../../docs/16-configuration-and-safety-model.md#22-data-freshness-what-stale-means) (data age, thresholds, session awareness, monitor reaction) · decision [17 §A](../../../docs/17-decisions-register.md#a-s2-items-all-resolved) P1-B001 (replaces "detection → paused < 2 s")
- Spec: [03 M16](../../../docs/03-build-spec.md#m16-live-cost--data-quality-monitor--mt_monitor-always-on-autonomous) (stale feed row) · SLO [02 §9.2](../../../docs/02-v1-architecture.md#92-observability--slos) · subjects [02 §6](../../../docs/02-v1-architecture.md#6-messaging-nats) · degraded modes [02 §9.3](../../../docs/02-v1-architecture.md#93-degraded-modes) · UI [D07 Data & Quality](../../../docs/ui/dashboards/D07-data-quality.md) ("What stale means")
- Downstream: from P2, M11 checks data age inline on every order (R2.58) and bots register their own thresholds; until then the thresholds come from the freshness profiles in `config/dq_checks.yaml`
- Exit criterion 3 ([phase 1 §6 exit criteria](../../../docs/roadmap/phase-1-data-and-monitoring.md#6-exit-criteria-demo))
- Depends on (this phase): P1-T030, P1-T009

## Requirements

- Data age = `monotonic_now − last_receive_monotonic` per (venue, instrument, stream); `ingest_time` is the wall-clock record of the same receive; the exchange timestamp is never used (its gap is the clock-skew check, P1-T035)
- Thresholds: freshness profiles `fast` (default 2 s) and `slow` (default 60 s), configurable ([16 §2.2](../../../docs/16-configuration-and-safety-model.md#22-data-freshness-what-stale-means)); each stream is evaluated against every distinct threshold of the bots that use it (P1: the profiles set per instrument in `config/dq_checks.yaml`; from P2 the bot registry supplies per-bot thresholds). `dq.status` carries `age_ms` and the thresholds exceeded, so a slow bot is never paused by a fast bot's threshold
- Session-aware: outside the instrument's session (`exchange_calendars`, FX weekend, venue maintenance) the status is `closed`, never `stale`; crypto is 24/7
- Connection-level signals (socket closed, venue heartbeat missed, `feed_status=disconnected`) mark the stream `stale` immediately for every threshold, without waiting for the age to cross
- Reaction SLO: `stale` published ≤ 250 ms p99 after the threshold is crossed (deadline timers from P1-T030); metrics `mt_dq_stale_reaction_seconds` (publish time − (last receive + threshold), histogram) and `mt_dq_data_age_seconds{venue,symbol}`
- SLO alert: reaction p99 > 250 ms over 1 h → `alert.warning.slo_stale` (window configurable)
- Threshold changes: tighten C1; loosen C3 (the break-glass CLI (`mtctl approve <id>` + TOTP) until Telegram C3 lands in P2)

## ToDo

- [ ] Implement data-age tracking on the monotonic clock and per-threshold deadline timers
- [ ] Implement the freshness profiles in `config/dq_checks.yaml` (defaults linked to 16 §2.2) and the per-stream threshold set
- [ ] Implement `closed` from the session resolver (P1-T009) and connection-level stale
- [ ] Export the reaction and data-age metrics and the SLO alert rule
- [ ] Fault-injection tests: silence one symbol, kill the socket, TCP blackhole, venue maintenance, closed session
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Fault injection (CI, fake venues, SimClock where possible): silence one symbol → `stale` published ≤ 250 ms after its age crosses 2 s in ≥ 99 of 100 runs (assert p99 ≤ 250 ms; record the max)
- Fault injection: kill the socket → `stale` for all its streams immediately (connection-level); TCP blackhole (no FIN) → caught by the data-age threshold or the heartbeat miss, whichever comes first
- Unit: data age uses our receive time, not exchange time (a 10 s old exchange timestamp with a fresh receive is not stale); closed session → `closed`; two thresholds (2 s, 60 s) → `age_ms` and `exceeded=[fast]` at 3 s

### Scenarios

- Given BTCUSDT on Binance stops sending while the socket stays open, when its data age crosses the 2 s fast threshold, then `dq.status` is `stale` (exceeded: fast) within 250 ms, and at 60 s it also lists slow
- Given the US market is closed, when Alpaca symbols are silent, then their status is `closed`, not `stale`, and no incident opens
- Given the feed resumes, when 3 healthy evaluations pass (default hysteresis), then status returns to `ok` and the incident resolves with a new row

### Stress / failure injection

- Chaos: randomly silence 1 of 5 crypto feeds every 2 min for 1 h with 500 instruments loaded; every silence reaches `stale` ≤ 250 ms p99 after the threshold, zero false stales on the others

## Acceptance criteria

- [ ] Reaction ≤ 250 ms p99 after the threshold in the CI fault-injection suite; metrics exported and graphed
- [ ] Closed sessions report `closed`; thresholds come from settings with 16 §2.2 defaults (no constants in code)
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Illiquid instruments can legitimately go quiet for longer than 2 s: that's a bot-threshold choice (use the slow profile), never a hidden per-instrument timeout
- Clock: data age uses the monotonic clock, so chrony steps don't create false stales
- Monitor restart: statuses start `unknown` until the first message; age is measured from that receive

## Cardinal rules (do NOT)

- Do NOT UPDATE or DELETE WORM rows (`audit.*`); resolutions and corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT measure data age from the exchange timestamp; it is now − our receive time
- Do NOT let any path loosen DQ thresholds, risk or alert routing without C3 (Telegram + TOTP + cool-down; in P1 via the break-glass CLI `mtctl approve` + TOTP); tightening is C1.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.27 once every task traced to it in PHASE.md is done; note P1-T031 next to it.
- `docs/02-v1-architecture.md` §9.2: state exactly what the 2 s measures
- `docs/03-build-spec.md` §M16: document the two-layer stale rule

## Branch & PR

- Branch: `p1/P1-T031-dq-check-stale-feed`
- PR title: `P1-T031: Add the session-aware stale-feed check (data age, ≤ 250 ms reaction)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T031` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (rewritten for data age = now − our receive time, per-bot thresholds 2 s/60 s, closed sessions, ≤ 250 ms p99 reaction (P1-B001, R1.17))
