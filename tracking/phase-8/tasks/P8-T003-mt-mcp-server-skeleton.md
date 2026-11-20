---
id: P8-T003
kind: task
title: "`mt-mcp` server: transports, mt-api client and OpenAPI-generated tool schemas"
phase: 8
type: BUILD
status: backlog
priority: critical
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P8-T002, P0-T014, P0-T032]
requirements: [R8.01, R8.02, R8.03, R8.08]
roadmap_todos: [T8.20, T8.24]
modules: [M20]
dashboards: [D17]
tools: [cargo, docker, git]
mcp: []
env: []
services: [supabase-postgres, nats]
branch: p8/P8-T003-mt-mcp-server-skeleton
pr: ""
doc_sync: [docs/03-build-spec.md, docs/02-v1-architecture.md, docs/roadmap/phase-8-mcp.md]
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

# P8-T003 · `mt-mcp` server: transports, mt-api client and OpenAPI-generated tool schemas

## Goal / expected outcome

`crates/mt-mcp` is a working MCP server (Rust, official `rmcp` SDK) that turns the `mt-api` OpenAPI document into MCP tools, filtered by the server-side registry (`/mcp/tools`, P8-T004) and the token's scopes. Each tool call becomes exactly one `mt-api` HTTP call made with the caller's token. It runs over **stdio** (newline-delimited JSON, local) or **Streamable HTTP** (JSON-RPC 2.0, SSE streaming, resumable) behind Caddy on Tailscale/TLS. It holds no business logic and no credentials of its own. Tested with the `rmcp` client against a local mt-api test instance; no real client app or key needed.

## Context & references

