---
id: P2-T110
kind: task
title: MC permutation, bootstrap Sharpe CI and deflated Sharpe
phase: 2
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T106, P2-T108]
requirements: [R2.42]
roadmap_todos: [T2.27]
modules: [M7]
dashboards: [D04, D03]
branch: p2/P2-T110-permutation-bootstrap-deflated-sharpe
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/03-build-spec.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T110 · MC permutation, bootstrap Sharpe CI and deflated Sharpe

## Goal / expected outcome

Robustness statistics for every validated strategy: a Monte Carlo permutation p-value, a bootstrap Sharpe confidence interval and the deflated Sharpe ratio computed from per-period Sharpe, observation count, skew/kurtosis and the automatic trial counter.

## Context & references

- Roadmap: [R2.42](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.27
- [14 §6 gate 2](../../../docs/14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) (DSR inputs; pass > 0.95) · [03 §8 item 2](../../../docs/03-build-spec.md#8-promotion-gates-per-strategy-configurable) (MC permutation p < 0.05) — threshold conflict tracked in P2-B050
- [01 §3.4](../../../docs/01-repo-vetting-report.md#34-hkudsvibe-trading--research-and-strategy-generation-layer): Vibe-Trading `validation.py` (MIT) as a reference implementation
- Inputs from P2-T106 (per-period returns) and P2-T108 (trial count, Sharpe variance across trials)

## Requirements

- MC permutation: ≥ 1,000 permutations (default 2,000) of signal-to-return alignment (or trade-order shuffling for path stats); p-value = share of permuted Sharpe ≥ observed; seeded.
- Bootstrap Sharpe CI: stationary block bootstrap (block length auto from autocorrelation), 5,000 resamples, 95% CI.
- Deflated Sharpe (Bailey & López de Prado 2014): uses per-period (not annualised) Sharpe, T observations, skewness, kurtosis, N = trial count, variance of Sharpe across trials; returns a probability in [0,1].
- Thresholds configurable per strategy (03 §8 'configurable'); defaults MC p < 0.05 and DSR > 0.95 pending P2-B050.
- All results stored with the inputs used (N, T, skew, kurt) so the D04 Robustness tab can show them.

## ToDo

- [ ] Implement `mt_lab/validation/stats.py`: permutation test, block bootstrap, PSR/DSR
- [ ] Wire inputs from metrics + trial counter; persist results
- [ ] Known-answer tests against published DSR examples and a random-signal fixture
- [ ] Doc formulas and defaults

## Verification

### Tests
- Known-answer: DSR reproduces the worked example in Bailey & López de Prado (2014) to 1e-4.
- Property: on 200 random-signal strategies the permutation p-values are ~uniform (KS test p > 0.01).
- Unit: DSR decreases monotonically as N (trial count) increases, all else equal.

### Scenarios
- Given a strategy found after 500 trials with annualised Sharpe 1.2 over 2 years, when DSR is computed, then it is well below 0.95 and the gate fails.
- Given an annualised Sharpe accidentally passed in, then a guard detects a periods/year mismatch and raises.

### Stress / failure injection
- 10,000 permutations on a 5-year daily series in < 60 s using vectorised numpy on 4 cores.

## Acceptance criteria

- [ ] Permutation, bootstrap CI and DSR stored per validation run
- [ ] Known-answer and uniformity tests pass
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Non-normal returns: DSR uses sample skew/kurtosis; document that heavy tails lower it.
- Zero-trade or constant series: statistics 'undefined', gate fails with reason.

## Cardinal rules (do NOT)

- Do NOT compute DSR without the automatic trial count.
- Do NOT change the RNG seed between a run and its re-run.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §6: formulas, permutation count, bootstrap method.
- `docs/03-build-spec.md` §8: confirmed thresholds after P2-B050.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.27 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T110-permutation-bootstrap-deflated-sharpe`
- PR title: `P2-T110: MC permutation, bootstrap Sharpe CI and deflated Sharpe`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T110` run

## Progress log

- 2026-10-21 00:00 · planner · created
