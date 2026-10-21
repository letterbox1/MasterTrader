---
id: P8-T017
kind: task
title: MCP incident runbook and client setup guide
phase: 8
type: DOC
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P8-T015, P8-T016]
requirements: [R8.02, R8.06]
roadmap_todos: [T8.02]
modules: [M20]
dashboards: [D17]
branch: p8/P8-T017-mcp-runbook-client-guide
pr: ""
doc_sync: [docs/runbooks/mcp-incident.md, docs/runbooks/mcp-client-setup.md, docs/07-security-notes.md, docs/roadmap/phase-8-mcp.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P8-T017 · MCP incident runbook and client setup guide

## Goal / expected outcome

Two short docs exist and have been dry-run: `docs/runbooks/mcp-incident.md` (token leaked, unexpected MCP action, suspected prompt injection) and `docs/runbooks/mcp-client-setup.md` (Claude Desktop/Code over stdio or Streamable HTTP, with the token in the keychain or sops file).

## Context & references

- Roadmap: [R8.02, R8.06](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDo [T8.02](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets) (you configure the client using this guide)
- Security: [07 §6](../../../docs/07-security-notes.md#6-application-controls) · [07 §9 runbooks](../../../docs/07-security-notes.md#9-monitoring--incident-response)
- UI: [D17](../../../docs/ui/dashboards/D17-mcp-console.md) (revoke token, disable tools) · [D16](../../../docs/ui/dashboards/D16-system.md)
- Related: P8-T018 (you follow the setup guide).

## Requirements

- Incident runbook steps: (1) if an unwanted trade happened, `/kill` in Telegram first; (2) revoke the token in D17 (or D16 → Sessions); (3) disable trade/risk tools (C1); (4) review `audit.mcp_call` for the session; (5) reject pending MCP approvals; (6) rotate tokens; (7) file a P8 bug with the session id. Include "mt-api down" (Telegram `/kill` via NATS still works).
- Client guide: Claude Desktop `claude_desktop_config.json` stdio entry (`uv run --directory <repo> mt-mcp --stdio`, env `MT_API_URL=https://<host>.<tailnet>.ts.net/api/v1`, token via `MT_MCP_TOKEN_CMD` reading the OS keychain); Claude Code (`claude mcp add` with stdio or HTTP transport); Streamable HTTP URL `https://<host>.<tailnet>.ts.net/mcp` with a bearer header from the keychain; how to verify (list tools, D17 Connection).
- Explicit warnings: never paste the token into the conversation; MCP conversations can be prompt-injected, so approve cards on the card's facts, not on Claude's summary.

## ToDo

- [ ] Write both docs.
- [ ] Dry-run the incident runbook on paper (revoke + disable + kill) and record timings.
- [ ] Dry-run the client guide on a clean laptop profile.
- [ ] Update docs.

## Verification

### Tests
- Doc lint (markdownlint, link check) in CI.

### Scenarios
- Given a leaked token drill, when you follow the runbook, then the token is dead in < 1 min and trade tools are disabled; timings recorded.

### Stress / failure injection
- n/a: documentation; the drill above is the check.

## Acceptance criteria

- [ ] Both docs merged, links valid
- [ ] Incident drill done with timings in the Progress log

## Exceptions & edge cases

- Client config paths differ per OS: list macOS, Windows and Linux paths.

## Cardinal rules (do NOT)

- Do NOT include real tokens, hostnames or tailnet names in the docs; use placeholders.
- Do NOT commit secrets or paste them into chats/issues (including into the Claude conversation); secrets live in the sops/age file (07 §2).

## Doc sync on completion

- `docs/runbooks/mcp-incident.md`, `docs/runbooks/mcp-client-setup.md`: new.
- `docs/07-security-notes.md` §9: add the MCP runbook to the list.
- `docs/roadmap/phase-8-mcp.md`: note on T8.02 (guide available).

## Branch & PR

- Branch: `p8/P8-T017-mcp-runbook-client-guide`
- PR title: `P8-T017: MCP incident runbook and client setup guide`
- PR checklist: docs added · link check green · drill timings logged · `./kanban done P8-T017` run

## Progress log

- 2026-10-21 00:00 · planner · created
