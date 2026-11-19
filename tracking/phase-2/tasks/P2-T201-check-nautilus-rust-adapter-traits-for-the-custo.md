---
id: P2-T201
kind: task
title: Check Nautilus Rust adapter traits for the custom Alpaca, OANDA and IG adapters
phase: 2
type: RESEARCH
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.30]
roadmap_todos: [T2.25]
modules: [M12, mt-engine]
dashboards: []
tools: [git, cargo]
mcp: []
env: []
services: []
branch: p2/P2-T201-nautilus-rust-adapter-traits
pr: ""
doc_sync: [docs/research/engines-nautilus-hummingbot-freqtrade.md, docs/18-platform-and-deployment.md, docs/03-build-spec.md]
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

# P2-T201 · Check Nautilus Rust adapter traits for the custom Alpaca, OANDA and IG adapters

## Goal / expected outcome

Before P2-T024–P2-T026 write the custom **Alpaca, OANDA v20 and IG** adapters in Rust ([18 §2.1](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates)), a dated, cited note says how to build them against the pinned NautilusTrader release: which Rust data/execution client traits to implement, how a Rust adapter is registered with the Rust live node, and how the same adapter is reached from the Python node (PyO3 exposure) for venues or strategies that run there. The three adapter tasks start from one agreed skeleton instead of three guesses.

## Context & references

- Roadmap: [R2.30](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.25
- Platform: [18 §2.1 `mt-engine`](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates) (custom adapters in Rust against Nautilus's adapter traits) · [18 §10](../../../docs/18-platform-and-deployment.md#10-sources)
- Spec: [03 M12 custom adapters](../../../docs/03-build-spec.md#m12-execution--mt_engine)
- Related: P2-T200 (built-in venues), P2-T024 Alpaca, P2-T025 OANDA, P2-T026 IG, P2-T073 (cancel-after per venue).

## Requirements

- The trait set (data client, execution client, instrument provider, reconciliation reports) and its stability in the pinned release; breaking changes in the last releases; a reference Rust adapter to copy the shape from.
- Registration: how the Rust live node loads a custom client factory; how the Python node reaches it (PyO3 wrapper) or whether a Python-node fallback adapter is needed (U).
- Per venue (Alpaca, OANDA v20, IG): REST/stream protocols (Alpaca WS, OANDA v20 streaming, IG Lightstreamer) and the Rust crates available for them (licence checked), auth model on paper/practice/demo, netting (no STP field), cancel-after support.
- Output: a skeleton module layout under `crates/mt-engine/src/adapters/` agreed for all three, written into the research doc with sources and the check date; (U) where unconfirmed.

## ToDo

- [ ] Read the pinned Nautilus adapter traits and one reference Rust adapter
- [ ] Check Rust client options for Lightstreamer (IG) and OANDA streaming; note licences
- [ ] Write the skeleton layout and a compile-only stub adapter (`cargo check -p mt-engine`)
- [ ] Research doc section with sources and date; progress log

## Verification

### Tests
- Commands: `cargo check -p mt-engine` and `cargo test -p mt-engine adapters::stub` (the stub client factory registers with the node and returns empty instrument lists).

### Scenarios
- Given the stub adapter, when the Rust node starts with it configured, then it reports the venue as connected to a mock server and reconciles zero orders.

### Stress / failure injection
- n/a: research task with a compile-only stub.

## Acceptance criteria

- [ ] Trait set, registration path and Python-node reach documented with sources and date
- [ ] Per-venue protocol notes and crate licences recorded
- [ ] Stub compiles in the workspace

## Exceptions & edge cases

- If no maintained Rust Lightstreamer client exists (U), IG streaming is written against the Lightstreamer TLCP protocol directly, or IG stays on the Python node; the note records which.

## Cardinal rules (do NOT)

- Do NOT pull in a crate with an incompatible licence; record every licence.
- Do NOT use real credentials; mock servers only.
- Do NOT bypass `mt-api`, the risk manager (M11) or `pit(as_of)`.

## Doc sync on completion

- `docs/research/engines-nautilus-hummingbot-freqtrade.md`: custom-adapter section.
- `docs/18-platform-and-deployment.md` §2.1 and `docs/03-build-spec.md` M12: link the note; replace any (U) it closes.

## Branch & PR

- Branch: `p2/P2-T201-nautilus-rust-adapter-traits`
- PR title: `P2-T201: Check Nautilus Rust adapter traits for the custom Alpaca, OANDA and IG adapters`
- PR checklist: sources cited and dated · stub compiles · task file ticked · `./kanban done P2-T201` run

## Progress log

- 2026-11-19 00:00 · aligner · created: re-platformed per docs/18 (custom adapters move to Rust; nothing checked the Nautilus adapter traits first)
