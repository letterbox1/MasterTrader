---
id: P2-T202
kind: task
title: mt-risk PyO3 binding for the Python node, Python strategies and lab backtests
phase: 2
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T017, P0-T071]
requirements: [R2.10, R2.N2]
roadmap_todos: [T2.22]
modules: [M11, mt-risk]
dashboards: []
tools: [git, cargo, uv, maturin]
mcp: []
env: []
services: []
branch: p2/P2-T202-mt-risk-pyo3-binding
pr: ""
doc_sync: [docs/03-build-spec.md, docs/18-platform-and-deployment.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T202 · mt-risk PyO3 binding for the Python node, Python strategies and lab backtests

## Goal / expected outcome

The Python side calls the **same** `mt-risk` code as the Rust side: a PyO3 binding exposes `RiskGate` (decide and preview), the compiled policy cache and the sizing models to the Nautilus Python node, Python strategies (`mt_strategy`'s `RiskGateProtocol`) and the lab's truth backtests. There is one risk implementation ([18 §2.1](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates), [03 M11](../../../docs/03-build-spec.md#m11-risk-manager--mt_risk-built-in-user-inputs-via-uitelegram-later-mcp)); the risk golden suite runs against the crate and a parity subset runs through the binding.

## Context & references

- Roadmap: [R2.10, R2.N2](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.22
- Platform: [18 §2.1 `mt-risk`](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates) · [18 §2.2 rule](../../../docs/18-platform-and-deployment.md#22-python-uv-workspace-packages-only-where-absolutely-required) (Python never places orders without `mt-risk`)
- Built on: P2-T017 (`RiskGate` in the crate), P0-T071 (the `mt_store` PyO3 module carrying the `mt-core` types; this binding reuses those classes).
- Used by: P2-T003 (`RiskGateProtocol` default implementation), P2-T021 (Python node path), P2-T105 (truth backtests), P2-T052 (no-bypass tests through Python).

## Requirements

- Python module `mt_risk` (PyO3 abi3, built with maturin in the uv workspace) exposing `RiskGate.decide(intent, state)`, `RiskGate.preview(intent)`, the KV-fed policy cache handle and the sizing models; `OrderIntent` and decisions are the `mt-core` classes from `mt_store`, never redefined in Python.
- No logic in Python: the binding is a thin wrapper; any check added to `mt-risk` appears in Python with no Python change.
- Hot path: the decision call releases the GIL and adds ≤ 20 µs p99 over the native call (keeps R2.N1).
- Default-deny holds across the boundary: a Rust error or panic becomes a `reject` with `internal_default_deny`, never a Python exception that a caller could swallow and submit anyway.
- Type stubs (`mt_risk.pyi`) checked by mypy `--strict`.

## ToDo

- [ ] `python` feature (or thin cdylib) in `crates/mt-risk` with PyO3 wrappers; maturin config; uv workspace member
- [ ] Map errors and panics to default-deny decisions
- [ ] Type stubs + mypy check in a consumer test package
- [ ] Parity subset: 50 golden cases run through the binding and must equal the crate's results
- [ ] Overhead benchmark (native vs binding)
- [ ] Update docs listed under Doc sync

## Verification

### Tests
- Commands: `cargo test -p mt-risk`, `cargo clippy -p mt-risk`, `uv run pytest packages/mt_strategy -k risk_binding`.
- Parity: the golden subset gives identical decisions, reasons and sizes through Python and Rust.
- Default-deny: a forced panic in a check returns `reject internal_default_deny` to Python.

### Scenarios
- Given a Python strategy on the Python node, when it submits an intent above the sleeve limit, then the binding returns the same reject reason the Rust node would.

### Stress / failure injection
- 1M decisions through the binding: p99 overhead ≤ 20 µs over native; no memory growth.

## Acceptance criteria

- [ ] Python and Rust return identical decisions on the golden subset
- [ ] Errors and panics are default-deny
- [ ] Overhead benchmark recorded
- [ ] CI green: `cargo clippy`, `cargo test -p mt-risk`, `uv run pytest`, mypy on the stubs

## Exceptions & edge cases

- The binding never caches policy itself; it reads the crate's cache, so a policy change applies to both nodes at once.

## Cardinal rules (do NOT)

- Do NOT reimplement any risk check in Python.
- Do NOT bypass `mt-api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.

## Doc sync on completion

- `docs/03-build-spec.md` M11 and `docs/18-platform-and-deployment.md` §2.1: binding name and use.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.22 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T202-mt-risk-pyo3-binding`
- PR title: `P2-T202: mt-risk PyO3 binding for the Python node, Python strategies and lab backtests`
- PR checklist: tests added and green · docs synced · task file ticked · `./kanban done P2-T202` run

## Progress log

- 2026-11-19 00:00 · aligner · created: re-platformed per docs/18 (`mt-risk` is one Rust crate; the Python node, strategies and lab need a binding no task built)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (Rust/Python split per 18 §2; `cargo` + `uv run pytest` commands)
