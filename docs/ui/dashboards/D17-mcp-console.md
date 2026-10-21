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
| Connection | MCP server status, transport (stdio / Streamable HTTP on Tailscale), connected clients, token expiry | `/system/services?kind=mcp` |
| Tool registry | Tools grouped as Read & analyse / Talk to agents / Trade & adjust / Strategies / Risk / Curation. Per tool: enabled, confirmation level applied (orders default **approval-required**), rate limit, calls/day. **Never-exposed list:** withdrawals, keys, mandates (shown greyed with a lock). | `/mcp/tools` |
| Pending approvals | MCP-originated orders/changes awaiting approval (`ApprovalCard` with source "MCP" + conversation excerpt) | `/orders?status=pending_approval&source=mcp`, `/risk/changes?status=pending&source=mcp` |
| Session activity | Per session: time, client, tool calls (args redacted), results, linked audit entries, tokens | `/audit/log?source=mcp` |

## Actions

| Control | Command | Level |
|---|---|---|
| Enable/disable a tool | `mcp.tool.set` | Enabling a trade/risk tool = C3; disabling = C1 |
| Set the order policy for MCP (always approve / auto under size X) | `mcp.policy.set` | Loosening = C3 |
| Revoke client token | `mcp.token.revoke` | C1 |
| Approve / reject | `approval.approve` / `approval.reject` | C2 / C1 |

## Acceptance criteria

1. **Same rules as the UI:** MCP actions follow the same confirmation levels as the web; there's no bypass.
2. **Never-exposed tools:** the never-exposed tools can't be enabled.

## Backend contract

- **Queries:** `/mcp/tools`, `/audit/log?source=mcp`, `/orders?source=mcp`, `/risk/changes?source=mcp`, `/system/services?kind=mcp`.
- **WebSocket topics:** `orders`, `risk.event`, `system`.
- **Commands:** `mcp.tool.set`, `mcp.policy.set`, `mcp.token.revoke`, `approval.*` _(added)_.
