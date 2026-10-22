---
id: P8-B006
kind: bug
title: Research note says order placement is never exposed via MCP and audits to `audit.risk_config_changes`
phase: 8
type: DOC
status: done
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R8.03, R8.07]
roadmap_todos: []
modules: [M20]
dashboards: []
branch: p8/P8-B006-research-note-contradicts-m20
pr: ""
doc_sync: [docs/research/observability-storage-dataquality.md, docs/roadmap/phase-8-mcp.md]
doc_sync_status: done
found_in: docs/research/observability-storage-dataquality.md §MCP security items 5 and 7
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
---

# P8-B006 · Research note says order placement is never exposed via MCP and audits to `audit.risk_config_changes`

## Goal / expected outcome

The docs agree and are specific about this point, so the P8 tasks that depend on it can be built and tested without guessing. Proposed resolution: add a "Superseded by 03 M20 / 07 §6 (orders allowed via M11 + approve mode; audit in `audit.command` / `audit.mcp_call`)" note to items 5 and 7.

## Context & references

- Docs: [research MCP security](../../../docs/research/observability-storage-dataquality.md#mcp-security) · [03 M20](../../../docs/03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) · [07 §6](../../../docs/07-security-notes.md#6-application-controls)

## Requirements

- **Steps to reproduce:** Read research §MCP security item 7 ("Never exposed via MCP: order placement, withdrawals, key management") and item 5 (`audit.risk_config_changes`); compare with 03 M20 (MCP can place/modify/cancel orders, approve mode) and 02 §7.2 (`audit.command`).
- **Expected:** The research note matches the adopted design, or is clearly marked as superseded by 03 M20 / 07 §6.
- **Actual:** The two contradict each other on whether MCP may place orders and on the audit table.
- **Impact:** A developer reading the research note would build the wrong thing or dispute the exit demo (S3)
- **Suggested fix:** add a "Superseded by 03 M20 / 07 §6 (orders allowed via M11 + approve mode; audit in `audit.command` / `audit.mcp_call`)" note to items 5 and 7.

## ToDo

- [x] Decision recorded: 17 §D (P8-B006): the old research note is superseded
- [x] Docs carry it: docs/research/observability-storage-dataquality.md §MCP security now opens with a 'Superseded by 03 M20, 02 §7.4, 16 §2.12 (P8-B006)' note; items 4, 5 and 7 marked historical
- [x] Implementation owned by n/a (documentation only)
- [x] Resolution noted in the Progress log

## Verification

### Tests
- Regression: the implementing task's test (named in Context) pins the documented behaviour.

### Scenarios
- Given the docs are fixed, when a developer reads only the linked sections, then they implement the same behaviour as the P8 task describes.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Docs updated and mutually consistent (checked 2026-10-22: docs/research/observability-storage-dataquality.md §MCP security now opens with a 'Superseded by 03 M20, 02 §7.4, 16 §2.12 (P8-B006)' note; items 4, 5 and 7 marked historical)
- [x] Implementing work owned and its test named: n/a (documentation only)
- [x] Root cause noted: the research note was written before M20 allowed orders via approval cards

## Exceptions & edge cases

- If the user rejects the proposal, record the alternative here and update the implementing task before it starts.

## Cardinal rules (do NOT)

- Do NOT close without the docs actually agreeing.
- Do NOT edit WORM records to "fix" data; append a correction instead.
- Do NOT expose withdrawals, API-key management or wallet mandate signing through MCP, in any form (R8.06).

## Doc sync on completion

- `docs/research/observability-storage-dataquality.md`: as described in the suggested fix.
- `docs/roadmap/phase-8-mcp.md`: note the clarified behaviour if it changes a requirement's wording.

## Branch & PR

- Branch: `p8/P8-B006-research-note-contradicts-m20`
- PR title: `P8-B006: fix research note says order placement is never exposed via MCP and audits to `audit.risk_config_changes``
- PR checklist: docs consistent · implementing test referenced · `./kanban done P8-B006` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by 17 §D (P8-B006); docs checked: docs/research/observability-storage-dataquality.md §MCP security now opens with a 'Superseded by 03 M20, 02 §7.4, 16 §2.12 (P8-B006)' note; items 4, 5 and 7 marked historical; implementation owned by n/a (documentation only); root cause: the research note was written before M20 allowed orders via approval cards
- 2026-10-22 02:26 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 §D (P8-B006); docs updated: docs/research/observability-storage-dataquality.md §MCP security now opens with a 'Superseded by 03 M20, 02 §7.4, 16 §2.12 (P8-B006)' note; items 4, 5 and 7 marked historical; implementation owned by n/a (documentation only)
- 2026-10-22 02:26 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:26 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
