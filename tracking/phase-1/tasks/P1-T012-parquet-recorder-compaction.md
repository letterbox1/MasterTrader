---
id: P1-T012
kind: task
title: Build the Parquet recorder with daily compaction
phase: 1
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T010]
requirements: [R1.02, R1.N3]
roadmap_todos: [T1.21]
modules: [M1]
dashboards: [D07]
branch: p1/P1-T012-parquet-recorder-compaction
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/02-v1-architecture.md, docs/03-build-spec.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P1-T012 · Build the Parquet recorder with daily compaction

## Goal / expected outcome

A durable JetStream consumer writes every `md.*` trade, quote and L2 delta into the Nautilus `ParquetDataCatalog`, rolling files every 1–5 minutes and compacting each day into one file per (venue, symbol, type, day).

## Context & references

- Roadmap: requirements [R1.02](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.N3](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.21](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M1](../../../docs/03-build-spec.md#m1-market--macro-data--mt_datamarket) (recording pipeline) · flow [02 §8 F1](../../../docs/02-v1-architecture.md#8-end-to-end-flows) step 3 · stores [02 §5.1](../../../docs/02-v1-architecture.md#51-stores) (Parquet forever; hot NVMe 90 days → cold HDD)
- Storage budget R1.N3: ~0.3–1 TB/year for ~10 symbols at trades + L1 + L2@1s
- Depends on (this phase): P1-T010

## Requirements

- Durable pull consumer on stream `MD` with explicit ack after the file containing the message is fsynced (at-least-once; dedupe on (venue, symbol, seq) at compaction)
- Roll interval configurable 1–5 min (default 1 min for trades/L2, 5 min for quotes); files written to `/data/hot/catalog/<type>/<venue>/<symbol>/<date>/` as Nautilus-compatible Parquet (zstd)
- Daily compaction at 00:30 UTC: merge, sort by `event_time`, dedupe, verify row counts, write provenance metadata, then delete fragments
- Nanosecond timestamps kept; `ingest_time` stored next to `event_time`
- Metrics: rows/s written, consumer lag, bytes/day per venue/type (feeds the storage tab and P1-T052)

## ToDo

- [ ] Implement recorder service inside `ingest-market` (separate process) with durable consumer
- [ ] Implement compaction flow (Prefect) with verification and idempotent re-run
- [ ] Read API through `mt_store` catalog helpers (DuckDB) for P1-T058 and P2
- [ ] Write the tests listed under Verification
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Unit: roll logic; dedupe by sequence; file naming
- Integration: publish 1M synthetic messages, kill the recorder mid-file, restart → no loss, no duplicates after compaction
- Golden: compacted file for a recorded hour equals the reference row set

### Scenarios

- Given the recorder is down for 10 min, when it restarts, then it resumes from the durable consumer position (within the 24 h stream window) and nothing is lost
- Given compaction fails half-way, when re-run, then it produces the same file and fragments are only deleted after verification

### Stress / failure injection

- Load: sustain 3× the universe's peak message rate for 1 h; consumer lag stays < 30 s
- Fault: disk-full on hot tier → recorder stops acking, raises `alert.critical.disk_hot`, and resumes when space frees (no corrupt files)

## Acceptance criteria

- [ ] Zero loss and zero duplicates in the crash test
- [ ] Daily bytes per venue/type visible in Prometheus and projected yearly growth inside R1.N3
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Outage longer than the stream max age (24 h) loses data; gap report (P1-T032/T065) lists it and backfills fill what free history allows
- Clock: file partitioning uses `event_time` date (UTC), not wall-clock

## Cardinal rules (do NOT)

- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; research and backtest reads go through `pit` only.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.21 once every task traced to it in PHASE.md is done; note P1-T012 next to it.
- `docs/02-v1-architecture.md` §5.1: record roll interval and compaction time actually used
- `docs/03-build-spec.md` §M1: link the catalog layout

## Branch & PR

- Branch: `p1/P1-T012-parquet-recorder-compaction`
- PR title: `P1-T012: Build the Parquet recorder with daily compaction`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T012` run

## Progress log

- 2026-10-21 00:00 · planner · created
