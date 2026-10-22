---
id: P8-B008
kind: gap
title: No mt_api command to request an M10 anomaly explanation
phase: 8
type: DOC
status: done
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R8.03]
roadmap_todos: [T8.20]
modules: [M10, M20]
dashboards: [D09]
branch: p8/P8-B008-anomaly-explain-command-missing
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/ui/dashboards/D09-agents.md, docs/roadmap/phase-8-mcp.md]
doc_sync_status: done
found_in: docs/02-v1-architecture.md §7.1/§7.2; docs/ui/dashboards/D09-agents.md
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
---

# P8-B008 · No mt_api command to request an M10 anomaly explanation

## Goal / expected outcome

The docs agree and are specific about this point, so the P8 tasks that depend on it can be built and tested without guessing. Proposed resolution: add `anomaly.explain` (C1; args `anomaly_id`; publishes a request to `mt_anomaly`; result as a notification) to 02 §7.2 and D09's backend contract; P8-T009 implements it.

## Context & references

- Spec: [03 M20](../../../docs/03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted) · [02 §7](../../../docs/02-v1-architecture.md#7-api-contract-mt_api) · [D09](../../../docs/ui/dashboards/D09-agents.md)
- Cross-phase: P6 R6.05 / T6.22
- Implementing task: P8-T009

## Requirements

- **Steps to reproduce:** R8.03 / 03 M20 list "request an anomaly explanation (M10)". Search 02 §7 for an anomaly endpoint or command.
- **Expected:** A command (e.g. `anomaly.explain`, C1) and/or query exists so MCP (and the UI) can request a brief for an anomaly id.
- **Actual:** Only `/notifications?kind=anomaly` (read) exists; the explain agent runs on its own trigger.
- **Impact:** One R8.03 capability has no API to wrap; the thin adapter can't invent it (S3)
- **Suggested fix:** add `anomaly.explain` (C1; args `anomaly_id`; publishes a request to `mt_anomaly`; result as a notification) to 02 §7.2 and D09's backend contract; P8-T009 implements it.

## ToDo

- [x] Decision recorded: 17 §D (P8-B008): add `anomaly.explain`
- [x] Docs carry it: 02 §7.2 Agents & models row (`anomaly.explain` C1, result as a notification); 02 §4 M10 row; D09 widget, actions and backend contract
- [x] Implementation owned by P8-T009 (MCP tool + mt_api command if P6 didn't add it)
- [x] Resolution noted in the Progress log

## Verification

### Tests
- Regression: the implementing task's test (named in Context) pins the documented behaviour.

### Scenarios
- Given the docs are fixed, when a developer reads only the linked sections, then they implement the same behaviour as the P8 task describes.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Docs updated and mutually consistent (checked 2026-10-22: 02 §7.2 Agents & models row (`anomaly.explain` C1, result as a notification); 02 §4 M10 row; D09 widget, actions and backend contract)
- [x] Implementing work owned and its test named: P8-T009 (MCP tool + mt_api command if P6 didn't add it)
- [x] Root cause noted: the explain agent only had its own trigger

## Exceptions & edge cases

- If the user rejects the proposal, record the alternative here and update the implementing task before it starts.

## Cardinal rules (do NOT)

- Do NOT close without the docs actually agreeing.
- Do NOT edit WORM records to "fix" data; append a correction instead.
- Do NOT expose withdrawals, API-key management or wallet mandate signing through MCP, in any form (R8.06).

## Doc sync on completion

- `docs/02-v1-architecture.md`: as described in the suggested fix.
- `docs/ui/dashboards/D09-agents.md`: as described in the suggested fix.
- `docs/roadmap/phase-8-mcp.md`: note the clarified behaviour if it changes a requirement's wording.

## Branch & PR

- Branch: `p8/P8-B008-anomaly-explain-command-missing`
- PR title: `P8-B008: fix no mt_api command to request an M10 anomaly explanation`
- PR checklist: docs consistent · implementing test referenced · `./kanban done P8-B008` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by 17 §D (P8-B008); docs checked: 02 §7.2 Agents & models row (`anomaly.explain` C1, result as a notification); 02 §4 M10 row; D09 widget, actions and backend contract; implementation owned by P8-T009 (MCP tool + mt_api command if P6 didn't add it); root cause: the explain agent only had its own trigger
- 2026-10-22 02:26 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 §D (P8-B008); docs updated: 02 §7.2 Agents & models row (`anomaly.explain` C1, result as a notification); 02 §4 M10 row; D09 widget, actions and backend contract; implementation owned by P8-T009 (MCP tool + mt_api command if P6 didn't add it)
- 2026-10-22 02:26 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:26 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
