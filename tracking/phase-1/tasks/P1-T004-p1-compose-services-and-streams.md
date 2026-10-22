---
id: P1-T004
kind: task
title: Add P1 containers and NATS JetStream streams
phase: 1
type: OPS
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T016, P0-T018, P0-T020, P0-T021, P0-T022]
requirements: [R1.01, R1.10, R1.14]
roadmap_todos: [T1.20, T1.27, T1.31]
modules: [M1, M16, M17]
dashboards: [D16]
tools: [git, uv, docker]
mcp: []
env: []
services: [nats, postgres]
branch: p1/P1-T004-p1-compose-services-and-streams
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/02-v1-architecture.md]
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

# P1-T004 · Add P1 containers and NATS JetStream streams

## Goal / expected outcome

`ingest-market`, `ingest-batch`, `monitor` and `telegram-bot` (alerts only) run under Compose with health checks, the right networks and scoped secrets, and JetStream streams/KV buckets exist for `md.*`, `dq.*` (incl. `dq.raw.*`), `cost.*`, `recon.*`, `egress.*` and `alert.*`.

## Context & references

- Roadmap: requirements [R1.01](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.10](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.14](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.20](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets), [T1.27](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets), [T1.31](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Containers: [02 §3.2](../../../docs/02-v1-architecture.md#32-containers) · networks [02 §3.1](../../../docs/02-v1-architecture.md#31-networks) · subjects [02 §6](../../../docs/02-v1-architecture.md#6-messaging-nats) · stores [02 §5.1](../../../docs/02-v1-architecture.md#51-stores)
- Cross-phase prerequisites (depends_on): P0-T020 (Compose core: NATS JetStream, Postgres, Prefect; image lock), P0-T021 (networks), P0-T022 (sops → tmpfs per service), P0-T016 (`mt_core.schemas`), P0-T018 (`mt_obs` metrics and logging)
- `ib-gateway` (only when IBKR is used) is a separate opt-in service: P1-T070

## Requirements

- Services in `infra/docker-compose.yml`: `ingest-market` (`mt_data.market`), `ingest-batch` (Prefect worker pool `batch`), `monitor` (`mt_monitor`), `telegram-bot` (`mt_ui.telegram`, alerts only); all on network `core` with venue egress via the allow-list; images pinned by digest
- Health checks: each service publishes `sys.heartbeat.{service}` every 1 s and exposes `/healthz` + Prometheus `/metrics`
- JetStream streams (file storage): `MD` (`md.>`, max age 24 h, discard old), `DQ` (`dq.>`, 7 d), `COST` (`cost.>`, 7 d), `RECON` (`recon.>`, 7 d), `EGRESS` (`egress.>`, 7 d), `ALERT` (`alert.>`, 7 d); KV buckets `feed_status` (created in P0), `quota` and `egress` (history 1); retention values are configurable defaults in `infra/nats/streams.yaml`
- Payload schemas are msgspec structs in `mt_core.schemas` (versioned, `schema_version` field)
- Secrets scoped per service: `ingest-*` get data API keys and practice stream credentials, `monitor` gets the recon/fee-tier credentials (read-only testnet keys, practice credentials), `telegram-bot` gets only the alert-channel secrets (bot token, chat ID, ntfy notifier token, SMTP app password). Builds and CI run with no secrets: a service with a missing secret starts and reports `credentials_missing` for that feed
- Resource limits per container so a runaway recorder cannot starve Postgres

## ToDo

- [ ] Add the four services to `infra/docker-compose.yml` with digests, networks, tmpfs secrets mounts and resource limits
- [ ] Add `infra/nats/streams.yaml` and a bootstrap job (`mt-ops nats-bootstrap`) that creates/updates streams and KV idempotently
- [ ] Add msgspec schemas for `md.trade`, `md.quote`, `md.book`, `md.bar`, `dq.raw`, `dq.status` (`ok | degraded | stale | closed | bad` + reasons + data age), `cost`, `recon`, `egress.status`, `alert` in `mt_core.schemas`
- [ ] Add heartbeat helper in `mt_obs` used by every P1 service
- [ ] Write compose smoke test and stream bootstrap test
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Integration: `docker compose up` brings all four services to healthy in CI (testcontainers or compose-in-CI)
- Unit: schema round-trip (encode/decode) for every new payload; unknown `schema_version` is rejected with a logged error
- Integration: bootstrap is idempotent (run twice → no diff); stream limits match `streams.yaml`

### Scenarios

- Given NATS restarts, when services reconnect, then streams and KV survive (file storage) and publishers resume without manual steps
- Given the `telegram-bot` container, when its environment is inspected, then it holds no venue keys

### Stress / failure injection

- Publish 50k msgs/s of synthetic `md.trade` to `MD` for 60 s; stream stays within max age/bytes and consumers do not fall more than 5 s behind

## Acceptance criteria

- [ ] All four services healthy; heartbeats visible in Grafana and D16
- [ ] Streams and KV buckets exist with the documented limits, created by code not by hand
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Partial start: `monitor` starting before `ingest-market` shows feeds as `unknown`, not `stale`, until the first message
- Disk full on the NATS volume: publishers get errors, alert `alert.critical.nats_disk` fires (P1-T052 adds disk alerts)

## Cardinal rules (do NOT)

- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file (kept outside the repo) mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT add an image without pinning it by digest, or vendored code that carries telemetry or referral IDs.
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.20, T1.27, T1.31 once every task traced to it in PHASE.md is done; note P1-T004 next to it.
- `docs/02-v1-architecture.md` §6/§5.1: `recon.*`, `dq.raw.*` and `egress.status` are already in the subject table (alignment wave); confirm the stream retention actually configured and add KV `quota`/`egress`

## Branch & PR

- Branch: `p1/P1-T004-p1-compose-services-and-streams`
- PR title: `P1-T004: Add P1 containers and NATS JetStream streams`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T004` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (dq.raw/egress streams and KV, dq.status incl. closed, keyless start; P0 deps explicit)
