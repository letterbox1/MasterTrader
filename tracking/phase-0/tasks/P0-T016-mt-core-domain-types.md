---
id: P0-T016
kind: task
title: Implement mt-core domain types and versioned message schemas (Rust)
phase: 0
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T014]
requirements: [R0.01]
roadmap_todos: [T0.21]
modules: [mt-core]
dashboards: []
tools: [git, cargo]
mcp: []
env: []
services: []
branch: p0/P0-T016-mt-core-domain-types
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/roadmap/phase-0-foundations.md]
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

# P0-T016 · Implement mt-core domain types and versioned message schemas (Rust)

## Goal / expected outcome

The `mt-core` crate defines typed, immutable domain types (Instrument, BarSpec, Tick, Event, Signal, OrderIntent, RiskPolicy, JournalEvent) and versioned message schemas (`mt_core::schemas`) that NATS payloads and `mt-api` bodies use, with Decimal money and UTC time enforced. These are the **one** definition: Python gets them through the `mt_store` PyO3 module (P0-T071), TypeScript through the generated OpenAPI/JSON Schema.

## Context & references

- [Roadmap P0 T0.21](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [18 §2.1](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates) (`mt-core` row) · [03 §3 repo layout](../../../docs/03-build-spec.md#3-repository-layout)
- [02 §5.2 key conventions](../../../docs/02-v1-architecture.md#52-key-conventions)
- [02 §6 NATS](../../../docs/02-v1-architecture.md#6-messaging-nats) (payloads are versioned schemas)
- [02 §7 API contract](../../../docs/02-v1-architecture.md#7-api-contract-mt-api) (decimals as strings, ISO-8601 UTC)
- Depends on: P0-T014 · Unblocks: P0-T071 (Python bindings), P0-T024/P0-T027 (`mt-store`), P0-T032 (`mt-api`)

## Requirements

- Types as Rust structs/enums with `serde` (deny unknown fields) and a `schema_version: u16` on every message type; immutable by construction (no public setters; builders validate).
- Money/price/size fields are `rust_decimal::Decimal`, serialised as **strings**; JSON numbers/floats are rejected at decode.
- Times are UTC (`time::OffsetDateTime` or `chrono::DateTime<Utc>`); offsets other than UTC are normalised, missing offsets rejected. Every fact-like type has `event_time` and `ingest_time`; `ts_ns: i64` alongside where Parquet needs ns.
- IDs are UUIDv7 (`mt_core::ids::uuid7()`); instruments use Nautilus-style `InstrumentId` strings (`BTCUSDT.BINANCE`) validated by regex.
- `BarSpec` supports time bars (1s…1W), tick, volume and value bars (03 M0) with a canonical string form (`1m`, `100t`, `1000v`, `1e6V`).
- `OrderIntent` carries `client_order_id = {bot}-{engine_epoch}-{seq}` and a separate `signal_hash` used for idempotency ([17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P2-B007, 02 §8 F1); no execution logic here.
- `Signal` has the 03 M8 fields ([17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P6-B004): id, ts, as_of, instrument, horizon, direction, edge, calibrated confidence, rationale summary, sources[], model/prompt versions, run id.
- `Mode` enum is exactly `paper | hitl | autonomous` ([17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer)); the retired aliases `approve`/`auto` are rejected at decode.
- `RiskPolicy` carries its layer (`L0`–`L4`, [16 §1](../../../docs/16-configuration-and-safety-model.md#1-configuration-layers-tighten-only-inheritance)) and values as data; no limit is a code constant.
- Provenance struct (`source`, `licence`, `train_ok`, `model_input_ok`, `display_ok`, `retention_days`, `commercial_ok`) shared with `mt-store`.
- JSON Schema per message generated with `schemars` into `docs/schemas/` (consumed by `mt-api`'s utoipa OpenAPI and the web client).

## ToDo

- [ ] Implement the types and the `mt_core::schemas` registry (`name → (version, type)`), JSON + msgpack (`rmp-serde`) codecs.
- [ ] Implement `ids::uuid7()` and `InstrumentId` parsing.
- [ ] Implement `BarSpec` parse/format round trip.
- [ ] Write property tests (`proptest`) for encode/decode round trips and Decimal precision.
- [ ] Export JSON Schema per message to `docs/schemas/`.

## Verification

### Tests
- `cargo test -p mt-core`: each type validates/rejects (missing offset, float price, bad InstrumentId).
- Property (`proptest`): JSON and msgpack round trips preserve Decimal exactly; `BarSpec` parse∘format = identity.
- Golden: `client_order_id` = `{bot}-{engine_epoch}-{seq}` for fixed inputs; `signal_hash` stable across Rust and the Python binding (checked again in P0-T071).
- Unit: `Mode` decode rejects `approve` and `auto`.
- `cargo clippy -p mt-core -- -D warnings`.

### Scenarios
- Given a payload with `"price": 1.1` (a JSON number), when decoded, then a typed validation error is raised.
- Given schema_version 2 of a message, when a v1 consumer decodes it, then it fails loudly with the version in the error.

### Stress / failure injection
- Decode benchmark (`criterion`): small `Tick` messages per second per core (logged, not gated).

## Acceptance criteria

- [ ] All eight types + provenance struct implemented with tests
- [ ] proptest round-trip tests pass
- [ ] JSON Schemas exported
- [ ] clippy `-D warnings` clean
- [ ] CI green (clippy, cargo test, ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- Nanosecond timestamps: keep `ts_ns` alongside the datetime where Parquet needs ns (02 §5.2); Python sees µs `datetime` + `ts_ns`.

## Cardinal rules (do NOT)

- Do NOT use floats for money, prices, sizes, fees or tax.
- Do NOT put business logic (risk, sizing, execution) in `mt-core`.
- Do NOT define a second copy of these types in Python or TypeScript by hand; generate or bind them.
- Do NOT skip, weaken or delete a test to get CI green.
- Do NOT bypass `mt-api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.

## Doc sync on completion

- `docs/02-v1-architecture.md` §6: link the generated schema folder.
- `docs/roadmap/phase-0-foundations.md`: tick T0.21 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T016-mt-core-domain-types`
- PR title: `P0-T016: Implement mt-core domain types and versioned message schemas`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T016` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (client order ID format (17 §D P2-B007), Signal fields (P6-B004), modes paper/hitl/autonomous (17 §B), RiskPolicy layers (16 §1); run fields added)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (Rust `mt-core` crate: serde + rust_decimal + proptest + schemars replace msgspec/hypothesis; Python access via the `mt_store` PyO3 module, P0-T071)
