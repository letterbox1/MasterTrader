---
id: P8-T002
kind: task
title: Scoped, revocable MCP tokens and the `mcp` principal in mt_api
phase: 8
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P8-T001, P8-B004]
requirements: [R8.02, R8.07]
roadmap_todos: [T8.20]
modules: [M20, M17]
dashboards: [D16, D17]
branch: p8/P8-T002-scoped-mcp-tokens
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/07-security-notes.md, docs/ui/dashboards/D16-system.md, docs/ui/dashboards/D17-mcp-console.md, docs/roadmap/phase-8-mcp.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P8-T002 · Scoped, revocable MCP tokens and the `mcp` principal in mt_api

## Goal / expected outcome

`mt_api` accepts bearer tokens bound to a principal with `source = mcp`. Each token has scopes (tool groups), an expiry and a label, is stored only as a hash, and can be revoked instantly. Every request made with one carries `source = mcp`, `token_id` and the MCP session id into the command bus and audit. This is the authentication base for every other P8 item.

## Context & references

- Roadmap: [R8.02, R8.07](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDo [T8.20](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- Architecture: [02 §7 transport & auth](../../../docs/02-v1-architecture.md#7-api-contract-mt_api) ("scoped tokens for Telegram and MCP") · [02 §7.2 MCP commands](../../../docs/02-v1-architecture.md#72-commands-rest-write) (`mcp.token.revoke`)
- Security: [07 §6 MCP server](../../../docs/07-security-notes.md#6-application-controls) · [07 §2 secrets & 90-day rotation](../../../docs/07-security-notes.md#2-secrets) · research: [MCP security](../../../docs/research/observability-storage-dataquality.md#mcp-security)
- UI: [D16 Security → Sessions](../../../docs/ui/dashboards/D16-system.md) ("MCP tokens (Phase 8)") · [D17 Connection widget](../../../docs/ui/dashboards/D17-mcp-console.md) (token expiry, revoke)
- Cross-phase: P0 R0.08 / T0.24 (`mt_api` auth, command bus, confirmation engine, `audit.command`).
- Gap: P8-B004 (token lifecycle undefined); this task implements the proposal there once it is accepted.

## Requirements

- Token = 256-bit random (`secrets.token_urlsafe(32)`), shown **once**; stored in `ops.mcp_token` as SHA-256 hash + 8-char prefix, with `id, label, scopes[], created_at, expires_at, last_used_at, revoked_at, created_by_command_id`.
- Scopes = tool groups `read`, `agents`, `curation`, `strategies`, `trade`, `risk`. A token with `trade`, `strategies` or `risk` scope grants write capability, so creating it (or adding such a scope) is **C3**; read-only tokens are C1.
- Commands: `mcp.token.create` (C1 read-only scopes / C3 write scopes) and `mcp.token.revoke` (C1). Both callable from web/Telegram only, **never** by an MCP principal (no self-escalation).
- Query: `/mcp/tokens` (masked: prefix, label, scopes, expiry, last used, revoked) for D16/D17.
- Expiry: default 30 days, maximum 90 days (aligned with the 07 §2 rotation rhythm). Numbers are proposals until P8-B004 closes.
- Revocation takes effect on the next request (< 1 s); revoked/expired → 401 problem+json with `type` `token_revoked` / `token_expired`.
- MCP tokens can't open a web session, call `/auth/*`, call any `mcp.*` command, or use the WebSocket command path.
- Constant-time comparison; failed auth limited to 10/min per source IP, then `alert.warn.mcp_auth` to Telegram.
- Request context carries `source = mcp`, `token_id`, `client_label`, `mcp_session_id` (from the `Mcp-Session-Id` header); the command bus writes them to `audit.command`.

## ToDo

- [ ] Alembic migration for `ops.mcp_token` (mutable ops table; create/revoke events themselves land in WORM `audit.command`).
- [ ] `packages/mt_api/auth/mcp_tokens.py`: issue, verify (hash lookup, expiry, revoked), revoke; FastAPI dependency `require_mcp(scope=...)`.
- [ ] Register commands `mcp.token.create` / `mcp.token.revoke` with their confirmation levels in the command catalogue; add `/mcp/tokens` query.
- [ ] Principal plumbing: `source`, `token_id`, `client_label`, `mcp_session_id` in request context and `audit.command` columns (add columns via migration if P0 didn't).
- [ ] Prometheus counters `mt_api_mcp_auth_total{result}`; Telegram alert on failed-auth bursts.
- [ ] Never log the `Authorization` header (structlog redaction processor + test).
- [ ] Regenerate and version the OpenAPI document.
- [ ] Write tests (see Verification); update docs listed under Doc sync.

## Verification

### Tests
- Unit: verify accepts a fresh token, rejects expired, revoked, unknown and malformed tokens; hash-only storage (no plaintext column).
- Unit: scope check matrix (scope × tool group) → allow/deny.
- Integration: create (C1 read) → call `/positions` → revoke → next call 401 within 1 s.
- Integration: create with `trade` scope triggers the C3 flow (Telegram approve + TOTP + cool-down) before the token is shown.
- Integration: MCP principal calling `mcp.token.create` or `/auth/login` → 403 and an audit row.
- Property: random 32-byte strings never verify.

### Scenarios
- Given a read-only token, when Claude calls `order_place`, then mt_api returns 403 `scope_missing` and nothing reaches M11.
- Given a token past `expires_at`, when it calls any endpoint, then 401 `token_expired` and D17 shows it as expired.
- Given a leaked token, when you revoke it in D17, then the next call fails and the audit shows the revoke command (C1, source web).

### Stress / failure injection
- 1,000 invalid-token requests/min from one IP → throttled after 10/min; mt_api p95 for web requests unchanged (± 10%).
- Postgres restart during verification → requests fail closed (401/503), never open.

## Acceptance criteria

- [ ] Tokens hashed at rest; plaintext shown once and never logged
- [ ] Revocation effective < 1 s in the integration test
- [ ] Write-scope token creation requires C3; MCP principals can't call `mcp.*` or `/auth/*`
- [ ] `audit.command` rows from MCP carry `source = mcp`, `token_id`, `mcp_session_id`
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Postgres down: verification can't read tokens → fail closed; web login unaffected only if its own path is up.
- Clock: expiry is evaluated server-side in UTC (chrony); client clocks are irrelevant.
- Restart: tokens persist in Postgres; in-memory caches (if any) expire within 5 s.
- Lost token: there is no recovery; revoke and create a new one.

## Cardinal rules (do NOT)

- Do NOT store or log plaintext tokens or the `Authorization` header.
- Do NOT let an MCP principal create, widen or revoke tokens, or change MCP policy (no self-escalation).
- Do NOT reuse the Telegram token or the web session for MCP.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues (including into the Claude conversation); secrets live in the sops/age file (07 §2).
- Do NOT update or delete WORM rows; corrections are new rows (15 §2).
- Do NOT make loosening risk, autonomous mode, mandates or kill-switch OFF anything less than C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code (including the MCP SDK).

## Doc sync on completion

- `docs/02-v1-architecture.md` §7 + §7.2: token model, `mcp.token.create` command and `/mcp/tokens` query.
- `docs/07-security-notes.md` §6: token scopes, expiry, revocation.
- `docs/ui/dashboards/D16-system.md` Sessions and `docs/ui/dashboards/D17-mcp-console.md` Connection: token fields.
- `docs/roadmap/phase-8-mcp.md`: tick T8.20 when P8-T003 and the tool groups are also done (note partial progress here).

## Branch & PR

- Branch: `p8/P8-T002-scoped-mcp-tokens`
- PR title: `P8-T002: Scoped, revocable MCP tokens and the `mcp` principal in mt_api`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T002` run

## Progress log

- 2026-10-21 00:00 · planner · created
