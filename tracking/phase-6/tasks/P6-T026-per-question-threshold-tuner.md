---
id: P6-T026
kind: task
title: Per-question threshold tuner from measured disagreement
phase: 6
type: BUILD
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T025, P6-T022]
requirements: [R6.13]
roadmap_todos: [T6.26]
modules: [M21]
dashboards: [D10]
tools: [git, uv, python>=3.12, docker]
mcp: []
env: []
services: [postgres, prefect]
branch: p6/P6-T026-per-question-threshold-tuner
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

# P6-T026 · Per-question threshold tuner from measured disagreement

## Goal / expected outcome

A weekly job proposes per-question abstention/veto thresholds from measured disagreement with the teacher and with outcomes (not one global cut-off); proposals are applied only as new question versions via `models.question.update` (C1).

## Context & references

- Roadmap: [R6.13](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.26
- Spec: [10 §4.3](../../../docs/10-memory-rag-and-models.md#43-design) (thresholds per question from measured disagreement with teacher and outcomes)
- UI: [D10](../../../docs/ui/dashboards/D10-models-memory.md) Decision questions (Edit question C1)
- Depends on (this phase): P6-T025, P6-T022
- Defaults: [16 §2.10](../../../docs/16-configuration-and-safety-model.md#210-models-tier-b-and-llm-budgets)

## Requirements

- Inputs: last N weeks of decisions, shadow checks, settled outcomes, user labels per question.
- Objective: maximise coverage subject to precision ≥ target (outcome/user labels) and teacher disagreement ≤ configured ceiling; bootstrap CI reported.
- Output: proposal row (`models.question_proposal`) with old/new thresholds, expected coverage/precision; never auto-applied.
- Applying a proposal is `models.question.update` (C1, new version); a threshold below its default bar in 16 §2.10 (auto-decide precision < 0.75, veto precision < 0.90) is loosening and needs C3 (02 §7.2).

## ToDo

- [ ] Tuner job (Prefect weekly).
- [ ] Proposal table + D10 surfacing (via P6-T042).
- [ ] Command handler rules for veto threshold direction.
- [ ] Tests; docs.

## Verification

### Tests
- Unit: optimiser respects precision floor; direction classification for veto thresholds.
- Integration: proposal → C1 apply → new question version used by decision-svc.

### Scenarios
- Given precision on `relevance` is 0.92 at threshold 0.6, then the tuner proposes a lower threshold with higher coverage and shows the CI.
- Given a C1 request that sets veto precision below 0.90, then the server requires C3.

### Stress / failure injection
- n/a: weekly batch over bounded data.

## Acceptance criteria

- [ ] Weekly proposals visible in D10.
- [ ] Threshold changes only via versioned commands.

## Exceptions & edge cases

- Too few labelled samples (< 100) → no proposal, reason shown.

## Cardinal rules (do NOT)

- Do NOT auto-apply thresholds.
- Do NOT loosen anything (risk, LLM budgets, treasury policy, allow-list, autonomous mode, mandates) without C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/10-memory-rag-and-models.md` §4.3: tuner objective.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.26 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T026-per-question-threshold-tuner`
- PR title: `P6-T026: Per-question threshold tuner from measured disagreement`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T026` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (C3 only below the 16 §2.10 default bars (02 §7.2); run fields)
