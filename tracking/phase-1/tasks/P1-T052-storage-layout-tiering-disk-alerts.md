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
tools: [git, cargo, docker]
mcp: []
env: []
services: [supabase-postgres, mt-scheduler, prometheus]
branch: p1/P1-T052-storage-layout-tiering-disk-alerts
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/02-v1-architecture.md, docs/03-build-spec.md]
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

# P1-T052 · Set up hot/cold storage tiers, compaction schedule and disk alerts

## Goal / expected outcome

Parquet lives on NVMe for 90 days then moves to the HDD cold tier automatically, compaction runs on schedule, disk growth is projected against the ~0.3–1 TB/year budget, and disk alerts fire before anything fills up.

## Context & references

- Roadmap: requirements [R1.N3](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.40](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Budget: R1.N3 · [03 M1](../../../docs/03-build-spec.md#m1-market--macro-data) (storage budget) · [03 §2](../../../docs/03-build-spec.md#2-target-environment) (2–4 TB NVMe + HDD) · [02 §5.1](../../../docs/02-v1-architecture.md#51-stores) (hot NVMe 90 days → cold HDD; restic for cold)
- L2 policy: native diffs only for ≤ 3 order-book symbols by default, others 1 s snapshots ([17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P1-B002); budget recalculated from the soak (P1-T065)
- Depends on (this phase): P1-T012

## Requirements

- Mounts: `/data/hot` (NVMe, ext4/xfs, noatime) and `/data/cold` (HDD); catalog paths resolve across tiers transparently for the `mt-store` catalog readers (Rust and its Python binding) and Nautilus; on the workstation these are directories on whatever disks you have (a separate HDD is optional, [18 §9](../../../docs/18-platform-and-deployment.md#9-workstation-first-build-path))
- Tiering job daily (`mt-recorder tier`, Rust, an `mt-scheduler` job; schedule in P1-T053): move compacted files older than 90 days (default, configurable) to cold, verify checksum, then delete hot copy; restic backup of cold tier (P0 backup infra)
- Metrics: bytes per tier/venue/type, daily growth, 30-day projection to 1 year; bar partition sizes and the Parquet hot-window export (P1-T075)
- Alerts (defaults, configurable): hot tier > 75% warning, > 85% critical; projected yearly growth > 1 TB warning; HDD SMART failure warning; Supabase Postgres volume > 80%
- Recorder backpressure: if hot > 95%, stop recording L2 first (lowest priority), then quotes, never trades; alert

## ToDo

- [ ] Configure mounts and paths in Compose and the workstation setup docs
- [ ] Implement the tiering job in `crates/mt-recorder` with verification and the backpressure policy
- [ ] Prometheus exporters/rules and Grafana storage panels; D07 Storage tab data
- [ ] Write the tests listed under Verification
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Run: `cargo test -p mt-recorder tiering`, `cargo clippy`
- Integration: files older than 90 days move to cold and remain readable through the catalog helper
- Unit: projection maths; backpressure order L2 → quotes → never trades

### Scenarios

- Given the HDD is unmounted, when tiering runs, then it aborts without deleting hot copies and alerts

### Stress / failure injection

- Fault: fill a test hot volume to 96%; recorder sheds L2 then quotes, trades continue, alert fires, recovery resumes L2

## Acceptance criteria

- [ ] Tiering and alerts work in tests; projected yearly growth visible and inside the budget for the universe
- [ ] CI green (`cargo clippy`, `cargo test`, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Reads spanning tiers (e.g. a 120-day backtest) work without manual copying

## Cardinal rules (do NOT)

- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file (kept outside the repo) mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
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
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (L2 policy (P1-B002); thresholds as configurable defaults)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (tiering job in Rust `mt-recorder`; partition stats replace Timescale compression stats; workstation disks; tools cargo; services supabase-postgres)
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (tiering job scheduled by `mt-scheduler`; services prefect-server → mt-scheduler)
