---
id: P1-T035
kind: task
title: Add the clock-skew check (recv minus exchange time, chrony offset)
phase: 1
type: BUILD
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T030, P0-T019]
requirements: [R1.10]
roadmap_todos: [T1.27]
modules: [M16]
dashboards: [D07]
tools: [git, uv, docker]
mcp: []
env: []
services: [nats, postgres, prometheus]
branch: p1/P1-T035-dq-check-clock-skew
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

# P1-T035 · Add the clock-skew check (recv minus exchange time, chrony offset)

## Goal / expected outcome

Per-feed p99 of `recv_ts − exchange_ts` and the host's chrony offset are tracked; skew beyond thresholds degrades the affected feeds and alerts, protecting timestamps that pit and TCA rely on.

## Context & references

- Roadmap: requirements [R1.10](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.27](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M16](../../../docs/03-build-spec.md#m16-live-cost--data-quality-monitor--mt_monitor-always-on-autonomous) (DQ checks table) · flow [02 §8 F1](../../../docs/02-v1-architecture.md#8-end-to-end-flows) step 5 · subjects [02 §6](../../../docs/02-v1-architecture.md#6-messaging-nats) · degraded modes [02 §9.3](../../../docs/02-v1-architecture.md#93-degraded-modes) · UI [D07 Data & Quality](../../../docs/ui/dashboards/D07-data-quality.md) Quality tab
- Host time: chrony set up in P0 (R0.N2, T0.40)
- Depends on (this phase): P1-T030
- Cross-phase prerequisites (depends_on): P0-T019 (host hardening: Tailscale, chrony offset metric)

## Requirements

- Rolling p50/p99 of `ingest_time − event_time` per feed (60 s window); baseline per venue (network latency) learned over 24 h
- Skew incident when p99 exceeds baseline + 250 ms (default) or goes negative beyond −50 ms (our clock behind)
- Chrony offset from the node_exporter textfile metric set up in P0-T019 (no new exporter); |offset| > 50 ms (default, configurable) → `alert.critical.clock`
- Metrics feed the D07 clock-skew chart

## ToDo

- [ ] Implement skew stats and incident rules
- [ ] Read the P0-T019 chrony offset metric (add a scrape rule only if missing)
- [ ] Fault injection: shift exchange timestamps +1 s and −200 ms; fake chrony offset
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Fault injection: +1 s skew → incident; negative skew → `clock` alert
- Unit: baseline learning ignores reconnect bursts

### Scenarios

- Given chrony loses sync, when offset drifts past 50 ms, then a critical alert fires on all channels and all feeds show `degraded` (timestamps untrustworthy)

### Stress / failure injection

- n/a: covered by the fault-injection tests

## Acceptance criteria

- [ ] Skew charts populated; injected skew detected; chrony offset scraped
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Data age (P1-T031) uses our receive time, so exchange-clock skew never makes a feed stale; skew is reported separately ([16 §2.2](../../../docs/16-configuration-and-safety-model.md#22-data-freshness-what-stale-means))
- Venues whose timestamps are batch times (e.g. 100 ms book frames) have a higher baseline; per-venue baselines avoid false alerts

## Cardinal rules (do NOT)

- Do NOT UPDATE or DELETE WORM rows (`audit.*`); resolutions and corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT let any path loosen DQ thresholds, risk or alert routing without C3 (Telegram + TOTP + cool-down; in P1 via the break-glass CLI `mtctl approve` + TOTP); tightening is C1.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).
- Do NOT add an image without pinning it by digest, or vendored code that carries telemetry or referral IDs.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.27 once every task traced to it in PHASE.md is done; note P1-T035 next to it.
- `docs/03-build-spec.md` §M16: skew thresholds

## Branch & PR

- Branch: `p1/P1-T035-dq-check-clock-skew`
- PR title: `P1-T035: Add the clock-skew check (recv minus exchange time, chrony offset)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T035` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (reuse P0-T019 chrony metric; skew separate from data age (16 §2.2))
