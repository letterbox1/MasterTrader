---
id: P8-T025
kind: task
title: "Audit check: every MCP call audited (source = mcp) and visible in D17"
phase: 8
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P8-T007, P8-T008, P8-T009, P8-T010, P8-T011, P8-T012, P8-T013, P8-T016]
requirements: [R8.07]
roadmap_todos: [T8.22]
modules: [M17, M20]
dashboards: [D17, D16]
branch: p8/P8-T025-verify-audit-d17
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

# P8-T025 · Audit check: every MCP call audited (source = mcp) and visible in D17

## Goal / expected outcome

R8.07's "Audit check" passes. A scripted session of 200 mixed MCP calls yields exactly 200 `audit.mcp_call` rows, each command linked to one `audit.command` row with `source = mcp`. The hash chain verifies, and D17 and D16 show all of them with args redacted.

## Context & references

- Roadmap: [R8.07](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDo [T8.22](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- WORM: [15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many) · UI: [D17](../../../docs/ui/dashboards/D17-mcp-console.md), [D16 Audit](../../../docs/ui/dashboards/D16-system.md)
- Related: P8-T007, P8-T016.

## Requirements

- Session mix: reads from every group, C1 writes, C2 orders (pending/approved/rejected/expired), a C3 request, denied never-exposed calls, rate-limited calls, one call with a fake secret in `reason`.
- Checks: row counts match; every command row has `source = mcp` and `token_id`; `audit.verify` passes; the next daily seal includes the rows; the fake secret is redacted in `args_redacted`; an `UPDATE` on `audit.mcp_call` is blocked.
- Playwright: D17 Session activity lists all 200 with linked audit entries; D16 Audit filter source = mcp shows the commands.

## ToDo

- [ ] Write the scripted session + checks `tests/scenarios/mcp_audit/`.
- [ ] Run and record counts in the Progress log.
- [ ] Doc sync.

## Verification

### Tests
- The scripted check; Playwright assertions for D17/D16.

### Scenarios
- Given a tampered row in a restored copy, when `audit.verify` runs, then the mismatch is reported (and on the live DB would halt new trading per 07 §8).

### Stress / failure injection
- Run the 200-call session 5× concurrently (1,000 calls): chain intact, counts exact.

## Acceptance criteria

- [ ] Counts exact; chain verifies; secret redacted; D17/D16 show everything
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Seal job runs at night: verify inclusion the next morning and log it.

## Cardinal rules (do NOT)

- Do NOT test tampering on the live audit tables; use a restored copy.
- Do NOT update or delete WORM rows; corrections are new rows (15 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code (including the MCP SDK).

## Doc sync on completion

- `docs/roadmap/phase-8-mcp.md`: R8.07 verified (link).

## Branch & PR

- Branch: `p8/P8-T025-verify-audit-d17`
- PR title: `P8-T025: Audit check: every MCP call audited (source = mcp) and visible in D17`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T025` run

## Progress log

- 2026-10-21 00:00 · planner · created
