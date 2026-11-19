---
id: P0-T032
kind: task
title: Build the mt-api axum skeleton (utoipa OpenAPI, problem+json, health)
phase: 0
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T018, P0-T024]
requirements: [R0.08]
roadmap_todos: [T0.24]
modules: [mt-api]
dashboards: []
tools: [git, cargo, docker, supabase]
mcp: []
env: []
services: [supabase-postgres, nats]
branch: p0/P0-T032-mt-api-skeleton
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/roadmap/phase-0-foundations.md]
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

# P0-T032 · Build the mt-api axum skeleton (utoipa OpenAPI, problem+json, health)

## Goal / expected outcome

`mt-api` (Rust, `crates/mt-api`) runs as the `mt-api` container: axum + tokio under `/api/v1`, OpenAPI 3.1 generated with **utoipa** and published at build time (so `openapi-typescript` still generates the web client), RFC 9457 problem+json errors, snake_case JSON with Decimals as strings and ISO-8601 UTC times, cursor pagination helpers, and liveness/readiness probes that work even when Postgres is down ([18 §2.1](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates)).

## Context & references

- [Roadmap P0 R0.08](../../../docs/roadmap/phase-0-foundations.md#3-requirements) · [T0.24](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [18 §2.1](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates) (`mt-api` row) · [18 §4.5 access rules](../../../docs/18-platform-and-deployment.md#45-access-rules) (the browser reads only through `mt-api`)
- [02 §7 API contract](../../../docs/02-v1-architecture.md#7-api-contract-mt_api)
- [02 §9.3 degraded modes](../../../docs/02-v1-architecture.md#93-degraded-modes) (mt-api / Postgres down)
- [D16 System](../../../docs/ui/dashboards/D16-system.md) (acceptance 1: read-only on outage)
- Depends on: P0-T018 (tracing layer), P0-T024 (DB roles, `mt-store` pools)

## Requirements

- Binary `mt-api` with `build_router(state)`; tokio runtime; `tower` layers: trace context (P0-T018), request logging (no bodies), body limit 1 MiB, timeout; trusts `X-Forwarded-*` only from Caddy; routes under `/api/v1`.
- OpenAPI 3.1 via `utoipa` derives exported to `crates/mt-api/openapi.json` in CI; a diff check fails if routes change without the file being regenerated (feeds `openapi-typescript` in P0-T048).
- Errors: `application/problem+json` with `type` (URI under `https://mastertrader.local/problems/<slug>`), `title`, `status`, `detail`, `instance`, `trace_id`; validation errors list fields. Never leak panics, backtraces or SQL.
- Encoding: serde with `rust_decimal` as string and UTC `Z` datetimes (the `mt-core` types); snake_case keys.
- Pagination: `?cursor=&limit=` (max 500) returning `{items, next_cursor}`.
- Probes: `/system/live` (process up), `/system/ready` (Supabase Postgres + NATS + Auth JWKS reachable; reports which is down). Postgres-down mode: mt-api stays up, read-only, returns 503 problem+json for writes (02 §9.3).
- CORS **off** by default (same-origin via Caddy); a strict allow-list for the Vercel origin exists only behind `web.host: vercel` / `api.exposure: public` ([16 §2.15](../../../docs/16-configuration-and-safety-model.md#215-platform-deployment-and-regions)), off in P0.
- DB access through `mt-store` sqlx pools as `mt_api_rw`; never as `service_role` or `postgres`.
- Dockerfile: multi-stage `cargo build --release --locked`, non-root uid, distroless/static base pinned by digest.

## ToDo

- [ ] Implement the router, state, error type (`IntoResponse` → problem+json), encoders, pagination helper, probes.
- [ ] Add utoipa docs and the OpenAPI export + CI diff check.
- [ ] Write the Dockerfile and compose service wiring (secrets mount, networks `edge`+`core`).
- [ ] Tests below.

## Verification

### Tests
- `cargo test -p mt-api`: problem+json shape for 400/401/403/404/409/422/503; Decimal and datetime encoding (axum `oneshot` tests).
- Integration (Supabase CLI stack): `/system/ready` reports `postgres: down` when the DB container is paused, and writes return 503.
- Contract: OpenAPI diff check fails when a route is added without regenerating.
- `cargo clippy -p mt-api -- -D warnings`.

### Scenarios
- Given Postgres is paused, when the web app loads D16, then mt-api still answers `/system/live` and `/system/health` (degraded fields) within 1 s.
- Given a handler panics, then the client gets a 500 problem+json with `trace_id` (catch-panic layer) and the log line carries the same `trace_id`.

### Stress / failure injection
- Load: 500 req/s on `/system/live` for 60 s, p99 < 20 ms on the workstation (logged).

## Acceptance criteria

- [ ] Container healthy in compose; OpenAPI exported and diff-checked
- [ ] problem+json everywhere (tested)
- [ ] Postgres-down read-only mode proven
- [ ] CI green (clippy, cargo test, ruff, mypy, pytest, `supabase test db`, gitleaks, `pit` check)

## Exceptions & edge cases

- NATS down: commands that need NATS fail closed with 503 problem+json, except Kill ON (P0-T035): it is accepted, written straight to `audit.command` (Postgres up) and its KV write/publish retries until NATS returns. With Postgres down instead, Kill records go through the JetStream WORM buffer (16 §3.3).
- Supabase Auth down: existing JWTs keep verifying from the cached JWKS until they expire; new logins fail with a clear message.

## Cardinal rules (do NOT)

- Do NOT enable CORS by default or bind mt-api to a published port (Caddy only).
- Do NOT return panics, backtraces or SQL in errors.
- Do NOT connect as `service_role`/`postgres` or expose a generic SQL/Data-API passthrough.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT bypass `mt-api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get CI green.
- Pin every image by digest (no `:latest` or floating tags); no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/02-v1-architecture.md` §7: link the generated OpenAPI file and problem `type` URIs.
- `docs/roadmap/phase-0-foundations.md`: tick T0.24 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T032-mt-api-skeleton`
- PR title: `P0-T032: Build the mt-api axum skeleton (utoipa OpenAPI, problem+json, health)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T032` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (Kill ON record path per 16 §3.3 instead of a local spool; run fields added)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (FastAPI/uvicorn → Rust axum + tokio with utoipa OpenAPI; readiness includes Supabase Auth JWKS; DB via `mt-store` sqlx pools; Rust Dockerfile)
