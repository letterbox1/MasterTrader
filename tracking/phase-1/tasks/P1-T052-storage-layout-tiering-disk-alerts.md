---
id: P1-T052
kind: task
title: Set up hot/cold storage tiers, compaction schedule and disk alerts
phase: 1
type: OPS
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T012]
requirements: [R1.N3]
roadmap_todos: [T1.40]
modules: [M1, M17]
dashboards: [D07, D16]
branch: p1/P1-T052-storage-layout-tiering-disk-alerts
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

# P1-T052 · Set up hot/cold storage tiers, compaction schedule and disk alerts

## Goal / expected outcome

Parquet lives on NVMe for 90 days then moves to the HDD cold tier automatically, compaction runs on schedule, disk growth is projected against the ~0.3–1 TB/year budget, and disk alerts fire before anything fills up.

## Context & references

- Roadmap: requirements [R1.N3](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.40](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Budget: R1.N3 · [03 M1](../../../docs/03-build-spec.md#m1-market--macro-data--mt_datamarket) (storage budget) · [03 §2](../../../docs/03-build-spec.md#2-target-environment) (2–4 TB NVMe + HDD) · [02 §5.1](../../../docs/02-v1-architecture.md#51-stores) (hot NVMe 90 days → cold HDD; restic for cold)
- L2 granularity vs budget: P1-B002
- Depends on (this phase): P1-T012

## Requirements

- Mounts: `/data/hot` (NVMe, ext4/xfs, noatime) and `/data/cold` (HDD); catalog paths resolve across tiers transparently for DuckDB/Nautilus readers
- Tiering flow daily: move compacted files older than 90 days to cold, verify checksum, then delete hot copy; restic backup of cold tier (P0 backup infra)
- Metrics: bytes per tier/venue/type, daily growth, 30-day projection to 1 year; Timescale chunk/compression stats
- Alerts: hot tier > 75% warning, > 85% critical; projected yearly growth > 1 TB warning; HDD SMART failure warning; Postgres volume > 80%
- Recorder backpressure: if hot > 95%, stop recording L2 first (lowest priority), then quotes, never trades; alert

## ToDo

- [ ] Configure mounts and paths in Compose/host docs
- [ ] Implement tiering flow with verification and the backpressure policy
- [ ] Prometheus exporters/rules and Grafana storage panels; D07 Storage tab data
- [ ] Write the tests listed under Verification
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Integration: files older than 90 days move to cold and remain readable through the catalog helper
- Unit: projection maths; backpressure order L2 → quotes → never trades

### Scenarios

- Given the HDD is unmounted, when tiering runs, then it aborts without deleting hot copies and alerts

### Stress / failure injection

- Fault: fill a test hot volume to 96%; recorder sheds L2 then quotes, trades continue, alert fires, recovery resumes L2

## Acceptance criteria

- [ ] Tiering and alerts work in tests; projected yearly growth visible and inside the budget for the universe
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Reads spanning tiers (e.g. a 120-day backtest) work without manual copying

## Cardinal rules (do NOT)

- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.40 once every task traced to it in PHASE.md is done; note P1-T052 next to it.
- `docs/02-v1-architecture.md` §5.1: actual tier paths and alert thresholds
- `docs/03-build-spec.md` §M1: measured bytes/day per symbol vs budget

## Branch & PR

- Branch: `p1/P1-T052-storage-layout-tiering-disk-alerts`
- PR title: `P1-T052: Set up hot/cold storage tiers, compaction schedule and disk alerts`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T052` run

## Progress log

- 2026-10-21 00:00 · planner · created
