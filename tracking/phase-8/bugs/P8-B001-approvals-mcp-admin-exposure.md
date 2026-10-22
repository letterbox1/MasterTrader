---
id: P8-B001
kind: gap
title: Approvals and MCP self-admin commands are not classified for MCP
phase: 8
type: DOC
status: done
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
doc_sync_status: done
found_in: docs/02-v1-architecture.md §7.2/§7.4; docs/03-build-spec.md M20
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
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

- [x] Decision recorded: 17 §A (P8-B001): MCP can never approve; `approval.*` and `mcp.*` are never exposed; approvals only from you on Telegram/web
- [x] Docs carry it: 16 §2.12 never-exposed row; 02 §7.2 Approvals row (`web`/`telegram` only) and §7.4; 03 M20 safeguards; 07 §6; 15 §1.3; D17 backend contract
- [x] Implementation owned by P8-T004 (never set incl. `approval.*`, `mcp.*`), P8-T021 (bypass cases 4–5), P8-T023 (tool-list audit)
- [x] Resolution noted in the Progress log

## Verification

### Tests
- Regression: the implementing task's test (named in Context) pins the documented behaviour.

### Scenarios
- Given the docs are fixed, when a developer reads only the linked sections, then they implement the same behaviour as the P8 task describes.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Docs updated and mutually consistent (checked 2026-10-22: 16 §2.12 never-exposed row; 02 §7.2 Approvals row (`web`/`telegram` only) and §7.4; 03 M20 safeguards; 07 §6; 15 §1.3; D17 backend contract)
- [x] Implementing work owned and its test named: P8-T004 (never set incl. `approval.*`, `mcp.*`), P8-T021 (bypass cases 4–5), P8-T023 (tool-list audit)
- [x] Root cause noted: the never-exposed list originally named only withdrawals, keys and mandates

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
- 2026-10-22 00:00 · aligner · resolved by 17 §A (P8-B001); docs checked: 16 §2.12 never-exposed row; 02 §7.2 Approvals row (`web`/`telegram` only) and §7.4; 03 M20 safeguards; 07 §6; 15 §1.3; D17 backend contract; implementation owned by P8-T004 (never set incl. `approval.*`, `mcp.*`), P8-T021 (bypass cases 4–5), P8-T023 (tool-list audit); root cause: the never-exposed list originally named only withdrawals, keys and mandates
- 2026-10-22 02:26 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 §A (P8-B001); docs updated: 16 §2.12 never-exposed row; 02 §7.2 Approvals row (`web`/`telegram` only) and §7.4; 03 M20 safeguards; 07 §6; 15 §1.3; D17 backend contract; implementation owned by P8-T004 (never set incl. `approval.*`, `mcp.*`), P8-T021 (bypass cases 4–5), P8-T023 (tool-list audit)
- 2026-10-22 02:26 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:26 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
