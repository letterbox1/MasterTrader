---
id: P8-T020
kind: task
title: "Auth + transport tests: tokens hashed and shown once, instant revocation, expiry, transports, every call audited"
phase: 8
type: VERIFY
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P8-T002, P8-T003, P8-T007, P8-T015, P8-T031, P8-T032]
requirements: [R8.02, R8.07, R8.08]
roadmap_todos: [T8.64, T8.40]
modules: [M20]
dashboards: [D17]
tools: [uv, docker, git, nmap]
mcp: []
env: []
services: [postgres, nats, caddy, tailscale]
branch: p8/P8-T020-verify-auth-transport
pr: ""
doc_sync: [docs/roadmap/phase-8-mcp.md]
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

# P8-T020 · Auth + transport tests: tokens hashed and shown once, instant revocation, expiry, transports, every call audited

## Goal / expected outcome

A security test suite (`tests/security/test_mcp_auth.py`, `tests/security/test_mcp_transport.py`) plus an ops exposure check proves T8.64 on the test stack with the MCP SDK's own client and a fixture pepper (no real client app, no real token): a token is shown once and stored only as HMAC-SHA-256; revocation is instant; expiry is enforced and indefinite needs C3; Streamable HTTP resume, stdio, OAuth 2.1 and the optional legacy HTTP+SSE work; every call, reads included, lands in `audit.mcp_call`; and `/mcp` is reachable only through Caddy on Tailscale/TLS. The same checks with your real client are P8-T035.

## Context & references

- Roadmap: [R8.02, R8.07, R8.08](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDos [T8.64](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets) (auth + transport tests), [T8.40](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets) (container exposure check)
- Decisions: [16 §2.12](../../../docs/16-configuration-and-safety-model.md#212-mcp-phase-8) · [17 §A P8-B004](../../../docs/17-decisions-register.md#a-s2-items-all-resolved)
- Spec: [03 M20](../../../docs/03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) · [02 §7.4](../../../docs/02-v1-architecture.md#74-telegram--mcp) · [07 §5](../../../docs/07-security-notes.md#5-network--host), [07 §6](../../../docs/07-security-notes.md#6-application-controls)
- Related: P8-T002 (tokens), P8-T003 (transports), P8-T007 (audit), P8-T015 (container), P8-T031 (OAuth), P8-T032 (subscriptions, legacy endpoint).

## Requirements

- Token cases: no token → 401; malformed/unknown/expired/revoked → 401 with the right `type`; token in a query string → rejected; the create response is the only place the secret appears (a second `/mcp/tokens` read shows metadata only); the DB column holds an HMAC, and recomputing it with the fixture pepper matches.
- Expiry: each of 1d/7d/30d/1y/custom is enforced with an injected clock; indefinite triggers the C3 flow and the warning flag; the monthly reminder job fires.
- Scope cases: `read` token on a write tool → 403; any MCP token on `/auth/*`, `approval.*`, `mcp.*` or the WS command path → 403; a web session cookie on `/mcp` → rejected.
- Revocation: < 1 s from `mcp.token.revoke` to the first refused call, including mid-Streamable-HTTP-session and on an open subscription stream.
- Transport: Streamable HTTP initialize → call → stream cut → resume with `Last-Event-ID` (no duplicate execution); stdio round trip; legacy HTTP+SSE round trip when enabled, 404 when disabled; OAuth 2.1 authorization-code + PKCE flow with a resource indicator yields a token bound to `mt_api`; HTTP rejects a foreign `Origin`.
- Audit: every call in the suite (reads included, denied included) has exactly one `audit.mcp_call` row with the right transport and result status.
- Exposure: nmap from a LAN host shows no open port for `mcp`; a Tailscale peer reaches `/mcp` only through Caddy TLS. Results stored as CI artefacts; the port-scan summary (no IPs) goes in the Progress log.

## ToDo

- [ ] Write the pytest suites (MCP SDK client against the compose test stack, fake Telegram + TOTP harness, injected clock).
- [ ] Write the exposure script `ops/checks/mcp_exposure.sh`.
- [ ] Run both and record results.
- [ ] Update the roadmap progress note.

## Verification

### Tests
- The suites themselves (≥ 30 cases above), run in CI on every PR touching `mt_api/auth`, `mt_api/mcp` or `mt_mcp`.

### Scenarios
- Given a token revoked while a session is mid-conversation, when the client calls the next tool, then it fails with `token_revoked` and D17 marks the session ended.
- Given an indefinite-expiry create request without TOTP, then no token is issued.

### Stress / failure injection
- Brute force: 10,000 random tokens in 10 min → none verify; throttling and the alert fire.
- 500 concurrent Streamable HTTP sessions with random disconnects → every resumed stream consistent; no cross-session event leakage.

## Acceptance criteria

- [ ] All auth, expiry, scope and transport cases pass in CI
- [ ] Revocation < 1 s measured
- [ ] Every call in the suite has its `audit.mcp_call` row
- [ ] Exposure check shows `/mcp` only via Caddy on Tailscale/TLS
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- CI can't run nmap against the real host: the exposure check runs as a manual ops check on the host, logged with date.
- OAuth not supported by the SDK version in use: the case is marked blocked with a P8 bug, never skipped silently.

## Cardinal rules (do NOT)

- Do NOT run scans against hosts you don't own.
- Do NOT use real tokens or the real pepper; fixtures only.
- Do NOT log tokens in test output.
- Do NOT commit secrets or paste them into chats/issues (including the Claude conversation); secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/roadmap/phase-8-mcp.md`: tick T8.64 when P8-T035 has also passed; tick T8.40 with P8-T015; R8.02/R8.08 verified (link to CI run).

## Branch & PR

- Branch: `p8/P8-T020-verify-auth-transport`
- PR title: `P8-T020: Auth + transport tests: tokens hashed and shown once, instant revocation, expiry, transports, every call audited`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T020` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (now the keyless T8.64 suite: HMAC + pepper, shown once, expiry options incl. indefinite → C3, Streamable HTTP resume, stdio, OAuth 2.1, legacy HTTP+SSE, `audit.mcp_call` for every call; real-client checks split to P8-T035; deps P8-T007/T031/T032; added R8.07/R8.08; tools/env/services)
