# Phase 8 · MCP Control Plane (last, optional)

| | |
|---|---|
| **Goal** | Talk to and control MasterTrader from Claude (or another MCP client): read and analyse, ask the agents, **trade and adjust positions**, manage strategies, risk and curation, with every action going through `mt_api`, the risk manager and the audit log. |
| **Duration** | 1–2 weeks (mostly wiring, because the UI and Telegram already use `mt_api`) |
| **Depends on** | P2 (commands, risk), P6 (agents, memory); the platform in daily use. **Hard-gated** ([17 §E](../17-decisions-register.md#e-ratification-2026-10-22)): the phase opens only after its prerequisite phases exit and the T8.01 decision |
| **Unlocks** | — |
| **Modules** | M20 `mt_mcp` |
| **Containers** | `mcp` |
| **Dashboards** | [D17](../ui/dashboards/D17-mcp-console.md) MCP Console |
| **Primary docs** | [03 M20](../03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) · [02 §7.4](../02-v1-architecture.md#74-telegram--mcp) · [07 §6](../07-security-notes.md#6-application-controls) |

## 1. Scope

**In:** the MCP server over `mt_api` (stdio locally, or Streamable HTTP via the `mcp` container behind Caddy, Tailscale only, with token auth); tools for read & analyse, agents, trade & adjust, strategies, risk, curation; safeguards; D17.

**Out:** everything on the never-exposed list ([16 §2.12](../16-configuration-and-safety-model.md#212-mcp-phase-8)): withdrawals, `wallet.sweep`, `treasury.*` moves, `airdrop.claim.execute`, mandates, key/token management, `approval.*`, `mcp.*`, restore/delete, audit writes.

## 2. Entry criteria

- **Decision gate (T8.01):** you've used the web UI and Telegram daily for ≥ 4 weeks and still want MCP. If not, skip this phase.

## 3. Requirements

| ID | Requirement | Source | Verified by |
|---|---|---|---|
| R8.01 | Thin adapter over `mt_api` (official `mcp` SDK or FastMCP); no new business logic | [03 M20](../03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) | Code review |
| R8.02 | Transport stdio locally, or Streamable HTTP via the `mcp` container on the internal network behind Caddy, Tailscale only; scoped token auth; tokens revocable (details in R8.08) | [03 M20](../03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted), [02 §7](../02-v1-architecture.md#7-api-contract-mt_api) | Auth tests |
| R8.03 | Tool groups: read & analyse; talk to agents (M8/M9/M10, incl. `anomaly.explain`); trade & adjust (place/modify/cancel, adjust/close, stops/targets, scale, flatten); strategies; risk (view, tighten, loosen out-of-band, kill); curation; queries include `/bots`, `/approvals` and `source=` filters | [03 M20](../03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) | Tool tests |
| R8.04 | **Every MCP order goes through M11**; MCP orders **always** need your approval card (Telegram/web, TTL 5 min, expiry = reject; no skip-approval option); C0 reads, C1 per token scope, C3 via Telegram + TOTP as usual; MCP can never approve | [03 M20](../03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted), [SPEC NN2](../../SPEC.md#non-negotiable-requirements) | Bypass tests |
| R8.05 | Loosening risk is never an MCP scope: it's C3 (Telegram + TOTP), out of band; MCP may tighten (L0 ceilings included) but never loosen | [07 §6](../07-security-notes.md#6-application-controls) | C3 tests |
| R8.06 | **Never exposed:** withdrawals, `wallet.sweep`, `treasury.*` moves, `airdrop.claim.execute`, mandates, key/token management, `approval.*`, `mcp.*`, restore/delete, audit writes | [03 M20](../03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted), [16 §2.12](../16-configuration-and-safety-model.md#212-mcp-phase-8), [17 §D](../17-decisions-register.md#d-other-decisions) | Tool list audit |
| R8.07 | Every MCP call, reads included, is logged to `audit.mcp_call` (WORM); commands also land in `audit.command` with source `mcp`; D17 shows sessions (`/mcp/sessions`), calls, approvals, tool/policy settings and tokens (`/mcp/tokens`, revoke) | [D17](../ui/dashboards/D17-mcp-console.md) | Audit check |
| R8.08 | **Transport & tokens:** Streamable HTTP (JSON-RPC 2.0, SSE streaming, resumable) on Tailscale/TLS + stdio (newline-delimited JSON) locally, optional legacy HTTP+SSE endpoint; server notifications via resource subscriptions; tokens opaque 256-bit, shown once, stored hashed (HMAC-SHA-256 with a server pepper), scoped, revocable instantly, last-used + client identity recorded, expiry 1d/7d/30d/1y/custom/indefinite (indefinite = warning + C3 + monthly reminder), OAuth 2.1 (PKCE, resource indicators) where the client supports it; MCP can never approve | [16 §2.12](../16-configuration-and-safety-model.md#212-mcp-phase-8), [17 §A](../17-decisions-register.md#a-s2-items-all-resolved) | Auth + transport tests |
| R8.09 | **Response guard:** MCP responses pass the provenance filter like any model input: no Telegram text, no `model_input_ok = false` rows, PII (TFN, addresses, statements) redacted, untrusted text wrapped and marked | [03 M20](../03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted), [12 §5](../12-policy-and-compliance.md#5-data-provenance-tagging-one-mechanism-for-all-data-terms), [17 §A](../17-decisions-register.md#a-s2-items-all-resolved) | Guard tests |
| R8.10 | **Limits:** default 60 reads/min and 10 writes/min per token; response cap 256 KB per tool result; configurable | [16 §2.12](../16-configuration-and-safety-model.md#212-mcp-phase-8) | Limit tests |

## 4. ToDo sets

### A. Your actions (`USER`)
- [ ] **T8.01** `USER` **Decide whether to build MCP** (decision gate above).
- [ ] **T8.02** `USER` Configure your MCP client (Claude Desktop/Code) with the server and a scoped token. → R8.02
- [ ] **T8.03** `USER` Choose MCP token scopes and expiry per client (1d/7d/30d/1y/custom/indefinite with warning); MCP orders always need your approval. → R8.04, R8.08

### B. Build (`BUILD`, code)
- [ ] **T8.20** `BUILD` `mt_mcp` server, tool schemas generated from `mt_api` OpenAPI (incl. `anomaly.explain`, `/bots`, `/approvals`, `source=` filters), token auth. → R8.01–R8.03
- [ ] **T8.21** `BUILD` MCP policy layer: confirmation mapping (C0 reads, C1 by scope, every order → approval card with TTL 5 min, C3 out of band), never-exposed filter (16 §2.12), rate limits and response cap. → R8.04–R8.06, R8.10
- [ ] **T8.22** `BUILD` D17 MCP Console (sessions, calls, approvals, tokens). → R8.07
- [ ] **T8.23** `BUILD` Response guard in `mt_api` for `source = mcp`: provenance filter, PII redaction, secret scrub, untrusted-text wrapping. → R8.09
- [ ] **T8.24** `BUILD` Token lifecycle and transports: `mcp.token.create`/revoke (HMAC-SHA-256 + pepper, shown once, expiry options, monthly reminder for indefinite), OAuth 2.1 (PKCE, resource indicators), Streamable HTTP + stdio + optional legacy HTTP+SSE, resource subscriptions (fills, approvals, alerts); `audit.mcp_call` logging. → R8.08, R8.07

### C. Ops & config (`OPS`)
- [ ] **T8.40** `OPS` `mcp` container on the internal network behind Caddy (`/mcp`), Tailscale only; token pepper in secrets. → R8.02

### D. Verify & test (`VERIFY`)
- [ ] **T8.60** `VERIFY` Bypass tests: an MCP order can't skip M11 or its approval card (expiry = reject); MCP can't call `approval.*` or `mcp.*`; loosening needs Telegram + TOTP out of band. → R8.04, R8.05
- [ ] **T8.61** `VERIFY` Tool-list audit: no tool from the 16 §2.12 never-exposed list exists. → R8.06
- [ ] **T8.62** `VERIFY` Prompt-injection test: an instruction hidden in a news item read via MCP can't place an order without your Telegram approval. → R8.04
- [ ] **T8.63** `VERIFY` Response-guard test: a Telegram-sourced row, a `model_input_ok = false` row and a TFN/address never reach the MCP client unredacted. → R8.09
- [ ] **T8.64** `VERIFY` Auth + transport tests: token shown once and stored hashed, revocation instant, expiry enforced, indefinite needs C3; Streamable HTTP resume and stdio work; every call, reads included, lands in `audit.mcp_call`. → R8.08, R8.07
- [ ] **T8.65** `VERIFY` Limit tests: the 61st read or 11th write in a minute is throttled; a result over 256 KB is capped with a marker. → R8.10

### E. Run / soak (`RUN`)
- [ ] **T8.80** `RUN` Two weeks of use; review D17 audit for anything surprising.

## 5. Deliverables

`mt_mcp` · policy layer · D17 · tests.

## 6. Exit criteria (demo)

From Claude: "how are my strategies doing, tighten BTC max position to X, and close half my EURUSD" → the tighten applies instantly, the close waits for your Telegram approval, and both appear in D17, `audit.mcp_call` and `audit.command`.
