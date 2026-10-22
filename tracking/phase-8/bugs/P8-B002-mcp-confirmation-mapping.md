---
id: P8-B002
kind: gap
title: C1/C2 confirmation levels and approval TTL are undefined for MCP clients
phase: 8
type: DOC
status: done
priority: high
size: S
severity: S2
owner: agent
claimed_by: ""
depends_on: []
requirements: [R8.04, R8.05]
roadmap_todos: [T8.21]
modules: [M20]
dashboards: [D17]
branch: p8/P8-B002-mcp-confirmation-mapping
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/ui/dashboards/D17-mcp-console.md, docs/03-build-spec.md, docs/roadmap/phase-8-mcp.md]
doc_sync_status: done
found_in: docs/02-v1-architecture.md §7.2; docs/ui/dashboards/D17-mcp-console.md acceptance 1; docs/03-build-spec.md M20
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
---

# P8-B002 · C1/C2 confirmation levels and approval TTL are undefined for MCP clients

## Goal / expected outcome

The docs agree and are specific about this point, so the P8 tasks that depend on it can be built and tested without guessing. Proposed resolution: C0 → immediate; C1 → immediate + Telegram notice; C2 → Telegram/web approval (approve mode) unless a C3-approved auto rule matches; C3 → full C3; Kill ON immediate; Kill OFF C3. MCP approval TTL default 15 min (configurable 1–60). MCP-initiated closes/reductions are **not** protective exits (they wait), matching the exit demo. Protective stop cancels and bracket widening are C2. Document in 02 §7.2 and D17.

## Context & references

- Spec: [02 §7.2](../../../docs/02-v1-architecture.md#72-commands-rest-write) · [D17](../../../docs/ui/dashboards/D17-mcp-console.md) · [15 §1.2–1.3](../../../docs/15-bots-hitl-and-worm-audit.md#1-trading-bots) · [roadmap §6 exit demo](../../../docs/roadmap/phase-8-mcp.md#6-exit-criteria-demo)
- Implementing task: P8-T005 (golden decision table)

## Requirements

- **Steps to reproduce:** Read 02 §7.2: C1 = in-app confirm sheet, C2 = confirm sheet + risk preview + hold-to-confirm. D17 says "MCP actions follow the same confirmation levels as the web". Ask: what is a confirm sheet for an MCP client?
- **Expected:** A table mapping each level for `source = mcp`, plus the TTL for MCP approval cards and whether MCP-initiated closes count as protective exits.
- **Actual:** Undefined. The MCP client's own tool-approval prompt is client-side and can't be trusted, and no TTL is given for manual (non-bot) MCP orders.
- **Impact:** P8-T005 can't be built or tested against an agreed spec; risk of either over-blocking (tighten not instant, contradicting the exit demo) or under-blocking (S2)
- **Suggested fix:** C0 → immediate; C1 → immediate + Telegram notice; C2 → Telegram/web approval (approve mode) unless a C3-approved auto rule matches; C3 → full C3; Kill ON immediate; Kill OFF C3. MCP approval TTL default 15 min (configurable 1–60). MCP-initiated closes/reductions are **not** protective exits (they wait), matching the exit demo. Protective stop cancels and bracket widening are C2. Document in 02 §7.2 and D17.

## ToDo

- [x] Decision recorded: 17 §A (P8-B002): C0 reads; C1 per token scope; C2 orders always your approval card (TTL 5 min, expiry = reject); C3 Telegram + TOTP; no skip-approval option (also resolves P8-B010)
- [x] Docs carry it: 16 §2.3 (MCP-originated orders row); 02 §7.4 levels for `source = mcp`; 03 M20 safeguards; 15 §1.3 table; D17 acceptance 1
- [x] Implementation owned by P8-T005 (policy + golden decision table), P8-T014 (card), P8-T021 (bypass)
- [x] Resolution noted in the Progress log

## Verification

### Tests
- Regression: the implementing task's test (named in Context) pins the documented behaviour.

### Scenarios
- Given the docs are fixed, when a developer reads only the linked sections, then they implement the same behaviour as the P8 task describes.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Docs updated and mutually consistent (checked 2026-10-22: 16 §2.3 (MCP-originated orders row); 02 §7.4 levels for `source = mcp`; 03 M20 safeguards; 15 §1.3 table; D17 acceptance 1)
- [x] Implementing work owned and its test named: P8-T005 (policy + golden decision table), P8-T014 (card), P8-T021 (bypass)
- [x] Root cause noted: 02 §7.2 levels were defined for the web confirm sheet only

## Exceptions & edge cases

- If the user rejects the proposal, record the alternative here and update the implementing task before it starts.

## Cardinal rules (do NOT)

- Do NOT close without the docs actually agreeing.
- Do NOT edit WORM records to "fix" data; append a correction instead.
- Do NOT expose withdrawals, API-key management or wallet mandate signing through MCP, in any form (R8.06).

## Doc sync on completion

- `docs/02-v1-architecture.md`: as described in the suggested fix.
- `docs/ui/dashboards/D17-mcp-console.md`: as described in the suggested fix.
- `docs/03-build-spec.md`: as described in the suggested fix.
- `docs/roadmap/phase-8-mcp.md`: note the clarified behaviour if it changes a requirement's wording.

## Branch & PR

- Branch: `p8/P8-B002-mcp-confirmation-mapping`
- PR title: `P8-B002: fix c1/C2 confirmation levels and approval TTL are undefined for MCP clients`
- PR checklist: docs consistent · implementing test referenced · `./kanban done P8-B002` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by 17 §A (P8-B002); docs checked: 16 §2.3 (MCP-originated orders row); 02 §7.4 levels for `source = mcp`; 03 M20 safeguards; 15 §1.3 table; D17 acceptance 1; implementation owned by P8-T005 (policy + golden decision table), P8-T014 (card), P8-T021 (bypass); root cause: 02 §7.2 levels were defined for the web confirm sheet only
- 2026-10-22 02:26 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 §A (P8-B002); docs updated: 16 §2.3 (MCP-originated orders row); 02 §7.4 levels for `source = mcp`; 03 M20 safeguards; 15 §1.3 table; D17 acceptance 1; implementation owned by P8-T005 (policy + golden decision table), P8-T014 (card), P8-T021 (bypass)
- 2026-10-22 02:26 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:26 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
