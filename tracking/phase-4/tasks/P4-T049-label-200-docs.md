---
id: P4-T049
kind: task
title: Label ~200 sampled documents for the SemIf relevance gate
phase: 4
type: USER
status: backlog
priority: high
size: S
severity: ""
owner: user
claimed_by: ""
depends_on: [P4-T062, P4-T030]
requirements: [R4.12, R4.16]
roadmap_todos: [T4.04]
modules: [M21]
dashboards: [D08]
tools: []
mcp: []
env: []
services: [mt-web]
branch: p4/P4-T049-label-200-docs
pr: ""
doc_sync: [docs/roadmap/phase-4-intel.md]
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

# P4-T049 · Label ~200 sampled documents for the SemIf relevance gate

## Goal / expected outcome

You have labelled the ~200-document batch relevant/irrelevant (and, where obvious, direction), so the relevance-gate threshold can be calibrated and P4-T053 can measure precision/recall on your own judgement.

## Context & references

- Roadmap: [R4.12](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.04](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Tool: P4-T062 (minimal labelling tool, D08 Label mode, `models.label.add`; [R4.16](../../../docs/roadmap/phase-4-intel.md#3-requirements)). Calibration on your labels: P4-T048.
- Unblocks: P4-T053.

## Requirements

- 'Relevant' = about a tradable instrument in your universe or a macro event that could move it.
- Label honestly from the text; don't look at the model's score (it is hidden in Label mode).
- ≈ 60–90 minutes; can be split over several sessions.

## ToDo

- [ ] Open the link the agent posts to Telegram (`/intel?label=batch-<id>`) on desktop or phone.
- [ ] Label each document: **1** relevant, **0** irrelevant, **s** skip if unsure (aim for < 10% skips).
- [ ] Optionally set direction (bull/bear/neutral) when clear.
- [ ] When done, reply 'labels done' to the agent or tick this task; the agent runs calibration in P4-T053.

## Verification

### Tests
- Agent checks ≥ 180 non-skip labels exist for the batch.

### Scenarios
- Given you skip more than 20 docs, then the agent adds a top-up batch of the same strata.

### Stress / failure injection
- n/a: human step.

## Acceptance criteria

- [ ] ≥ 180 non-skip labels recorded
- [ ] Agent confirms calibration ran on your labels (P4-T053)

## Exceptions & edge cases

- If a document is paywalled/headline-only, label on the headline or skip.

## Cardinal rules (do NOT)

- Do NOT share or export the labelled set outside the host.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).

## Doc sync on completion

- `docs/roadmap/phase-4-intel.md`: tick T4.04

## Branch & PR

- Branch: `p4/P4-T049-label-200-docs`
- PR title: `P4-T049: Label ~200 sampled documents for the SemIf relevance gate`
- PR checklist: no PR needed for the human step itself; the agent records the outcome (non-secret parts only) in this file and runs `./kanban done P4-T049`

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (labelling tool is now P4-T062 (R4.16, 17 §D P4-B007))
