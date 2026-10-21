---
id: P8-B001
kind: gap
title: Approvals and MCP self-admin commands are not classified for MCP
phase: 8
type: DOC
status: backlog
priority: high
size: S
severity: S2
owner: agent
claimed_by: ""
depends_on: []
requirements: [R8.06, R8.04]
roadmap_todos: [T8.21]
modules: [M20]
dashboards: [D17]
branch: p8/P8-B001-approvals-mcp-admin-exposure
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/03-build-spec.md, docs/07-security-notes.md, docs/roadmap/phase-8-mcp.md]
doc_sync_status: n/a
found_in: docs/02-v1-architecture.md §7.2/§7.4; docs/03-build-spec.md M20
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P8-B001 · Approvals and MCP self-admin commands are not classified for MCP

## Goal / expected outcome

The docs agree and are specific about this point, so the P8 tasks that depend on it can be built and tested without guessing. Proposed resolution: add `approval.approve`, `approval.approve_partial`, `mcp.tool.set`, `mcp.policy.set`, `mcp.token.*` and auth/session endpoints to the never-exposed list in 02 §7.4, 03 M20 and 07 §6 (`approval.reject` may stay exposed; it only tightens).

## Context & references

- Spec: [02 §7.4](../../../docs/02-v1-architecture.md#74-telegram--mcp) · [03 M20](../../../docs/03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) · [07 §6](../../../docs/07-security-notes.md#6-application-controls) · [D17 Actions](../../../docs/ui/dashboards/D17-mcp-console.md)
- Implementing tasks: P8-T004 (registry), P8-T021 (bypass test case 4)

## Requirements

- **Steps to reproduce:** Read 02 §7.4 ("MCP exposes the queries plus a subset of commands") and the 03 M20 never-exposed list; look for `approval.approve`, `approval.approve_partial`, `mcp.tool.set`, `mcp.policy.set`, `mcp.token.*`.
- **Expected:** An explicit statement that MCP can never approve (its own or any) pending approval and can never change MCP tools, policy or tokens.
- **Actual:** Only withdrawals, key management and mandate signing are named. A literal reading allows an MCP client to call `approval.approve` on its own order, or `mcp.policy.set` to remove approve mode.
- **Impact:** Approve mode and the prompt-injection defence (T8.62) would be void if MCP could approve or reconfigure itself (S2)
- **Suggested fix:** add `approval.approve`, `approval.approve_partial`, `mcp.tool.set`, `mcp.policy.set`, `mcp.token.*` and auth/session endpoints to the never-exposed list in 02 §7.4, 03 M20 and 07 §6 (`approval.reject` may stay exposed; it only tightens).

## ToDo

- [ ] Confirm the proposed resolution (with the user if it changes behaviour)
- [ ] Edit the listed docs so they agree with each other
- [ ] Write or point to the test in the implementing P8 task that pins the behaviour
- [ ] Note the resolution in the Progress log

## Verification

### Tests
- Regression: the implementing task's test (named in Context) pins the documented behaviour.

### Scenarios
- Given the docs are fixed, when a developer reads only the linked sections, then they implement the same behaviour as the P8 task describes.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [ ] Docs updated and mutually consistent
- [ ] Implementing task test exists and passes
- [ ] Resolution noted in the Progress log

## Exceptions & edge cases

- If the user rejects the proposal, record the alternative here and update the implementing task before it starts.

## Cardinal rules (do NOT)

- Do NOT close without the docs actually agreeing.
- Do NOT edit WORM records to "fix" data; append a correction instead.
- Do NOT expose withdrawals, API-key management or wallet mandate signing through MCP, in any form (R8.06).

## Doc sync on completion

- `docs/02-v1-architecture.md`: as described in the suggested fix.
- `docs/03-build-spec.md`: as described in the suggested fix.
- `docs/07-security-notes.md`: as described in the suggested fix.
- `docs/roadmap/phase-8-mcp.md`: note the clarified behaviour if it changes a requirement's wording.

## Branch & PR

- Branch: `p8/P8-B001-approvals-mcp-admin-exposure`
- PR title: `P8-B001: fix approvals and MCP self-admin commands are not classified for MCP`
- PR checklist: docs consistent · implementing test referenced · `./kanban done P8-B001` run

## Progress log

- 2026-10-21 00:00 · planner · opened
