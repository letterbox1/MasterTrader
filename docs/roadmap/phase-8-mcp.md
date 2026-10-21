# Phase 8 · MCP Control Plane (last, optional)

| | |
|---|---|
| **Goal** | Talk to and control MasterTrader from Claude (or another MCP client): read and analyse, ask the agents, **trade and adjust positions**, manage strategies, risk and curation, with every action going through `mt_api`, the risk manager and the audit log. |
| **Duration** | 1–2 weeks (mostly wiring, because the UI and Telegram already use `mt_api`) |
| **Depends on** | P2 (commands, risk), P6 (agents, memory); the platform in daily use |
| **Unlocks** | — |
| **Modules** | M20 `mt_mcp` |
| **Containers** | `mcp` |
| **Dashboards** | [D17](../ui/dashboards/D17-mcp-console.md) MCP Console |
| **Primary docs** | [03 M20](../03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) · [02 §7.4](../02-v1-architecture.md#74-telegram--mcp) · [07 §6](../07-security-notes.md#6-application-controls) |

## 1. Scope

**In:** the MCP server over `mt_api` (stdio or Streamable HTTP on localhost/Tailscale with token auth); tools for read & analyse, agents, trade & adjust, strategies, risk, curation; safeguards; D17.

**Out:** withdrawals, API-key management, wallet mandate signing (never exposed).

## 2. Entry criteria

- **Decision gate (T8.01):** you've used the web UI and Telegram daily for ≥ 4 weeks and still want MCP. If not, skip this phase.

## 3. Requirements

| ID | Requirement | Source | Verified by |
|---|---|---|---|
| R8.01 | Thin adapter over `mt_api` (official `mcp` SDK or FastMCP); no new business logic | [03 M20](../03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) | Code review |
| R8.02 | Transport stdio, or Streamable HTTP on localhost/Tailscale with scoped token auth; tokens revocable | [03 M20](../03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted), [02 §7](../02-v1-architecture.md#7-api-contract-mt_api) | Auth tests |
| R8.03 | Tool groups: read & analyse; talk to agents (M8/M9/M10); trade & adjust (place/modify/cancel, adjust/close, stops/targets, scale, flatten); strategies; risk (view, tighten, loosen out-of-band, kill); curation | [03 M20](../03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) | Tool tests |
| R8.04 | **Every MCP order goes through M11**; MCP orders **always** need your approval card (Telegram/web, TTL 5 min); MCP can never approve | [03 M20](../03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted), [SPEC NN2](../../SPEC.md#non-negotiable-requirements) | Bypass tests |
| R8.05 | Loosening risk = C3 (Telegram + TOTP); hard ceilings unwritable | [07 §6](../07-security-notes.md#6-application-controls) | C3 tests |
| R8.06 | **Never exposed:** withdrawals, key management, mandate signing | [03 M20](../03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) | Tool list audit |
| R8.07 | Every call audited (`audit.command`, source = mcp); D17 shows sessions, calls, approvals, tool/policy settings, token revoke | [D17](../ui/dashboards/D17-mcp-console.md) | Audit check |
| R8.08 | **Transport & tokens:** Streamable HTTP (JSON-RPC 2.0, SSE streaming, resumable) on Tailscale/TLS + stdio (newline-delimited JSON) locally, optional legacy HTTP+SSE endpoint; server notifications via resource subscriptions; tokens opaque 256-bit, hashed at rest, scoped, revocable, expiry 1d/7d/30d/1y/custom/indefinite (indefinite = warning + C3 + monthly reminder), OAuth 2.1 (PKCE, resource indicators) where the client supports it; MCP can never approve | [16 §2.12](../16-configuration-and-safety-model.md#212-mcp-phase-8), [17 §A](../17-decisions-register.md#a-s2-items-all-resolved) | Auth + transport tests |

## 4. ToDo sets

### A. Your actions (`USER`)
- [ ] **T8.01** `USER` **Decide whether to build MCP** (decision gate above).
- [ ] **T8.02** `USER` Configure your MCP client (Claude Desktop/Code) with the server and a scoped token. → R8.02
- [ ] **T8.03** `USER` Choose MCP token scopes and expiry per client (1d/7d/30d/1y/custom/indefinite with warning); MCP orders always need your approval. → R8.04, R8.08

### B. Build (`BUILD`, code)
- [ ] **T8.20** `BUILD` `mt_mcp` server, tool schemas generated from `mt_api` OpenAPI, token auth. → R8.01–R8.03
- [ ] **T8.21** `BUILD` MCP policy layer (approve-mode defaults, never-exposed filter). → R8.04–R8.06
- [ ] **T8.22** `BUILD` D17 MCP Console. → R8.07

### C. Ops & config (`OPS`)
- [ ] **T8.40** `OPS` `mcp` container bound to localhost/Tailscale; token in secrets. → R8.02

### D. Verify & test (`VERIFY`)
- [ ] **T8.60** `VERIFY` Bypass tests: an MCP order can't skip M11 or approve mode; loosening needs TOTP. → R8.04, R8.05
- [ ] **T8.61** `VERIFY` Tool-list audit: no withdrawal/key/mandate tool exists. → R8.06
- [ ] **T8.62** `VERIFY` Prompt-injection test: an instruction hidden in a news item read via MCP can't place an order without your Telegram approval. → R8.04

### E. Run / soak (`RUN`)
- [ ] **T8.80** `RUN` Two weeks of use; review D17 audit for anything surprising.

## 5. Deliverables

`mt_mcp` · policy layer · D17 · tests.

## 6. Exit criteria (demo)

From Claude: "how are my strategies doing, tighten BTC max position to X, and close half my EURUSD" → the tighten applies instantly, the close waits for your Telegram approval, and both appear in D17 and `audit.command`.
