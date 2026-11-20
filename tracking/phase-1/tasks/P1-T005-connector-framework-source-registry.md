---
id: P1-T005
kind: task
title: Build the connector framework and source registry
phase: 1
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T004, P0-T014, P0-T017]
requirements: [R1.01, R1.08, R1.09]
roadmap_todos: [T1.20]
modules: [M1]
dashboards: [D07]
tools: [git, cargo, docker]
mcp: []
env: []
services: [nats]
branch: p1/P1-T005-connector-framework-source-registry
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

# P1-T005 · Build the connector framework and source registry

## Goal / expected outcome

Every connector shares one base: streaming connectors in `mt-recorder` (Rust) implement one lifecycle (reconnect with backoff, heartbeats, metrics, provenance defaults, quota hooks), batch connectors in `mt-connectors` (Rust, P1-T078) build on the same registry, and all are registered in one `config/sources.yaml` with licence and cost tags, so new feeds are uniform and a paid feed cannot be enabled.

## Context & references

- Roadmap: requirements [R1.01](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.08](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.09](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.20](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M1](../../../docs/03-build-spec.md#m1-market--macro-data--mt_datamarket) · [03 §1](../../../docs/03-build-spec.md#1-ground-rules) (free only, quota tracker per connector) · [03 §9](../../../docs/03-build-spec.md#9-future-proof-hygiene) (source tags `license`, `cost`) · [12 §5](../../../docs/12-policy-and-compliance.md#5-data-provenance-tagging-one-mechanism-for-all-data-terms)
- Source list and licences: [06 §3 Market data](../../../docs/06-aggregators-and-market-providers.md#market-data-m1), [06 §3 Skip list](../../../docs/06-aggregators-and-market-providers.md#skip-list)
- UI: [D07 Data & Quality](../../../docs/ui/dashboards/D07-data-quality.md) Feeds tab shows licence/cost tags; acceptance 2 ("a paid feed can't be enabled")
- Depends on (this phase): P1-T004
- Cross-phase prerequisites (depends_on): P0-T014 (repository skeleton: Cargo and uv workspaces), P0-T017 (`mt-core` settings and clock)
- Platform: [18 §2](../../../docs/18-platform-and-deployment.md#2-language-split-rust-first-python-where-necessary) (streaming and batch connectors are Rust; `mt-connectors` replaces OpenBB, fredapi, sdmx1, edgartools and yfinance) · [17 §H](../../../docs/17-decisions-register.md#h-rust-max-borrowed-code-rebuilt-in-rust-scenario-simulator-copyleft-register-2026-11-20)

## Requirements

- Layout: `crates/mt-recorder/src/connector/` (`StreamConnector` trait, reconnect, heartbeat, metrics) for streaming; the batch base (`BatchConnector`) is `crates/mt-connectors` (P1-T078); one `SourceRegistry` in `mt-core` (Rust) loading `config/sources.yaml`, used by both
- `config/sources.yaml` entry per source: `id`, `kind` (stream|batch), `licence` (personal|commercial_ok|unknown), `cost` (free|paid), `use_flags` defaults (`train_ok`, `model_input_ok`, `display_ok`, `retention_days`, `commercial_ok`), `quota` reference, `docs` link to 06
- Registry refuses to start a source with `cost: paid` (server-side) and `data.feed.resume` on it returns problem+json 409
- Reconnect: exponential backoff with jitter (defaults 1 s → 60 s cap, reset after 5 min healthy; configurable per source in `config/sources.yaml`, not constants); never hammer a venue (Binance 418 escalates to multi-day bans, [12 §2](../../../docs/12-policy-and-compliance.md#2-venue-access-registry))
- Every message carries `event_time` (venue) and `ingest_time` (our clock, UTC, ns) per [02 §5.2](../../../docs/02-v1-architecture.md#52-key-conventions)
- Metrics per feed: msgs/s, last-message age, reconnects, latency p50/p99, errors (Prometheus labels: `source`, `venue`; symbol only on low-cardinality series)
- Keyless by default ([17 §E](../../../docs/17-decisions-register.md#e-ratification-2026-10-22): build first, keys last): a source whose credentials are absent starts in `credentials_missing` (shown in D07) instead of failing; CI and builds never need real keys; live keyed checks are P1-T073
- Every message carries our receive time (`ingest_time`), the basis of data age ([16 §2.2](../../../docs/16-configuration-and-safety-model.md#22-data-freshness-what-stale-means))
- Default fixture `config/universe.yaml` (3 crypto, 2 FX, 2 ETFs) until P1-T001 lands

## ToDo

- [ ] Implement the Rust `StreamConnector` trait with start/stop, backoff, heartbeat, metrics and structured logs (`trace_id`) (the batch base is P1-T078)
- [ ] Implement `SourceRegistry` in `mt-core` (serde) loading and validating `config/sources.yaml`, with the paid-feed refusal
- [ ] Seed `config/sources.yaml` with every P1 source from 06 §3 and 03 M1 (licence and cost per 06; Twelve Data and any Yahoo-sourced daily data = personal; a `terms` field per source is added by P1-T078)
- [ ] Add CLIs: `mt-recorder feed run <id>` (streams) and `mt sources list`, `mt universe validate` (Rust `mt` CLI; batch runs are `mt-connectors run <id>`, P1-T078)
- [ ] Unit + integration tests; docs
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- `cargo test -p mt-core registry` and `cargo test -p mt-recorder connector`: registry validation (missing licence → error; `cost: paid` → refused); backoff schedule; timestamp fields always set
- Integration: a fake WS server drops the connection 5 times; the connector reconnects with growing delays and publishes again
- Property: `ingest_time >= event_time - max_skew` holds or the message is flagged for the clock-skew check

### Scenarios

- Given a source marked `cost: paid`, when the user tries to resume it from D07, then the API rejects it and the UI shows the reason
- Given a venue closes the socket with an HTTP 429/418, when the connector reconnects, then backoff honours `Retry-After` and the quota tracker records it

### Stress / failure injection

- Fault injection: kill the fake server for 10 min; the connector caps retries at 60 s spacing and recovers within one interval after the server returns

## Acceptance criteria

- [ ] All P1 sources listed with licence and cost tags; `mt sources list` matches 06
- [ ] Paid sources cannot be enabled through API or CLI (tested)
- [ ] CI green (`cargo clippy`, `cargo test`, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Clock: never use the venue timestamp as `ingest_time`; if the venue omits `event_time`, set it to `ingest_time` and flag `approx_time=true`
- Restart: connectors resume from scratch; gaps during downtime are detected by P1-T032 and filled by backfills where a history source exists

## Cardinal rules (do NOT)

- Do NOT hard-code symbols or keys in connector code; use the universe and sops
- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file (kept outside the repo) mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).
- Do NOT bypass `mt-api`, the risk manager (M11) or `pit(as_of)` (`mt-store`, also through its Python binding); research and backtest reads go through `pit` only.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.20 once every task traced to it in PHASE.md is done; note P1-T005 next to it.
- `docs/03-build-spec.md` §M1: link `config/sources.yaml` as the source-of-truth for licence/cost tags
- `docs/06-aggregators-and-market-providers.md` §3: note that each listed source now has a registry entry

## Branch & PR

- Branch: `p1/P1-T005-connector-framework-source-registry`
- PR title: `P1-T005: Build the connector framework and source registry`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T005` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (configurable backoff defaults, keyless credentials_missing state, receive time as data-age basis; P0 deps explicit)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (streaming connector trait in Rust `mt-recorder`, batch base in Python `mt_data`, one `SourceRegistry` in `mt-core` with Python binding; tools cargo+uv)
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (the Python `mt_data` `BatchConnector` base moved to the Rust `mt-connectors` crate (P1-T078); `SourceRegistry` without a Python binding; CLIs `mt sources list`/`mt universe validate`; tools drop uv)