- Roadmap: [R8.01–R8.03, R8.08](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDos [T8.20, T8.24](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets) (Streamable HTTP + stdio part; OAuth in P8-T031; subscriptions and legacy HTTP+SSE in P8-T032)
- Platform: [18 §2.1](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates) (`mt-mcp` in Rust on the official `rmcp` SDK, still a thin adapter over `mt-api` (axum)) · [18 §4.6](../../../docs/18-platform-and-deployment.md#46-auth) (Supabase Auth for your web session; MCP tokens stay opaque `mt-api` tokens)
- Spec: [03 M20](../../../docs/03-build-spec.md#m20-mcp-control-plane-built-last-phase-8-only-if-wanted) (thin adapter, transports) · repo layout `crates/mt-mcp/` ([18 §3](../../../docs/18-platform-and-deployment.md#3-repository-layout))
- Architecture: [02 §7.4](../../../docs/02-v1-architecture.md#74-telegram--mcp) (transport at `/mcp` on Caddy) · [02 §7](../../../docs/02-v1-architecture.md#7-api-contract-mt-api) conventions (snake_case, decimals as strings, ISO-8601 UTC, cursor pagination, RFC 9457 errors)
- Decisions: [17 §A P8-B004](../../../docs/17-decisions-register.md#a-s2-items-all-resolved) (transport) · [16 §2.12](../../../docs/16-configuration-and-safety-model.md#212-mcp-phase-8)
- Research: [MCP security](../../../docs/research/observability-storage-dataquality.md#mcp-security) (superseded items noted there) · SDK: `rmcp`, the official Rust MCP SDK (version and licence (U), checked and pinned in `Cargo.lock` at build time)
- Cross-phase (depends_on): P0-T014 (repo skeleton incl. the Cargo workspace), P0-T032 (mt-api OpenAPI).
- Related: P8-T002 (tokens), P8-T004 (registry), P8-T006 (response guard), P8-T030 (limits), P8-T031/T032, P8-T008–T013 (tool groups), P8-T015 (container).

## Requirements

- Generator `crates/mt-mcp/src/gen.rs` reads `/api/v1/openapi.json` (version-pinned via `info.version`) and emits one tool per registry entry: name (`order.place` → `order_place`, `GET /positions` → `get_positions`), description (OpenAPI summary + units + confirmation level + "orders create an approval card for you; MCP can't approve"), JSON Schema input from the request model.
- Only tools whose registry state is `enabled` **and** whose scope is on the token are listed; the list refreshes on WS `system` event `mcp.registry.changed` (and on a configurable poll, default 60 s), emitting `notifications/tools/list_changed`.
- Commands are sent as `{args, idempotency_key, reason}`: `idempotency_key` = UUIDv7 per logical call, reused on retries; `reason` = client-supplied justification, length-capped (setting), passed as untrusted text.
- Errors: problem+json mapped to MCP tool errors (`type`, `title`, `detail`, `approval_id` when pending); no stack traces.
- Timeouts (settings, default 10 s); long jobs (`agents.run_analysis`, `lab.*`) return a job/run id that read tools poll.
- **stdio:** newline-delimited JSON-RPC on stdin/stdout; logs to stderr only.
- **Streamable HTTP:** single endpoint (POST + GET) with JSON-RPC 2.0, SSE streaming and **resumability** (SSE event ids; `Last-Event-ID` replays missed events from a bounded per-session buffer); `Mcp-Session-Id` issued on initialize; binds only to the `edge` network interface (no `0.0.0.0` publish, no host port); validates `Origin` (DNS-rebinding protection); requires a bearer token.
- No token passthrough beyond its audience: the token is issued by `mt-api` for `mt-api`; `mt-mcp` forwards it unchanged and holds no token, pepper or key of its own.
- Thin adapter enforced by a dependency allow-list check in CI (`cargo metadata`/`cargo deny`): `mt-mcp` may depend only on `rmcp`, `tokio`, the HTTP transport (`axum`/`hyper`), `reqwest`, `serde`, `tracing` and `mt-core` types. No SQL, NATS, broker SDKs, `mt-risk`, or policy decisions (rate limits, guard and levels are enforced in `mt-api`).
- `tracing` JSON logs with `trace_id`, args redacted; no telemetry.

## ToDo

- [ ] Scaffold `crates/mt-mcp` (Cargo workspace member, `mt-mcp` binary, `--stdio` / `--http --bind <ip>:<port>`).
- [ ] Pin `rmcp` in `Cargo.lock` (checksums); review its source (`cargo vendor`) for telemetry/network calls and note the result in the PR.
- [ ] Implement `client.rs` (reqwest, retries only with the same idempotency key, configurable timeout) and `gen.rs` (OpenAPI + registry + token scopes → tools).
- [ ] Implement Streamable HTTP session handling: session id, SSE event ids, `Last-Event-ID` resume buffer (size/TTL as settings).
- [ ] Commit `crates/mt-mcp/tests/golden/tools.snapshot.json` (generated tool list for a fixture OpenAPI + registry) so tool changes show up in review.
- [ ] Registry refresh plus `tools/list_changed` notifications.
- [ ] Add the dependency allow-list check to CI.
- [ ] Write tests (see Verification); crate README (run modes, env names `MT_API_URL`, `MT_MCP_TOKEN` / `MT_MCP_TOKEN_CMD` for local clients; no values).

## Verification

### Tests
- Golden: fixture OpenAPI + registry → `tools.snapshot.json` (names, schemas, descriptions).
- Unit: problem+json → MCP error mapping; UUIDv7 key reused across 3 retries; `reason` truncated to the configured cap.
- Unit: bind validation rejects `0.0.0.0`, LAN IPs and IPv6 `::`.
- Integration (`cargo test -p mt-mcp`; local mt-api test instance, `rmcp` client): initialize → `tools/list` → call over stdio and Streamable HTTP; a disabled tool disappears after refresh.
- Integration: Streamable HTTP stream cut mid-response, client reconnects with `Last-Event-ID` → missed events replayed once, no duplicate tool execution.
- Contract: HTTP rejects a bad `Origin` and a missing bearer.
- Static: the dependency check fails on an injected `async-nats` dependency.

### Scenarios
- Given the registry disables `order_place`, when the list refreshes, then the tool disappears and a cached call returns `tool_disabled` from mt-api.
- Given mt-api answers 503, when a command tool is called, then the client gets "mt-api unavailable" and no automatic replay happens later.
- Given a token with only `read` scope, when the client lists tools, then no write tool is listed.

### Stress / failure injection
- 50 concurrent tool calls: `mt-mcp` adds ≤ 20 ms p95 over direct mt-api calls (target).
- mt-api killed mid-call: the session stays alive, the call errors within the timeout, nothing hangs.
- 1,000 reconnects with `Last-Event-ID` in 1 min: memory bounded by the resume buffer setting.

## Acceptance criteria

- [ ] stdio and Streamable HTTP (incl. resume) both work with the SDK test client
- [ ] HTTP refuses non-edge binds, bad `Origin` and missing bearer
- [ ] Tool list is generated from OpenAPI + registry + scopes and matches the golden snapshot
- [ ] The dependency allow-list check proves there is no business logic or DB/NATS/broker access
- [ ] SDK pinned in `Cargo.lock`; no telemetry found
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- OpenAPI version mismatch with the generator: refuse to start with a clear error (no partial tool list).
- mt-api down at startup: start with zero tools and report status `degraded`; retry.
- Registry refresh fails: keep the last list for a bounded time (setting, default 5 min), then drop to zero tools (fail closed).
- Client disconnects mid-command: the command result is still visible through read tools/audit; no rollback.
- Resume buffer expired: the client must re-initialize; no events are invented.

## Cardinal rules (do NOT)

- Do NOT add business logic, composite multi-command tools, DB/NATS/broker access or policy decisions to `mt-mcp`; policy lives in `mt-api` (P8-T004/T005/T006/T030).
- Do NOT bind to `0.0.0.0` or publish a host port; reachable only via Caddy on Tailscale or stdio.
- Do NOT give `mt-mcp` its own super-token, the pepper or any secret.
- Do NOT expose anything on the never-exposed list (16 §2.12, 02 §7.4), in any form.
- Do NOT bypass `mt-api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues (including the Claude conversation); secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code (including the MCP SDK).

## Doc sync on completion

- `docs/03-build-spec.md` M20: chosen SDK + version, tool naming rule, transports as built.
- `docs/02-v1-architecture.md` §7.4: generated-from-OpenAPI note.
- `docs/roadmap/phase-8-mcp.md`: progress notes on T8.20 and T8.24.

## Branch & PR

- Branch: `p8/P8-T003-mt-mcp-server-skeleton`
- PR title: `P8-T003: mt-mcp server: transports, mt-api client and OpenAPI-generated tool schemas`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T003` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (Streamable HTTP JSON-RPC 2.0 + SSE + resumability, stdio newline-delimited JSON, edge network behind Caddy on Tailscale, scope-filtered tool list, limits/guard stay in mt-api; added T8.24/R8.08; cross-phase deps P0-T014/T032; tools/env/services)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (`mt-mcp` in Rust on `rmcp`; dependency allow-list replaces import-linter; Cargo workspace)
