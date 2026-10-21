---
id: P6-T032
kind: task
title: Monthly fine-tune flow
phase: 6
type: BUILD
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T031]
requirements: [R6.13]
roadmap_todos: [T6.26]
modules: [M21]
dashboards: [D10]
branch: p6/P6-T032-monthly-finetune-flow
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

# P6-T032 · Monthly fine-tune flow

## Goal / expected outcome

On the first weekend of each month a full fine-tune (not warm-start) of each production tier-B head runs on all eligible labels, followed by calibration, the full bake-off subset and a promotion proposal — promoted only through the gates.

## Context & references

- Roadmap: [R6.13](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.26
- Spec: [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design) (retraining cadence: monthly fine-tune, promoted only through the gates)
- Depends on (this phase): P6-T031

## Requirements

- Prefect schedule monthly; uses the latest user + outcome labels; full hyper-parameter search budget smaller than initial (default 20 trials).
- Compares against current production and the frozen baseline; result is a proposal in D10.
- Notification with summary to Telegram/D10.

## ToDo

- [ ] Prefect deployment `finetune_monthly` reusing P6-T031 steps with `mode=full`.
- [ ] Summary notification.
- [ ] Tests; docs.

## Verification

### Tests
- Integration: dry run with `--as-of` produces a proposal and no routing change.

### Scenarios
- Given a month of new labels, then a monthly candidate appears with a comparison table.

### Stress / failure injection
- n/a: monthly batch; shares the nightly flow's caps.

## Acceptance criteria

- [ ] Monthly schedule registered; dry run green.

## Exceptions & edge cases

- If the nightly flow is failing, the monthly run is skipped and alerts.

## Cardinal rules (do NOT)

- Do NOT auto-promote.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md` §4.3: monthly cadence details.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.26 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T032-monthly-finetune-flow`
- PR title: `P6-T032: Monthly fine-tune flow`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T032` run

## Progress log

- 2026-10-21 00:00 · planner · created
