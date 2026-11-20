---
id: P1-T078
kind: task
title: mt-connectors crate skeleton: HTTP client, quotas, provenance, pit writer, fixture harness
phase: 1
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T005, P1-T006, P1-T007, P0-T027]
requirements: [R1.19, R1.08, R1.09]
roadmap_todos: [T1.36]
modules: [M1, mt-connectors]
dashboards: [D07]
tools: [git, cargo, supabase, docker]
mcp: []
env: []
services: [supabase-postgres, nats]
branch: p1/P1-T078-mt-connectors-crate-skeleton-http-client-quotas-
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/18-platform-and-deployment.md, docs/03-build-spec.md, docs/06-aggregators-and-market-providers.md]
doc_sync_status: n/a
found_in: ""
created: 2026-11-20
updated: 2026-11-20
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P1-T078 · mt-connectors crate skeleton: HTTP client, quotas, provenance, pit writer, fixture harness

## Goal / expected outcome

`crates/mt-connectors` exists with everything a batch provider client needs, so each provider (P1-T009, P1-T015, P1-T018–T020, P1-T022–T029) is only a typed request/parse module: one shared HTTP client that asks the quota tracker before every call, the provenance-tagged `pit` writer, a resumable unit manifest, a terms gate, a CLI, and a recorded-fixture test harness that keeps CI keyless. It replaces OpenBB, fredapi, sdmx1, edgartools and yfinance (R1.19).

## Context & references

