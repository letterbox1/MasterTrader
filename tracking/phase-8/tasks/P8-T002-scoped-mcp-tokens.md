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
depends_on: [P8-T001, P0-T032, P0-T033, P0-T034, P0-T035]
requirements: [R8.02, R8.07, R8.08]
roadmap_todos: [T8.24]
modules: [M20, M17]
dashboards: [D16, D17]
tools: [uv, docker, git]
mcp: []
env: []
services: [postgres, nats]
branch: p8/P8-T002-scoped-mcp-tokens
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/07-security-notes.md, docs/ui/dashboards/D16-system.md, docs/ui/dashboards/D17-mcp-console.md, docs/roadmap/phase-8-mcp.md]
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

# P8-T002 · Scoped, revocable MCP tokens and the `mcp` principal in mt_api

## Goal / expected outcome

`mt_api` issues, verifies and revokes MCP tokens exactly as decided in [16 §2.12](../../../docs/16-configuration-and-safety-model.md#212-mcp-phase-8): opaque 256-bit, shown once, stored as HMAC-SHA-256 with a server pepper, scoped, revocable instantly, with last use and client identity recorded and an expiry you choose per token (1 day · 7 days · 30 days · 1 year · custom · indefinite). Every request made with one carries `source = mcp`, `token_id`, client identity and the MCP session id into the command bus and audit. This is the authentication base for every other P8 item (the OAuth 2.1 flow in P8-T031 issues the same tokens).

## Context & references

- Roadmap: [R8.02, R8.07, R8.08](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDo [T8.24](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets) (token lifecycle part)
- Decisions: [17 §A P8-B004](../../../docs/17-decisions-register.md#a-s2-items-all-resolved) (token model) · [16 §2.12](../../../docs/16-configuration-and-safety-model.md#212-mcp-phase-8) (scopes, expiry options, creation levels) · [17 §E](../../../docs/17-decisions-register.md#e-ratification-2026-10-22)
- Architecture: [02 §7 auth](../../../docs/02-v1-architecture.md#7-api-contract-mt_api) · [02 §7.2 MCP commands row](../../../docs/02-v1-architecture.md#72-commands-rest-write) (`mcp.token.create` C1, C3 for indefinite or `trade`/`strategy`/`risk_tighten`; `mcp.token.revoke` C1; web/Telegram only) · [02 §7.4](../../../docs/02-v1-architecture.md#74-telegram--mcp)
- Security: [07 §6 MCP server](../../../docs/07-security-notes.md#6-application-controls) · [07 §2 secrets](../../../docs/07-security-notes.md#2-secrets) (the MCP token pepper lives in the sops file)
- UI: [D17 Tokens widget + actions](../../../docs/ui/dashboards/D17-mcp-console.md) · [D16 Security → Sessions](../../../docs/ui/dashboards/D16-system.md)
- Cross-phase (depends_on): P0-T032 (mt_api skeleton, OpenAPI), P0-T033 (single-user auth/sessions), P0-T034 (command bus + `audit.command`), P0-T035 (confirmation engine C0–C3).

## Requirements

- Token = 256 random bits (`secrets.token_bytes(32)`, base64url with a short non-secret prefix such as `mtm_` for secret scanning), returned **once** in the create response and never again.
- Storage `ops.mcp_token`: `id, label, scopes[], token_hmac (HMAC-SHA-256(pepper, token)), prefix (first 8 chars), created_at, expiry_kind (1d|7d|30d|1y|custom|indefinite), expires_at (null for indefinite), last_used_at, last_client (clientInfo name/version + source IP), revoked_at, created_by_command_id`. No plaintext column. The pepper is read from the secrets file at start (tmpfs); tests use a fixture pepper.
- Scopes ([16 §2.12](../../../docs/16-configuration-and-safety-model.md#212-mcp-phase-8)): `read`, `analyse`, `trade` (creates approval cards only), `strategy`, `risk_tighten`, `curation`. There is no loosening scope.
- `mcp.token.create` (web/Telegram only): **C1** for `read`/`analyse`/`curation`; **C3** (Telegram + TOTP + cool-down, 16 §2.3) for any of `trade`/`strategy`/`risk_tighten` and for any indefinite expiry. The token is shown only after the C3 completes.
- Indefinite expiry: the create form shows a red exposure/security warning; a monthly reminder job lists indefinite tokens (Telegram + D17) until revoked.
- `mcp.token.revoke` (C1, immediate): the next request with that token fails (< 1 s, no cache longer than that).
- Query `/mcp/tokens`: metadata only (prefix, label, scopes, created, expiry, last used + client, revoked); never the secret.
- MCP principals can't call `/auth/*`, any `mcp.*` or `approval.*` command, or open a web session (never exposed, 02 §7.4).
- Constant-time comparison (HMAC compare); failed auth is throttled per source IP (configurable, default 10/min in settings) and alerts on bursts.
- Request context carries `source = mcp`, `token_id`, client identity and `mcp_session_id` (`Mcp-Session-Id` header); the command bus writes them to `audit.command`, and P8-T007 to `audit.mcp_call`.
- All numbers (throttle, reminder cadence) are settings defaults, not constants.

## ToDo

- [ ] Alembic migration for `ops.mcp_token` (mutable ops table; create/revoke events themselves are WORM rows in `audit.command`).
- [ ] `packages/mt_api/auth/mcp_tokens.py`: issue (HMAC with pepper), verify (HMAC lookup by prefix, expiry, revoked), revoke; FastAPI dependency `require_mcp(scope=...)`; last-used + client identity update.
- [ ] Commands `mcp.token.create` / `mcp.token.revoke` in the command catalogue with the level rules above; query `/mcp/tokens`.
- [ ] Indefinite-token warning flag in the create response and a monthly reminder job (Prefect) publishing `alert.info.mcp_token_indefinite`.
- [ ] Principal plumbing (`source`, `token_id`, client identity, `mcp_session_id`) into request context and `audit.command`.
- [ ] Prometheus `mt_api_mcp_auth_total{result}`; alert on failed-auth bursts.
- [ ] structlog processor that never logs the `Authorization` header or token values (+ test).
- [ ] Regenerate and version the OpenAPI document.
- [ ] Write tests (see Verification); update docs listed under Doc sync.

## Verification

### Tests
- Unit: verify accepts a fresh token; rejects expired, revoked, unknown, malformed; the DB holds only the HMAC (no plaintext column); changing the pepper invalidates all tokens.
- Unit: level matrix for `mcp.token.create`: each scope set × expiry option → C1 or C3, exactly as 16 §2.12.
- Unit: scope check matrix (scope × tool group) → allow/deny; no scope permits loosening.
- Integration (test stack, fixture pepper): create (`read`, 7d) → call `/positions` → revoke → next call 401 `token_revoked` within 1 s.
- Integration: create with `trade` scope or indefinite expiry triggers the C3 flow (fake Telegram + TOTP harness, injected clock for the cool-down) before the token is shown.
- Integration: an MCP principal calling `mcp.token.create`, `approval.approve` or `/auth/login` → 403 and an audit row.
- Property: random 32-byte strings never verify.

### Scenarios
- Given a `read`-only token, when Claude calls `order_place`, then mt_api returns 403 `scope_missing` and nothing reaches M11.
- Given a token past `expires_at`, when it calls any endpoint, then 401 `token_expired` and D17 shows it expired.
- Given you choose "indefinite" in D17, then a red warning shows, the token appears only after Telegram + TOTP + cool-down, and a reminder arrives each month.
- Given a leaked token, when you revoke it in D17, then the next call fails and `audit.command` shows the revoke (C1, source web).

### Stress / failure injection
- 1,000 invalid-token requests/min from one IP → throttled; mt_api p95 for web requests unchanged (± 10%).
- Postgres restart during verification → requests fail closed (401/503), never open.
- Pepper missing from the secrets mount → mt_api refuses MCP auth (503) and alerts; web login unaffected.

## Acceptance criteria

- [ ] Tokens 256-bit, shown once, stored only as HMAC-SHA-256 with the pepper; never logged
- [ ] Every expiry option works; indefinite = warning + C3 + monthly reminder
- [ ] `trade`/`strategy`/`risk_tighten` scope creation requires C3; `read`/`analyse`/`curation` C1
- [ ] Revocation effective < 1 s in the integration test; last use + client identity recorded
- [ ] MCP principals can't call `mcp.*`, `approval.*` or `/auth/*`
- [ ] `audit.command` rows from MCP carry `source = mcp`, `token_id`, `mcp_session_id`
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Postgres down: verification can't read tokens → fail closed; web login unaffected only if its own path is up.
- Clock: expiry evaluated server-side in UTC (chrony); client clocks irrelevant.
- Restart: tokens persist; any in-memory cache expires within 1 s so revocation stays instant.
- Lost token: no recovery; revoke and create a new one.
- Pepper rotation: rotating the pepper invalidates every token (documented in the runbook, P8-T017).

## Cardinal rules (do NOT)

- Do NOT store or log plaintext tokens, the pepper or the `Authorization` header.
- Do NOT let an MCP principal create, widen or revoke tokens, change MCP policy or approve anything (`mcp.*`, `approval.*` never exposed).
- Do NOT add a loosening scope or a "skip approval" option.
- Do NOT reuse the Telegram token or the web session for MCP.
- Do NOT hard-code throttle or reminder values; they are settings defaults.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues (including the Claude conversation); secrets live in the sops/age file (07 §2).
- Do NOT update or delete WORM rows; corrections are new rows (15 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/02-v1-architecture.md` §7.1/§7.2/§7.4: token fields as built.
- `docs/07-security-notes.md` §6: token storage and pepper handling.
- `docs/ui/dashboards/D16-system.md` Sessions and `docs/ui/dashboards/D17-mcp-console.md` Tokens: fields as built.
- `docs/roadmap/phase-8-mcp.md`: progress note on T8.24 (ticked when P8-T003, P8-T007, P8-T031 and P8-T032 are also done).

## Branch & PR

- Branch: `p8/P8-T002-scoped-mcp-tokens`
- PR title: `P8-T002: Scoped, revocable MCP tokens and the mcp principal in mt_api`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T002` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (HMAC-SHA-256 + pepper, 16 §2.12 scopes and expiry options incl. indefinite = warning + C3 + monthly reminder, C1/C3 creation levels, client identity; mapped to T8.24/R8.08; dropped gap dep P8-B004; cross-phase deps P0-T032/T033/T034/T035; tools/env/services)
