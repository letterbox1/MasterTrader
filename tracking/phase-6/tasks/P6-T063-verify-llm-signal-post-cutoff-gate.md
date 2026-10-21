---
id: P6-T063
kind: task
title: LLM-signal strategy gate check on post-cutoff data
phase: 6
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T017, P6-T016]
requirements: [R6.06]
roadmap_todos: []
modules: [M0, M7]
dashboards: [D03, D10]
branch: p6/P6-T063-verify-llm-signal-post-cutoff-gate
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P6-T063 · LLM-signal strategy gate check on post-cutoff data

## Goal / expected outcome

A sample LLM-signal strategy is run through the full gate set; the cutoff gate rejects pre-cutoff windows and accepts post-cutoff+embargo windows, and the strategy can enter paper mode only after passing.

## Context & references

- Roadmap: [R6.06](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo none (supporting item)
- Roadmap: R6.06 'Gate check' · [03 §8](../../../docs/03-build-spec.md#8-promotion-gates-per-strategy-configurable) item 4 · [14 §6](../../../docs/14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8)
- Gap: P6-B001
- Depends on (this phase): P6-T017, P6-T016

## Requirements

- Two backtest configs (pre-cutoff and post-cutoff) for the same strategy; gate outcomes recorded.
- Lifecycle transition to `paper` succeeds only with the passing config.

## ToDo

- [ ] Create sample strategy `strategies/llm_signal_majors/`.
- [ ] Run both configs through the gate runner.
- [ ] Promote to paper (C1) if passing.
- [ ] Record results.

## Verification

### Tests
- Integration test in the lab suite.

### Scenarios
- Given a window starting before the model cutoff, then the gate fails with `pre_cutoff_window`.

### Stress / failure injection
- n/a: gate logic.

## Acceptance criteria

- [ ] Gate outcomes as expected; strategy in paper with passing evidence.

## Exceptions & edge cases

- Insufficient post-cutoff data → strategy stays in validated; documented.

## Cardinal rules (do NOT)

- Do NOT move the strategy to approve/auto in P6.
- Do NOT touch live money or live keys; keys stay trade-only, IP-locked, withdrawals disabled (live is gated to P7).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order and on-chain move goes through M11.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §6: example result.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick the matching ToDo (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T063-verify-llm-signal-post-cutoff-gate`
- PR title: `P6-T063: LLM-signal strategy gate check on post-cutoff data`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T063` run

## Progress log

- 2026-10-21 00:00 · planner · created
