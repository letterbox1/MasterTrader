---
id: P0-T018
kind: task
title: Implement mt_obs structured logging, metrics and tracing
phase: 0
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T017]
requirements: [R0.10]
roadmap_todos: [T0.25]
modules: [M17, mt_obs]
dashboards: []
branch: p0/P0-T018-mt-obs-logging-metrics-tracing
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P0-T018 · Implement mt_obs structured logging, metrics and tracing

## Goal / expected outcome

Every Python service calls `mt_obs.setup(service_name)` once and gets structlog JSON logs carrying `trace_id`/`span_id`, Prometheus metrics helpers, OpenTelemetry tracing, secret redaction, and a NATS heartbeat on `sys.heartbeat.{service}`.

## Context & references

- [Roadmap P0 T0.25](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [03 M17](../../../docs/03-build-spec.md#m17-observability--audit--mt_obs)
- [02 §6 NATS](../../../docs/02-v1-architecture.md#6-messaging-nats) (`sys.heartbeat.{service}`)
- [02 §9.2 SLOs](../../../docs/02-v1-architecture.md#92-observability--slos)
- Related: P0-T023 (Vector/Loki), P0-T045
- Depends on: P0-T017

## Requirements

- structlog JSON to stdout: `ts` (UTC ISO-8601 ms), `level`, `service`, `event`, `trace_id`, `span_id`, `logger`; only low-cardinality fields (`service`, `level`) become Loki labels.
- Redaction processor masks keys matching `(?i)(secret|token|password|api_key|authorization|cookie|totp)` and any `SecretStr` value.
- OpenTelemetry SDK with W3C traceparent propagation (HTTP + NATS headers); OTLP exporter **off** by default (no telemetry leaves the box).
- Prometheus helpers: counter/histogram/gauge factories with a `service` label; buckets for µs–s; `/metrics` ASGI app.
- Heartbeat: publish `{service, ts, version, status}` to `sys.heartbeat.{service}` every 5 s and update NATS KV `heartbeat`.
- Audit writers (later) take the current `trace_id` so a row links to its logs (03 M17).

## ToDo

- [ ] Implement `mt_obs.logging`, `metrics`, `tracing`, `heartbeat` and `setup()`.
- [ ] Add a FastAPI middleware that sets trace context and returns `traceparent`.
- [ ] Tests for redaction, propagation and heartbeat cadence.
- [ ] Document label conventions in the package README.

## Verification

### Tests
- Unit: `api_key='abc'` is emitted masked.
- Unit: an incoming `traceparent` id appears in every log line of the request.
- Integration: heartbeat on NATS every 5 s ± 1 s (nats-server test container).

### Scenarios
- Given NATS is down, when a service starts, then heartbeats retry with backoff and logging/metrics still work.
- Given a log line contains a JWT-shaped string in free text, then the regex redactor masks it (best effort, tested).

### Stress / failure injection
- 10k log lines/s for 60 s without blocking the event loop (logged).

## Acceptance criteria

- [ ] `mt_obs.setup()` used by a sample service; JSON logs show trace_id
- [ ] Redaction tests pass
- [ ] Heartbeats visible on NATS and KV
- [ ] OTel exporter off by default
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- Loki down: logs still go to stdout/Docker; Vector buffers (P0-T023).

## Cardinal rules (do NOT)

- Do NOT use high-cardinality Loki labels (trace_id, instrument, user agent).
- Do NOT enable any SaaS telemetry/OTel endpoint.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test to get CI green.
- Pin every image by digest (no `:latest` or floating tags); no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/03-build-spec.md` M17: note label conventions and the heartbeat interval.
- `docs/roadmap/phase-0-foundations.md`: tick T0.25 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T018-mt-obs-logging-metrics-tracing`
- PR title: `P0-T018: Implement mt_obs structured logging, metrics and tracing`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T018` run

## Progress log

- 2026-10-21 00:00 · planner · created
