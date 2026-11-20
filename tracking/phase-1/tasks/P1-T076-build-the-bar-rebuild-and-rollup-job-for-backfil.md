---
id: P1-T076
kind: task
title: Build the bar rebuild and rollup job for backfills and corrections
phase: 1
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T013, P1-T012]
requirements: [R1.02]
roadmap_todos: [T1.21]
modules: [M1]
dashboards: [D07]
tools: [git, cargo, supabase, docker]
mcp: []
env: []
services: [supabase-postgres, nats]
branch: p1/P1-T076-build-the-bar-rebuild-and-rollup-job-for-backfil
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/03-build-spec.md, docs/02-v1-architecture.md]
doc_sync_status: n/a
found_in: ""
created: 2026-11-19
updated: 2026-11-20
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P1-T076 · Build the bar rebuild and rollup job for backfills and corrections

## Goal / expected outcome

One idempotent job in `mt-recorder` rebuilds bars for an (instrument, time range) when history is backfilled or a late correction arrives: 1s and 1m bars from Parquet trades/quotes, then every higher standard size (5m, 15m, 1h, 4h, 1D, 1W) from 1m, upserted by key. This replaces the continuous-aggregate refresh that TimescaleDB used to do ([18 §4.3](../../../docs/18-platform-and-deployment.md#43-bars-without-timescaledb)), so backfilled and corrected periods show the same bars at every size as live-built ones.

## Context & references

- Roadmap: requirements [R1.02](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.21](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets) ("rollup job for backfills and corrections")
- Platform: [18 §4.3](../../../docs/18-platform-and-deployment.md#43-bars-without-timescaledb) (backfills and corrections re-run a rollup job that rebuilds the affected higher sizes from 1m, idempotent, upsert by key) · [18 §2.1](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates) (`mt-recorder`)
- Flow: [02 §8 F1](../../../docs/02-v1-architecture.md#8-end-to-end-flows) step 4 · [03 M1](../../../docs/03-build-spec.md#m1-market--macro-data)
- Built on: P1-T013 (bar builder logic and tables; late-data queue), P1-T012 (Parquet catalog)
- Used by: P1-T015 and P1-T022 (backfills call it after writing trades), P1-T013 (corrections later than the late-data window), P1-T058 (parity after a seeded backfill), P1-T075 (corrections to exported months)

## Requirements

- `mt-recorder rebuild --instrument … --from … --to …`: rebuilds 1s and 1m bars from the Parquet catalog's trades (or mids from quotes where no trades exist) with **the same code path** as the live builder, then rolls up 5m … 1W from 1m
- `mt-recorder rollup --instrument … --from … --to …`: rolls up 5m … 1W from existing 1m bars only (for vendor-free corrections)
- Range alignment: the job widens the range to whole buckets of the largest affected size (e.g. a correction on a Wednesday rebuilds that 1W bucket)
- Idempotent: upsert by (instrument, event_time) per size; running twice gives byte-identical rows; concurrent runs on overlapping ranges are serialised by an advisory lock per instrument
- Triggers: a NATS request `md.rollup.request` (from `mt-connectors` backfill jobs and the late-data queue) and the CLI; backfill jobs (P1-T015, P1-T022) call it through the request subject or as a follow-on `mt-scheduler` job, never by writing higher sizes themselves
- Vendor bars (`market.bar_*_vendor`) are never rolled into built bars
- Each run logs (instrument, range, sizes, rows written) to `ops.bar_rollup_run` and a metric `mt_bar_rollup_rows_total`

## ToDo

- [ ] Implement `rebuild` and `rollup` subcommands and the `md.rollup.request` handler in `crates/mt-recorder`, sharing the live builder's aggregation code
- [ ] Supabase migration for `ops.bar_rollup_run`; pgTAP test
- [ ] Advisory locking and bucket-aligned ranges
- [ ] Wire the P1-T013 late-data queue to the handler
- [ ] Write the tests listed under Verification
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- `cargo test -p mt-recorder rollup`: rollup of 1m into 5m … 1W equals direct aggregation of the 1m rows (exact, `rust_decimal`)
- `cargo test -p mt-recorder rebuild_matches_live`: a recorded hour replayed live and rebuilt offline gives identical bars at every size
- `cargo test -p mt-recorder rollup_idempotent`: two runs → identical rows; overlapping concurrent runs → no duplicates
- `supabase test db`: `ops.bar_rollup_run` grants and columns

### Scenarios

- Given a Binance backfill writes a past day's trades to Parquet, when it requests a rebuild, then that day's 1s … 1D bars and the containing 1W bar exist and match a rebuild from ticks
- Given a trade arrives 30 s late, when the late-data queue hands it over, then the affected 1s/1m bars and every higher size are corrected
- Given vendor 1m bars for a day, when the rollup runs, then built bars are unchanged

### Stress / failure injection

- Load: rebuild 30 days of 1s bars for one liquid symbol within 10 min on the workstation
- Fault: kill the job mid-range; the re-run completes the range with no duplicates or gaps

## Acceptance criteria

- [ ] Backfilled and corrected ranges show the same bars at every standard size as a rebuild from ticks
- [ ] The job is idempotent and serialised per instrument
- [ ] CI green (`cargo clippy`, `cargo test`, `supabase test db`, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Range in an exported month (P1-T075): the job re-imports the partition, corrects it and re-exports, logged
- Trades missing in Parquet for part of the range: the job rebuilds what exists and reports the gap; it never fabricates bars

## Cardinal rules (do NOT)

- Do NOT use floats for prices or sizes; `numeric` / `rust_decimal` only ([02 §5.2](../../../docs/02-v1-architecture.md#52-key-conventions))
- Do NOT mix vendor bars into built bars
- Do NOT use TimescaleDB, continuous aggregates or `time_bucket` ([18 §4.2](../../../docs/18-platform-and-deployment.md#42-extensions))
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT bypass `mt-api`, the risk manager (M11) or `pit(as_of)` (`mt-store`, also through its Python binding); research and backtest reads go through `pit` only.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.21 once every task traced to it in PHASE.md is done; note P1-T076 next to it.
- `docs/03-build-spec.md` §M1: name the rebuild/rollup commands and their triggers
- `docs/02-v1-architecture.md` §8 F1: confirm the backfill/correction path in step 4

## Branch & PR

- Branch: `p1/P1-T076-build-the-bar-rebuild-and-rollup-job-for-backfil`
- PR title: `P1-T076: Build the bar rebuild and rollup job for backfills and corrections`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T076` run

## Progress log

- 2026-11-19 00:00 · aligner · created in the re-platform wave per docs/18 §4.3 (no task owned the rollup job that replaces continuous-aggregate refreshes for backfills and corrections)
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (callers are the Rust `mt-connectors` backfill jobs on `mt-scheduler`, not Prefect flows)
