---
id: P2-T108
kind: task
title: Automatic, append-only trial counter per strategy family
phase: 2
type: BUILD
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T101, P2-T107]
requirements: [R2.42]
roadmap_todos: [T2.27]
modules: [M7]
dashboards: [D03, D04]
branch: p2/P2-T108-automatic-trial-counter
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T108 · Automatic, append-only trial counter per strategy family

## Goal / expected outcome

Every distinct parameter set / code version evaluated for a strategy family increments a trial counter automatically and irreversibly, and the count (plus the variance of Sharpe across trials) feeds deflated Sharpe and is shown on D03/D04.

## Context & references

- Roadmap: [R2.42](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.27 · roadmap risk 'Overfitting through many tweaks'
- [14 §6 trial counter](../../../docs/14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) · [03 §8 item 7](../../../docs/03-build-spec.md#8-promotion-gates-per-strategy-configurable)

## Requirements

- Table `strategy.trial` (insert-only for app roles): family_id, strategy_version, params_hash, code_sha, run_id, per-period Sharpe, n_obs, created_at.
- Trial identity = (family, code_sha, params_hash, dataset spec hash); re-running an identical trial does not increment, any tweak does.
- Family = the strategy lineage incl. clones and generator variants (clones inherit the parent count; it never resets).
- Expose `trial_count`, `sharpe_variance_across_trials` to the DSR calculator and the API.

## ToDo

- [ ] Migration for `strategy.trial` with INSERT/SELECT-only grants
- [ ] Hook into `tracked_run` so screener, truth and sweep trials register automatically
- [ ] Family resolution incl. `strategy.clone` lineage
- [ ] Tests + doc

## Verification

### Tests
- Unit: identical trial → no increment; param tweak → +1; clone → inherits count.
- Integration: app role UPDATE/DELETE on `strategy.trial` fails.

### Scenarios
- Given 50 Optuna trials, when the sweep finishes, then the family count rose by 50 and DSR uses N ≥ 50.
- Given a user clones a strategy to 'start fresh', then the clone's trial count equals the parent's.

### Stress / failure injection
- n/a: insert-only counter with trivial load; covered by sweep stress in P2-T115.

## Acceptance criteria

- [ ] Counter increments automatically on every tweak and never decreases
- [ ] Count + Sharpe variance exposed to DSR
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Screener trials count too (they are tries); document that choice.
- Generator variants count against the family that the saved strategy belongs to.

## Cardinal rules (do NOT)

- Do NOT provide any API or UI to reset or decrement the trial counter.
- Do NOT update or delete WORM rows (`audit.*`); corrections are new rows referencing the original (15 §2).
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §6: trial identity and family definition.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.27 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T108-automatic-trial-counter`
- PR title: `P2-T108: Automatic, append-only trial counter per strategy family`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T108` run

## Progress log

- 2026-10-21 00:00 · planner · created
