---
id: P8-B013
kind: gap
title: No numbers for MCP rate limits, response size caps or token expiry
phase: 8
type: DOC
status: done
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R8.02, R8.04]
roadmap_todos: []
modules: [M20]
dashboards: [D17]
branch: p8/P8-B013-mcp-limits-unspecified
pr: ""
doc_sync: [docs/03-build-spec.md, docs/ui/dashboards/D17-mcp-console.md, docs/roadmap/phase-8-mcp.md]
doc_sync_status: done
found_in: docs/ui/dashboards/D17-mcp-console.md Tool registry ("rate limit" column); docs/03-build-spec.md M20
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
---

# P8-B013 · No numbers for MCP rate limits, response size caps or token expiry

## Goal / expected outcome

The docs agree and are specific about this point, so the P8 tasks that depend on it can be built and tested without guessing. Proposed resolution: document defaults in 03 M20: reads 60/min, agents 10/h, trade commands 10/min and 50/day, risk tighten 10/min, kill unlimited; response cap 64 KB, 4,000 chars per text field; token expiry 30 days default, 90 max; MCP approval TTL 15 min.

## Context & references

- Spec: [D17](../../../docs/ui/dashboards/D17-mcp-console.md) · [03 M20](../../../docs/03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) · research [MCP security](../../../docs/research/observability-storage-dataquality.md#mcp-security)
- Implementing tasks: P8-T002, P8-T005, P8-T006

## Requirements

- **Steps to reproduce:** D17 shows a per-tool rate limit and token expiry; research says "rate limits and cool-downs". Look for values.
- **Expected:** Default values documented and testable.
- **Actual:** No values anywhere.
- **Impact:** P8-T005/T006/T002 use proposed numbers that nobody has agreed (S3)
- **Suggested fix:** document defaults in 03 M20: reads 60/min, agents 10/h, trade commands 10/min and 50/day, risk tighten 10/min, kill unlimited; response cap 64 KB, 4,000 chars per text field; token expiry 30 days default, 90 max; MCP approval TTL 15 min.

## ToDo

- [x] Decision recorded: 17 §C (P8-B013): MCP limits are 16 defaults
- [x] Docs carry it: 16 §2.12 (60 reads/min and 10 writes/min per token; 256 KB per result; token expiry options); 16 §2.3 (MCP approval TTL 5 min); 02 §7.4 Audit; 03 M20 Limits; D17 Tool registry; roadmap R8.10
- [x] Implementation owned by P8-T030 (limits + cap), P8-T034 (limit tests), P8-T002 (expiry), P8-T005 (TTL)
- [x] Resolution noted in the Progress log

## Verification

### Tests
- Regression: the implementing task's test (named in Context) pins the documented behaviour.

### Scenarios
- Given the docs are fixed, when a developer reads only the linked sections, then they implement the same behaviour as the P8 task describes.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Docs updated and mutually consistent (checked 2026-10-22: 16 §2.12 (60 reads/min and 10 writes/min per token; 256 KB per result; token expiry options); 16 §2.3 (MCP approval TTL 5 min); 02 §7.4 Audit; 03 M20 Limits; D17 Tool registry; roadmap R8.10)
- [x] Implementing work owned and its test named: P8-T030 (limits + cap), P8-T034 (limit tests), P8-T002 (expiry), P8-T005 (TTL)
- [x] Root cause noted: D17 showed limit columns before any values were set

## Exceptions & edge cases

- If the user rejects the proposal, record the alternative here and update the implementing task before it starts.

## Cardinal rules (do NOT)

- Do NOT close without the docs actually agreeing.
- Do NOT edit WORM records to "fix" data; append a correction instead.
- Do NOT expose withdrawals, API-key management or wallet mandate signing through MCP, in any form (R8.06).

## Doc sync on completion

- `docs/03-build-spec.md`: as described in the suggested fix.
- `docs/ui/dashboards/D17-mcp-console.md`: as described in the suggested fix.
- `docs/roadmap/phase-8-mcp.md`: note the clarified behaviour if it changes a requirement's wording.

## Branch & PR

- Branch: `p8/P8-B013-mcp-limits-unspecified`
- PR title: `P8-B013: fix no numbers for MCP rate limits, response size caps or token expiry`
- PR checklist: docs consistent · implementing test referenced · `./kanban done P8-B013` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by 17 §C (P8-B013); docs checked: 16 §2.12 (60 reads/min and 10 writes/min per token; 256 KB per result; token expiry options); 16 §2.3 (MCP approval TTL 5 min); 02 §7.4 Audit; 03 M20 Limits; D17 Tool registry; roadmap R8.10; implementation owned by P8-T030 (limits + cap), P8-T034 (limit tests), P8-T002 (expiry), P8-T005 (TTL); root cause: D17 showed limit columns before any values were set
- 2026-10-22 02:26 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 §C (P8-B013); docs updated: 16 §2.12 (60 reads/min and 10 writes/min per token; 256 KB per result; token expiry options); 16 §2.3 (MCP approval TTL 5 min); 02 §7.4 Audit; 03 M20 Limits; D17 Tool registry; roadmap R8.10; implementation owned by P8-T030 (limits + cap), P8-T034 (limit tests), P8-T002 (expiry), P8-T005 (TTL)
- 2026-10-22 02:26 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:26 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
