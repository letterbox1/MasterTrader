---
id: P8-B012
kind: gap
title: R8.07 says every call is audited in `audit.command`, but reads aren't commands
phase: 8
type: DOC
status: backlog
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R8.07]
roadmap_todos: [T8.22]
modules: [M17, M20]
dashboards: [D17]
branch: p8/P8-B012-mcp-read-calls-audit-home
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/03-build-spec.md, docs/15-bots-hitl-and-worm-audit.md, docs/roadmap/phase-8-mcp.md]
doc_sync_status: n/a
found_in: docs/roadmap/phase-8-mcp.md R8.07; docs/03-build-spec.md M17; docs/15-bots-hitl-and-worm-audit.md §2.1
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P8-B012 · R8.07 says every call is audited in `audit.command`, but reads aren't commands

## Goal / expected outcome

The docs agree and are specific about this point, so the P8 tasks that depend on it can be built and tested without guessing. Proposed resolution: add WORM table `audit.mcp_call` (all MCP calls, linked to `audit.command` for commands) to 02 §5.3, 03 M17 and the 15 §2.1 WORM scope; keep `audit.command` for commands.

## Context & references

- Spec: [03 M17](../../../docs/03-build-spec.md#m17-observability--audit--mt_obs) · [15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many) · [D17](../../../docs/ui/dashboards/D17-mcp-console.md) · roadmap [R8.07](../../../docs/roadmap/phase-8-mcp.md#3-requirements)
- Implementing tasks: P8-T007, P8-T025

## Requirements

- **Steps to reproduce:** R8.07: "Every call audited (`audit.command`, source = mcp)". 02 §7.2: only commands are written to `audit.command`. D17 Session activity needs every tool call including reads.
- **Expected:** A defined, WORM-protected home for MCP read calls and session data.
- **Actual:** Reads via MCP would leave no audit trail; D17's session view has no source table.
- **Impact:** R8.07 "every call" can't be met; reads by a possibly prompt-injected client go unrecorded (S3)
- **Suggested fix:** add WORM table `audit.mcp_call` (all MCP calls, linked to `audit.command` for commands) to 02 §5.3, 03 M17 and the 15 §2.1 WORM scope; keep `audit.command` for commands.

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
- `docs/15-bots-hitl-and-worm-audit.md`: as described in the suggested fix.
- `docs/roadmap/phase-8-mcp.md`: note the clarified behaviour if it changes a requirement's wording.

## Branch & PR

- Branch: `p8/P8-B012-mcp-read-calls-audit-home`
- PR title: `P8-B012: fix r8.07 says every call is audited in `audit.command`, but reads aren't commands`
- PR checklist: docs consistent · implementing test referenced · `./kanban done P8-B012` run

## Progress log

- 2026-10-21 00:00 · planner · opened
