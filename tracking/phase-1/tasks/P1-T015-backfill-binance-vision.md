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
depends_on: [P1-T012, P1-T013, P1-T006, P1-T076, P1-T078]
requirements: [R1.03]
roadmap_todos: [T1.22]
modules: [M1]
dashboards: [D07]
tools: [git, cargo, docker]
mcp: []
env: []
services: [supabase-postgres]
branch: p1/P1-T015-backfill-binance-vision
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/03-build-spec.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-11-20
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P1-T015 · Backfill crypto history from data.binance.vision

## Goal / expected outcome

A resumable `mt-connectors` job (Rust; run as an `mt-scheduler` backfill run, schedule in P1-T053) downloads trades, aggTrades and 1s klines for universe symbols from data.binance.vision, verifies checksums, writes them into the Parquet catalog, asks the rebuild/rollup job (P1-T076) to build our bars for the backfilled range, and produces a backfill report.

## Context & references

- Roadmap: requirements [R1.03](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.22](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M1](../../../docs/03-build-spec.md#m1-market--macro-data--mt_datamarket) (History: data.binance.vision trades, aggTrades, klines down to 1s) · [06 §3 Market data](../../../docs/06-aggregators-and-market-providers.md#market-data-m1) (top pick)
- Verified by: backfill report (R1.03)
- Depends on (this phase): P1-T012, P1-T013, P1-T006, P1-T076, P1-T078 (`mt-connectors` base)
- Platform: [18 §2.1](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates) (`mt-connectors` covers data.binance.vision)

## Requirements

- Download monthly then daily ZIPs per (symbol, type), verify the `.CHECKSUM` (SHA-256) before use
- Write trades/aggTrades to the catalog (`source=binance_vision`, through the `mt-connectors` `pit` writer and the `mt-store` catalog helpers) and 1s klines to `market.bar_1s_vendor` (`bar_source=vendor_kline`), never into the built bars; then request `mt-recorder rebuild` for the range (P1-T076), which builds 1s/1m from the trades and rolls up 5m … 1W ([18 §4.3](../../../docs/18-platform-and-deployment.md#43-bars-without-timescaledb)); overlaps are compared in P1-T058
- Resumable: the shared manifest `ops.backfill_job` (P1-T078) records (job, symbol, type, date, status, sha256) so restarts skip done files
- Polite download rate through the quota tracker; run as an `mt-scheduler` backfill run (kind `backfill`, visible in `/lab/jobs?kind=backfill` and the D16 Jobs widget)
- Report: per symbol/type, date range covered, missing days, row counts, checksum failures → stored and shown in D07 Storage

## ToDo

- [ ] Implement the `binance_vision` provider in `mt-connectors`: downloader, checksum verifier and loaders (manifest from P1-T078)
- [ ] Expose progress for `/lab/jobs?kind=backfill`
- [ ] Write report generator (Markdown + JSON) saved under `reports/backfill/`
- [ ] Write the tests listed under Verification
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- `cargo test -p mt-connectors binance_vision`: checksum mismatch → file rejected and retried once; manifest resume logic
- Integration: fixture ZIPs → catalog + bars; re-run is a no-op

### Scenarios

- Given a missing daily file on the server, when the job runs, then the report lists the date as missing and the job still completes
- Given the job is killed mid-month, when re-run, then it continues from the manifest

### Stress / failure injection

- Load: one year of 1s klines for 10 symbols completes within the quota and the storage budget estimate (recorded in the report)

## Acceptance criteria

- [ ] Backfill report exists for the universe with ≥ 1 year of trades/aggTrades/1s klines (or the full listed history if shorter)
- [ ] All files checksum-verified
- [ ] CI green (`cargo clippy`, `cargo test`, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Symbols renamed on Binance: map through the instrument master's successor link
- Spot vs USDⓈ-M paths differ; both supported

## Cardinal rules (do NOT)

- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).
- Do NOT bypass `mt-api`, the risk manager (M11) or `pit(as_of)` (`mt-store`, also through its Python binding); research and backtest reads go through `pit` only.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.22 once every task traced to it in PHASE.md is done; note P1-T015 next to it.
- `docs/03-build-spec.md` §M1: link the backfill report location

## Branch & PR

- Branch: `p1/P1-T015-backfill-binance-vision`
- PR title: `P1-T015: Backfill crypto history from data.binance.vision`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T015` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (vendor klines in market.bar_1s_vendor so aggregates stay pure; keyless public source)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (stays a Python Prefect flow; built bars for the backfilled range come from the rebuild/rollup job P1-T076 (new dep), vendor klines stay separate; services supabase-postgres)
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (Python Prefect flow → `mt-connectors` provider (Rust) run as an `mt-scheduler` backfill; shared manifest from P1-T078; deps +P1-T078; tools cargo; services drop prefect-server)
