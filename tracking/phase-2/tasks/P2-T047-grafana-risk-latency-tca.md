---
id: P2-T047
kind: task
title: Grafana boards and alerts for risk, ladder, kill/dead-man, SLOs and TCA
phase: 2
type: OPS
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T017, P2-T031, P2-T032, P2-T029, P0-T045, P1-T045]
requirements: [R2.N1, R2.34]
roadmap_todos: [T2.42]
modules: [M17, M11]
dashboards: []
tools: [docker]
mcp: []
env: []
services: [grafana, prometheus]
branch: p2/P2-T047-grafana-risk-latency-tca
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T047 · Grafana boards and alerts for risk, ladder, kill/dead-man, SLOs and TCA

## Goal / expected outcome

Provisioned Grafana dashboards show risk state, ladder rung, kill and dead-man status, the Phase 2 latency SLOs and TCA, with alert rules routed to Telegram + ntfy.

## Context & references

- Roadmap: [R2.N1, R2.34](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.42
- SLOs: [02 §9.2](../../../docs/02-v1-architecture.md#92-observability--slos) · [03 M16 TCA](../../../docs/03-build-spec.md#m16-live-cost--data-quality-monitor--mt_monitor-always-on-autonomous)
- Cross-phase (`depends_on`): Grafana provisioning + baseline alert rules (P0-T045, T0.46); one alert fan-out Grafana → webhook → `alert.*` → Telegram/ntfy/email (P1-T045, 17 §D P1-B007).

## Requirements

- Dashboards (JSON in `ops/grafana/dashboards/`): Risk (trading allowed, kill, ladder per sleeve, sleeve and system drawdown vs their two stages, limit usage, rejects by reason incl. safety-state rejects: data age, `audit.integrity`, egress), Dead-man (three layers: in-engine heartbeat ages, `deadman` sidecar heartbeat, venue timer refresh age), Latency SLOs (`mt_risk_check_seconds` p99 < 1 ms, signal→submit p99 < 5 ms, tier-A p99 < 50 µs (metric from Part B), `mt_kill_to_cancels_seconds` < 1 s), TCA (IS bps by strategy/venue, realised-vs-modelled ratio).
- Alerts: SLO burn (p99 above target for 5 min), kill ON, dead-man fired (any layer), `deadman` sidecar missing, venue timer not refreshed, ladder ≥ 4, sleeve/system drawdown stage reached, cost ratio > 1.5× over 20 fills, key age > 90 days. Thresholds read from the 16 defaults, not duplicated by hand where a metric carries the limit.
- Loki links via `trace_id` exemplars.

## ToDo

- [ ] Dashboards as code
- [ ] Alert rules + contact points
- [ ] Screenshot in PR
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Provisioning test: Grafana API lists the dashboards and rules after `compose up`.
- Synthetic metric push triggers each alert in a test environment.

### Scenarios
- Given risk check p99 rises to 2 ms for 5 min, when evaluated, then a warning alert fires on Telegram and ntfy.

### Stress / failure injection
- n/a: observability config.

## Acceptance criteria

- [ ] Dashboards provisioned
- [ ] All listed alerts fire on synthetic breaches
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Prometheus down: alerts from Alertmanager watchdog fire (P0).

## Cardinal rules (do NOT)

- Do NOT put high-cardinality labels (order ids) on metrics; use exemplars/logs.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/02-v1-architecture.md` §9.2: dashboard names per SLO.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.42 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T047-grafana-risk-latency-tca`
- PR title: `P2-T047: Grafana boards and alerts for risk, ladder, kill/dead-man, SLOs and TCA`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T047` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (three-layer dead-man panels, two-stage drawdown and safety-state panels/alerts, alert fan-out per 17 §D)
