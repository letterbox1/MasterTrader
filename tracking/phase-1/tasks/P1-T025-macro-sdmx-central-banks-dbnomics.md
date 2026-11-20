---
id: P1-T025
kind: task
title: Ingest SDMX, central-bank and DBnomics series
phase: 1
type: BUILD
status: backlog
priority: medium
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T024, P1-T078]
requirements: [R1.06]
roadmap_todos: [T1.24]
modules: [M1]
dashboards: [D02]
tools: [git, cargo, docker]
mcp: []
env: []
services: [supabase-postgres]
branch: p1/P1-T025-macro-sdmx-central-banks-dbnomics
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/03-build-spec.md, docs/06-aggregators-and-market-providers.md]
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

# P1-T025 · Ingest SDMX, central-bank and DBnomics series

## Goal / expected outcome

One Rust SDMX client in `mt-connectors` (SDMX REST, JSON/CSV; replaces sdmx1) loads ECB/IMF/OECD/BIS/Eurostat series, direct fetchers load BoE IADB, BoC Valet, RBA, SNB and BoJ series, and DBnomics fills the rest, all into the same point-in-time macro tables.

## Context & references

- Roadmap: requirements [R1.06](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.24](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M1](../../../docs/03-build-spec.md#m1-market--macro-data--mt_datamarket) (Rates & macro) · [06 §3 Calendars & central banks](../../../docs/06-aggregators-and-market-providers.md#calendars--central-banks-m5--m3) (one SDMX client, direct fetchers, DBnomics) · [18 §2.1](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates) (the Rust `mt-connectors` SDMX client replaces sdmx1; DBnomics through its REST API, no client library)
- Open checks feeding this task: IMF SDMX 3.0 base URL, BoC/BoJ keyless (P1-T056)
- Depends on (this phase): P1-T024, P1-T078 (`mt-connectors` base)

## Requirements

- SDMX client agencies (config per agency in `config/sources.yaml`): ECB, IMF (SDMX 3.0 URL from P1-T056), OECD, BIS, Eurostat
- Direct fetchers: BoE IADB CSV, BoC Valet JSON, RBA statistical tables (cash rate F1, yields F2), SNB data portal, BoJ time-series
- DBnomics as catch-all for anything else in the universe list
- Same table schema and pit rules as P1-T024; `source` per provider; licence tags from 06
- Each provider has a quota entry (most are keyless; conservative defaults)

## ToDo

- [ ] Implement the provider modules in `mt-connectors` (`providers::sdmx` with per-agency config; `providers::{boe,boc,rba_stats,snb,boj,dbnomics}`) behind one `MacroSource` trait
- [ ] Map each universe series to provider + key in `config/universe.yaml`
- [ ] Tests with recorded fixtures per provider
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- `cargo test -p mt-connectors macro_sdmx`: parsers per provider (fixtures), SDMX 2.1 and 3.0 responses
- Integration: each adapter loads its fixture into macro tables; pit query works

### Scenarios

- Given BoJ requires a key after all (open check fails), when the job runs, then BoJ is disabled with a reason and DBnomics is used if it mirrors the series

### Stress / failure injection

- n/a: small batch volumes

## Acceptance criteria

- [ ] Every universe macro series from these providers loaded with history and a daily/weekly update
- [ ] CI green (`cargo clippy`, `cargo test`, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- SDMX structure changes: adapter fails loudly; other providers continue

## Cardinal rules (do NOT)

- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file (kept outside the repo) mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).
- Do NOT bypass `mt-api`, the risk manager (M11) or `pit(as_of)` (`mt-store`, also through its Python binding); research and backtest reads go through `pit` only.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.24 once every task traced to it in PHASE.md is done; note P1-T025 next to it.
- `docs/03-build-spec.md` §M1: list providers implemented
- `docs/06-aggregators-and-market-providers.md` §3: confirm the IMF/BoC/BoJ endpoints used

## Branch & PR

- Branch: `p1/P1-T025-macro-sdmx-central-banks-dbnomics`
- PR title: `P1-T025: Ingest sdmx1, central-bank and DBnomics series`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T025` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (run fields; keyless providers)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (stays a Python Prefect flow (sdmx1 is Python-only); services supabase-postgres)
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (sdmx1 → Rust SDMX client in `mt-connectors` (shared with ABS, P1-T027); central-bank and DBnomics fetchers as Rust provider modules; title drops sdmx1; deps +P1-T078; tools cargo; services drop prefect-server)
