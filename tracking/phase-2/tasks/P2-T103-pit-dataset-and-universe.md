---
id: P2-T103
kind: task
title: Point-in-time dataset builder and survivorship-free universes
phase: 2
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T101]
requirements: [R2.41]
roadmap_todos: [T2.27]
modules: [M7]
dashboards: [D04]
branch: p2/P2-T103-pit-dataset-and-universe
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

# P2-T103 · Point-in-time dataset builder and survivorship-free universes

## Goal / expected outcome

One `mt_lab.data` layer that every backtest, feature job and tier-A training job uses to get bars/ticks/L2 for a data range and `as_of`, with survivorship-free universes, a single UTC bar-close convention and a content hash, so all results are point-in-time and reproducible.

## Context & references

- Roadmap: [R2.41](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.27
- Rules: [14 §6 backtest engine requirements](../../../docs/14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) · [SPEC NN1](../../../SPEC.md#non-negotiable-requirements) · [03 §4 point-in-time rule](../../../docs/03-build-spec.md#4-data-model-overview)
- [14 §4 porting pitfalls](../../../docs/14-strategy-evidence-and-validation.md#4-trading-methods-enforced-in-code-defaults-user-editable-in-d06): fixed UTC daily cut for 24/7 crypto
- Cross-phase: P0 T0.22 `pit(as_of)` + Parquet catalog helpers; P1 T1.21/T1.22 bars and backfills; `market.instrument` listing/delisting dates

## Requirements

- `DatasetSpec(instruments|universe_rule, bar_specs, start, end, as_of, resolution)` → `Dataset` with a SHA-256 `data_hash` over the exact rows/files read.
- All reads through `mt_store.pit(as_of)` (Timescale) and catalog helpers (Parquet ticks/L2); anything with `ingest_time > as_of` is excluded and counted for the D04 point-in-time audit.
- Universe rules resolve membership as of each rebalance date, keeping delisted, rugged and dead instruments (14 §6); a universe that silently drops them fails a test.
- One timezone (UTC) and one bar-close convention: bars are labelled by close time; daily bars for 24/7 markets cut at 00:00 UTC; session markets use `exchange_calendars`.
- Multi-timeframe requests are aligned so a higher-timeframe bar is visible only after its close (no partial-bar leakage).
- Rows with `display_ok`/`train_ok` flags are carried through so tier-A training (P2-T125) can refuse `train_ok = false` rows.

## ToDo

- [ ] Implement `mt_lab/data.py`: `DatasetSpec`, `Dataset`, hashing, pit + catalog readers
- [ ] Implement universe resolver using `market.instrument` listed/delisted dates and venue status history
- [ ] Implement bar-close alignment helper for multi-timeframe and the UTC daily cut
- [ ] Record PIT audit counts (rows excluded by as_of) on the dataset for D04 'Bias checks'
- [ ] Tests incl. a delisted-coin fixture and a multi-timeframe alignment fixture
- [ ] Doc the convention in 14 §6 / 03 M7

## Verification

### Tests
- Unit: hash stable across runs; alignment helper never exposes the 1D bar before 00:00 UTC close.
- Integration: fixture with an instrument delisted mid-range stays in the universe until delisting and its final loss is counted.
- `pit` CI bypass test covers `mt_lab.data`.

### Scenarios
- Given a top-20 momentum universe for 2022, when resolved, then LUNA/FTT-style delisted names appear until their delisting date.
- Given a row back-filled later (ingest_time after as_of), when the dataset is built with that as_of, then the row is excluded and the audit count is 1.
- Given a request for 1m bars on an instrument whose finest resolution is 1D, then the request is refused with the native minimum reported.

### Stress / failure injection
- Build a 2-year 1m dataset for 10 crypto symbols (~10M rows) in < 2 min with streaming reads; RSS < 4 GB.
- Missing Parquet file mid-range: dataset build fails with the gap listed (never silently shortened).

## Acceptance criteria

- [ ] Survivorship and alignment fixtures pass
- [ ] Every backtest stores `data_hash`; same spec → same hash
- [ ] PIT exclusion count exposed for D04
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- DST changes for session markets handled by `exchange_calendars`; crypto ignores DST.
- Instrument symbol changes (rebrands) map through instrument ids, not tickers.
- Bad-DQ periods (`audit.dq_event` severity bad) are marked so engines can skip trading there.

## Cardinal rules (do NOT)

- Do NOT drop delisted/rugged instruments from historical universes.
- Do NOT fill forward across a data gap without marking it.
- Do NOT read research/backtest data except through `mt_store.pit(as_of=…)`; the `pit` CI bypass test must stay green.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §6: state the UTC bar-close convention used.
- `docs/03-build-spec.md` M7: dataset hash.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.27 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T103-pit-dataset-and-universe`
- PR title: `P2-T103: Point-in-time dataset builder and survivorship-free universes`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T103` run

## Progress log

- 2026-10-21 00:00 · planner · created
