---
id: P0-T018
kind: task
title: Implement mt-obs structured logging, metrics and tracing (Rust, with the Python logging setup)
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
modules: [mt-obs]
dashboards: []
tools: [git, cargo, uv, python>=3.12, docker]
mcp: []
env: []
services: [nats]
branch: p0/P0-T018-mt-obs-logging-metrics-tracing
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-11-19
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P0-T018 · Implement mt-obs structured logging, metrics and tracing (Rust, with the Python logging setup)

## Goal / expected outcome

Every Rust service calls `mt_obs::setup(service_name)` once and gets `tracing` JSON logs carrying `trace_id`/`span_id`, Prometheus metrics helpers, OpenTelemetry tracing, secret redaction, and a NATS heartbeat on `sys.heartbeat.{service}`. Python services call `mt_store.obs.setup(service_name)` (a pure-Python submodule shipped in the same `mt_store` wheel, P0-T071) and get structlog JSON with the **same field names**, redaction and heartbeat, so Loki and Grafana see one format.

## Context & references

- [Roadmap P0 R0.10](../../../docs/roadmap/phase-0-foundations.md#3-requirements) · [T0.25](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [18 §2.1](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates) (`mt-obs` row) · [03 M17](../../../docs/03-build-spec.md#m17-observability--audit)
- [02 §6 NATS](../../../docs/02-v1-architecture.md#6-messaging-nats) (`sys.heartbeat.{service}`)
- [02 §9.2 SLOs](../../../docs/02-v1-architecture.md#92-observability--slos)
- Related: P0-T023 (Vector/Loki), P0-T045, P0-T071 (the `mt_store` wheel)
- Depends on: P0-T017

## Requirements

- Rust: `tracing` + `tracing-subscriber` JSON to stdout: `ts` (UTC ISO-8601 ms), `level`, `service`, `event`/`message`, `trace_id`, `span_id`, `target`; only low-cardinality fields (`service`, `level`) become Loki labels.
- Python: structlog JSON with identical keys; `trace_id`/`span_id` from the OTel context.
- Redaction (both): mask keys matching `(?i)(secret|token|password|api_key|authorization|cookie|totp|jwt)` and every `SecretString`/secret value; best-effort regex for JWT-shaped strings in free text.
- OpenTelemetry (`opentelemetry` + `tracing-opentelemetry` in Rust, the OTel SDK in Python) with W3C traceparent propagation (HTTP + NATS headers); OTLP exporter **off** by default (no telemetry leaves the box).
- Prometheus helpers: counter/histogram/gauge factories with a `service` label; buckets for µs–s; a `/metrics` route helper for axum (`mt-api`) and for Python services.
- Heartbeat: publish `{service, ts, version, status}` to `sys.heartbeat.{service}` (async-nats in Rust) at the configured interval (default **1 s**, the cadence the three-layer dead-man watches, [16 §3.1](../../../docs/16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch), [16 §2.14](../../../docs/16-configuration-and-safety-model.md#214-platform--operations)) and update NATS KV `heartbeat`.
- Audit writers (later) take the current `trace_id` so a row links to its logs (03 M17).

## ToDo

- [ ] Implement `mt_obs::{logging, metrics, tracing, heartbeat, setup}` in Rust.
- [ ] Add an axum/tower layer that sets trace context and returns `traceparent` (used by `mt-api`, P0-T032).
- [ ] Add the Python `mt_store.obs` submodule (structlog config, redaction, heartbeat) with the same field names.
- [ ] Tests for redaction, propagation and heartbeat cadence in both languages.
- [ ] Document label conventions in the crate README.

## Verification

### Tests
- `cargo test -p mt-obs`: `api_key="abc"` is emitted masked; an incoming `traceparent` id appears in every log line of the request (tower test service).
- `uv run pytest` on `mt_store.obs`: same redaction and key set as the Rust output (a shared golden log line).
- Integration: heartbeat on NATS at the configured interval (default 1 s) ± 20 % (nats-server test container).

### Scenarios
- Given NATS is down, when a service starts, then heartbeats retry with backoff and logging/metrics still work.
- Given a log line contains a JWT-shaped string in free text, then the redactor masks it (best effort, tested).

### Stress / failure injection
- 10k log lines/s for 60 s without blocking the tokio runtime (non-blocking writer; logged).

## Acceptance criteria

- [ ] `mt_obs::setup()` used by a sample Rust service and `mt_store.obs.setup()` by a sample Python service; JSON logs show `trace_id` with identical keys
- [ ] Redaction tests pass in both languages
- [ ] Heartbeats visible on NATS and KV
- [ ] OTel exporter off by default
- [ ] CI green (clippy, cargo test, ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- Loki down: logs still go to stdout/Docker; Vector buffers (P0-T023).

## Cardinal rules (do NOT)

- Do NOT use high-cardinality Loki labels (trace_id, instrument, user agent).
- Do NOT enable any SaaS telemetry/OTel endpoint.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test to get CI green.
- Pin every image by digest (no `:latest` or floating tags); no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/03-build-spec.md` M17: note label conventions, the shared Rust/Python log keys and the heartbeat interval setting.
- `docs/roadmap/phase-0-foundations.md`: tick T0.25 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T018-mt-obs-logging-metrics-tracing`
- PR title: `P0-T018: Implement mt-obs structured logging, metrics and tracing`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T018` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (heartbeat interval is a setting, default 1 s (16 §3.1); run fields added)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (Rust `mt-obs` with `tracing`/OTel/async-nats; Python structlog setup ships as `mt_store.obs` with the same keys; FastAPI middleware → tower layer)
