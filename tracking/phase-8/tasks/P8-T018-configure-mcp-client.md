---
id: P8-T018
kind: task
title: Generate the token pepper and configure your MCP client with the server and a scoped token
phase: 8
type: USER
status: backlog
priority: high
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: [P8-T015, P8-T016, P8-T017]
requirements: [R8.02, R8.08]
roadmap_todos: [T8.02]
modules: [M20]
dashboards: [D17]
tools: [sops, claude-desktop]
mcp: []
env: []
services: [tailscale, telegram-bot]
branch: p8/P8-T018-configure-mcp-client
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

# P8-T018 · Generate the token pepper and configure your MCP client with the server and a scoped token

## Goal / expected outcome

The MCP token pepper exists in your sops file (never seen by anyone), and your Claude Desktop (or Claude Code) is connected to MasterTrader through `mt_mcp` with a token you created, labelled, scoped and given an expiry. The token is stored only in your OS keychain or the sops file (or obtained by OAuth 2.1 sign-in, if your client supports it). A first read call appears in D17.

## Context & references

- Roadmap: [R8.02, R8.08](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDo [T8.02](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- Decisions: [16 §2.12](../../../docs/16-configuration-and-safety-model.md#212-mcp-phase-8) (scopes, expiry options, creation levels) · [17 §A P8-B004](../../../docs/17-decisions-register.md#a-s2-items-all-resolved) · [07 §2](../../../docs/07-security-notes.md#2-secrets) (the MCP token pepper is a secret you add yourself)
- Guide: `docs/runbooks/mcp-client-setup.md` (P8-T017)
- UI: [D17 Tokens / Connection](../../../docs/ui/dashboards/D17-mcp-console.md)
- Unblocks: P8-T019, P8-T028, P8-T029, P8-T035 (live client check).

## Requirements

- Pepper: 32 random bytes generated on the host straight into the sops file key `mcp_token_pepper` (never printed, never pasted). Restart `mt-api` so it loads it.
- First token: scopes `read`, `analyse`, `curation` (C1). Write scopes come in P8-T019.
- Expiry: your choice per token from 1 day · 7 days · 30 days · 1 year · custom · indefinite. Indefinite shows a red warning, needs C3 (Telegram + TOTP + cool-down) and reminds you monthly; an expiring token is recommended.
- Where the token goes: laptop → OS keychain entry `mt-mcp` (macOS Keychain / Windows Credential Manager / libsecret); host-local client → the sops file key `mcp_client_token_<label>`. If your client supports MCP OAuth, sign in instead and no token is copied at all. **Never** chat (including Claude itself), email, git or `.env`.

## ToDo

- [ ] On the host, add the pepper with the command in the guide (e.g. `sops set` fed by `openssl rand -base64 32`, output never shown), then restart `mt-api`; D16 shows `mt-api` healthy.
- [ ] In D17 → Tokens → Create: label (e.g. `claude-desktop-laptop`), scopes `read` + `analyse` + `curation`, pick an expiry.
- [ ] Copy the shown-once token straight into the keychain (`security add-generic-password -s mt-mcp -a mt -w` on macOS, or the Windows/Linux equivalent in the guide) or into the sops file. Or, if your client supports it, use the OAuth sign-in from the guide instead.
- [ ] Add the MasterTrader server to your client config exactly as in the guide (stdio on the host, or Streamable HTTP over Tailscale).
- [ ] Restart the client; ask Claude: "list my MasterTrader tools" and "show my portfolio summary".
- [ ] Check D17: Connection shows your client; Session activity shows `get_portfolio_summary` with source mcp; Tokens shows last used + client identity.
- [ ] Write in the Progress log: date, client, transport, auth method (token/OAuth), scopes, expiry choice (no token or pepper value).

## Verification

### Tests
- n/a: user configuration; confirmed by the D17 check below.

### Scenarios
- Given the client is configured, when you ask for the portfolio summary, then D17 Session activity shows the call within a few seconds.
- Given you mistype the token, then the client shows 401 and D17 shows no session; fix it in the keychain.
- Given you chose indefinite expiry, then you completed the C3 on Telegram and D17 shows the red indefinite chip.

### Stress / failure injection
- n/a: one-off setup.

## Acceptance criteria

- [ ] Pepper in sops; `mt-api` healthy after restart
- [ ] Client connected; a read call visible in D17 with source mcp
- [ ] Token stored only in keychain/sops or obtained by OAuth (stated in the Progress log, no value)

## Exceptions & edge cases

- Not on Tailscale: HTTP transport won't connect; use the host or connect Tailscale first.
- Token shown once was lost: revoke it in D17 and create a new one.
- You regenerate the pepper later: every token stops working; create new ones.

## Cardinal rules (do NOT)

- Do NOT paste the token or the pepper into Claude or any chat, issue or commit.
- Do NOT give this first token write scopes; that's P8-T019.
- Do NOT commit secrets or paste them into chats/issues (including the Claude conversation); secrets live in the sops/age file (07 §2).
- Do NOT use live money before the P7 gates; keys stay trade-only, IP-locked, withdrawals disabled.

## Doc sync on completion

- `docs/roadmap/phase-8-mcp.md`: tick T8.02.

## Branch & PR

- Branch: `p8/P8-T018-configure-mcp-client`
- PR title: `P8-T018: Generate the token pepper and configure your MCP client with the server and a scoped token`
- PR checklist: no PR (user setup) · Progress log entry written · `./kanban done P8-T018` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (pepper generation into sops added (keys last), 16 §2.12 scope names and expiry options incl. indefinite = warning + C3 + monthly reminder, OAuth 2.1 option; added R8.08; tools/env/services)
