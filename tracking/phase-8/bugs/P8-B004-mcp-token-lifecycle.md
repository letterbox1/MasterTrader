---
id: P8-B004
kind: gap
title: "MCP token lifecycle is undefined: no create command, scopes, expiry or storage rule"
phase: 8
type: DOC
status: done
priority: high
size: S
severity: S2
owner: agent
claimed_by: ""
depends_on: []
requirements: [R8.02]
roadmap_todos: [T8.20]
modules: [M20]
dashboards: [D17, D16]
branch: p8/P8-B004-mcp-token-lifecycle
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/ui/dashboards/D17-mcp-console.md, docs/ui/dashboards/D16-system.md, docs/07-security-notes.md, docs/roadmap/phase-8-mcp.md]
doc_sync_status: done
found_in: docs/02-v1-architecture.md §7/§7.2; docs/ui/dashboards/D17-mcp-console.md; docs/ui/dashboards/D16-system.md
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
---

# P8-B004 · MCP token lifecycle is undefined: no create command, scopes, expiry or storage rule

## Goal / expected outcome

The docs agree and are specific about this point, so the P8 tasks that depend on it can be built and tested without guessing. Proposed resolution: add `mcp.token.create` (C1 for read-only scopes, C3 for trade/strategies/risk scopes) and `/mcp/tokens`; scopes = the six tool groups; expiry default 30 days, max 90; SHA-256 hash at rest; revocation < 1 s; client token in OS keychain or sops file. `mt_mcp` forwards the mt_api-issued token unchanged and holds none of its own (audience = mt_api).

## Context & references

- Spec: [02 §7](../../../docs/02-v1-architecture.md#7-api-contract-mt_api) · [D17](../../../docs/ui/dashboards/D17-mcp-console.md) · [D16](../../../docs/ui/dashboards/D16-system.md) · research [MCP security](../../../docs/research/observability-storage-dataquality.md#mcp-security)
- Implementing tasks: P8-T002, P8-T020

## Requirements

- **Steps to reproduce:** Search the docs for how an MCP token is issued. 02 §7 says "scoped tokens for Telegram and MCP"; 02 §7.2 lists only `mcp.token.revoke`; D17 shows "token expiry"; the research note says "no token passthrough".
- **Expected:** A defined lifecycle: create command and level, scopes, expiry, hashing at rest, revocation latency, where the client stores it, and how "no token passthrough" applies to a thin adapter.
- **Actual:** Only revoke exists; scopes, expiry and storage are unspecified.
- **Impact:** R8.02 can't be verified ("tokens revocable" yes, "scoped" undefined); risk of over-privileged long-lived tokens (S2)
- **Suggested fix:** add `mcp.token.create` (C1 for read-only scopes, C3 for trade/strategies/risk scopes) and `/mcp/tokens`; scopes = the six tool groups; expiry default 30 days, max 90; SHA-256 hash at rest; revocation < 1 s; client token in OS keychain or sops file. `mt_mcp` forwards the mt_api-issued token unchanged and holds none of its own (audience = mt_api).

## ToDo

- [x] Decision recorded: 17 §A (P8-B004): opaque 256-bit tokens, shown once, HMAC-SHA-256 with a server pepper, scoped, instantly revocable, last use + client identity, expiry 1d/7d/30d/1y/custom/indefinite (indefinite = warning + C3 + monthly reminder), OAuth 2.1 (PKCE, resource indicators), Streamable HTTP + stdio + optional legacy HTTP+SSE, resource subscriptions
- [x] Docs carry it: 16 §2.12 (expiry, scopes, token creation C1/C3); 02 §7.1 `/mcp/tokens`, §7.2 MCP row (`mcp.token.create`/`revoke`), §7.4 Tokens/Transport; 03 M20; 07 §2 (pepper in sops) and §6; D17 Tokens widget + actions; D16 Sessions
- [x] Implementation owned by P8-T002 (tokens), P8-T003 (transports), P8-T031 (OAuth), P8-T032 (subscriptions, legacy SSE), P8-T020 + P8-T035 (tests)
- [x] Resolution noted in the Progress log

## Verification

### Tests
- Regression: the implementing task's test (named in Context) pins the documented behaviour.

### Scenarios
- Given the docs are fixed, when a developer reads only the linked sections, then they implement the same behaviour as the P8 task describes.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Docs updated and mutually consistent (checked 2026-10-22: 16 §2.12 (expiry, scopes, token creation C1/C3); 02 §7.1 `/mcp/tokens`, §7.2 MCP row (`mcp.token.create`/`revoke`), §7.4 Tokens/Transport; 03 M20; 07 §2 (pepper in sops) and §6; D17 Tokens widget + actions; D16 Sessions)
- [x] Implementing work owned and its test named: P8-T002 (tokens), P8-T003 (transports), P8-T031 (OAuth), P8-T032 (subscriptions, legacy SSE), P8-T020 + P8-T035 (tests)
- [x] Root cause noted: only `mcp.token.revoke` existed; the lifecycle was never specified

## Exceptions & edge cases

- If the user rejects the proposal, record the alternative here and update the implementing task before it starts.

## Cardinal rules (do NOT)

- Do NOT close without the docs actually agreeing.
- Do NOT edit WORM records to "fix" data; append a correction instead.
- Do NOT expose withdrawals, API-key management or wallet mandate signing through MCP, in any form (R8.06).

## Doc sync on completion

- `docs/02-v1-architecture.md`: as described in the suggested fix.
- `docs/ui/dashboards/D17-mcp-console.md`: as described in the suggested fix.
- `docs/ui/dashboards/D16-system.md`: as described in the suggested fix.
- `docs/07-security-notes.md`: as described in the suggested fix.
- `docs/roadmap/phase-8-mcp.md`: note the clarified behaviour if it changes a requirement's wording.

## Branch & PR

- Branch: `p8/P8-B004-mcp-token-lifecycle`
- PR title: `P8-B004: fix mCP token lifecycle is undefined: no create command, scopes, expiry or storage rule`
- PR checklist: docs consistent · implementing test referenced · `./kanban done P8-B004` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by 17 §A (P8-B004); docs checked: 16 §2.12 (expiry, scopes, token creation C1/C3); 02 §7.1 `/mcp/tokens`, §7.2 MCP row (`mcp.token.create`/`revoke`), §7.4 Tokens/Transport; 03 M20; 07 §2 (pepper in sops) and §6; D17 Tokens widget + actions; D16 Sessions; implementation owned by P8-T002 (tokens), P8-T003 (transports), P8-T031 (OAuth), P8-T032 (subscriptions, legacy SSE), P8-T020 + P8-T035 (tests); root cause: only `mcp.token.revoke` existed; the lifecycle was never specified
- 2026-10-22 02:26 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 §A (P8-B004); docs updated: 16 §2.12 (expiry, scopes, token creation C1/C3); 02 §7.1 `/mcp/tokens`, §7.2 MCP row (`mcp.token.create`/`revoke`), §7.4 Tokens/Transport; 03 M20; 07 §2 (pepper in sops) and §6; D17 Tokens widget + actions; D16 Sessions; implementation owned by P8-T002 (tokens), P8-T003 (transports), P8-T031 (OAuth), P8-T032 (subscriptions, legacy SSE), P8-T020 + P8-T035 (tests)
- 2026-10-22 02:26 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:26 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
