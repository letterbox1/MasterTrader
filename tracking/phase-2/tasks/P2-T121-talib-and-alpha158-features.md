---
id: P2-T121
kind: task
title: TA-Lib and Alpha158 core feature sets
phase: 2
type: BUILD
status: backlog
priority: medium
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T120]
requirements: [R2.46]
roadmap_todos: [T2.29]
modules: [M6]
dashboards: [D03, D04]
branch: p2/P2-T121-talib-and-alpha158-features
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

# P2-T121 · TA-Lib and Alpha158 core feature sets

## Goal / expected outcome

The core market feature library: TA-Lib indicators and the Qlib Alpha158 factor set registered as versioned features with batch/incremental parity, ready for templates, the lab and tier A.

## Context & references

- Roadmap: [R2.46](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.29
- [03 M6 market and factor features](../../../docs/03-build-spec.md#m6-features--mt_features) · licences in [01](../../../docs/01-repo-vetting-report.md) (Qlib MIT; Vibe-Trading MIT bundles Qlib factors under Apache-2.0 — keep NOTICE; TA-Lib BSD)
- Vibe-Trading factor zoo is optional/out of P2 scope; tracked for later

## Requirements

- TA-Lib set: SMA/EMA/WMA, RSI, MACD, ATR, ADX, Bollinger, Stoch, OBV, CCI, ROC, MFI (+ any used by templates), registered as `ta.<name>` with params.
- Alpha158 set: the 158 Qlib expressions (KBAR, price, volume, rolling ops windows 5/10/20/30/60) ported as pure pandas/numpy expressions, registered as `alpha158.<name>` v1.
- All incremental implementations pass the parity harness (P2-T120) or are marked `batch_only=true` with a reason.
- Computation from OHLCV via `pit`; no Yahoo/Qlib prebuilt dataset used (personal-terms data excluded).

## ToDo

- [ ] Wrap TA-Lib (pinned) as registry features with incremental counterparts
- [ ] Port Alpha158 expressions into `mt_features/alpha158.py` with attribution/NOTICE
- [ ] Parity tests for each feature; golden values vs Qlib reference on a fixture
- [ ] Record licences in `third_party/LICENSES.md`

## Verification

### Tests
- Golden: each Alpha158 feature equals the Qlib reference implementation on a fixture to 1e-8.
- Parity: incremental vs batch for every TA-Lib feature marked incremental.

### Scenarios
- Given a 1D bar strategy subscribing to `ta.atr(14)`, when run in backtest and paper, then values match bar-for-bar.

### Stress / failure injection
- Alpha158 batch for 30 symbols × 5 years daily in < 3 min on 4 cores.

## Acceptance criteria

- [ ] TA-Lib and Alpha158 features registered with versions
- [ ] Golden + parity tests pass
- [ ] Licences recorded
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Instruments without volume (FX spot): volume features return NaN with `unsupported=true`.
- Different session calendars: rolling windows count bars, not calendar days (documented).

## Cardinal rules (do NOT)

- Do NOT use Yahoo/Qlib prebuilt datasets as feature inputs.
- Do NOT add telemetry or referral IDs via vendored code; pin images by digest; record vendored code in `third_party/LICENSES.md`.
- Do NOT add paid data/APIs or services; free tiers and self-hosted components only (03 §1).
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/03-build-spec.md` M6: feature set list v1.
- `third_party/LICENSES.md`: Qlib/Vibe-Trading NOTICE.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.29 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T121-talib-and-alpha158-features`
- PR title: `P2-T121: TA-Lib and Alpha158 core feature sets`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T121` run

## Progress log

- 2026-10-21 00:00 · planner · created
