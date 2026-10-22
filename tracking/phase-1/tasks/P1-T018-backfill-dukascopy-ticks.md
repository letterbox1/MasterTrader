---
id: P1-T018
kind: task
title: Backfill Dukascopy ticks with a bi5 parser
phase: 1
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T012, P1-T006]
requirements: [R1.04]
roadmap_todos: [T1.22]
modules: [M1]
dashboards: [D07]
tools: [git, uv, docker]
mcp: []
env: []
services: [prefect-server]
branch: p1/P1-T018-backfill-dukascopy-ticks
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/03-build-spec.md, docs/06-aggregators-and-market-providers.md]
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

# P1-T018 · Backfill Dukascopy ticks with a bi5 parser

## Goal / expected outcome

A resumable flow downloads Dukascopy hourly `.bi5` tick files for universe FX/metals, decodes them with our own parser, and stores them in the Parquet catalog as the FX reference history; TrueFX/HistData hooks exist for cross-checks.

## Context & references

- Roadmap: requirements [R1.04](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.22](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M1](../../../docs/03-build-spec.md#m1-market--macro-data--mt_datamarket) (Dukascopy historical ticks, TrueFX/HistData for cross-checks) · [03 §6](../../../docs/03-build-spec.md#6-smallest-free-timeframe-by-asset-class) (Dukascopy is the FX reference) · [06 §3 Skip list](../../../docs/06-aggregators-and-market-providers.md#skip-list) (`duka` is dead; dukascopy-node or own bi5 parser)
- Depends on (this phase): P1-T012, P1-T006

## Requirements

- Own Python bi5 parser (LZMA-compressed 20-byte records: ms offset, ask, bid, ask vol, bid vol; point size per instrument, e.g. 1e-5 for EURUSD, 1e-3 for JPY pairs, metals per instrument metadata)
- Download per hour `.../{SYMBOL}/{YYYY}/{MM-1}/{DD}/{HH}h_ticks.bi5` (month is zero-based), politely via the quota tracker; empty files are valid (no ticks)
- Store in catalog as quote ticks with `source=dukascopy`, `licence=personal`; manifest in `ops.backfill_job`
- Optional cross-check adapters for TrueFX/HistData monthly files (gated on the P1-T056 TrueFX check); output a daily mid-diff report

## ToDo

- [ ] Implement and unit-test the bi5 decoder against known files (fixtures checked into tests)
- [ ] Implement the downloader + manifest + loader
- [ ] Implement the cross-check report (daily mean/max mid diff in bps vs OANDA recorded quotes)
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Unit: decoder golden test (known hour → known first/last tick and count); zero-based month path
- Integration: fixture hour → catalog rows; re-run idempotent

### Scenarios

- Given a weekend hour, when downloaded, then an empty file yields zero rows and is marked done
- Given a corrupt LZMA stream, when parsed, then the hour is marked failed and retried once, then reported

### Stress / failure injection

- Load: one year of EURUSD ticks backfills within quota; report time and bytes

## Acceptance criteria

- [ ] ≥ 1 year of ticks for universe FX/metal pairs in the catalog with a backfill report
- [ ] Cross-check report produced for at least one week where OANDA quotes were recorded
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- DST: Dukascopy hours are UTC; no local-time conversion
- Instrument point sizes differ; read from metadata, never hard-code a single divisor

## Cardinal rules (do NOT)

- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file (kept outside the repo) mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; research and backtest reads go through `pit` only.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.22 once every task traced to it in PHASE.md is done; note P1-T018 next to it.
- `docs/03-build-spec.md` §M1: note "own bi5 parser" choice
- `docs/06-aggregators-and-market-providers.md` §3: note the cross-check result

## Branch & PR

- Branch: `p1/P1-T018-backfill-dukascopy-ticks`
- PR title: `P1-T018: Backfill Dukascopy ticks with a bi5 parser`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T018` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (run fields; keyless public source)
