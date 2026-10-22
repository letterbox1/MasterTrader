---
id: P2-T164
kind: task
title: Verify validation harness with known-answer and null-strategy tests
phase: 2
type: VERIFY
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T114, P2-T115]
requirements: [R2.41, R2.42, R2.44]
roadmap_todos: [T2.27]
modules: [M7]
dashboards: [D04]
tools: [uv, docker]
mcp: []
env: []
services: [nats, postgres]
branch: p2/P2-T164-verify-harness-known-answers
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T164 · Verify validation harness with known-answer and null-strategy tests

## Goal / expected outcome

An independent test pack proving the harness rejects what it should: random strategies fail, overfit sweep winners are deflated, survivorship-biased universes are detected and fixed-bps slippage is refused — so a 'validated' badge can be trusted.

## Context & references

- Roadmap: [R2.41, R2.42, R2.44](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) ('Harness tests') · ToDo T2.27
- [14 §6](../../../docs/14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) · [03 §8](../../../docs/03-build-spec.md#8-promotion-gates-per-strategy-configurable)

## Requirements

- Null test: 100 random-entry strategies on BTC 1h over 3 years → ≥ 95% fail the gate set at defaults; MC p-values ~uniform.
- Overfit test: 500-trial sweep on a noise-only strategy → best in-sample Sharpe high, DSR < 0.95, worst fold negative.
- Survivorship test: momentum on a top-20 universe with delisted coins removed vs kept → kept version has lower return; the harness flags universes without delisted members as 'survivorship risk'.
- Cost test: illiquid instrument with fixed-bps slippage config → refused (14 §6).
- Planted-edge test: synthetic series with a real lagged edge → strategy passes all gates (no false rejection).

## ToDo

- [ ] Write `tests/harness/` scenarios with synthetic data generators
- [ ] Run and record results
- [ ] File bugs for any wrong verdict

## Verification

### Tests
- The scenarios above as CI-slow tests (nightly).

### Scenarios
- Given the planted-edge series with 2× costs, then it still passes; at 10× costs it fails (sanity).

### Stress / failure injection
- Nightly run time ≤ 90 min on 4 workers; failure to finish is itself a failure.

## Acceptance criteria

- [ ] Null, overfit, survivorship, cost and planted-edge tests give the expected verdicts
- [ ] Nightly job green

## Exceptions & edge cases

- Random seeds fixed and recorded so failures reproduce.

## Cardinal rules (do NOT)

- Do NOT adjust gate defaults to make these tests pass; fix the harness.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §6: link the evidence pack.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.27 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T164-verify-harness-known-answers`
- PR title: `P2-T164: Verify validation harness with known-answer and null-strategy tests`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T164` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (run fields (no decision change))
