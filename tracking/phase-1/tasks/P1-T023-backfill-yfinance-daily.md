---
id: P1-T023
kind: task
title: Load daily history for stocks, ETFs and futures from terms-checked free sources
phase: 1
type: BUILD
status: backlog
priority: medium
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T013, P1-T006, P1-T009, P1-T078]
requirements: [R1.05, R1.06, R1.19]
roadmap_todos: [T1.22]
modules: [M1, mt-connectors]
dashboards: [D02]
tools: [git, cargo, docker]
mcp: []
env: []
services: [supabase-postgres]
branch: p1/P1-T023-backfill-yfinance-daily
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

# P1-T023 · Load daily history for stocks, ETFs and futures from terms-checked free sources

## Goal / expected outcome

A daily `mt-connectors` job (Rust; replaces yfinance) loads daily bars for universe stocks/ETFs, daily futures (e.g. gold and crude continuous contracts) and macro proxies (VIX) from free sources whose terms allow automated personal use, so every asset class has a 1D series for D02 and exit criterion 1. Yahoo chart data is used only if its terms allow it (U); the terms check is the first step and its result decides the sources.

## Context & references

- Roadmap: requirements [R1.05](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.06](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.19](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.22](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Platform: [18 §2.1](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates) (`mt-connectors`: daily futures from free sources whose terms allow automated personal use; Yahoo chart data only if its terms allow (U)) · [17 §H](../../../docs/17-decisions-register.md#h-rust-max-borrowed-code-rebuilt-in-rust-scenario-simulator-copyleft-register-2026-11-20) (yfinance → Rust connectors)
- Spec: [03 M1](../../../docs/03-build-spec.md#m1-market--macro-data--mt_datamarket) (daily history; futures daily only) · [03 §6](../../../docs/03-build-spec.md#6-smallest-free-timeframe-by-asset-class) (futures: daily only) · [06 §3 Market data](../../../docs/06-aggregators-and-market-providers.md#market-data-m1) (Twelve Data free tier for backup bars; akshare for Asia futures as an optional `mt_research` job)
- Terms: [12 §4](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules) (no scraping against terms) · licence personal use only ([06 §4](../../../docs/06-aggregators-and-market-providers.md#4-saas-note-for-these-sources))
- Depends on (this phase): P1-T013 (bar tables), P1-T006 (quota tracker), P1-T009 (instrument master), P1-T078 (`mt-connectors` base with the terms gate)

## Requirements

- **Terms check first (U):** read the current terms of each candidate and record the verdict, date and link in `config/sources.yaml` (`terms: ok|blocked|unknown`, `terms_checked`) and in 06 §3. Candidates: Yahoo chart data (stocks/ETFs, futures, `^VIX`), Stooq daily CSV (U), Alpaca daily bars from the IEX feed (stocks/ETFs; keyed, live in P1-T073), Twelve Data free tier (800/day, keyed), FRED `VIXCLS` (VIX, keyless). A source with `terms: unknown` or `blocked` stays disabled (terms gate, P1-T078)
- Pick, per asset class, the first allowed source in this order of preference (configurable in `config/sources.yaml`): stocks/ETFs and VIX may fall back to Alpaca daily bars and FRED `VIXCLS`; if no allowed free source covers daily futures, record that in the progress log, file a gap with the consequence for exit criterion 1, and load what is allowed
- Typed Rust clients in `mt-connectors` (`providers::{yahoo_chart,stooq,twelvedata}` as allowed); daily bars into `market.bar_daily_vendor` (separate from built bars) with the source's provenance (`licence=personal`, `commercial_ok=false` unless its terms say otherwise)
- Polite request rate via the quota tracker (sources without a published limit run at a conservative default and back off on errors)
- Store unadjusted OHLC plus adjusted close where the source provides it; record the source and client version
- Futures continuous contracts flagged `continuous=true` (roll gaps are not data errors)
- Optional Asia futures: the akshare daily backfill stays Python as an `mt_research` offline batch job run by `mt-scheduler` ([18 §2.2](../../../docs/18-platform-and-deployment.md#22-python-uv-workspace-packages-only-where-absolutely-required)); off by default and not part of this task's acceptance

## ToDo

- [ ] Run the terms check for every candidate; record verdicts in `config/sources.yaml` and the progress log
- [ ] Implement the allowed provider modules in `mt-connectors` with recorded fixtures (history once, then daily after US close; schedule in P1-T053)
- [ ] Map the universe's daily instruments (P1-T001) to their chosen source
- [ ] Write the tests listed under Verification
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- `cargo test -p mt-connectors daily_bars`: response → rows mapping per provider; missing/NaN rows dropped and counted; re-run idempotent
- `cargo test -p mt-connectors terms`: a provider with `terms: unknown` can't be enabled (shared gate from P1-T078)
- Integration: fixture responses → `market.bar_daily_vendor` rows with provenance; `pit(as_of)` returns only bars dated before `as_of`

### Scenarios

- Given a source returns an empty response, when the job runs, then it retries later and marks the source degraded after 3 failures
- Given Yahoo's terms don't allow automated use, when the job is configured, then Yahoo stays disabled with the reason in D07 and the fallback sources cover stocks/ETFs and VIX

### Stress / failure injection

- n/a: one daily batch per source; the quota tracker covers rate

## Acceptance criteria

- [ ] Every candidate source has a recorded terms verdict; only allowed sources are enabled
- [ ] Daily history for all universe stocks/ETFs and every daily future an allowed source covers; daily update running (keyed sources live in P1-T073)
- [ ] CI green (`cargo clippy`, `cargo test`, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Unofficial endpoints break often: failures alert and the job keeps the last good data with a stale flag, never silent
- A source whose terms change to "not allowed" is disabled (`terms: blocked`); history already stored keeps its provenance

## Cardinal rules (do NOT)

- Do NOT call a source before its terms verdict is `ok`; do NOT scrape against a site's terms
- Do NOT use yfinance or any Python SDK in this job; the clients are Rust ([18 §2.1](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates))
- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file (kept outside the repo) mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).
- Do NOT bypass `mt-api`, the risk manager (M11) or `pit(as_of)` (`mt-store`, also through its Python binding); research and backtest reads go through `pit` only.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.22 once every task traced to it in PHASE.md is done; note P1-T023 next to it.
- `docs/03-build-spec.md` §M1: note which daily sources and futures are loaded
- `docs/06-aggregators-and-market-providers.md` §3: record the terms verdicts (clear the Yahoo (U))

## Branch & PR

- Branch: `p1/P1-T023-backfill-yfinance-daily`
- PR title: `P1-T023: Load daily history for stocks, ETFs and futures from terms-checked free sources`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T023` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (run fields; keyless source)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (stays a Python Prefect flow (yfinance is Python-only); daily vendor bars in a monthly-partitioned vendor table; services supabase-postgres)
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (re-scoped, not cancelled: yfinance → typed Rust clients in `mt-connectors`; a terms check comes first and Yahoo is used only if its terms allow (U), with Alpaca daily bars, Stooq (U), Twelve Data and FRED `VIXCLS` as allowed fallbacks; akshare stays an optional `mt_research` job; deps +P1-T078; tools cargo; services drop prefect-server)
