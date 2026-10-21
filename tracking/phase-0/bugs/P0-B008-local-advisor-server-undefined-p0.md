---
id: P0-B008
kind: gap
title: No P0 container serves the `local-advisor` route LiteLLM falls back to
phase: 0
type: DOC
status: ready
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R0.09]
roadmap_todos: [T0.45]
modules: []
dashboards: []
branch: p0/P0-B008-local-advisor-server-undefined-p0
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/10-memory-rag-and-models.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: docs/roadmap/phase-0-foundations.md R0.09 ('a local model')
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P0-B008 · No P0 container serves the `local-advisor` route LiteLLM falls back to

## Goal / expected outcome

The docs agree and the implementing tasks have one unambiguous answer. Suggested fix: Add `local-advisor` (llama.cpp `llama-server`, CPU, small Qwen GGUF) to 02 §3.2 for P0; upgrade to vLLM when the GPU arrives.

## Context & references

- Found in: `docs/roadmap/phase-0-foundations.md R0.09 ('a local model')`
- Related: P0-T044, P0-T042
- [02 §3.2 containers](../../../docs/02-v1-architecture.md#32-containers)
- [10 §5 model gateway](../../../docs/10-memory-rag-and-models.md#5-model-gateway-research-chat--debate-routing-m21)

## Requirements

- **Steps to reproduce:** R0.09 and 10 §5 need `local-advisor` (vLLM / llama-server); the P0 container list (roadmap header, 02 §3.2) has no such service; `vllm` appears only in 02 §3.1 networks; 04 Phase 0 mentions Ollama.
- **Expected:** A named P0 container for the local model (CPU-capable) and its model choice.
- **Actual:** Undefined; budget-exhaustion fallback can't work in P0.
- **Impact:** Gateway fallback (10 §5 'falls back to local models instead of failing') is untestable.
- **Suggested fix:** Add `local-advisor` (llama.cpp `llama-server`, CPU, small Qwen GGUF) to 02 §3.2 for P0; upgrade to vLLM when the GPU arrives.

## ToDo

- [ ] Confirm the decision with the user (or take the suggested fix if no objection)
- [ ] Update the listed docs so they agree
- [ ] Update the affected P0 task files' Context if the decision differs from the suggestion
- [ ] Add/adjust a regression check where one is possible (see Verification)

## Verification

### Tests
- Doc check: grep the listed docs for the conflicting statements; none remain after the fix.

### Scenarios
- Given a developer reads any of the listed docs, then they reach the same answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [ ] Listed docs updated and consistent
- [ ] Affected tasks reference the resolution
- [ ] Root cause (how the drift happened) noted in the progress log

## Exceptions & edge cases

- If the user decides differently from the suggestion, the affected tasks are updated before they start.

## Cardinal rules (do NOT)

- Do NOT close without updating every listed doc.
- Do NOT edit WORM records to 'fix' data; append a correction instead.

## Doc sync on completion

- `docs/02-v1-architecture.md`: reconcile as described.
- `docs/10-memory-rag-and-models.md`: reconcile as described.
- `docs/roadmap/phase-0-foundations.md`: reconcile as described.

## Branch & PR

- Branch: `p0/P0-B008-local-advisor-server-undefined-p0`
- PR title: `P0-B008: fix no P0 container serves the `local-advisor` route LiteLLM falls back to`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-B008` run

## Progress log

- 2026-10-21 00:00 · planner · opened
