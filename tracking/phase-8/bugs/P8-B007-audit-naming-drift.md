---
id: P8-B007
kind: bug
title: "Naming drift: `audit.commands` vs `audit.command`, source `ui` vs `web`, approve/reject levels"
phase: 8
type: DOC
status: done
priority: low
size: XS
severity: S4
owner: agent
claimed_by: ""
depends_on: []
requirements: [R8.07]
roadmap_todos: []
modules: [M20]
dashboards: []
branch: p8/P8-B007-audit-naming-drift
pr: ""
doc_sync: [docs/03-build-spec.md, docs/15-bots-hitl-and-worm-audit.md, docs/ui/dashboards/D17-mcp-console.md, docs/roadmap/phase-8-mcp.md]
doc_sync_status: done
found_in: docs/03-build-spec.md M20 + M17; docs/ui/dashboards/D17-mcp-console.md Actions; docs/15-bots-hitl-and-worm-audit.md §1.5
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
---

# P8-B007 · Naming drift: `audit.commands` vs `audit.command`, source `ui` vs `web`, approve/reject levels

## Goal / expected outcome

The docs agree and are specific about this point, so the P8 tasks that depend on it can be built and tested without guessing. Proposed resolution: use `audit.command` and `web` everywhere; set `approval.reject` = C1 (it only tightens) in 15 §1.5 to match D17, or C2 in D17 — the user picks; P8 uses C1 for reject.

## Context & references

- Docs: [03 M20](../../../docs/03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) · [03 M17](../../../docs/03-build-spec.md#m17-observability--audit--mt_obs) · [02 §7.2](../../../docs/02-v1-architecture.md#72-commands-rest-write) · [D17](../../../docs/ui/dashboards/D17-mcp-console.md) · [15 §1.5](../../../docs/15-bots-hitl-and-worm-audit.md#15-api-data-and-ui)

## Requirements

- **Steps to reproduce:** Compare 03 M20 (`audit.commands`) with 02 §4/§7.2 and roadmap R8.07 (`audit.command`); 03 M17 (source `ui / telegram / mcp / system`) with 02 §7.2 and D16 (`web | telegram | mcp | system`); D17 (approve C2 / reject C1) with 15 §1.5 (approve, approve_partial, reject all C2).
- **Expected:** One table name (`audit.command`), one source enum (`web | telegram | mcp | system`), one level per approval command.
- **Actual:** Three small inconsistencies.
- **Impact:** Wrong table/enum names in migrations or filters; inconsistent UI confirmation for reject (S4)
- **Suggested fix:** use `audit.command` and `web` everywhere; set `approval.reject` = C1 (it only tightens) in 15 §1.5 to match D17, or C2 in D17 — the user picks; P8 uses C1 for reject.

## ToDo

- [x] Decision recorded: 17 §B (P0-B017, P1-B010, P8-B007): canonical singular audit names incl. `audit.command`, `audit.mcp_call`; command source `web`/`telegram`/`mcp`/`system`
- [x] Docs carry it: 03 M20 and M17 use `audit.command` and source `web`; 02 §4/§5 canonical names; 15 §1.5 and 02 §7.2: `approval.reject` C1 (matches D17); D16 Audit columns
- [x] Implementation owned by P8-T007 (audit tables/filters use the canonical names)
- [x] Resolution noted in the Progress log

## Verification

### Tests
- Regression: the implementing task's test (named in Context) pins the documented behaviour.

### Scenarios
- Given the docs are fixed, when a developer reads only the linked sections, then they implement the same behaviour as the P8 task describes.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Docs updated and mutually consistent (checked 2026-10-22: 03 M20 and M17 use `audit.command` and source `web`; 02 §4/§5 canonical names; 15 §1.5 and 02 §7.2: `approval.reject` C1 (matches D17); D16 Audit columns)
- [x] Implementing work owned and its test named: P8-T007 (audit tables/filters use the canonical names)
- [x] Root cause noted: names drifted across docs written at different times

## Exceptions & edge cases

- If the user rejects the proposal, record the alternative here and update the implementing task before it starts.

## Cardinal rules (do NOT)

- Do NOT close without the docs actually agreeing.
- Do NOT edit WORM records to "fix" data; append a correction instead.
- Do NOT expose withdrawals, API-key management or wallet mandate signing through MCP, in any form (R8.06).

## Doc sync on completion

- `docs/03-build-spec.md`: as described in the suggested fix.
- `docs/15-bots-hitl-and-worm-audit.md`: as described in the suggested fix.
- `docs/ui/dashboards/D17-mcp-console.md`: as described in the suggested fix.
- `docs/roadmap/phase-8-mcp.md`: note the clarified behaviour if it changes a requirement's wording.

## Branch & PR

- Branch: `p8/P8-B007-audit-naming-drift`
- PR title: `P8-B007: fix naming drift: `audit.commands` vs `audit.command`, source `ui` vs `web`, approve/reject levels`
- PR checklist: docs consistent · implementing test referenced · `./kanban done P8-B007` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by 17 §B (P0-B017, P1-B010, P8-B007); docs checked: 03 M20 and M17 use `audit.command` and source `web`; 02 §4/§5 canonical names; 15 §1.5 and 02 §7.2: `approval.reject` C1 (matches D17); D16 Audit columns; implementation owned by P8-T007 (audit tables/filters use the canonical names); root cause: names drifted across docs written at different times
- 2026-10-22 02:26 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 §B (P0-B017, P1-B010, P8-B007); docs updated: 03 M20 and M17 use `audit.command` and source `web`; 02 §4/§5 canonical names; 15 §1.5 and 02 §7.2: `approval.reject` C1 (matches D17); D16 Audit columns; implementation owned by P8-T007 (audit tables/filters use the canonical names)
- 2026-10-22 02:26 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:26 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
