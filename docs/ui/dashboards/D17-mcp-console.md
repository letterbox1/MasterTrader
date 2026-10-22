# D17 · MCP Console

| | |
|---|---|
| **Route** | `/mcp` |
| **Modules** | M20 MCP control plane (a thin adapter over `mt_api`) |
| **Phase** | 8 (optional, built last; hidden from nav until enabled) |
| **Mock-up reference** | `claude-mcp-sovereign-autonomous-node-control.png` (fix: current Claude model naming; execution tools default to approval-required; no "autonomous" order tools) |

## Purpose

Supervise conversational control of the system from Claude (Desktop/Code) or another MCP client:
- which tools are exposed;
- what was asked and done;
- what's waiting for approval.

The conversation itself happens in the MCP client. This page is the **control and audit surface**.

## Layout by tier

| Tier | Layout |
|---|---|
| ≥ xl | Tool registry (12) + session activity (12); pending MCP approvals pinned top |
| ≤ ph | Pending approvals → sessions → tools |

## Widgets

| Widget | Shows | Source |
|---|---|---|
| Connection | MCP server status, transport (Streamable HTTP on Tailscale/TLS; stdio locally; optional legacy HTTP+SSE), connected clients | `/system/services?kind=mcp` |
| **Tokens** | Per token: name, scopes (`read`, `analyse`, `trade` (creates approval cards only), `strategy`, `risk_tighten`, `curation`), created, **expiry**, last used + client identity, rate limits. Tokens are opaque, shown **once** at creation, stored hashed. **Expiry is your choice per token: 1 day · 7 days · 30 days · 1 year · custom · indefinite.** Indefinite shows a red exposure/security warning, needs C3 and sends a monthly reminder ([16 §2.12](../../16-configuration-and-safety-model.md#212-mcp-phase-8)) | `/mcp/tokens` |
| Tool registry | Tools grouped as Read & analyse / Talk to agents / Trade & adjust / Strategies / Risk / Curation. Per tool: enabled, confirmation level applied (orders **always** create an approval card), rate limit (defaults 60 reads/min, 10 writes/min per token; response cap 256 KB; configurable), calls/day. **Never-exposed list** (shown greyed with a lock, [16 §2.12](../../16-configuration-and-safety-model.md#212-mcp-phase-8)): withdrawals, `wallet.sweep`, `treasury.*` moves, `airdrop.claim.execute`, mandates, key/token management, `approval.*`, `mcp.*`, restore/delete, audit writes. Loosening risk is never a tool; it's C3. | `/mcp/tools` |
| Pending approvals | MCP-originated orders/changes awaiting **your** approval on this page or Telegram (`ApprovalCard` with source "MCP" + conversation excerpt; TTL default 5 min, expiry = reject). MCP can never approve anything itself | `/approvals?status=pending&source=mcp`, `/risk/changes?status=pending&source=mcp` |
| Session activity | Per session: time, client, every tool call incl. reads (args redacted), results, linked audit entries, token used | `/mcp/sessions`, `/audit/log?source=mcp` (from the WORM `audit.mcp_call` table) |

## Actions

| Control | Command | Level |
|---|---|---|
| Enable/disable a tool | `mcp.tool.set` | Enabling a trade/risk tool = C3; disabling = C1. Never-exposed tools can't be enabled |
| Set MCP policy (scopes, rate limits, venues) | `mcp.policy.set` | Tighten C1; loosen C3. There is **no** "skip approval" or auto-execute option: MCP orders always need your approval card |
| Create a token (scopes, expiry) | `mcp.token.create` | C1 for read-only scopes; C3 for `trade`/`strategy`/`risk_tighten` scopes and for any indefinite expiry |
| Revoke client token | `mcp.token.revoke` | C1 (immediate) |
| Approve / reject | `approval.approve` / `approval.reject` | C2 / C1 |

## Acceptance criteria

1. **Confirmation mapping for `source = mcp`:** C0 reads run immediately; C1 actions run per the token's scope; C2 (orders) always create your approval card (TTL 5 min, expiry = reject); C3 needs Telegram approve + TOTP + cool-down as usual. There's no bypass.
2. **Never-exposed tools:** the never-exposed tools can't be enabled.
3. **Token expiry:** creating a token offers every expiry option; choosing indefinite shows the red warning and routes through C3.

## Backend contract

- **Queries:** `/mcp/tools`, `/mcp/tokens`, `/mcp/sessions`, `/approvals?source=mcp`, `/audit/log?source=mcp`, `/orders?source=mcp`, `/risk/changes?source=mcp`, `/system/services?kind=mcp`.
- **WebSocket topics:** `orders`, `risk.event`, `system`.
- **Commands:** `mcp.tool.set`, `mcp.policy.set`, `mcp.token.create`, `mcp.token.revoke`, `approval.*` _(added)_. All are web/Telegram only; none is ever exposed to MCP.
