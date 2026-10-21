---
id: P8-B009
kind: gap
title: 02 §7.1 lacks `/bots`, `/approvals`, `/mcp/tokens`, `/mcp/sessions` and the `source=` filters D17 uses
phase: 8
type: DOC
status: backlog
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R8.03, R8.07]
roadmap_todos: []
modules: [M20]
dashboards: [D17]
branch: p8/P8-B009-api-query-table-gaps
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/roadmap/phase-8-mcp.md]
doc_sync_status: n/a
found_in: docs/02-v1-architecture.md §7.1
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P8-B009 · 02 §7.1 lacks `/bots`, `/approvals`, `/mcp/tokens`, `/mcp/sessions` and the `source=` filters D17 uses

## Goal / expected outcome

The docs agree and are specific about this point, so the P8 tasks that depend on it can be built and tested without guessing. Proposed resolution: add the bots/approvals queries, `/mcp/tokens`, `/mcp/sessions`, and note the `source=` / `kind=` filters in 02 §7.1.

## Context & references

- Spec: [02 §7.1](../../../docs/02-v1-architecture.md#71-queries-rest-read) · [15 §1.5](../../../docs/15-bots-hitl-and-worm-audit.md#15-api-data-and-ui) · [D17](../../../docs/ui/dashboards/D17-mcp-console.md)
- Implementing tasks: P8-T007, P8-T008, P8-T016

## Requirements

- **Steps to reproduce:** Compare 02 §7.1 with 15 §1.5 (`/bots`, `/bots/{id}`, `/bots/{id}/approvals`, `/approvals?status=pending`) and D17's backend contract (`/orders?source=mcp`, `/risk/changes?source=mcp`, `/audit/log?source=mcp`, `/system/services?kind=mcp`).
- **Expected:** The query table lists every endpoint the UI/MCP use, including filter parameters.
- **Actual:** Missing from 02 §7.1; MCP tools are generated from the OpenAPI, so missing endpoints mean missing tools.
- **Impact:** Read tools for bots/approvals and the D17 widgets may be skipped or built ad hoc (S3)
- **Suggested fix:** add the bots/approvals queries, `/mcp/tokens`, `/mcp/sessions`, and note the `source=` / `kind=` filters in 02 §7.1.

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
- `docs/roadmap/phase-8-mcp.md`: note the clarified behaviour if it changes a requirement's wording.

## Branch & PR

- Branch: `p8/P8-B009-api-query-table-gaps`
- PR title: `P8-B009: fix 02 §7.1 lacks `/bots`, `/approvals`, `/mcp/tokens`, `/mcp/sessions` and the `source=` filters D17 uses`
- PR checklist: docs consistent · implementing test referenced · `./kanban done P8-B009` run

## Progress log

- 2026-10-21 00:00 · planner · opened
