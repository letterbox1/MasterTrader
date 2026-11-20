---
id: P1-T010
kind: task
title: Stream Binance and Bybit public trades, L1 and L2 to NATS
phase: 1
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T005, P1-T006, P1-T007, P1-T009]
requirements: [R1.01]
roadmap_todos: [T1.20]
modules: [M1]
dashboards: [D02, D07]
tools: [git, cargo, docker]
mcp: []
env: []
services: [nats]
branch: p1/P1-T010-crypto-ws-binance-bybit
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/03-build-spec.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-11-19
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P1-T010 · Stream Binance and Bybit public trades, L1 and L2 to NATS

## Goal / expected outcome

`ingest-market` (`mt-recorder`, Rust) streams public trades, top-of-book and L2 diff depth for the universe's Binance and Bybit symbols (spot and perps) and publishes normalised messages on `md.{venue}.{symbol}.trade|quote|book`.

## Context & references

- Roadmap: requirements [R1.01](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.20](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M1](../../../docs/03-build-spec.md#m1-market--macro-data) (Crypto real-time) · [03 §6](../../../docs/03-build-spec.md#6-smallest-free-timeframe-by-asset-class) (L2 diff 100 ms) · subjects [02 §6](../../../docs/02-v1-architecture.md#6-messaging-nats) · flow [02 §8 F1](../../../docs/02-v1-architecture.md#8-end-to-end-flows) steps 1–2
- Platform: [18 §2.1](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates) (`mt-recorder`: Nautilus Rust data clients where available (U)) · [18 §9](../../../docs/18-platform-and-deployment.md#9-workstation-first-build-path) (runs on the workstation)
- Bybit is a **data source only** for AU (derivatives blocked; [12 §2](../../../docs/12-policy-and-compliance.md#2-venue-access-registry))
- Depends on (this phase): P1-T005, P1-T006, P1-T007, P1-T009

## Requirements

- Use NautilusTrader's Rust data clients (Binance, Bybit) where the pinned version supports the stream (U: check per venue and stream first and record the result); otherwise a thin Rust WebSocket client (`tokio-tungstenite`) behind the same `StreamConnector` trait. No ccxt in the Rust path
- Streams: trades, best bid/ask, L2 diffs with sequence numbers (Binance `U/u`, Bybit `seq`/`u`) and a REST snapshot on (re)subscribe; local book rebuilt and published as `md.*.book` snapshots every 1 s for every symbol, plus raw diffs to the recorder for native-L2 symbols only
- Native-speed L2 diffs are recorded only for symbols marked `l2: true` (default cap 3, `market.l2.max_native_symbols`, configurable); all other symbols get 1 s book snapshots ([17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P1-B002, [03 M1](../../../docs/03-build-spec.md#m1-market--macro-data), R1.N3)
- Messages carry venue sequence IDs so the gap check (P1-T032) works; `event_time` from the venue, `ingest_time` from our clock
- Public endpoints only; no API keys needed; connection counts and subscribe rates within venue limits via the quota tracker
- Stamps every message with our receive time (`ingest_time`, workstation clock), the basis of data age ([16 §2.2](../../../docs/16-configuration-and-safety-model.md#22-data-freshness-what-stale-means)), and publishes connection status to KV `feed_status` and receive times/sequence breaks on `dq.raw.{venue}.{symbol}` immediately (inputs to the DQ monitor)

## ToDo

- [ ] Check which Binance/Bybit streams the pinned Nautilus Rust data clients support (U) and record it in the progress log
- [ ] Implement Binance spot + USDⓈ-M perps and Bybit spot + linear perps stream connectors in `crates/mt-recorder`
- [ ] Normalise to `mt-core` schema payloads; include `seq`, `prev_seq`
- [ ] Book builder with snapshot + diff sync and resync on sequence break
- [ ] Record raw WS fixtures for tests (no secrets in fixtures)
- [ ] Write the tests listed under Verification
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- `cargo test -p mt-recorder binance bybit`: normaliser golden tests from recorded frames; book builder applies diffs and detects `U > last+1`
- Integration: replay a 10-min recorded session through the connector → identical published messages (golden)
- Integration (nightly, network): connect to live public endpoints for 60 s and receive all three streams per symbol

### Scenarios

- Given the socket drops, when it reconnects, then the book is resynced from a fresh snapshot before diffs are published again and a `dq.raw.resync` event is emitted
- Given a symbol without `l2: true`, when subscribed, then no raw diffs are recorded and only 1 s book snapshots are published
- Given 4 symbols marked `l2: true` with the default cap of 3, when the connector starts, then it refuses the config and names the setting that raises the cap

### Stress / failure injection

- Burst: replay a volatile hour at 10× speed; publish latency p99 (`ingest_time` → NATS ack) < 50 ms and no dropped sequence
- Fault: inject a skipped diff; the builder resyncs within one snapshot round-trip

## Acceptance criteria

- [ ] Live `md.binance.*` and `md.bybit.*` trade/quote/book messages for every universe symbol, visible in Grafana msg-rate panels
- [ ] Golden replay tests pass in CI without network
- [ ] CI green (`cargo clippy`, `cargo test`, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Venue maintenance windows: status `maintenance` from venue system-status endpoints, shown as degraded not stale
- Binance 24 h connection limit: reconnect proactively before forced disconnect
- Testnet endpoints are not used for market data (they are not representative)

## Cardinal rules (do NOT)

- Do NOT send any private/authenticated request from `ingest-market`
- Do NOT place, modify or cancel orders from this code; P1 is read-only toward venues (orders arrive in P2 through M11).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).
- Do NOT add an image without pinning it by digest, or vendored code that carries telemetry or referral IDs.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.20 once every task traced to it in PHASE.md is done; note P1-T010 next to it.
- `docs/03-build-spec.md` §M1: note which streams use Nautilus Rust clients vs the thin Rust WS fallback (clears the (U))

## Branch & PR

- Branch: `p1/P1-T010-crypto-ws-binance-bybit`
- PR title: `P1-T010: Stream Binance and Bybit public trades, L1 and L2 to NATS`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T010` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (L2 native diffs ≤ 3 symbols, 1 s snapshots for others (P1-B002); receive time + dq.raw for data age)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (connectors in Rust `mt-recorder` on Nautilus Rust data clients where available (U, checked first), else thin `tokio-tungstenite` clients; no ccxt; tools cargo)
