---
id: P1-T053
kind: task
title: Schedule the batch jobs on mt-scheduler by source update time in AEST/AEDT
phase: 1
type: OPS
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T077, P1-T078, P1-T006, P1-T008, P1-T009, P1-T012, P1-T015, P1-T018, P1-T019, P1-T020, P1-T022, P1-T023, P1-T024, P1-T025, P1-T026, P1-T027, P1-T028, P1-T029, P1-T037, P1-T052, P1-T071, P1-T075, P1-T076]
requirements: [R1.06, R1.08, R1.18, R1.19]
roadmap_todos: [T1.41]
modules: [M1, mt-scheduler, mt-connectors]
dashboards: [D07, D16]
tools: [git, cargo, docker]
mcp: []
env: []
services: [mt-scheduler, supabase-postgres, nats]
branch: p1/P1-T053-prefect-batch-schedules
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/03-build-spec.md, docs/02-v1-architecture.md]
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

# P1-T053 · Schedule the batch jobs on mt-scheduler by source update time in AEST/AEDT

## Goal / expected outcome

Every P1 batch job has an `mt-scheduler` schedule aligned to its source's publication time, timezone-aware (Australia/Sydney for display, the source's timezone for triggers), within quota, with retries and alerts on failure; the `ingest-batch` worker runs the `mt-connectors` jobs with the data API keys and nothing else does. No Prefect deployment exists.

## Context & references