- Roadmap: requirements [R1.19](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.08](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.09](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.36](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Platform: [18 §2.1](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates) (`mt-connectors`: typed Rust clients for FRED/ALFRED, EIA, USDA NASS, US Treasury, BLS, ECB/SDMX, CFTC COT, World Bank, IMF, SEC EDGAR (submissions + XBRL `companyfacts` JSON), Dukascopy (`bi5`), data.binance.vision, daily futures from free sources whose terms allow automated personal use, CoinGecko, DefiLlama, Myfxbook, Finnhub, CryptoPanic, Twelve Data, calendars; every client writes through `pit` with provenance) · [19 §3](../../../docs/19-third-party-register.md#3-borrowed-designs-rebuilt-in-rust-no-third-party-code-in-the-runtime) (FinRobot's XBRL ideas rebuilt in `mt-connectors`)
- Decision: [17 §H](../../../docs/17-decisions-register.md#h-rust-max-borrowed-code-rebuilt-in-rust-scenario-simulator-copyleft-register-2026-11-20) (OpenBB, fredapi, sdmx1, edgartools, yfinance → Rust connectors)
- Rules: [03 §1](../../../docs/03-build-spec.md#1-ground-rules) (free only; quota tracker per connector) · [12 §5](../../../docs/12-policy-and-compliance.md#5-data-provenance-tagging-one-mechanism-for-all-data-terms) (provenance at write) · [12 §4](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules) (per-platform terms) · build first, keys last ([17 §E](../../../docs/17-decisions-register.md#e-ratification-2026-10-22))
- Depends on (this phase): P1-T005 (`SourceRegistry` and `config/sources.yaml`), P1-T006 (quota tracker), P1-T007 (`provenance::Tagged` writer)
- Cross-phase prerequisites (depends_on): P0-T027 (`pit(as_of)` and the Parquet catalog helpers in `mt-store`)
- Scheduling: the connectors become `mt-scheduler` jobs in P1-T053 (the `ingest-batch` worker); this crate does not depend on `mt-scheduler`

## Requirements

- **Layout:** `crates/mt-connectors/src/{http,source,manifest,writer,terms,testing}/` plus one module per provider under `src/providers/` (added by the provider tasks); binary `mt-connectors` with `sources list`, `run <source> [--from --to] [--dry-run]`, `check <source>` (one live probe, used by P1-T056/P1-T073) and `fixtures record <source>`
- **`BatchConnector` trait** (async): `plan(range) -> Vec<Unit>` (file, page, date or series), `run_unit(unit, ctx) -> UnitOutcome`; the context carries the HTTP client, quota handle, `pit` writer, clock, the source's registry entry and its credentials (absent → the source reports `credentials_missing`, never panics)
- **Shared HTTP client** (`reqwest` + rustls): per-source User-Agent (SEC EDGAR's declared contact from the `SEC_EDGAR_USER_AGENT` setting), timeouts, gzip, a response size cap, retries with exponential backoff and jitter honouring `Retry-After`, and `QuotaTracker::acquire` before every request; response headers feed the tracker's live overrides. No provider code may build its own HTTP client (enforced by a test)
- **Writer:** every row goes through `mt-store` `provenance::Tagged` with the source defaults; the `pit` writer sets `event_time` (publication/known-at time) and `ingest_time`, and a revision is a new row, never an update (vintages for FRED/ALFRED, RBA, ABS, ECB); Parquet output goes through the catalog helpers with provenance metadata
- **Manifest:** `ops.backfill_job` (source, unit key, status, checksum, rows, attempts, error) shared by every connector; a re-run skips done units, so every job is idempotent and resumable
- **Terms gate:** a source can be enabled only when its `config/sources.yaml` entry has `terms: ok` with a `terms_checked` date and a doc link; `terms: unknown` (e.g. Yahoo chart data until P1-T023's check) keeps it disabled with the reason shown in D07
- **Fixture harness** (`mt_connectors::testing`): record real responses once (`fixtures record`, run by hand with keys where needed), scrub them (keys, tokens, emails, account IDs; the harness fails if a secret pattern survives), replay them with `wiremock` in CI; snapshot the parsed rows (`insta`); helper `assert_no_lookahead(source, as_of)` for `pit` tests; live tests sit behind `--features live` and never run in normal CI
- **Metrics:** `mt_connector_requests_total{source,status}`, `mt_connector_request_seconds{source}`, `mt_connector_rows_written_total{source}`, `mt_connector_last_success_timestamp{source}` (D07 Feeds shows batch sources from these)

## ToDo

- [ ] Create the crate, the `BatchConnector` trait, the context and the CLI
- [ ] Implement the shared HTTP client with quota `acquire`, header feedback, retries and User-Agent handling
- [ ] Implement the `pit` writer on top of `provenance::Tagged` (vintage rows, Parquet path) and the `ops.backfill_job` manifest (Supabase migration + pgTAP test)
- [ ] Implement the terms gate and add `terms`/`terms_checked` fields to `config/sources.yaml` (validated by the `SourceRegistry` from P1-T005)
- [ ] Implement the fixture harness (record, scrub, replay, snapshot, look-ahead helper) and a test-only `demo` provider that exercises it end to end
- [ ] Add the "no raw HTTP client outside `mt_connectors::http`" test (extends P1-T006's check to this crate)
- [ ] Write the tests listed under Verification
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- `cargo test -p mt-connectors http`: every request calls `acquire` first; `Retry-After: 120` pauses the source; a 429 storm causes no retry burst; missing User-Agent for EDGAR fails the request before sending
- `cargo test -p mt-connectors writer`: rows carry the source's provenance; a looser override is refused; a revised value adds a row and `pit(as_of)` before the revision returns the old value
- `cargo test -p mt-connectors manifest`: a killed run resumes at the first unfinished unit; a re-run is a no-op
- `cargo test -p mt-connectors terms`: a source with `terms: unknown` cannot be enabled through the CLI or `mt-api`
- `cargo test -p mt-connectors testing`: the scrubber removes a planted API key and the harness fails if one survives; the `demo` provider replays its fixture and matches its snapshot
- `supabase test db`: `ops.backfill_job` constraints; `cargo clippy --all-targets -- -D warnings`

### Scenarios

- Given a keyed source without its key on the workstation, when `mt-connectors run <source>` starts, then it reports `credentials_missing` in D07 and exits 0
- Given a provider changes a field type, when its fixture is re-recorded, then the snapshot test fails loudly instead of loading misaligned data

### Stress / failure injection

- Fake server returns 500 for 10 minutes; the client backs off to its cap, the unit is retried per policy, and the manifest records the failure without losing done units
- Load: 1,000 fixture pages through the writer; the quota tracker never lets the request rate exceed the configured budget (counted by the fake server)

## Acceptance criteria

- [ ] Provider tasks can add a client by implementing `BatchConnector` only; the `demo` provider proves the path from HTTP to tagged `pit` rows to manifest
- [ ] No outbound request bypasses the quota tracker; no row is written without provenance; CI runs keyless
- [ ] CI green (`cargo clippy`, `cargo test`, `supabase test db`, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Bulk file sources (data.binance.vision ZIPs, Dukascopy `bi5`, CFTC/Baker Hughes files) stream to disk with checksum verification before parsing; partial files are deleted
- Providers without a published limit run at a conservative default budget (`verify: true` in `config/quotas.yaml`) until checked
- A source whose terms change to "not allowed" is disabled by setting `terms: blocked`; its stored history keeps its provenance tags

## Cardinal rules (do NOT)

- Do NOT wrap or vendor OpenBB, fredapi, sdmx1, edgartools, yfinance or any Python SDK; clients are typed Rust ([18 §2.1](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates))
- Do NOT call a source whose terms are unknown or forbid automated personal use; no scraping against terms ([12 §4](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules))
- Do NOT commit unscrubbed fixtures; do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file (kept outside the repo) mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).
- Do NOT bypass `mt-api`, the risk manager (M11) or `pit(as_of)` (`mt-store`, also through its Python binding); research and backtest reads go through `pit` only.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.36 once every task traced to it in PHASE.md is done; note P1-T078 next to it.
- `docs/18-platform-and-deployment.md` §2.1: link the crate layout and the terms gate
- `docs/03-build-spec.md` §M1: name `mt-connectors` as the batch client base (shared HTTP client, `pit` writer, manifest, fixture harness)
- `docs/06-aggregators-and-market-providers.md` §3: note that each source's `terms` status lives in `config/sources.yaml`

## Branch & PR

- Branch: `p1/P1-T078-mt-connectors-crate-skeleton-http-client-quotas-`
- PR title: `P1-T078: mt-connectors crate skeleton: HTTP client, quotas, provenance, pit writer, fixture harness`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T078` run

## Progress log

- 2026-11-20 01:08 · cloud:vm:be04b6ae61f8 · created
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (filled the stub: `mt-connectors` base per 18 §2.1 and R1.19/T1.36: shared quota-aware HTTP client, provenance `pit` writer, shared `ops.backfill_job` manifest (moved here from P1-T015), terms gate, recorded-fixture harness; the batch base moved here from P1-T005; scheduling stays in P1-T053)
