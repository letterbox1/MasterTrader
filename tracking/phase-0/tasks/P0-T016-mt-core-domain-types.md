---
id: P0-T016
kind: task
title: Implement mt_core domain types and versioned message schemas
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
modules: [mt_core]
dashboards: []
tools: [git, uv, python>=3.12]
mcp: []
env: []
services: []
branch: p0/P0-T016-mt-core-domain-types
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P0-T016 · Implement mt_core domain types and versioned message schemas

## Goal / expected outcome

`mt_core` exposes typed, immutable domain types (Instrument, BarSpec, Tick, Event, Signal, OrderIntent, RiskPolicy, JournalEvent) and versioned msgspec schemas in `mt_core.schemas` that NATS payloads and API bodies use, with Decimal money and UTC time enforced.

## Context & references

- [Roadmap P0 T0.21](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [03 §3 repo layout](../../../docs/03-build-spec.md#3-repository-layout)
- [02 §5.2 key conventions](../../../docs/02-v1-architecture.md#52-key-conventions)
- [02 §6 NATS](../../../docs/02-v1-architecture.md#6-messaging-nats) (payloads are versioned msgspec schemas in `mt_core.schemas`)
- [02 §7 API contract](../../../docs/02-v1-architecture.md#7-api-contract-mt_api) (decimals as strings, ISO-8601 UTC)
- Depends on: P0-T014

## Requirements

- Types as `msgspec.Struct(frozen=True, kw_only=True)` with `schema_version: int` on every message type.
- Money/price/size fields are `Decimal`, serialised as **strings**; floats are rejected at decode.
- Times are timezone-aware UTC; naive datetimes raise. Every fact-like type has `event_time` and `ingest_time`.
- IDs are UUIDv7 (`mt_core.ids.uuid7()`); instruments use Nautilus-style `InstrumentId` strings (`BTCUSDT.BINANCE`) validated by regex.
- `BarSpec` supports time bars (1s…1W), tick, volume and value bars (03 M0) with a canonical string form (`1m`, `100t`, `1000v`, `1e6V`).
- `OrderIntent` carries `client_order_id = {bot}-{engine_epoch}-{seq}` and a separate `signal_hash` used for idempotency ([17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P2-B007, 02 §8 F1); no execution logic here.
- `Signal` has the 03 M8 fields ([17 §D] P6-B004): id, ts, as_of, instrument, horizon, direction, edge, calibrated confidence, rationale summary, sources[], model/prompt versions, run id.
- `Mode` enum is exactly `paper | hitl | autonomous` ([17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer)); the retired aliases `approve`/`auto` are rejected at decode.
- `RiskPolicy` carries its layer (`L0`–`L4`, [16 §1](../../../docs/16-configuration-and-safety-model.md#1-configuration-layers-tighten-only-inheritance)) and values as data; no limit is a code constant.
- Provenance mixin (`source`, `licence`, `train_ok`, `model_input_ok`, `display_ok`, `retention_days`, `commercial_ok`) shared with `mt_store`.

## ToDo

- [ ] Implement the types and the `mt_core.schemas` registry (`name → (version, Struct)`), JSON + msgpack encoders.
- [ ] Implement `ids.uuid7()` and `InstrumentId` parsing.
- [ ] Implement `BarSpec.parse/format` round trip.
- [ ] Write property tests (hypothesis) for encode/decode round trips and Decimal precision.
- [ ] Export JSON Schema per message to `docs/schemas/` for the web/OpenAPI side.

## Verification

### Tests
- Unit: each type validates/rejects (naive time, float price, bad InstrumentId).
- Property: JSON and msgpack round trips preserve Decimal exactly; `BarSpec` parse∘format = identity.
- Golden: `client_order_id` = `{bot}-{engine_epoch}-{seq}` for fixed inputs; `signal_hash` stable.
- Unit: `Mode` decode rejects `approve` and `auto`.

### Scenarios
- Given a payload with `price: 1.1` (float), when decoded, then a typed validation error is raised.
- Given schema_version 2 of a message, when a v1 consumer decodes it, then it fails loudly with the version in the error.

### Stress / failure injection
- Decode benchmark: ≥ 200k small `Tick` messages/s per core (logged, not gated).

## Acceptance criteria

- [ ] All eight types + provenance mixin implemented with tests
- [ ] Hypothesis round-trip tests pass
- [ ] JSON Schemas exported
- [ ] mypy strict clean
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- Nanosecond timestamps: Python datetime is µs; keep `ts_ns: int` alongside where Parquet needs ns (02 §5.2).

## Cardinal rules (do NOT)

- Do NOT use floats for money, prices, sizes, fees or tax.
- Do NOT put business logic (risk, sizing, execution) in `mt_core`.
- Do NOT skip, weaken or delete a test to get CI green.
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.

## Doc sync on completion

- `docs/02-v1-architecture.md` §6: link the generated schema folder.
- `docs/roadmap/phase-0-foundations.md`: tick T0.21 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T016-mt-core-domain-types`
- PR title: `P0-T016: Implement mt_core domain types and versioned message schemas`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T016` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (client order ID format (17 §D P2-B007), Signal fields (P6-B004), modes paper/hitl/autonomous (17 §B), RiskPolicy layers (16 §1); run fields added)
