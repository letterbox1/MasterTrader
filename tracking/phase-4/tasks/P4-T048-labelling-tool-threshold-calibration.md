---
id: P4-T048
kind: task
title: Labelling tool and SemIf gate threshold calibration
phase: 4
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T030]
requirements: [R4.12]
roadmap_todos: [T4.28]
modules: [M21]
dashboards: [D08]
branch: p4/P4-T048-labelling-tool-threshold-calibration
pr: ""
doc_sync: [docs/ui/dashboards/D08-intel.md, docs/02-v1-architecture.md, docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P4-T048 · Labelling tool and SemIf gate threshold calibration

## Goal / expected outcome

A minimal labelling flow lets you label a stratified sample of ~200 documents relevant/irrelevant (plus optional direction/event-type), stores labels in `models.label` (`label_source = user`), and a calibration script picks the relevance-gate threshold at a target precision, writing it as a new `models.question` version — the data path P4-T049 (labelling) and P4-T053 (precision/recall) need.

## Context & references

- Roadmap: [R4.12](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDos [T4.28, T4.04](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Design: [10 §4.3 operating rules](../../../docs/10-memory-rag-and-models.md#43-design) (labels from outcomes or you, never shadow outputs; per-question thresholds) · [D10 labelling queue](../../../docs/ui/dashboards/D10-models-memory.md) (full queue in P6)
- Gap: P4-B007 (no P4 labelling tool; `models.label.add` not in 02 §7.2).

## Requirements

- Sampler: 200 docs stratified by source kind and by SemIf P(yes) decile; excludes Telegram (never sampled) and `model_input_ok=false` rows.
- UI: a 'Label' mode in the D08 document sheet (keyboard 1/0/skip; phone buttons), reachable at `/intel?label=batch-<id>`; command `models.label.add` (C0).
- `models.label`: id, subject, question id+version, label, source (`user`/`outcome`), labelled_at; insert-only.
- Calibration: choose the threshold maximising recall subject to precision ≥ 0.9 (configurable); report precision/recall/F1, confusion matrix and the chosen value to MLflow; activate via `models.question.update` (C1).

## ToDo

- [ ] Sampler + batch creation.
- [ ] Label mode UI + command + table.
- [ ] Calibration script + MLflow logging.
- [ ] Tests.

## Verification

### Tests
- Unit: sampler never includes Telegram or flagged rows.
- Unit: threshold selection on a synthetic labelled set.
- Playwright: label 5 docs via keyboard.

### Scenarios
- Given only 150 labels so far, then calibration still runs and reports a wider confidence interval.
- Given a label is changed, then a new row is inserted (latest wins), old kept.

### Stress / failure injection
- n/a: small human-labelling volume.

## Acceptance criteria

- [ ] 200-doc batch can be created and labelled end to end
- [ ] Calibration writes a new question version with the chosen threshold
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, viewport matrix + axe)

## Exceptions & edge cases

- If precision ≥ 0.9 is unreachable, keep the gate permissive (low threshold) and record the finding for P6.

## Cardinal rules (do NOT)

- Do NOT use shadow-model or teacher outputs as labels.
- Do NOT sample Telegram content.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT UPDATE or DELETE WORM rows (`audit.*`); corrections are new rows ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/ui/dashboards/D08-intel.md`: note the interim Label mode
- `docs/02-v1-architecture.md`: §7.2: add `models.label.add`
- `docs/roadmap/phase-4-intel.md`: tick T4.28 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T048-labelling-tool-threshold-calibration`
- PR title: `P4-T048: Labelling tool and SemIf gate threshold calibration`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T048` run

## Progress log

- 2026-10-21 00:00 · planner · created
