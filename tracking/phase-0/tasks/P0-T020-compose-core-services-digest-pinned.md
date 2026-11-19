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
depends_on: [P0-T014, P0-T070]
requirements: [R0.02]
roadmap_todos: [T0.41]
modules: [ops, mt-api]
dashboards: []
tools: [docker, just, cargo]
mcp: []
env: []
services: [supabase-postgres, nats, prefect-server, mlflow, caddy, mt-api]
branch: p0/P0-T020-compose-core-services-digest-pinned
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/03-build-spec.md, docs/roadmap/phase-0-foundations.md]
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

# P0-T020 · Build the Compose stack for core services pinned by digest

## Goal / expected outcome

`infra/compose/workstation.yml` (the Mode 1 compose file, [18 §5](../../../docs/18-platform-and-deployment.md#5-deployment-modes)) brings up the P0 core services next to the Supabase stack (P0-T070): `nats` (JetStream), `prefect-server` + `prefect-worker`, `mlflow`, `caddy` and `mt-api` (the Rust binary). Every image is pinned by `@sha256:` digest from one lock file, every service has a health check, everything binds to localhost, and `just up` ends with all of them healthy.

## Context & references

- [Roadmap P0 R0.02](../../../docs/roadmap/phase-0-foundations.md#3-requirements) · [T0.41](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [18 §2.3 third-party services](../../../docs/18-platform-and-deployment.md#23-third-party-services-any-language-run-as-pinned-containers) · [18 §3 layout](../../../docs/18-platform-and-deployment.md#3-repository-layout) · [18 §5 deployment modes](../../../docs/18-platform-and-deployment.md#5-deployment-modes)
- [02 §3.2 containers](../../../docs/02-v1-architecture.md#32-containers) · [02 §5.1 stores](../../../docs/02-v1-architecture.md#51-stores)
- [03 §2 target environment](../../../docs/03-build-spec.md#2-target-environment) · [07 §5 network & host](../../../docs/07-security-notes.md#5-network--host)
- Database: P0-T070 (Supabase); observability: P0-T023; models: P0-T042, P0-T043, P0-T044; networks: P0-T021; secrets: P0-T022; `docker-proxy`: P0-T065
- Depends on: P0-T014, P0-T070

## Requirements

- Images (digest-pinned, recorded in `infra/images.lock` as `name tag digest`, shared with the Supabase stack): `nats:2.10-alpine`, `prefecthq/prefect:3-python3.12`, `ghcr.io/mlflow/mlflow`, `caddy:2`, and `mt-api` built from `crates/mt-api/Dockerfile` (multi-stage `cargo build --release --locked`, distroless/static base pinned by digest).
- Health checks: nats `/healthz?js-enabled-only=true`; prefect `/api/health`; mlflow `/health`; caddy static `/healthz`; mt-api `/api/v1/system/live`.
- Database: no separate Postgres container. Prefect, MLflow and LiteLLM get their own databases (`prefect`, `mlflow`, `litellm`) on the Supabase Postgres from P0-T070, created by an init migration outside the MasterTrader schemas; `wal_level=replica`, `archive_mode=on` set on the Supabase Postgres (archive_command by P0-T039).
- NATS: JetStream file store on NVMe; accounts `SYS`, `CORE`, `SCRAPE` (scrape may publish only `text.raw.>`); KV buckets from an init job: `risk_state`, `kill`, `feed_status`, `tierb_scores`, `heartbeat` and the WORM integrity status `audit.integrity` (02 §5.1; stored as bucket `audit`, key `integrity`, because KV bucket names can't contain dots). The same job creates the JetStream stream `WORM_BUFFER` for the WORM write buffer with the [16 §3.3](../../../docs/16-configuration-and-safety-model.md#33-records-the-write-path-vs-the-integrity-check) defaults read from settings (max 1 GB or 24 h).
- Prefect: server on the `prefect` DB; work pool `mt-default`; analytics off (`PREFECT_SERVER_ANALYTICS_ENABLED=false`, `DO_NOT_TRACK=1`).
- MLflow: backend store Postgres `mlflow`, artifacts on a local volume (restic-backed by P0-T039).
- Caddy: serves `apps/web/dist` (`web.host: local`, [16 §2.15](../../../docs/16-configuration-and-safety-model.md#215-platform-deployment-and-regions)), proxies `/api/*` (incl. WebSocket) to mt-api; binds to `127.0.0.1` on the workstation (internal TLS); if `tailscale0` exists it may also bind to the Tailscale IP with `*.ts.net` certs (optional before P7); headers CSP `default-src 'self'` plus the Supabase Auth origin in `connect-src`, HSTS, `X-Frame-Options DENY`.
- **No `ports:` on 0.0.0.0**; only caddy publishes. `infra/scripts/compose-lint` fails CI on any tag-only image, `:latest`, or a published port on a non-loopback, non-Tailscale address.
- Per-service `mem_limit`/`cpus`; `restart: unless-stopped`; `read_only: true` + tmpfs where the image allows.
- Volumes under a configurable data root (default `/srv/mastertrader/` or `~/.local/share/mastertrader/` on the workstation) for nats, mlflow, prefect; cold Parquet path configurable (P1).
- `justfile`: `up` (Supabase stack + compose), `health` (waits for all health checks, prints a table), `down`.

## ToDo

- [ ] Write `infra/compose/workstation.yml` and `infra/images.lock`; add `infra/scripts/pin-digests.sh` (tag → digest).
- [ ] Write `compose-lint` and wire it into CI.
- [ ] Add the `mt-api` Dockerfile (multi-stage Rust build, pinned bases).
- [ ] Add the init migration for the `prefect`, `mlflow`, `litellm` databases on the Supabase Postgres.
- [ ] Add NATS config (accounts, JetStream) and a one-shot `nats-init` service creating the KV buckets and stream.
- [ ] Add the Caddyfile (localhost, optional Tailscale) and headers.
- [ ] Add `just up` / `just health`; write the integration smoke test.

## Verification

### Tests
- Integration: `just up` then `just health` → Supabase services and every core service healthy within 180 s.
- Lint: compose-lint fails on a fixture with `image: nats:2.10` (no digest) and on `ports: ['4222:4222']`.
- NATS: KV `audit` bucket and `WORM_BUFFER` stream exist with the configured limits (not literals).
- Databases `prefect`, `mlflow`, `litellm` exist on the Supabase Postgres and hold no MasterTrader tables.

### Scenarios
- Given a service crashes, when Docker restarts it, then the health check returns to healthy and the restart count is visible (D16 via cAdvisor).
- Given `images.lock` holds a wrong digest, when pulling, then compose fails rather than pulling a different image.

### Stress / failure injection
- Cold start on the workstation: full stack healthy in ≤ 180 s (logged); restart the Supabase `db` container under `pgbench -c 8 -T 60` and confirm mt-api reconnects without manual action.

## Acceptance criteria

- [ ] `just up` → every P0 core service healthy (table attached)
- [ ] Every image in `images.lock` has a digest; compose-lint passes in CI
- [ ] Only caddy publishes a port, on localhost (and the Tailscale IP only if present)
- [ ] Prefect telemetry off
- [ ] CI green (clippy, cargo test, ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- ARM vs x86: lock digests per platform if you build on more than one machine.
- Other modes (`hybrid`, `regional`) get their own compose files at the shift (P7-T073); this task builds Mode 1 only.

## Cardinal rules (do NOT)

- Do NOT publish any port on 0.0.0.0 or the LAN interface.
- Do NOT use `:latest` or tag-only image references.
- Do NOT run a second Postgres next to the Supabase one.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Pin every image by digest (no `:latest` or floating tags); no telemetry or referral IDs in vendored code.
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/02-v1-architecture.md` §3.2: note the exact images used; `docs/18-platform-and-deployment.md` §3 / `docs/03-build-spec.md` §3: compose path per mode in `infra/compose/`.
- `docs/roadmap/phase-0-foundations.md`: tick T0.41 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T020-compose-core-services-digest-pinned`
- PR title: `P0-T020: Build the Compose stack for core services pinned by digest`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T020` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (KV audit.integrity + WORM_BUFFER stream with 16 §3.3 defaults; run fields added)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (Postgres+TimescaleDB container dropped (Supabase stack P0-T070, now a dependency); `mt-api` is a Rust image; Caddy binds to localhost, Tailscale optional; make → just)
