---
id: P2-T200
kind: task
title: Check Nautilus Rust live-node adapter readiness per venue (Binance, Bybit, IBKR)
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
tools: [git, cargo, uv]
mcp: []
env: []
services: []
branch: p2/P2-T200-nautilus-rust-node-readiness
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

# P2-T200 · Check Nautilus Rust live-node adapter readiness per venue (Binance, Bybit, IBKR)

## Goal / expected outcome

A dated, cited answer per venue to the (U) in [18 §2.1](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates): does the pinned NautilusTrader release have a **production-ready Rust live adapter** (data + execution) for the Nautilus built-in venues Phase 2 uses (Binance spot + USD-M futures testnet, Bybit testnet, IBKR paper), so `mt-engine` runs that venue on the **Rust live node**, or does it stay on the **Python node** with the same `mt-risk` binding? The answer becomes the per-venue default `engine.node: rust|python` in the venue registry config, which P2-T021 and P2-T023 read.

## Context & references

- Roadmap: [R2.30](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.25
- Platform: [18 §2.1 `mt-engine`](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates) · [18 §10 sources](../../../docs/18-platform-and-deployment.md#10-sources) · decision [17 §G](../../../docs/17-decisions-register.md#g-platform-rust-and-python-supabase-vercel-workstation-first-2026-11-19)
- Spec: [03 M12](../../../docs/03-build-spec.md#m12-execution--mt_engine) (built-in adapters: IBKR, Binance, Bybit, OKX, Coinbase, Kraken, Hyperliquid, Betfair)
- Prior research: [engines-nautilus-hummingbot-freqtrade](../../../docs/research/engines-nautilus-hummingbot-freqtrade.md)
- Unblocks: P2-T021 (node wrapper), P2-T023 (testnet configs). Custom adapters (Alpaca, OANDA, IG) are P2-T201.

## Requirements

- For each venue (Binance spot, Binance USD-M, Bybit, IBKR; plus a one-line status for OKX, Coinbase, Kraken, Hyperliquid, Betfair): Rust data client, Rust execution client, order types used by P2 (market, limit post-only, stop, reduce-only), STP field support, cancel-after / countdown support, reconciliation on start, testnet/paper endpoints, open issues marked blocking.
- "Production-ready" means: released (not only on `develop`), covered by Nautilus's own tests, documented, and no open blocking issue for the order types above. Anything else is "Python node".
- Pin the Nautilus version the answer applies to; the answer is re-checked on every Nautilus bump (supply-chain rule).
- Output: a short report section in the research doc (sources and check date), a per-venue table, and `config/defaults/engine.yaml` `venues.<venue>.node: rust|python` defaults (Python where unsure).
- Facts that stay unverified are marked **(U)** and default to the Python node.

## ToDo

- [ ] Read the pinned release notes, adapter docs and source for each venue; note test coverage and open issues
- [ ] Spike: start the Rust live node against Binance spot testnet with recorded fixtures (no keys) and place/cancel on a mock server
- [ ] Write the per-venue table and sources into the research doc (dated)
- [ ] Set `venues.<venue>.node` defaults in `config/defaults/engine.yaml`
- [ ] Update docs listed under Doc sync; progress log with sources

## Verification

### Tests
- Commands: `cargo test -p mt-engine node_selection` (the config loader picks the node per venue from the defaults file; an unknown venue defaults to `python`).

### Scenarios
- Given a venue marked `rust`, when P2-T021 builds the node config, then that venue runs on the Rust live node; given `python`, the Python node with the `mt-risk` binding (P2-T202).

### Stress / failure injection
- n/a: research task; the spike runs against a mock server only.

## Acceptance criteria

- [ ] Every P2 venue has a dated, cited `rust` or `python` answer with the Nautilus version
- [ ] `config/defaults/engine.yaml` holds the per-venue defaults
- [ ] (U) items listed with the check that would close them

## Exceptions & edge cases

- A venue whose Rust adapter lacks one P2 order type (e.g. STP or cancel-after) stays on the Python node until it has it.
- Mixed nodes are allowed: venues are independent; `mt-risk` is linked in either way.

## Cardinal rules (do NOT)

- Do NOT use real keys; keyless fixtures and mock servers only (build first, keys last).
- Do NOT mark a venue `rust` on the strength of unreleased code.
- Do NOT bypass `mt-api`, the risk manager (M11) or `pit(as_of)`.

## Doc sync on completion

- `docs/research/engines-nautilus-hummingbot-freqtrade.md`: per-venue table with sources and date.
- `docs/18-platform-and-deployment.md` §2.1 and `docs/03-build-spec.md` M12: replace the (U) with the answer.

## Branch & PR

- Branch: `p2/P2-T200-nautilus-rust-node-readiness`
- PR title: `P2-T200: Check Nautilus Rust live-node adapter readiness per venue (Binance, Bybit, IBKR)`
- PR checklist: sources cited and dated · defaults file added · task file ticked · `./kanban done P2-T200` run

## Progress log

- 2026-11-19 00:00 · aligner · created: re-platformed per docs/18 (18 §2.1 makes the Rust-vs-Python node a per-venue (U) answer; nothing checked it)
