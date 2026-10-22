---
id: P6-T059
kind: task
title: Bake-off report reviewed; promotion only via gates
phase: 6
type: VERIFY
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T029, P6-T030, P6-T031, P6-T002, P6-T068]
requirements: [R6.12, R6.14, R6.10]
roadmap_todos: [T6.60]
modules: [M21]
dashboards: [D10]
tools: [git, uv, python>=3.12, docker]
mcp: []
env: []
services: [mlflow, postgres]
branch: p6/P6-T059-verify-bakeoff-review-gates
pr: ""
doc_sync: [docs/10-memory-rag-and-models.md, docs/roadmap/phase-6-ai-models-treasury.md]
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

# P6-T059 · Bake-off report reviewed; promotion only via gates

## Goal / expected outcome

The bake-off report is reviewed (agent prepares, you sign off), it names a production tier-B model per question **or keeps SemIf** with calibration evidence, and the audit trail shows every promotion went through `models.promote` gates.

## Context & references

- Roadmap: [R6.12](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.14](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.10](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.60
- Roadmap: R6.12 'Bake-off report', R6.14 'Promotion audit', R6.10 'Calibration report' · [roadmap §6 exit criteria](../../../docs/roadmap/phase-6-ai-models-treasury.md#6-exit-criteria-demo) item 3
- Depends on (this phase): P6-T029, P6-T030, P6-T031, P6-T068 (Kev/licences), P6-T002 (FinMMEval data; if you declined it, the review documents the absence)
- Defaults: [16 §2.10](../../../docs/16-configuration-and-safety-model.md#210-models-tier-b-and-llm-budgets)

## Requirements

- Checklist: all contenders run or documented as excluded (Kev per P6-T068); FinMMEval included or documented; per-regime Brier/ECE; coverage at target precision; latency; flip rate; recommendation per question.
- Promotion audit: query `audit.command` for `models.promote` and registry status history; zero status changes outside commands; every promoted model spent ≥ 14 days in shadow meeting the 16 §2.10 thresholds.
- Your sign-off recorded in the progress log (comment, not a secret).

## ToDo

- [ ] Prepare a review summary from the report.
- [ ] Run the promotion audit query.
- [ ] Ask the user to review and record decision.
- [ ] Promote (via gates) or keep SemIf per question.

## Verification

### Tests
- Audit query script committed.

### Scenarios
- Given an attempted direct DB status change, then the audit query flags it (negative control in staging).

### Stress / failure injection
- n/a: review item.

## Acceptance criteria

- [ ] Signed-off report with a named production model or SemIf per question.
- [ ] Promotion audit clean.

## Exceptions & edge cases

- If no model beats SemIf, 'keep SemIf' is a valid outcome.

## Cardinal rules (do NOT)

- Do NOT promote outside `models.promote`.
- Do NOT UPDATE or DELETE WORM rows (`audit.*`, `journal.*`, policy changes); corrections are new rows referencing the original (15 §2).
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md` §4.3: record the production choice per question.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.60 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T059-verify-bakeoff-review-gates`
- PR title: `P6-T059: Bake-off report reviewed; promotion only via gates`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T059` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (shadow ≥ 14 days and thresholds per 16 §2.10; Kev via P6-T068; FinMMEval from P6-T002 at review time; run fields)
