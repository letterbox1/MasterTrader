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
depends_on: [P8-T007, P8-T008, P8-T009, P8-T010, P8-T011, P8-T012, P8-T013, P8-T016, P8-T030]
requirements: [R8.07]
roadmap_todos: [T8.22, T8.64]
modules: [M17, M20]
dashboards: [D17, D16]
tools: [uv, pnpm, docker, git]
mcp: []
env: []
services: [postgres, nats]
branch: p8/P8-T025-verify-audit-d17
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

# P8-T025 · Audit check: every MCP call audited (source = mcp) and visible in D17

## Goal / expected outcome

R8.07's "Audit check" and the audit part of T8.64 pass. A scripted session of 200 mixed MCP calls (reads included) yields exactly 200 `audit.mcp_call` rows, each command linked to one `audit.command` row with `source = mcp`. The hash chain verifies, and D17 (`/mcp/sessions`, Session activity) and D16 show all of them with args redacted. Test stack, SDK client, no keys.

## Context & references

- Roadmap: [R8.07](../../../docs/roadmap/phase-8-mcp.md#3-requirements) · ToDo [T8.22](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets)
- WORM: [15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many) · UI: [D17](../../../docs/ui/dashboards/D17-mcp-console.md), [D16 Audit](../../../docs/ui/dashboards/D16-system.md)
- Decisions: [17 §B P8-B007](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer) (canonical names) · [17 §D P8-B012](../../../docs/17-decisions-register.md#d-other-decisions) (reads logged to `audit.mcp_call`) · [16 §2.11](../../../docs/16-configuration-and-safety-model.md#211-worm-integrity)
- Related: P8-T007, P8-T016, P8-T030.

## Requirements

- Session mix: reads from every group, C1 writes, C2 orders (pending/approved/rejected/expired), a C3 request, denied never-exposed calls (`approval.approve`, `mcp.token.create`), rate-limited calls, a capped (> 256 KB) result, one call with a fake secret in `reason`.
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
- Given a tampered row in a restored copy, when `audit.verify` runs, then the mismatch is reported (on the live DB the default `block_new_entries` would apply, 16 §2.11).

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
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/roadmap/phase-8-mcp.md`: R8.07 verified (link).

## Branch & PR

- Branch: `p8/P8-T025-verify-audit-d17`
- PR title: `P8-T025: Audit check: every MCP call audited (source = mcp) and visible in D17`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P8-T025` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (reads included per 17 §D P8-B012, `/mcp/sessions`, denied `approval.*`/`mcp.*` and capped results in the mix, 16 §2.11 verify behaviour; added T8.64; dep P8-T030; tools/env/services)
