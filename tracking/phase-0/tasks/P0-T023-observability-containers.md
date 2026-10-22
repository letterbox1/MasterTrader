---
id: P0-T023
kind: task
title: Add the observability containers (Prometheus, Loki, Vector, Alertmanager, Grafana, exporters)
phase: 0
type: OPS
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T020, P0-T021]
requirements: [R0.02, R0.10]
roadmap_todos: [T0.41, T0.46]
modules: [M17]
dashboards: []
tools: [docker, uv]
mcp: []
env: []
services: [prometheus, loki, vector, alertmanager, grafana]
branch: p0/P0-T023-observability-containers
pr: ""
doc_sync: [docs/roadmap/phase-0-foundations.md]
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

# P0-T023 · Add the observability containers (Prometheus, Loki, Vector, Alertmanager, Grafana, exporters)

## Goal / expected outcome

The `obs` services run digest-pinned and healthy: Prometheus (90-day retention) scraping node_exporter, postgres_exporter, prometheus-nats-exporter, cAdvisor and every `/metrics` endpoint; Vector shipping Docker JSON logs and journald to Loki (retention 30–90 days, default 30); Alertmanager and Grafana up with provisioning folders ready for P0-T045.

## Context & references

- [Roadmap P0 R0.10](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [Roadmap P0 T0.41, T0.46](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [03 M17](../../../docs/03-build-spec.md#m17-observability--audit--mt_obs)
- [02 §5.1 stores](../../../docs/02-v1-architecture.md#51-stores) (Loki/Prometheus retention)
- [02 §3.1 networks](../../../docs/02-v1-architecture.md#31-networks) (obs network)
- Depends on: P0-T020, P0-T021

## Requirements

- Images digest-pinned in `images.lock`: prometheus, loki (single binary, filesystem store), vector, alertmanager, grafana (OSS), node-exporter, postgres-exporter, prometheus-nats-exporter, cadvisor.
- Prometheus: `--storage.tsdb.retention.time=90d`, scrape 15 s; file-based targets; `/-/ready` health.
- Loki: `retention_period=${LOKI_RETENTION:-720h}` with compactor retention on; a config test enforces 720h–2160h (30–90 d).
- Vector: `docker_logs` + `journald` sources; JSON parse; labels only `service`, `level`, `host`; secret-regex masking (defence in depth with P0-T018); 1 GiB disk buffer so Loki outages don't drop logs.
- Grafana: anonymous off, admin password from tmpfs, analytics and update checks off, reachable only via Caddy route `/grafana/` (Tailscale).
- cAdvisor and node-exporter with the minimum host mounts documented; postgres-exporter uses the read-only `mt_monitor_ro` role (P0-T024).

## ToDo

- [ ] Add services, configs (`infra/prometheus/`, `infra/loki/`, `infra/vector/`, `infra/alertmanager/`, `infra/grafana/provisioning/`) and health checks.
- [ ] Add the Caddy `/grafana/` route.
- [ ] Write the Loki retention config test.
- [ ] Integration test: a test container's log line is queryable via LogQL within 30 s.

## Verification

### Tests
- Integration: obs services healthy; `up == 1` for every target; LogQL `{service="mt-api"}` returns lines.
- Config: Loki retention in [720h, 2160h]; Prometheus 90d.

### Scenarios
- Given Loki is stopped for 10 min, when it returns, then Vector flushes its buffer and no lines from that window are lost (count check).

### Stress / failure injection
- 5k lines/s for 5 min from a generator container: Vector CPU < 1 core, `component_discarded_events_total` = 0.

## Acceptance criteria

- [ ] All obs services healthy and digest-pinned
- [ ] Every scrape target up
- [ ] Loki retention 30–90 d enforced by test
- [ ] Loki outage drill loses no lines
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- cAdvisor needs privileged mounts; keep it on `obs` only.

## Cardinal rules (do NOT)

- Do NOT expose Grafana/Prometheus/Loki outside the Tailscale route.
- Do NOT turn on Grafana usage analytics or update checks.
- Pin every image by digest (no `:latest` or floating tags); no telemetry or referral IDs in vendored code.
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- None beyond the roadmap tick (dashboards documented in P0-T045).
- `docs/roadmap/phase-0-foundations.md`: tick T0.41, T0.46 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T023-observability-containers`
- PR title: `P0-T023: Add the observability containers (Prometheus, Loki, Vector, Alertmanager, Grafana, exporters)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T023` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (no decision changes; run fields added)
