---
id: P6-T065
kind: task
title: Start the 4-week nightly distillation soak and LLM-signal paper trading
phase: 6
type: RUN
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T031, P6-T016, P6-T017, P6-T025, P6-T063]
requirements: [R6.14, R6.06]
roadmap_todos: [T6.80]
modules: [M21, M0, M8]
dashboards: [D10, D09, D03]
branch: p6/P6-T065-run-start-distillation-paper-soak
pr: ""
doc_sync: [docs/roadmap/phase-7-prove-and-go-live.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P6-T065 · Start the 4-week nightly distillation soak and LLM-signal paper trading

## Goal / expected outcome

The four-week soak is **started** and healthy: nightly distillation runs with the teacher in shadow, and at least one LLM-signal strategy trades on paper. Completion (4 clean weeks) is checked at P7 entry, so this phase can close.

## Context & references

- Roadmap: [R6.14](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.06](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.80
- Roadmap: T6.80 · [02 F4](../../../docs/02-v1-architecture.md#8-end-to-end-flows) · [03 §8](../../../docs/03-build-spec.md#8-promotion-gates-per-strategy-configurable) item 5 (paper period)
- Brief rule: RUN items outlasting the phase are modelled as 'start X'; completion checked in the phase that needs it (P7).
- Depends on (this phase): P6-T031, P6-T016, P6-T017, P6-T025, P6-T063

## Requirements

- Start date recorded; nightly distillation scheduled and green for the first 3 nights; shadow sampler active; LLM-signal strategy in paper mode.
- Weekly checkpoint note template: nights green/failed, candidates produced, promotions (should be via gates only), shadow disagreement, paper P&L vs backtest, LLM spend.
- Hand-over note for P7: where to read the soak results and what 'clean' means (≥ 26/28 nights green, no ungated promotion, spend within budget).

## ToDo

- [ ] Enable schedules; record start date in this file.
- [ ] Watch first 3 nights; fix or file bugs.
- [ ] Write week-1 checkpoint note.
- [ ] Write the P7 hand-over note (in this file's progress log).

## Verification

### Tests
- n/a: elapsed-time run; health checked via Grafana and D10.

### Scenarios
- Given night 2 fails, then the alert fires, the cause is fixed, and the soak counter notes the miss.

### Stress / failure injection
- n/a: soak itself is the endurance test; failures logged.

## Acceptance criteria

- [ ] Soak started with 3 consecutive green nights.
- [ ] LLM-signal strategy on paper.
- [ ] P7 hand-over note written.

## Exceptions & edge cases

- Host outage > 24 h restarts the clock for the affected week (noted).

## Cardinal rules (do NOT)

- Do NOT promote models outside gates during the soak.
- Do NOT move LLM-signal strategies beyond paper.
- Do NOT touch live money or live keys; keys stay trade-only, IP-locked, withdrawals disabled (live is gated to P7).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order and on-chain move goes through M11.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/roadmap/phase-6-ai-models-treasury.md`: annotate T6.80 'started <date>, completion checked at P7 entry'; tick it only once the 4 weeks are clean.
- `docs/roadmap/phase-7-prove-and-go-live.md`: entry criteria reference the soak results (P7 planner's file; raise it there, don't edit from P6).

## Branch & PR

- Branch: `p6/P6-T065-run-start-distillation-paper-soak`
- PR title: `P6-T065: Start the 4-week nightly distillation soak and LLM-signal paper trading`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T065` run

## Progress log

- 2026-10-21 00:00 · planner · created
