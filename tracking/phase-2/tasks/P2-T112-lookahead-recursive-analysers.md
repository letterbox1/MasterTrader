---
id: P2-T112
kind: task
title: Look-ahead and recursive bias analysers
phase: 2
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T105]
requirements: [R2.43]
roadmap_todos: [T2.27]
modules: [M7]
dashboards: [D04]
branch: p2/P2-T112-lookahead-recursive-analysers
pr: ""
doc_sync: [docs/03-build-spec.md, third_party/LICENSES.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T112 · Look-ahead and recursive bias analysers

## Goal / expected outcome

Automated look-ahead and recursive-indicator analysers (freqtrade's `lookahead-analysis` / `recursive-analysis` methods) that run on every validation and fail strategies whose signals change when future data is removed or whose indicators depend on start-up length.

## Context & references

- Roadmap: [R2.43](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.27 · verified by P2-T160
- [03 M7 'freqtrade analysers (vendored)'](../../../docs/03-build-spec.md#m7-research-lab--mt_lab) vs [01 §3.3 freqtrade GPL-3.0, re-implement](../../../docs/01-repo-vetting-report.md#33-freqtrade--reference-only): licence route decided in P2-B051 — default here is a clean-room re-implementation in `mt_lab/bias/`
- [D04 Bias checks tab](../../../docs/ui/dashboards/D04-research-lab.md) · [03 §8 item 3](../../../docs/03-build-spec.md#8-promotion-gates-per-strategy-configurable)

## Requirements

- Look-ahead analyser: for K sampled signal timestamps, re-run the strategy on data truncated at each timestamp; any signal/indicator value differing from the full-data run = look-ahead; report the offending signal names, timestamps and indicator columns.
- Recursive analyser: compute indicators with start-up lengths {N, 2N, 4N} bars; relative deviation > 1e-6 on the evaluation window = recursive/start-up dependence; report columns.
- Repainting check: indicator values for closed bars must not change when later bars arrive (streaming vs batch comparison).
- Results: pass/fail per analyser with details, stored on the validation run; any fail blocks the 'bias checks' gate.
- Runtime: default K = 50 sample points; ≤ 15 min for a 1h-bar strategy over 2 years.

## ToDo

- [ ] Decide licence route per P2-B051 (default: clean-room from the public docs, no GPL code copied); record in `third_party/LICENSES.md` if vendoring as an external process
- [ ] Implement `mt_lab/bias/lookahead.py`, `recursive.py`, `repaint.py` against the M0 strategy interface (works for template and code strategies)
- [ ] Register as validation sections; persist details for D04
- [ ] Fixture strategies: clean, look-ahead (uses `close.shift(-1)`), recursive (EMA without warm-up), repainting (uses the forming bar)
- [ ] Tests + docs

## Verification

### Tests
- Unit: each fixture is classified correctly (clean passes all; each buggy one fails exactly its analyser).
- Integration: analysers run on an EMA template via truth runner and pass.

### Scenarios
- Given a strategy that peeks one bar ahead, when validated, then the look-ahead analyser fails and names the signal and timestamps.
- Given an indicator that needs 200 bars warm-up but gets 50, then the recursive analyser fails with the column name.

### Stress / failure injection
- Strategy with 1m bars over 1 year: analyser sampling keeps runtime within the 15-min budget × 4 (documented) or the job times out cleanly.

## Acceptance criteria

- [ ] Four fixture strategies classified correctly
- [ ] Results visible per validation run
- [ ] Licence route recorded (P2-B051)
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Stochastic strategies: seeds fixed for both runs; remaining nondeterminism reported as 'inconclusive', which counts as fail.
- Tick/L2 strategies: truncation done on event time; sampling on events, not bars.

## Cardinal rules (do NOT)

- Do NOT copy freqtrade (GPL-3.0) source into the platform packages unless P2-B051 explicitly decides to accept GPL for this module.
- Do NOT add telemetry or referral IDs via vendored code; pin images by digest; record vendored code in `third_party/LICENSES.md`.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/03-build-spec.md` M7: replace 'vendored' with the chosen route.
- `third_party/LICENSES.md`: entry if anything is vendored.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.27 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T112-lookahead-recursive-analysers`
- PR title: `P2-T112: Look-ahead and recursive bias analysers`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T112` run

## Progress log

- 2026-10-21 00:00 · planner · created
