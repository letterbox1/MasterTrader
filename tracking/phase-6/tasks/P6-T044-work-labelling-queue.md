---
id: P6-T044
kind: task
title: Work the D10 labelling queue (~15 min/day while it's new)
phase: 6
type: USER
status: backlog
priority: medium
size: S
severity: ""
owner: user
claimed_by: ""
depends_on: [P6-T043]
requirements: [R6.13]
roadmap_todos: [T6.02]
modules: [M21]
dashboards: [D10]
branch: p6/P6-T044-work-labelling-queue
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

# P6-T044 · Work the D10 labelling queue (~15 min/day while it's new)

## Goal / expected outcome

For the first two weeks after the queue opens you label ~15 min/day, giving tier B human labels for abstentions, teacher disagreements and high-value calls.

## Context & references

- Roadmap: [R6.13](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.02
- Spec: [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design) (labels from outcomes or you) · [D10](../../../docs/ui/dashboards/D10-models-memory.md) labelling queue
- Feeds: P6-T020 datasets, P6-T026 thresholds, P6-T065 run
- Depends on (this phase): P6-T043

## Requirements

- ~15 min/day for 14 days (≈ 40 items/day default).
- Label honestly; skip when unsure (skips are fine).
- Never copy a model's answer; the UI hides shadow answers on purpose.

## ToDo

- [ ] Open D10 → Labelling queue daily (phone works).
- [ ] Label or skip each item; add a short note on odd cases.
- [ ] After 14 days, record the total labelled (from D10 counter) in the progress log.
- [ ] Tell us if items are confusing so the state template can improve.

## Verification

### Tests
- n/a: human labelling; counts visible in D10.

### Scenarios
- Given 14 days of labelling, then ≥ 400 user labels exist across questions.

### Stress / failure injection
- n/a

## Acceptance criteria

- [ ] ≥ 14 labelling sessions logged.
- [ ] ≥ 400 user labels (or the queue emptied).

## Exceptions & edge cases

- Travelling: pause; the queue keeps sampling and caps daily items.

## Cardinal rules (do NOT)

- Do NOT label from model outputs or other bots' calls.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md` §4.3: note real labelling throughput.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.02 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T044-work-labelling-queue`
- PR title: `P6-T044: Work the D10 labelling queue (~15 min/day while it's new)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T044` run

## Progress log

- 2026-10-21 00:00 · planner · created
