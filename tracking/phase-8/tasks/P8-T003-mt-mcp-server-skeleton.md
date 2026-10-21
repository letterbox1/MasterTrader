---
id: P8-T003
kind: task
title: "`mt_mcp` server: transports, mt_api client and OpenAPI-generated tool schemas"
phase: 8
type: BUILD
status: backlog
priority: critical
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P8-T002]
requirements: [R8.01, R8.02, R8.03]
roadmap_todos: [T8.20]
modules: [M20]
dashboards: [D17]
branch: p8/P8-T003-mt-mcp-server-skeleton
pr: ""
doc_sync: [docs/03-build-spec.md, docs/02-v1-architecture.md, docs/roadmap/phase-8-mcp.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P8-T003 · `mt_mcp` server: transports, mt_api client and OpenAPI-generated tool schemas

## Goal / expected outcome

`packages/mt_mcp` is a working MCP server that turns the `mt_api` OpenAPI document into MCP tools, filtered by the server-side registry (`/mcp/tools`, P8-T004). Each tool call becomes exactly one `mt_api` HTTP call made with the caller's token. It runs over **stdio** or **Streamable HTTP** bound to localhost/Tailscale only. It holds no business logic and no credentials of its own.

## Context & references

- Roadmap: [R8.01–R8.03](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDo [T8.20](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- Spec: [03 M20](../../../docs/03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) (official `mcp` SDK or FastMCP, thin adapter) · repo layout `packages/mt_mcp/` (03 §3)
- API: [02 §7](../../../docs/02-v1-architecture.md#7-api-contract-mt_api) conventions (snake_case, decimals as strings, ISO-8601 UTC, cursor pagination, RFC 9457 errors) · [02 §7.2](../../../docs/02-v1-architecture.md#72-commands-rest-write) command body
- Research: [MCP security](../../../docs/research/observability-storage-dataquality.md#mcp-security) (stdio preferred; read tools separate from typed write tools; annotations are hints only) · SDK pins: `mcp` 2.3.0 (MIT) or FastMCP 4.1.3 (Apache-2.0)
- Related: P8-T002 (tokens), P8-T004 (registry), P8-T006 (response guard), P8-T008–T013 (tool groups), P8-T015 (container).

## Requirements

- Generator `mt_mcp/gen.py` reads `/api/v1/openapi.json` (version-pinned via `info.version`) and emits one tool per registry entry: name (`order.place` → `order_place`, `GET /positions` → `get_positions`), description (OpenAPI summary + units + confirmation level + "may wait for your Telegram approval" for C2/C3), JSON Schema input from the request model.
- Only tools whose registry state is `enabled` **and** whose group is in the token's scopes are listed; the list refreshes every 60 s and on WS `system` event `mcp.registry.changed`, emitting `notifications/tools/list_changed`.
- Commands are sent as `{args, idempotency_key, reason}`: `idempotency_key` = UUIDv7 per logical call, reused on retries; `reason` = client-supplied justification/conversation excerpt, ≤ 500 chars, passed as untrusted text.
- Errors: problem+json mapped to MCP tool errors (`type`, `title`, `detail`, `approval_id` when pending); no stack traces.
- Timeouts: 10 s for queries and commands; long jobs (`agents.run_analysis`, `lab.*`) return a job/run id that read tools poll.
- Transport: stdio (default; launched by the client) or Streamable HTTP on `127.0.0.1` or the Tailscale IP only. Startup refuses `0.0.0.0`/LAN binds. HTTP validates the `Origin` header (DNS-rebinding protection) and requires a bearer token.
- No token passthrough beyond its audience: the token is issued by `mt_api` for `mt_api`; `mt_mcp` forwards it unchanged and holds no token or key of its own.
- Thin adapter enforced by an import-linter contract: `mt_mcp` may import only `mcp`/`fastmcp`, `httpx`, `pydantic`, `structlog`, `mt_core.schemas`. No SQL, NATS, broker SDKs or `mt_risk`.
- Structlog JSON logs with `trace_id`, args redacted; no telemetry.

## ToDo

- [ ] Scaffold `packages/mt_mcp` (uv workspace member, `mt-mcp` console script, `--stdio` / `--http --bind <ip>:<port>`).
- [ ] Pin the chosen SDK (`mcp==2.3.0` or `fastmcp==4.1.3`) with hashes in `uv.lock`; grep the vendored SDK for telemetry/network calls and note the result in the PR.
- [ ] Implement `client.py` (httpx, retries only with the same idempotency key, 10 s timeout) and `gen.py` (OpenAPI + registry → tools).
- [ ] Commit `packages/mt_mcp/tests/golden/tools.snapshot.json` (generated tool list for a fixture OpenAPI + registry) so tool changes show up in review.
- [ ] Implement registry refresh plus `tools/list_changed` notifications.
- [ ] Add the import-linter contract to CI.
- [ ] Write tests (see Verification); write the package README (run modes, env vars `MT_API_URL`, `MT_MCP_TOKEN` / `MT_MCP_TOKEN_CMD`).

## Verification

### Tests
- Golden: fixture OpenAPI + registry → `tools.snapshot.json` (names, schemas, descriptions).
- Unit: problem+json → MCP error mapping; UUIDv7 key reused across 3 retries; `reason` truncated to 500 chars.
- Unit: bind validation rejects `0.0.0.0`, LAN IPs and IPv6 `::`.
- Integration (mt_api test instance): `tools/list` over stdio and HTTP; `get_positions` round trip; a disabled tool disappears after refresh.
- Contract: an SDK test client completes initialize → list → call; HTTP rejects a bad `Origin`.
- Static: the import-linter contract fails on an injected `import nats`.

### Scenarios
- Given the registry disables `order_place`, when the list refreshes, then the tool disappears and a cached call returns `tool_disabled` from mt_api.
- Given mt_api answers 503, when a command tool is called, then Claude gets "mt_api unavailable" and no automatic replay happens later.
- Given a token with only `read` scope, when the client lists tools, then no write tool is listed.

### Stress / failure injection
- 50 concurrent tool calls: `mt_mcp` adds ≤ 20 ms p95 over direct mt_api calls (proposed target).
- mt_api killed mid-call: the session stays alive, the call errors within 10 s, nothing hangs.

## Acceptance criteria

- [ ] stdio and Streamable HTTP both work; HTTP refuses non-local/non-Tailscale binds and bad `Origin`
- [ ] Tool list is generated from OpenAPI + registry and matches the golden snapshot
- [ ] The import-linter contract proves there is no business logic or DB/NATS/broker access
- [ ] SDK pinned by hash; no telemetry found
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- OpenAPI version mismatch with the generator: refuse to start with a clear error (no partial tool list).
- mt_api down at startup: start with zero tools and report status `degraded`; retry every 10 s.
- Registry refresh fails: keep the last list for ≤ 5 min, then drop to zero tools (fail closed).
- Client disconnects mid-command: the command result is still visible through read tools/audit; no rollback is attempted.

## Cardinal rules (do NOT)

- Do NOT add business logic, composite multi-command tools, DB/NATS/broker access or policy decisions to `mt_mcp`; policy lives in `mt_api` (P8-T004/T005/T006).
- Do NOT bind to `0.0.0.0` or publish a port outside localhost/Tailscale.
- Do NOT give `mt_mcp` its own super-token or any secret.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT expose withdrawals, API-key management or wallet mandate signing through MCP, in any form (R8.06).
- Do NOT commit secrets or paste them into chats/issues (including into the Claude conversation); secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code (including the MCP SDK).

## Doc sync on completion

- `docs/03-build-spec.md` M20: chosen SDK + version, tool naming rule, transports.
- `docs/02-v1-architecture.md` §7.4: generated-from-OpenAPI note.
- `docs/roadmap/phase-8-mcp.md`: progress note on T8.20.

## Branch & PR

- Branch: `p8/P8-T003-mt-mcp-server-skeleton`
- PR title: `P8-T003: `mt_mcp` server: transports, mt_api client and OpenAPI-generated tool schemas`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T003` run

## Progress log

- 2026-10-21 00:00 · planner · created
