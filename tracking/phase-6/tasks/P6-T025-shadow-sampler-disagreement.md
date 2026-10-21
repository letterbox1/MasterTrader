---
id: P6-T025
kind: task
title: 5% teacher shadow sampler and per-question disagreement
phase: 6
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T024, P6-T019, P6-T009]
requirements: [R6.13]
roadmap_todos: [T6.26]
modules: [M21, M8]
dashboards: [D10]
branch: p6/P6-T025-shadow-sampler-disagreement
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P6-T025 · 5% teacher shadow sampler and per-question disagreement

## Goal / expected outcome

About 5% of tier-B decisions are re-asked of the teacher (M8 quick path / gateway model) in shadow; agreement is stored in `models.shadow_check` and tracked per question for D10 and threshold tuning — and never becomes a training label.

## Context & references

- Roadmap: [R6.13](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.26
- Spec: [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design) (shadow checks ~5%, disagreement tracked per question in D10) · [02 F4](../../../docs/02-v1-architecture.md#8-end-to-end-flows) (teacher in shadow)
- UI: [D10](../../../docs/ui/dashboards/D10-models-memory.md) Additions (shadow checks)
- Depends on (this phase): P6-T024, P6-T019, P6-T009

## Requirements

- Sampler: Bernoulli 5% per question (configurable 1–10%), stratified so low-traffic questions get ≥ 20 checks/week.
- Teacher call: compact prompt with the same state (≤ 320 tokens) → JSON option answer; runs async via gateway role `shadow` (budgeted; when exhausted, sampling pauses rather than falling back to the same local model being checked).
- Store `models.shadow_check` (decision_id, teacher model, teacher answer, agreement, cost); separate from labels (no grant to `models.label`).
- Metrics: disagreement rate per question/model (7d, 30d), Prometheus + `/models/questions` fields; alert when disagreement jumps > 2× baseline.
- Disagreements are offered to the labelling queue (P6-T019) for **your** label.

## ToDo

- [ ] Sampler hook in decision-svc (post-decision, non-blocking).
- [ ] Shadow worker consuming a NATS queue.
- [ ] Migration for `models.shadow_check`.
- [ ] Metrics + alert rule.
- [ ] Tests; docs.

## Verification

### Tests
- Unit: sampling rate within ±1% over 100k decisions; stratification floor.
- Integration: shadow worker writes checks; nothing appears in `models.label`.
- Budget: exhausted `shadow` budget pauses sampling.

### Scenarios
- Given 10,000 decisions, then ~500 shadow checks exist and D10 shows disagreement per question.
- Given disagreement on `event_type` doubles week-over-week, then an alert fires and items enter the labelling queue.

### Stress / failure injection
- Gateway down for 2 h: shadow queue bounded (drop oldest, counted); decision latency unaffected.

## Acceptance criteria

- [ ] Shadow sampling live with per-question disagreement visible.
- [ ] Zero shadow-derived labels (also P6-T056).

## Exceptions & edge cases

- Teacher returns invalid JSON → recorded as `teacher_invalid`, excluded from agreement.

## Cardinal rules (do NOT)

- Do NOT write shadow outputs into `models.label` or any dataset as labels.
- Do NOT block the decision path on shadow calls.
- Do NOT let Telegram text (or any `model_input_ok = false` / `train_ok = false` row) reach a model, prompt, RAG index, memory bank or training set (12 §4–5).
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md` §4.3: shadow sampler defaults and budget behaviour.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.26 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T025-shadow-sampler-disagreement`
- PR title: `P6-T025: 5% teacher shadow sampler and per-question disagreement`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T025` run

## Progress log

- 2026-10-21 00:00 · planner · created
