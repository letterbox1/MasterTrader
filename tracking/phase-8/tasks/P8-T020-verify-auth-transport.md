---
id: P8-T020
kind: task
title: "Verify auth and transport: scoped tokens, revocation, localhost/Tailscale only"
phase: 8
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P8-T002, P8-T003, P8-T015]
requirements: [R8.02]
roadmap_todos: [T8.20, T8.40]
modules: [M20]
dashboards: [D17]
branch: p8/P8-T020-verify-auth-transport
pr: ""
doc_sync: [docs/roadmap/phase-8-mcp.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P8-T020 · Verify auth and transport: scoped tokens, revocation, localhost/Tailscale only

## Goal / expected outcome

A security test suite (`tests/security/test_mcp_auth.py` plus an ops port-scan check) proves the R8.02 "Auth tests". Tokens are scoped, expire and revoke in < 1 s; transport is reachable only via stdio, localhost or Tailscale.

## Context & references

- Roadmap: [R8.02](../../../docs/roadmap/phase-8-mcp.md#3-requirements) (verified by: Auth tests) · ToDos [T8.20, T8.40](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- Spec: [03 M20](../../../docs/03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) · [02 §7](../../../docs/02-v1-architecture.md#7-api-contract-mt_api) · [07 §5](../../../docs/07-security-notes.md#5-network--host) · research [MCP security](../../../docs/research/observability-storage-dataquality.md#mcp-security)
- Related: P8-T002, P8-T003, P8-T015.

## Requirements

- Cases: no token → 401; malformed/unknown/expired/revoked → 401 with the right `type`; token in query string → rejected; read token on write tool → 403; MCP token on `/auth/*`, `mcp.*`, WS command path → 403; web session cookie on `/mcp` → rejected (no CORS, `SameSite=Strict`).
- Revocation: measured < 1 s from `mcp.token.revoke` to first refused call, including mid-Streamable-HTTP-session.
- Transport: HTTP `Origin` validation rejects a foreign origin; nmap from LAN and from a public VPS shows no open port; Tailscale peer reaches `/mcp` only through Caddy TLS.
- Results stored as CI artefacts; the port-scan result is pasted (no IPs) in the Progress log.

## ToDo

- [ ] Write the pytest suite.
- [ ] Write the port-scan script `ops/checks/mcp_exposure.sh`.
- [ ] Run both and record results.
- [ ] Update the roadmap progress note.

## Verification

### Tests
- The suite itself (≥ 15 cases above), run in CI on every PR touching `mt_api/auth` or `mt_mcp`.

### Scenarios
- Given a token revoked while Claude is mid-conversation, when Claude calls the next tool, then it fails with `token_revoked` and D17 marks the session ended.

### Stress / failure injection
- Brute force: 10,000 random tokens in 10 min → none verify; throttling and the Telegram alert fire.

## Acceptance criteria

- [ ] All auth cases pass in CI
- [ ] Revocation < 1 s measured
- [ ] Port scan shows exposure only via localhost/Tailscale
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- CI can't run nmap against the real host: the port-scan runs as a manual ops check, logged with date.

## Cardinal rules (do NOT)

- Do NOT run scans against hosts you don't own.
- Do NOT log real tokens in test output.
- Do NOT commit secrets or paste them into chats/issues (including into the Claude conversation); secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code (including the MCP SDK).

## Doc sync on completion

- `docs/roadmap/phase-8-mcp.md`: R8.02 verified (link to CI run).

## Branch & PR

- Branch: `p8/P8-T020-verify-auth-transport`
- PR title: `P8-T020: Verify auth and transport: scoped tokens, revocation, localhost/Tailscale only`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T020` run

## Progress log

- 2026-10-21 00:00 · planner · created
