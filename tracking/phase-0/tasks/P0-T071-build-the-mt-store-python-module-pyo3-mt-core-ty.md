---
id: P0-T071
kind: task
title: Build the mt_store Python module (PyO3): mt-core types and pit bindings
phase: 0
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T016, P0-T027]
requirements: [R0.01, R0.04]
roadmap_todos: [T0.21, T0.22]
modules: [mt-store, mt-core]
dashboards: []
tools: [git, cargo, uv, python>=3.12, maturin, supabase]
mcp: []
env: []
services: [supabase-postgres]
branch: p0/P0-T071-build-the-mt-store-python-module-pyo3-mt-core-ty
pr: ""
doc_sync: [docs/18-platform-and-deployment.md, docs/03-build-spec.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-11-19
updated: 2026-11-19
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P0-T071 · Build the mt_store Python module (PyO3): mt-core types and pit bindings

## Goal / expected outcome

Python research code imports **one** module, `mt_store`, built from `crates/mt-store` with PyO3 + maturin. It exposes the `mt-core` shared types and `pit(as_of)`, so Rust and Python share one definition of every type and one point-in-time read path ([18 §2.1](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates), [18 §4.4](../../../docs/18-platform-and-deployment.md#44-point-in-time-and-worm)). The wheel builds in the uv workspace, ships type stubs, and the `pit` golden tests pass through the binding as well as in Rust.

## Context & references

- [Roadmap P0 R0.01, R0.04](../../../docs/roadmap/phase-0-foundations.md#3-requirements) · [T0.21, T0.22](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [18 §2.1](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates) (`mt-core` exposed through the same PyO3 module as `pit`) · [18 §2.2 rule](../../../docs/18-platform-and-deployment.md#22-python-uv-workspace-packages-only-where-necessary)
- [03 §3 layout](../../../docs/03-build-spec.md#3-repository-layout) · [03 §4 point-in-time rule](../../../docs/03-build-spec.md#4-data-model-overview)
- [SPEC NN1](../../../SPEC.md#non-negotiable-requirements)
- Depends on: P0-T016 (`mt-core` types), P0-T027 (`pit` in Rust)
- Unblocks: P0-T028 (CI guard for Python), every Python research package from P1 on

## Requirements

- A `python` feature (or a thin `crates/mt-store-py` cdylib) builds the extension module `mt_store` with **PyO3** (abi3, Python ≥ 3.12) and **maturin**; the uv workspace lists it as a member so `uv sync` builds it.
- Exposed types: the `mt-core` types (Instrument, BarSpec, Tick, Event, Signal, OrderIntent, RiskPolicy, JournalEvent, Mode) as Python classes with the same field names; Decimal fields map to `decimal.Decimal`, times to timezone-aware `datetime` (UTC) plus `ts_ns: int`; floats for money are rejected exactly as in Rust.
- Exposed reads: `mt_store.pit(as_of=…)` returning the same query objects as Rust (bars, events, documents, features), materialising to **Arrow** (`pyarrow` / polars zero-copy) for frames; `as_of` is required and naive datetimes raise.
- Async boundary: the binding runs the Rust tokio runtime internally and releases the GIL during I/O; a sync API by default, an `asyncio` variant where useful.
- Type stubs (`mt_store.pyi`) generated and checked by mypy `--strict` in a consumer test package.
- Errors map to typed Python exceptions (`PitBypassError`, `AsOfRequiredError`, `SchemaVersionError`).
- No second implementation: the Python package contains no query logic of its own.

## ToDo

- [ ] Add the PyO3 module (feature or cdylib crate) and the maturin build config; wire it into the uv workspace.
- [ ] Bind the `mt-core` types (conversions for Decimal, datetime, enums) and `pit(as_of)` with Arrow output.
- [ ] Generate and commit `mt_store.pyi`; add a mypy-strict consumer test.
- [ ] Port the `pit` golden fixtures to a pytest suite that runs through the binding against the Supabase CLI stack.
- [ ] Update docs listed under Doc sync.

## Verification

### Tests
- `cargo test -p mt-store` (Rust side) and `uv run pytest packages/…/tests/test_mt_store_binding.py` (Python side) run the **same** golden `pit` fixtures and must return identical rows.
- Round trip: every `mt-core` type → Python → Rust is lossless (property tests with hypothesis on the Python side, proptest on the Rust side); a float price is rejected.
- mypy `--strict` passes on the consumer test using the stubs.

### Scenarios
- Given a Python notebook calls `mt_store.pit(as_of=t).bars(...)`, then it gets only rows with `ingest_time <= t`, identical to the Rust call.
- Given Python code passes a naive datetime, then `AsOfRequiredError` / a typed error is raised.

### Stress / failure injection
- Read 1M bar rows through the binding into polars: no copy beyond Arrow buffers; time logged (not gated). GIL released during the query (a second Python thread keeps running).

## Acceptance criteria

- [ ] `uv sync` builds `mt_store` from the Rust crate; `import mt_store` works on a clean clone
- [ ] `pit` golden fixtures pass in Rust and through the binding with identical results
- [ ] `mt-core` types round-trip losslessly; stubs pass mypy strict
- [ ] CI green (clippy, cargo test, ruff, mypy, pytest, `supabase test db`, gitleaks, `pit` check)

## Exceptions & edge cases

- A platform without a prebuilt wheel: maturin builds from source (Rust toolchain from `rust-toolchain.toml`).
- Nanosecond timestamps: Python `datetime` is µs; `ts_ns` carries the full value.

## Cardinal rules (do NOT)

- Do NOT reimplement `pit` or any `mt-core` type in Python; the binding is the only Python path.
- Do NOT expose a raw SQL or table-read function through the binding.
- Do NOT use floats for money, prices, sizes, fees or tax.
- Do NOT skip, weaken or delete a test to get CI green.
- Do NOT bypass `mt-api`, the risk manager (M11) or `pit(as_of)`; research reads only through `pit`.

## Doc sync on completion

- `docs/18-platform-and-deployment.md` §2.1 and `docs/03-build-spec.md` §3/§4: name the module and how it is built.
- `docs/roadmap/phase-0-foundations.md`: tick T0.21 and T0.22 when every item mapped to them is done.

## Branch & PR

- Branch: `p0/P0-T071-build-the-mt-store-python-module-pyo3-mt-core-ty`
- PR title: `P0-T071: Build the mt_store Python module (PyO3): mt-core types and pit bindings`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T071` run

## Progress log

- 2026-11-19 00:00 · aligner · created
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (new task: one PyO3 module `mt_store` carrying the `mt-core` types and `pit`, so Python shares the Rust implementation)
