---
id: P8-T018
kind: task
title: Configure your MCP client with the server and a scoped token
phase: 8
type: USER
status: backlog
priority: high
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: [P8-T015, P8-T016, P8-T017]
requirements: [R8.02]
roadmap_todos: [T8.02]
modules: [M20]
dashboards: [D17]
branch: p8/P8-T018-configure-mcp-client
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

# P8-T018 · Configure your MCP client with the server and a scoped token

## Goal / expected outcome

Your Claude Desktop (or Claude Code) is connected to MasterTrader through `mt_mcp` with a token you created, labelled and scoped. The token is stored only in your OS keychain or the sops file. A first read call appears in D17.

## Context & references

- Roadmap: [R8.02](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDo [T8.02](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- Guide: `docs/runbooks/mcp-client-setup.md` (P8-T017)
- UI: [D17 Connection / tokens](../../../docs/ui/dashboards/D17-mcp-console.md)
- Unblocks: P8-T019, P8-T024 (manual run), P8-T026, P8-T028, P8-T029.

## Requirements

- Start with scopes `read`, `agents`, `curation`; add `trade`, `strategies`, `risk` only if your decision in P8-T001 was `go-full` (this is C3: Telegram approve + TOTP, then a 15-min cool-down before the token is shown).
- Expiry: 30 days (you'll get an expiry chip in D17; create a new one before it lapses).
- Where the token goes: laptop → OS keychain entry `mt-mcp` (macOS Keychain / Windows Credential Manager / libsecret); host-local client → `secrets/mcp.sops.yaml` key `mcp_client_token_<label>` via `sops`. **Never** chat (including Claude itself), email, git or `.env`.

## ToDo

- [ ] In D17 → Tokens → Create: label e.g. `claude-desktop-laptop`, scopes as above, expiry 30 days; complete the Telegram + TOTP step if you asked for write scopes.
- [ ] Copy the shown-once token straight into the keychain (`security add-generic-password -s mt-mcp -a mt -w` on macOS, or the Windows/Linux equivalent in the guide) or into the sops file with `sops secrets/mcp.sops.yaml`.
- [ ] Add the MasterTrader server to your client config exactly as in the guide (stdio or Streamable HTTP over Tailscale).
- [ ] Restart the client; ask Claude: "list my MasterTrader tools" and "show my portfolio summary".
- [ ] Check D17: Connection shows your client; Session activity shows `get_portfolio_summary` with source mcp.
- [ ] Write in the Progress log: date, client, transport, scopes, expiry (no token value).

## Verification

### Tests
- n/a: user configuration; confirmed by the D17 check below.

### Scenarios
- Given the client is configured, when you ask for the portfolio summary, then D17 Session activity shows the call within a few seconds.
- Given you mistype the token, then the client shows 401 and D17 shows no session; fix it in the keychain.

### Stress / failure injection
- n/a: one-off setup.

## Acceptance criteria

- [ ] Client connected; a read call visible in D17 with source mcp
- [ ] Token stored only in keychain/sops (stated in the Progress log, no value)

## Exceptions & edge cases

- Not on Tailscale: HTTP transport won't connect; use the host or connect Tailscale first.
- Token shown-once was lost: revoke it in D17 and create a new one.

## Cardinal rules (do NOT)

- Do NOT paste the token into Claude or any chat, issue or commit.
- Do NOT give the token write scopes before you have decided `go-full`.
- Do NOT commit secrets or paste them into chats/issues (including into the Claude conversation); secrets live in the sops/age file (07 §2).
- Do NOT use live money before the P7 gates; keys stay trade-only, IP-locked, withdrawals disabled.

## Doc sync on completion

- `docs/roadmap/phase-8-mcp.md`: tick T8.02.

## Branch & PR

- Branch: `p8/P8-T018-configure-mcp-client`
- PR title: `P8-T018: Configure your MCP client with the server and a scoped token`
- PR checklist: no PR (user setup) · Progress log entry written · `./kanban done P8-T018` run

## Progress log

- 2026-10-21 00:00 · planner · created
