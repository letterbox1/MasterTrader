---
id: P8-B010
kind: gap
title: Skipping approve mode for MCP orders vs "human approval on trade decisions"
phase: 8
type: USER
status: done
priority: medium
size: XS
severity: S3
owner: user
claimed_by: ""
depends_on: []
requirements: [R8.04]
roadmap_todos: [T8.03]
modules: [M20]
dashboards: []
branch: p8/P8-B010-approval-skip-vs-human-approval-policy
pr: ""
doc_sync: [docs/12-policy-and-compliance.md, docs/07-security-notes.md, docs/roadmap/phase-8-mcp.md]
doc_sync_status: done
found_in: docs/12-policy-and-compliance.md §4 (Anthropic / OpenAI row); docs/roadmap/phase-8-mcp.md T8.03
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
---

# P8-B010 · Skipping approve mode for MCP orders vs "human approval on trade decisions"

## Goal / expected outcome

The docs agree and are specific about this point, so the P8 tasks that depend on it can be built and tested without guessing. Proposed resolution: keep the default "always approve"; allow auto rules only as a C3 decision you take knowingly, documented in 12 §4 as "you instruct each MCP trade in the conversation; auto rules are small-size, per-venue, C3-approved and audited"; or forbid auto rules entirely. You decide here; P8-T019 applies your decision in D17.

## Context & references

- Compliance: [12 §4](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules) · roadmap [T8.03](../../../docs/roadmap/phase-8-mcp.md#4-todo-sets) · [07 §6](../../../docs/07-security-notes.md#6-application-controls)
- Implementing tasks: P8-T005, P8-T019

## Requirements

- **Steps to reproduce:** Read 12 §4: Anthropic/OpenAI "Do: Human approval on trade decisions". Read T8.03: "Choose MCP policy: which venues/sizes may skip approve mode".
- **Expected:** A documented stance on whether and when MCP-originated orders may execute without a per-order human tap.
- **Actual:** Unstated. An auto rule lets Claude-originated orders execute without a per-order human approval, which may conflict with the 12 §4 usage-policy note.
- **Impact:** Possible usage-policy conflict; unclear default for P8-T019 (S3)
- **Suggested fix:** keep the default "always approve"; allow auto rules only as a C3 decision you take knowingly, documented in 12 §4 as "you instruct each MCP trade in the conversation; auto rules are small-size, per-venue, C3-approved and audited"; or forbid auto rules entirely. You decide here; P8-T019 applies your decision in D17.

## ToDo

- [x] Decision recorded: 17 §D (P8-B010, see P8-B002): MCP orders always need your approval card; there is no skip-approval or auto-rule option
- [x] Docs carry it: 16 §2.3 MCP-originated orders row; 12 §4 Anthropic/OpenAI row; 07 §6 ('no skip approval option'); 02 §7.4; D17 Actions (`mcp.policy.set` has no skip option); roadmap T8.03 reworded
- [x] Implementation owned by P8-T005 (no skip field in schema), P8-T019 (your scope/expiry choices), P8-T021 (no skip path test)
- [x] Resolution noted in the Progress log

## Verification

### Tests
- Regression: the implementing task's test (named in Context) pins the documented behaviour.

### Scenarios
- Given the docs are fixed, when a developer reads only the linked sections, then they implement the same behaviour as the P8 task describes.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Docs updated and mutually consistent (checked 2026-10-22: 16 §2.3 MCP-originated orders row; 12 §4 Anthropic/OpenAI row; 07 §6 ('no skip approval option'); 02 §7.4; D17 Actions (`mcp.policy.set` has no skip option); roadmap T8.03 reworded)
- [x] Implementing work owned and its test named: P8-T005 (no skip field in schema), P8-T019 (your scope/expiry choices), P8-T021 (no skip path test)
- [x] Root cause noted: the original T8.03 let venues/sizes skip approve mode

## Exceptions & edge cases

- If the user rejects the proposal, record the alternative here and update the implementing task before it starts.

## Cardinal rules (do NOT)

- Do NOT close without the docs actually agreeing.
- Do NOT edit WORM records to "fix" data; append a correction instead.
- Do NOT expose withdrawals, API-key management or wallet mandate signing through MCP, in any form (R8.06).

## Doc sync on completion

- `docs/12-policy-and-compliance.md`: as described in the suggested fix.
- `docs/07-security-notes.md`: as described in the suggested fix.
- `docs/roadmap/phase-8-mcp.md`: note the clarified behaviour if it changes a requirement's wording.

## Branch & PR

- Branch: `p8/P8-B010-approval-skip-vs-human-approval-policy`
- PR title: `P8-B010: fix skipping approve mode for MCP orders vs "human approval on trade decisions"`
- PR checklist: docs consistent · implementing test referenced · `./kanban done P8-B010` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by 17 §D (P8-B010, see P8-B002); docs checked: 16 §2.3 MCP-originated orders row; 12 §4 Anthropic/OpenAI row; 07 §6 ('no skip approval option'); 02 §7.4; D17 Actions (`mcp.policy.set` has no skip option); roadmap T8.03 reworded; implementation owned by P8-T005 (no skip field in schema), P8-T019 (your scope/expiry choices), P8-T021 (no skip path test); root cause: the original T8.03 let venues/sizes skip approve mode
- 2026-10-22 02:26 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 §D (P8-B010, see P8-B002); docs updated: 16 §2.3 MCP-originated orders row; 12 §4 Anthropic/OpenAI row; 07 §6 ('no skip approval option'); 02 §7.4; D17 Actions (`mcp.policy.set` has no skip option); roadmap T8.03 reworded; implementation owned by P8-T005 (no skip field in schema), P8-T019 (your scope/expiry choices), P8-T021 (no skip path test)
- 2026-10-22 02:26 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:26 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
