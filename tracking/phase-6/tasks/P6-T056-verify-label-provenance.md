---
id: P6-T056
kind: task
title: Label-provenance test: shadow outputs never become labels; Telegram excluded
phase: 6
type: VERIFY
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T019, P6-T020, P6-T025]
requirements: [R6.13]
roadmap_todos: [T6.62]
modules: [M21]
dashboards: [D10]
branch: p6/P6-T056-verify-label-provenance
pr: ""
doc_sync: [docs/12-policy-and-compliance.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P6-T056 · Label-provenance test: shadow outputs never become labels; Telegram excluded

## Goal / expected outcome

Tests prove that no shadow/model output can be written or used as a training label, and that Telegram-derived (or any `train_ok=false`) rows never reach a dataset, question state or trainer.

## Context & references

- Roadmap: [R6.13](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.62
- Roadmap: R6.13 'Rule tests' · [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design) · [12 §5](../../../docs/12-policy-and-compliance.md#5-data-provenance-tagging-one-mechanism-for-all-data-terms) · [SPEC non-negotiables](../../../SPEC.md#non-negotiable-requirements) NN10
- Cross-phase: P4 T4.60 Telegram gate
- Depends on (this phase): P6-T019, P6-T020, P6-T025

## Requirements

- DB-level: `label_source` CHECK; role grants (shadow writer can't insert labels).
- Code-level: dataset builder rejects any label whose lineage includes `models.shadow_check` or another model's output.
- Provenance: seeded Telegram rows traced through ingest → state builder → dataset → trainer: refused at every boundary with counters.
- D10 shows the excluded count.

## ToDo

- [ ] Write `tests/provenance/test_label_provenance.py` (DB + code + end-to-end).
- [ ] Run and record results.

## Verification

### Tests
- The suite above in CI.

### Scenarios
- Given a shadow disagreement, when building a dataset, then the teacher's answer is not a label.
- Given a Telegram-sourced document linked to a decision, then that decision is excluded from training and counted.

### Stress / failure injection
- Property test: random lineage graphs; no label with a model/shadow source ever passes.

## Acceptance criteria

- [ ] Suite green in CI.
- [ ] Excluded counts visible in D10.

## Exceptions & edge cases

- Outcome labels computed from market data are allowed even when the teacher was wrong.

## Cardinal rules (do NOT)

- Do NOT whitelist a model-derived label 'just for bootstrapping'.
- Do NOT let Telegram text (or any `model_input_ok = false` / `train_ok = false` row) reach a model, prompt, RAG index, memory bank or training set (12 §4–5).
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/12-policy-and-compliance.md` §5: link the test.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.62 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T056-verify-label-provenance`
- PR title: `P6-T056: Label-provenance test: shadow outputs never become labels; Telegram excluded`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T056` run

## Progress log

- 2026-10-21 00:00 · planner · created
