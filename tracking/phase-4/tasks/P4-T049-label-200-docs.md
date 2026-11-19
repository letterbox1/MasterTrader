---
id: P4-T049
kind: task
title: Optional - label ~200 sampled documents to refine the SemIf relevance gate
phase: 4
type: USER
status: backlog
priority: low
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
updated: 2026-11-19
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P4-T049 · Optional - label ~200 sampled documents to refine the SemIf relevance gate

## Goal / expected outcome

**Optional.** The relevance gate is calibrated and measured on silver labels from an LLM labeller via the gateway by default (P4-T048, P4-T053), so nothing waits for this. If you want the gate tuned to your own judgement, you label a ~200-document batch relevant/irrelevant (and, where obvious, direction) in D08 Label mode. Your labels then take precedence over the silver labels for the same documents, and the agent re-runs the calibration and reports precision/recall on your labels next to the silver-label figures.

## Context & references

- Roadmap: [R4.12](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.04](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Tool: P4-T062 (minimal labelling tool, D08 Label mode, `models.label.add`; [R4.16](../../../docs/roadmap/phase-4-intel.md#3-requirements)). Calibration: P4-T048. Measurement: P4-T053.
- Decision: [17 §G](../../../docs/17-decisions-register.md#g-platform-rust-and-python-supabase-vercel-workstation-first-2026-11-19): labels the human was asked to make become agent silver labels by default; the human's labels are an optional improvement that never blocks.
- Blocks nothing: P4-T053 and the exit demo run on silver labels.

## Requirements

- 'Relevant' = about a tradable instrument in your universe or a macro event that could move it (the same rubric the silver labels use).
- Label honestly from the text; don't look at the model's score (it is hidden in Label mode).
- ≈ 60–90 minutes; can be split over several sessions, or stopped part-way (partial batches still count).

## ToDo

- [ ] Open the link the agent posts to Telegram (`/intel?label=batch-<id>`) on desktop or phone.
- [ ] Label each document: **1** relevant, **0** irrelevant, **s** skip if unsure (aim for < 10% skips).
- [ ] Optionally set direction (bull/bear/neutral) when clear.
- [ ] When done, reply 'labels done' to the agent or tick this task; the agent re-runs the P4-T048 calibration with your labels taking precedence and adds your-label metrics to the P4-T053 report.

## Verification

### Tests
- Agent checks the count of your non-skip labels for the batch and records it.

### Scenarios
- Given you skip more than 20 docs, then the agent adds a top-up batch of the same strata.
- Given you label only part of the batch, then calibration uses your labels where present and silver labels elsewhere, and reports both sets.

### Stress / failure injection
- n/a: human step.

## Acceptance criteria

- [ ] Your labels recorded (any count; ≥ 180 non-skip labels for a stand-alone your-label report)
- [ ] Agent confirms the calibration re-ran with your labels taking precedence (P4-T048/P4-T053)

## Exceptions & edge cases

- If a document is paywalled/headline-only, label on the headline or skip.
- If you never do this task, it is cancelled at the phase exit with the reason "optional; silver labels used"; nothing else changes.

## Cardinal rules (do NOT)

- Do NOT share or export the labelled set outside the workstation.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).

## Doc sync on completion

- `docs/roadmap/phase-4-intel.md`: tick T4.04

## Branch & PR

- Branch: `p4/P4-T049-label-200-docs`
- PR title: `P4-T049: Optional - label ~200 sampled documents to refine the SemIf relevance gate`
- PR checklist: no PR needed for the human step itself; the agent records the outcome (non-secret parts only) in this file and runs `./kanban done P4-T049`

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (labelling tool is now P4-T062 (R4.16, 17 §D P4-B007))
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (per 17 §G this stays USER but is optional: silver labels from the gateway LLM labeller (P4-T048) are the default, your labels take precedence where present; P4-T053 no longer depends on this task; priority low; "host" → workstation)
