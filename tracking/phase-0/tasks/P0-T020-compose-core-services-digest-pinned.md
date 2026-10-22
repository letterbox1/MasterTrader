---
id: P0-T020
kind: task
title: Build the Compose stack for core services pinned by digest
phase: 0
type: OPS
status: backlog
priority: critical
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T014]
requirements: [R0.02]
roadmap_todos: [T0.41]
modules: [ops, mt_store]
dashboards: []
tools: [docker, make, uv]
mcp: []
env: []
services: [postgres, nats, prefect-server, mlflow, caddy, mt-api]
branch: p0/P0-T020-compose-core-services-digest-pinned
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/03-build-spec.md, docs/roadmap/phase-0-foundations.md]
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

# P0-T020 · Build the Compose stack for core services pinned by digest

## Goal / expected outcome

`infra/docker-compose.yml` brings up the P0 core services — `postgres` (16 + TimescaleDB TSL + pgvector + pg_trgm), `nats` (JetStream), `prefect-server` + `prefect-worker`, `mlflow`, `caddy`, `mt-api` — every image pinned by `@sha256:` digest from one lock file, every service with a health check, and `docker compose up` ends with all of them healthy.

## Context & references

- [Roadmap P0 R0.02](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [Roadmap P0 T0.41](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [02 §3.2 containers](../../../docs/02-v1-architecture.md#32-containers)
- [02 §5.1 stores](../../../docs/02-v1-architecture.md#51-stores)
- [03 §2 target environment](../../../docs/03-build-spec.md#2-target-environment)
- [07 §5 network & host](../../../docs/07-security-notes.md#5-network--host)
- Observability: P0-T023; models: P0-T042, P0-T043, P0-T044; networks: P0-T021; secrets: P0-T022; `docker-proxy`: P0-T065
- Depends on: P0-T014

## Requirements

- Images (digest-pinned, recorded in `infra/images.lock` as `name tag digest`): `timescale/timescaledb-ha:pg16` (TSL, includes pgvector and pgBackRest; enable `pg_trgm`), `nats:2.10-alpine`, `prefecthq/prefect:3-python3.12`, `ghcr.io/mlflow/mlflow`, `caddy:2`, and `mt-api` built from `packages/mt_api/Dockerfile` (base image digest-pinned).
- Health checks: postgres `pg_isready` + `SELECT 1`; nats `/healthz?js-enabled-only=true`; prefect `/api/health`; mlflow `/health`; caddy static `/healthz`; mt-api `/api/v1/system/live`.
- Postgres: databases `mastertrader`, `prefect`, `mlflow`, `litellm`; `shared_preload_libraries='timescaledb,pg_stat_statements'`; `wal_level=replica`, `archive_mode=on` (archive_command set by P0-T039); `timescaledb.telemetry_level=off`; data on NVMe.
- NATS: JetStream file store on NVMe; accounts `SYS`, `CORE`, `SCRAPE` (scrape may publish only `text.raw.>`); KV buckets from an init job: `risk_state`, `kill`, `feed_status`, `tierb_scores`, `heartbeat` and the WORM integrity status `audit.integrity` (02 §5.1; stored as bucket `audit`, key `integrity`, because KV bucket names can't contain dots). The same job creates the JetStream stream `AUDIT_BUFFER` for the WORM write buffer with the [16 §3.3](../../../docs/16-configuration-and-safety-model.md#33-records-the-write-path-vs-the-integrity-check) defaults read from settings (max 1 GB or 24 h).
- Prefect: server on the `prefect` DB; work pool `mt-default`; analytics off (`PREFECT_SERVER_ANALYTICS_ENABLED=false`, `DO_NOT_TRACK=1`).
- MLflow: backend store Postgres `mlflow`, artifacts on a local volume (restic-backed by P0-T039).
- Caddy: serves `apps/web/dist`, proxies `/api/*` (incl. WebSocket) to mt-api; TLS via Tailscale `*.ts.net` certs; binds **only** to the Tailscale IP; headers CSP `default-src 'self'`, HSTS, `X-Frame-Options DENY`.
- **No `ports:` on 0.0.0.0**; only caddy publishes, on `${TAILSCALE_IP}:443`. `infra/scripts/compose-lint.py` fails CI on any tag-only image, `:latest`, or non-Tailscale published port.
- Per-service `mem_limit`/`cpus`; `restart: unless-stopped`; `read_only: true` + tmpfs where the image allows.
- Volumes under `/srv/mastertrader/{pg,nats,mlflow,prefect}` on NVMe; `/srv/mastertrader/cold` on HDD (P1).

## ToDo

- [ ] Write `infra/docker-compose.yml` and `infra/images.lock`; add `infra/scripts/pin-digests.sh` (tag → digest).
- [ ] Write `compose-lint.py` and wire it into CI.
- [ ] Add Postgres init SQL (databases, extensions, telemetry off).
- [ ] Add NATS config (accounts, JetStream) and a one-shot `nats-init` service creating the KV buckets.
- [ ] Add the Caddyfile with Tailscale certs and headers.
- [ ] Add `make up` / `make health` (waits for all health checks, prints a table).
- [ ] Write the integration smoke test.

## Verification

### Tests
- Integration: `docker compose up -d` then `make health` → all services healthy within 180 s.
- Lint: compose-lint fails on a fixture with `image: postgres:16` (no digest) and on `ports: ['5432:5432']`.
- Postgres: `pg_extension` includes `timescaledb`, `vector`, `pg_trgm`; telemetry off.
- NATS: KV `audit` bucket and `AUDIT_BUFFER` stream exist with the configured limits (not literals).

### Scenarios
- Given a service crashes, when Docker restarts it, then the health check returns to healthy and the restart count is visible (D16 via cAdvisor).
- Given `images.lock` holds a wrong digest, when pulling, then compose fails rather than pulling a different image.

### Stress / failure injection
- Cold start on the host: full stack healthy in ≤ 180 s (logged); restart postgres under `pgbench -c 8 -T 60` and confirm mt-api reconnects without manual action.

## Acceptance criteria

- [ ] `docker compose up` → every P0 core service healthy (table attached)
- [ ] Every image in `images.lock` has a digest; compose-lint passes in CI
- [ ] Only caddy publishes a port, on the Tailscale IP
- [ ] Extensions present; Timescale and Prefect telemetry off
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- TimescaleDB Community (TSL) is free for self-hosted use; don't switch to the Apache-only image (no compression/continuous aggregates).
- ARM vs x86: lock digests per platform if you build on a laptop first.

## Cardinal rules (do NOT)

- Do NOT publish any port on 0.0.0.0 or the LAN interface.
- Do NOT use `:latest` or tag-only image references.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Pin every image by digest (no `:latest` or floating tags); no telemetry or referral IDs in vendored code.
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/02-v1-architecture.md` §3.2: note the exact images used; `docs/03-build-spec.md` §3: compose path is `infra/docker-compose.yml`.
- `docs/roadmap/phase-0-foundations.md`: tick T0.41 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T020-compose-core-services-digest-pinned`
- PR title: `P0-T020: Build the Compose stack for core services pinned by digest`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T020` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (KV audit.integrity + AUDIT_BUFFER stream with 16 §3.3 defaults; run fields added)
