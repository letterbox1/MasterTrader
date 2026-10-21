---
id: P1-T015
kind: task
title: Backfill crypto history from data.binance.vision
phase: 1
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T012, P1-T013, P1-T006]
requirements: [R1.03]
roadmap_todos: [T1.22]
modules: [M1]
dashboards: [D07]
branch: p1/P1-T015-backfill-binance-vision
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/03-build-spec.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P1-T015 · Backfill crypto history from data.binance.vision

## Goal / expected outcome

A resumable Prefect flow downloads trades, aggTrades and 1s klines for universe symbols from data.binance.vision, verifies checksums, writes them into the Parquet catalog and bar tables, and produces a backfill report.

## Context & references

- Roadmap: requirements [R1.03](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.22](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M1](../../../docs/03-build-spec.md#m1-market--macro-data--mt_datamarket) (History: data.binance.vision trades, aggTrades, klines down to 1s) · [06 §3 Market data](../../../docs/06-aggregators-and-market-providers.md#market-data-m1) (top pick)
- Verified by: backfill report (R1.03)
- Depends on (this phase): P1-T012, P1-T013, P1-T006

## Requirements

- Download monthly then daily ZIPs per (symbol, type), verify the `.CHECKSUM` (SHA-256) before use
- Write trades/aggTrades to the catalog (`source=binance_vision`) and 1s klines to `market.bar_1s` with `bar_source=vendor_kline`; never overwrite live-recorded bars, store side by side and flag overlaps for P1-T058
- Resumable: a manifest table `ops.backfill_job` (job, symbol, type, date, status, sha256) so restarts skip done files
- Polite download rate through the quota tracker; run as `data.backfill.run` job kind `backfill`
- Report: per symbol/type, date range covered, missing days, row counts, checksum failures → stored and shown in D07 Storage

## ToDo

- [ ] Implement downloader, checksum verifier, loaders and manifest
- [ ] Expose progress for `/lab/jobs?kind=backfill`
- [ ] Write report generator (Markdown + JSON) saved under `reports/backfill/`
- [ ] Write the tests listed under Verification
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Unit: checksum mismatch → file rejected and retried once; manifest resume logic
- Integration: fixture ZIPs → catalog + bars; re-run is a no-op

### Scenarios

- Given a missing daily file on the server, when the flow runs, then the report lists the date as missing and the job still completes
- Given the job is killed mid-month, when re-run, then it continues from the manifest

### Stress / failure injection

- Load: one year of 1s klines for 10 symbols completes within the quota and the storage budget estimate (recorded in the report)

## Acceptance criteria

- [ ] Backfill report exists for the universe with ≥ 1 year of trades/aggTrades/1s klines (or the full listed history if shorter)
- [ ] All files checksum-verified
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Symbols renamed on Binance: map through the instrument master's successor link
- Spot vs USDⓈ-M paths differ; both supported

## Cardinal rules (do NOT)

- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; research and backtest reads go through `pit` only.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.22 once every task traced to it in PHASE.md is done; note P1-T015 next to it.
- `docs/03-build-spec.md` §M1: link the backfill report location

## Branch & PR

- Branch: `p1/P1-T015-backfill-binance-vision`
- PR title: `P1-T015: Backfill crypto history from data.binance.vision`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T015` run

## Progress log

- 2026-10-21 00:00 · planner · created
