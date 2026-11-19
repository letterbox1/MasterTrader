---
id: P4-T048
kind: task
title: SemIf relevance-gate silver labels and threshold calibration (your labels optional)
phase: 4
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T062, P4-T030, P2-T046]
requirements: [R4.12]
roadmap_todos: [T4.28]
modules: [M21]
dashboards: [D08]
tools: [uv, git]
mcp: []
env: []
services: [supabase-postgres, mlflow, decision-svc]
branch: p4/P4-T048-labelling-tool-threshold-calibration
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/roadmap/phase-4-intel.md]
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

# P4-T048 · SemIf relevance-gate silver labels and threshold calibration (your labels optional)

## Goal / expected outcome

An LLM labeller via the gateway **silver-labels** the ~200-document P4-T062 batch against the written relevance rubric (the P4-T049 definition; [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design)), stored as `models.label` rows with `source = silver`. A calibration script reads the labels (your P4-T049 labels take precedence where present, silver labels elsewhere) and picks the relevance-gate threshold at the target precision, writing it as a new `models.question` version. Nothing waits for your labelling; P4-T053 runs it, activates the threshold and measures the result.

## Context & references

- Roadmap: [R4.12](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDos [T4.28, T4.04](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Design: [10 §4.3 operating rules](../../../docs/10-memory-rag-and-models.md#43-design) (labels from outcomes or you, never shadow outputs; per-question thresholds) · [D10 labelling queue](../../../docs/ui/dashboards/D10-models-memory.md) (full queue in P6)
- Decision: [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) (P4-B007): the minimal labelling tool and `models.label.add` (C0) are P4-T062 ([R4.16](../../../docs/roadmap/phase-4-intel.md#3-requirements)); this task is the calibration only.
- Thresholds: [16 §2.10](../../../docs/16-configuration-and-safety-model.md#210-models-tier-b-and-llm-budgets) (auto-decide coverage at ≥ 0.75 precision, direct veto only at ≥ 0.90, ECE ≤ 0.05), configurable per question.
- Cross-phase: P2-T046 (MLflow) is a `depends_on` entry.

## Requirements

- Input: the latest label per (subject, question) from `models.label`, `source = user` first, else `source = silver`, excluding skips; Telegram and `model_input_ok=false` subjects can't be there (P4-T062 sampler), and the script re-checks with the P4-T025 guard.
- Calibration: choose the threshold maximising recall subject to precision ≥ the question's target (default 0.75 for the auto-decide gate, 0.90 for any veto use, per 16 §2.10; configurable); report precision/recall/F1, ECE, confusion matrix, bootstrap CIs and the chosen value to MLflow; activate via `models.question.update` (C1) as a new question version.
- Cross-validated threshold choice (k-fold) so P4-T053 doesn't evaluate on the documents used to pick it.

## ToDo

- [ ] Silver-label the P4-T062 batch: an LLM labeller via the LiteLLM gateway applies the written rubric to each sampled document (only rows the P4-T025 guard allows as model input) and stores `models.label` rows with `source = silver` via the CLI path (never SemIf, the tier-B teacher or any shadow model as labeller).
- [ ] Calibration script (`tools/calibrate/semif_threshold.py`) + MLflow logging, reporting silver-label and your-label figures separately.
- [ ] `models.question.update` activation step with the chosen threshold.
- [ ] Tests.

## Verification

### Tests
- Unit: threshold selection on a synthetic labelled set hits the target precision.
- Unit: Telegram or flagged subjects in the label set are refused by the guard.
- Unit: ECE and bootstrap CI implementations match a reference.

### Scenarios
- Given only 150 labels so far, then calibration still runs and reports a wider confidence interval.
- Given a label is changed, then a new row is inserted (latest wins), old kept.

### Stress / failure injection
- n/a: small human-labelling volume.

## Acceptance criteria

- [ ] Calibration runs end to end on a synthetic labelled set and writes a new question version with the chosen threshold (the run on your labels is P4-T053)
- [ ] MLflow run records precision/recall/F1/ECE and the 16 §2.10 targets used
- [ ] CI green (ruff, mypy, `uv run pytest`, `pit` bypass check, `pnpm test`, `pnpm playwright` viewport matrix + axe)

## Exceptions & edge cases

- If the target precision is unreachable, keep the gate permissive (low threshold), leave stage-1 output advisory, and record the finding for P6.

## Cardinal rules (do NOT)

- Do NOT use shadow-model or teacher outputs as labels; silver labels come from the gateway LLM labeller applying the written rubric, checked against outcomes where available, recorded as `source = silver`.
- Do NOT calibrate on Telegram or `model_input_ok = false` subjects.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT UPDATE or DELETE WORM rows (`audit.*`); corrections are new rows ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md`: §4.3: record the calibrated stage-1 threshold and how it was chosen
- `docs/roadmap/phase-4-intel.md`: tick T4.28 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T048-labelling-tool-threshold-calibration`
- PR title: `P4-T048: SemIf relevance-gate silver labels and threshold calibration (your labels optional)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T048` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (labelling tool + models.label.add split out to new P4-T062 (R4.16/T4.31, 17 §D P4-B007); now calibration only, targets from 16 §2.10; depends on P4-T062, P4-T030, P2-T046)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (silver labels (`source = silver`, gateway LLM labeller per 10 §4.3) are the default per 17 §G; your P4-T049 labels optional and take precedence; services postgres → supabase-postgres; CI commands per 18 (cargo/uv/supabase/pnpm))