- Roadmap: requirements [R1.06](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.08](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.18](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.19](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.41](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets) (`mt-scheduler` schedules, respecting quotas and source update times, AEST/AEDT aware)
- Platform: [18 §2.1](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates) (`mt-scheduler`, `mt-connectors`) · [18 §2.2](../../../docs/18-platform-and-deployment.md#22-python-uv-workspace-packages-only-where-absolutely-required) (`mt_research` offline jobs run by `mt-scheduler`) · [02 §3.2](../../../docs/02-v1-architecture.md#32-containers) (`ingest-batch`: `mt-connectors` run as `mt-scheduler` jobs)
- Spec: [03 M1](../../../docs/03-build-spec.md#m1-market--macro-data--mt_datamarket) · UI [D07 Data & Quality](../../../docs/ui/dashboards/D07-data-quality.md) Feeds shows batch sources too · [D16 System](../../../docs/ui/dashboards/D16-system.md) Jobs
- Depends on (this phase): P1-T077 (scheduler, worker library), P1-T078 (`mt-connectors`), P1-T006 (quota tracker for the pre-run hook) and every job it schedules: P1-T008 (retention), P1-T009 (instrument sync, session calendar job), P1-T012 (compaction), P1-T015, P1-T018, P1-T022, P1-T023 (backfills and daily bars), P1-T019, P1-T020 (FX reference), P1-T024–P1-T028 (macro, commodities, CPI, filings), P1-T029 (enrichment), P1-T037 (nightly DQ report), P1-T052 (tiering), P1-T071 (GeoIP download), P1-T075 (partitions, cold export), P1-T076 (rollup)

## Requirements

- **`ingest-batch` worker:** a compose service running `mt-connectors worker --queue batch` (the `mt-scheduler` worker library with every `mt-connectors` provider registered as a `rust` job kind); digest-pinned image built from the Cargo workspace; it alone holds the data API keys (FRED, EIA, USDA, CoinGecko, Finnhub, Twelve Data, Alpaca history) from tmpfs; a missing key leaves that job `credentials_missing`, never a crash
- **Schedules** in `config/jobs.yaml` with cron + timezone per source, e.g. RBA F11 after 16:00 Australia/Sydney on business days, ABS CPI on release days 11:30 Australia/Canberra, ECB after 16:00 Europe/Berlin, FRED daily 08:00 America/New_York, COT Friday 15:30 America/New_York, EDGAR polling every 10 min US business hours, daily stock/ETF/futures bars after 17:00 America/New_York, retention hourly, compaction 00:30 UTC, nightly DQ report (`python` job on the `research-worker`) after compaction, session-calendar job daily, tiering daily, partition ensure daily and cold export daily, GeoIP download monthly; all times are settings in `config/jobs.yaml`, not code
- **Pre-run hook:** each run asks the quota tracker for headroom first and is `deferred` (not failed) until the reset when the budget is gone; sources disabled by the terms gate (P1-T078) are listed as disabled with the reason
- Retries with backoff (3× by default, from `config/jobs.yaml` defaults); failure → `alert.warning.job_failed` (P1-T077); success updates the source's last-success age in D07
- Concurrency 1 per source (`concurrency_key`); heavy backfills on the `batch` queue off-peak (default 01:00–06:00 Australia/Sydney, a setting)
- A validation test fails if a batch source in `config/sources.yaml` has no schedule or more than one, or if any Prefect deployment file remains

## ToDo

- [ ] Add the `ingest-batch` compose service (`mt-connectors worker --queue batch`) with scoped secrets, health check and heartbeat
- [ ] Write the job definitions and schedules in `config/jobs.yaml` for every job listed above
- [ ] Wire the quota pre-run hook and the D07 last-success fields
- [ ] Add the validation test (one schedule per batch source; no Prefect files) and DST tests for AU and US transitions
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- `cargo test -p mt-scheduler schedules`: next-run calculations for every configured job across DST changes (first Sunday of April/October in Sydney, March/November in New York)
- `cargo test -p mt-connectors jobs_config`: every batch source in `config/sources.yaml` has exactly one job; every job's `source` exists; no Prefect deployment file remains
- Integration (`supabase start` + compose): the jobs register in `ops.job` and `/system/jobs` lists them with their next run

### Scenarios

- Given a job fails three times, when retries are exhausted, then an alert fires and D07 shows the source as degraded with the error
- Given Twelve Data has no budget left today, when its job is due, then the run is `deferred` to the reset and no request is sent

### Stress / failure injection

- n/a: schedules; quota behaviour is tested in P1-T006 and scheduler recovery in P1-T077/P1-T079

## Acceptance criteria

- [ ] Every batch source scheduled on `mt-scheduler`; DST tests pass; failures alert; `ingest-batch` is the only service with data API keys
- [ ] CI green (`cargo clippy`, `cargo test`, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Source publishes late: the job re-checks every 30 min for up to 6 h (defaults, settings) before failing
- A job whose task isn't done yet is registered `enabled: false` and enabled by that task

## Cardinal rules (do NOT)

- Do NOT add Prefect or another orchestrator; schedules live only in `mt-scheduler`
- Do NOT hard-code schedule times in code; they are settings in `config/jobs.yaml`
- Do NOT give data API keys to any service other than `ingest-batch`
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).
- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file (kept outside the repo) mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.41 once every task traced to it in PHASE.md is done; note P1-T053 next to it.
- `docs/03-build-spec.md` §M1: link `config/jobs.yaml` as the schedule file
- `docs/02-v1-architecture.md` §3.2: `ingest-batch` runs `mt-connectors worker --queue batch` and holds the data API keys

## Branch & PR

- Branch: `p1/P1-T053-prefect-batch-schedules`
- PR title: `P1-T053: Schedule the batch jobs on mt-scheduler by source update time in AEST/AEDT`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T053` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (run fields)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (stays Python Prefect; also schedules the Rust jobs it triggers (`mt-recorder compact`/`tier`, `mt-store retention run`, `mt-store bars export-cold` from P1-T075, new dep))
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (Prefect deployments → `mt-scheduler` schedules in `config/jobs.yaml`; adds the Rust `ingest-batch` worker (`mt-connectors` on `mt-scheduler`, sole holder of data API keys); quota pre-run hook; title updated; deps +P1-T077, P1-T078, P1-T006, P1-T009, P1-T012, P1-T052, P1-T071; requirements +R1.18, R1.19; tools cargo; services prefect-server → mt-scheduler)
