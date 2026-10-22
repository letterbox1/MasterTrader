---
id: P8-T031
kind: task
title: OAuth 2.1 authorization for MCP clients (PKCE, resource indicators)
phase: 8
type: BUILD
status: backlog
priority: medium
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P8-T002, P8-T003]
requirements: [R8.08, R8.02]
roadmap_todos: [T8.24]
modules: [M20]
dashboards: [D17]
tools: [uv, docker, git]
mcp: []
env: []
services: [postgres, nats]
branch: p8/P8-T031-oauth-2-1-authorization-for-mcp-clients-pkce-res
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/03-build-spec.md, docs/07-security-notes.md, docs/ui/dashboards/D17-mcp-console.md, docs/roadmap/phase-8-mcp.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-22
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P8-T031 · OAuth 2.1 authorization for MCP clients (PKCE, resource indicators)

## Goal / expected outcome

MCP clients that support MCP authorization can connect to the Streamable HTTP endpoint by signing in instead of pasting a token: `mt_api` acts as the OAuth 2.1 authorization server for the `mt_mcp` resource, with authorization code + PKCE (S256) and resource indicators, and issues exactly the same scoped, expiring, HMAC-stored tokens as P8-T002. Consent happens in the web app after your normal login + TOTP, and write scopes or indefinite expiry still need C3. Tested with a scripted OAuth client on the test stack; no real client or key.

## Context & references

- Roadmap: [R8.08](../../../docs/roadmap/phase-8-mcp.md#3-requirements) ("OAuth 2.1 (PKCE, resource indicators) where the client supports it") · ToDo [T8.24](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- Decisions: [17 §A P8-B004](../../../docs/17-decisions-register.md#a-s2-items-all-resolved) · [16 §2.12](../../../docs/16-configuration-and-safety-model.md#212-mcp-phase-8) (scopes, expiry options, creation levels)
- Spec: [03 M20](../../../docs/03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) · [02 §7.4 Tokens](../../../docs/02-v1-architecture.md#74-telegram--mcp) · [07 §6](../../../docs/07-security-notes.md#6-application-controls)
- External specs (pin the versions in the PR): MCP authorization spec for HTTP transports; OAuth 2.1 draft; RFC 7636 (PKCE), RFC 8707 (resource indicators), RFC 8414 (authorization server metadata), RFC 9728 (protected resource metadata).
- Related: P8-T002 (token model), P8-T003 (Streamable HTTP), P8-T016 (D17 consent/tokens), P8-T020 (keyless tests), P8-T035 (real client check).

## Requirements

- `mt_mcp` (resource server) publishes protected-resource metadata pointing at `mt_api` as the authorization server and answers unauthenticated requests with 401 + `WWW-Authenticate` referencing it.
- `mt_api` publishes authorization-server metadata and implements: authorization endpoint (web app consent screen, requires an existing web session with TOTP), token endpoint, revocation endpoint. Authorization code + PKCE S256 only; no implicit or password grants; exact redirect-URI matching (loopback redirects for desktop clients allowed per OAuth 2.1); short-lived codes (setting).
- Resource indicators: the `resource` parameter must equal the canonical `mt_mcp` URL; tokens are audience-bound to it and refused elsewhere (no token passthrough).
- Client registration: dynamic client registration if the SDK client needs it, limited to loopback/Tailscale redirect URIs and recorded; or pre-registered clients via D17. Client identity is stored with the token (last used + client identity, 16 §2.12).
- Consent screen shows the requested scopes and an expiry picker (1 day · 7 days · 30 days · 1 year · custom · indefinite). `read`/`analyse`/`curation` = C1 confirm; `trade`/`strategy`/`risk_tighten` or indefinite = C3 (Telegram approve + TOTP + cool-down) before the token is issued; indefinite shows the red warning.
- Issued access tokens are the P8-T002 opaque tokens (HMAC-SHA-256 with the pepper, revocable instantly). Refresh tokens, if offered, are also opaque, HMAC-stored, rotated on use and capped by the chosen expiry.
- Only reachable via Caddy on Tailscale/TLS. Nothing about OAuth is exposed as an MCP tool (`mcp.*` never exposed).

## ToDo

- [ ] Choose and pin the library (e.g. the MCP SDK auth helpers or `authlib`), with hashes; check it for telemetry.
- [ ] Implement metadata endpoints, authorize/consent (web), token, revoke; PKCE S256 and `resource` validation.
- [ ] Hook token issuance into P8-T002 (same table, scopes, levels, C3 path, expiry options).
- [ ] Optional dynamic client registration with redirect-URI allow-list; pre-registered clients in D17.
- [ ] Scripted OAuth client tests on the test stack; update docs.

## Verification

### Tests
- Integration: full code + PKCE flow → token → `tools/list` over Streamable HTTP; wrong `code_verifier` → `invalid_grant`.
- Integration: missing or wrong `resource` → refused; a token issued for `mt_mcp` is rejected by any other audience.
- Integration: consent for `trade` scope routes through the fake Telegram + TOTP harness and cool-down before issuance; indefinite expiry the same.
- Unit: redirect-URI exact match; code reuse refused; code expiry enforced.
- Integration: revoking in D17 kills the access token (< 1 s) and any refresh token.

### Scenarios
- Given a client that supports MCP OAuth, when you connect it, then the browser opens the consent screen after login + TOTP, and the client gets a token without you copying anything.
- Given a client that doesn't support OAuth, then the bearer-token path from P8-T002 still works.
- Given a malicious page tries the authorize endpoint with a non-allow-listed redirect, then it's refused and alerted.

### Stress / failure injection
- 100 concurrent authorization flows: no code collision; token endpoint p95 < 200 ms.
- Postgres down mid-flow: the flow fails closed; no token issued.

## Acceptance criteria

- [ ] Code + PKCE (S256) and resource indicators work end to end with a scripted client
- [ ] Issued tokens follow 16 §2.12 exactly (scopes, expiry options, C1/C3 levels, HMAC storage, instant revoke)
- [ ] No implicit/password grants; exact redirect matching; audience binding enforced
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Client sends no `resource`: refused with a clear error (fail closed).
- Clock skew on the client: irrelevant; expiry is server-side.
- Consent abandoned: the code is never issued; pending C3 expires.

## Cardinal rules (do NOT)

- Do NOT add implicit, password or client-credentials grants.
- Do NOT issue a token with a write scope or indefinite expiry without C3.
- Do NOT accept tokens minted for another audience, or pass the client's token to any other service.
- Do NOT expose any OAuth or token management as an MCP tool.
- Do NOT commit secrets or paste them into chats/issues (including the Claude conversation); secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/02-v1-architecture.md` §7.4 and `docs/03-build-spec.md` M20: OAuth endpoints and grant types as built.
- `docs/07-security-notes.md` §6: OAuth controls.
- `docs/ui/dashboards/D17-mcp-console.md`: consent screen and registered clients.
- `docs/roadmap/phase-8-mcp.md`: progress on T8.24.

## Branch & PR

- Branch: `p8/P8-T031-oauth-2-1-authorization-for-mcp-clients-pkce-res`
- PR title: `P8-T031: OAuth 2.1 authorization for MCP clients (PKCE, resource indicators)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T031` run

## Progress log

- 2026-10-22 00:00 · aligner · created for R8.08 / T8.24 (OAuth 2.1 with PKCE and resource indicators per 17 §A P8-B004; same tokens and C1/C3 levels as P8-T002)
