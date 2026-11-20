---
id: P1-T028
kind: task
title: Ingest SEC EDGAR filings and XBRL company facts with a Rust client
phase: 1
type: BUILD
status: backlog
priority: medium
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T005, P1-T006, P1-T007, P1-T078]
requirements: [R1.07]
roadmap_todos: [T1.24]
modules: [M1]
dashboards: [D02]
tools: [git, cargo, supabase, docker]
mcp: []
env: []
services: [supabase-postgres]
branch: p1/P1-T028-sec-edgar-edgartools
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

# P1-T028 · Ingest SEC EDGAR filings and XBRL company facts with a Rust client

## Goal / expected outcome

An `mt-connectors` job (Rust; replaces edgartools) pulls filing metadata from EDGAR's `submissions` JSON and key documents (10-K/10-Q, 8-K, 13F, Form 4, S-1/424B) for universe stocks and IPO watch, plus XBRL facts from the `companyfacts` JSON API, with a declared User-Agent and ≤ 10 req/s, into `market.filing` and `market.filing_fact`.

## Context & references

- Roadmap: requirements [R1.07](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.24](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M1](../../../docs/03-build-spec.md#m1-market--macro-data--mt_datamarket) (Fundamentals: SEC EDGAR) · [18 §2.1](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates) (`mt-connectors`: SEC EDGAR submissions + XBRL `companyfacts` JSON) · [19 §3](../../../docs/19-third-party-register.md#3-borrowed-designs-rebuilt-in-rust-no-third-party-code-in-the-runtime) (FinRobot's XBRL use rebuilt here; its valuation desk consumes these facts in P6) · [06 §2](../../../docs/06-aggregators-and-market-providers.md#2-final-m2-social--news-ingestion-stack) (EDGAR official JSON/Atom, declared User-Agent, ≤ 10 req/s)
- Depends on (this phase): P1-T005, P1-T006, P1-T007, P1-T078 (`mt-connectors` base)

## Requirements

- Typed Rust EDGAR client (`providers::edgar`): `company_tickers.json` for ticker → CIK, `submissions/CIK##########.json` for filings, `api/xbrl/companyfacts/CIK##########.json` for XBRL facts; `User-Agent` from the `SEC_EDGAR_USER_AGENT` setting (`MasterTrader <your contact email>`; not a secret); the quota tracker caps at 8 req/s by default (headroom under SEC's 10 req/s)
- `market.filing` (cik, ticker, form, accession, filed_at, period, url, extracted financial facts JSON) with `event_time` = EDGAR acceptance timestamp
- Company facts (XBRL `companyfacts` JSON) for universe tickers in `market.filing_fact` (cik, taxonomy, concept, unit, period, value, accession, `filed`), `event_time` = the filing's acceptance time, restated values as new rows; Form 4 insider transactions; 13F holdings for a configured list of managers
- New-filing polling via EDGAR Atom/JSON feeds every 10 min (default) during US business hours

## ToDo

- [ ] Implement the EDGAR provider in `mt-connectors` (submissions, companyfacts, Form 4 and 13F parsers), the tables (Supabase migration + pgTAP) and polling
- [ ] Fixture-based tests
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- `cargo test -p mt-connectors edgar`: User-Agent always set (test fails if missing); rate cap ≤ 10 req/s enforced
- Integration: fixtures → `market.filing` and `market.filing_fact`; pit by acceptance time (a 10-K/A restatement is invisible before its acceptance)

### Scenarios

- Given EDGAR returns 403 for a missing/blocked User-Agent, when the job runs, then it stops and alerts instead of retrying

### Stress / failure injection

- Load: burst of 200 filings fetched; measured rate never exceeds 10 req/s (test with a fake server counting requests per second)

## Acceptance criteria

- [ ] Filings for universe tickers loaded; polling running within ≤ 10 req/s
- [ ] CI green (`cargo clippy`, `cargo test`, `supabase test db`, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Amended filings (10-K/A) stored as new rows linked to the original

## Cardinal rules (do NOT)

- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file (kept outside the repo) mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).
- Do NOT bypass `mt-api`, the risk manager (M11) or `pit(as_of)` (`mt-store`, also through its Python binding); research and backtest reads go through `pit` only.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.24 once every task traced to it in PHASE.md is done; note P1-T028 next to it.
- `docs/03-build-spec.md` §M1: list the forms covered

## Branch & PR

- Branch: `p1/P1-T028-sec-edgar-edgartools`
- PR title: `P1-T028: Ingest SEC EDGAR filings and XBRL company facts with a Rust client`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T028` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (rate cap and polling as defaults; keyless source)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (stays a Python Prefect flow (edgartools is Python-only); services supabase-postgres)
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (edgartools → typed Rust EDGAR client in `mt-connectors` (submissions JSON + XBRL `companyfacts` JSON into `market.filing_fact`, User-Agent from `SEC_EDGAR_USER_AGENT`); title updated; deps +P1-T078; tools cargo/supabase; services drop prefect-server)
