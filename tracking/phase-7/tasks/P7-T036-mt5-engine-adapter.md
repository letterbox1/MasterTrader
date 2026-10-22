---
id: P7-T036
kind: task
title: mt_engine MT5 execution and data adapter via the bridge
phase: 7
type: BUILD
status: backlog
priority: medium
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T034, P7-T035, P2-T021, P2-T027]
requirements: [R7.10]
roadmap_todos: [T7.24]
modules: [M12, M16]
dashboards: [D05]
tools: [git, uv, docker]
mcp: []
env: []
services: [postgres, nats, mt5-bridge (P7-T035), FP Markets MT5 demo]
branch: p7/P7-T036-mt5-engine-adapter
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-7-prove-and-go-live.md]
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

# P7-T036 · mt_engine MT5 execution and data adapter via the bridge

## Goal / expected outcome

NautilusTrader `ExecutionClient`/`DataClient` implementations in `mt_engine` talk to the MT5 bridge, so MasterTradingBot strategies run through M11, the journal, TCA and reconciliation exactly like other venues — paper (demo account) first.

## Context & references

- Roadmap: [R7.10 · ToDo T7.24](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [03 M12](../../../docs/03-build-spec.md#m12-execution--mt_engine) (MT5 Windows bridge for FP Markets) · [14 §8](../../../docs/14-strategy-evidence-and-validation.md#8-mastertradingbot-integration) · [03 M16](../../../docs/03-build-spec.md#m16-live-cost--data-quality-monitor--mt_monitor-always-on-autonomous) (TCA, recon)
- Cross-phase (`depends_on`): P2-T021 (engine node), P2-T027 (epoch client order IDs and restart reconciliation); recon adapter patterns from P1-T042.
- Related: P7-T034, P7-T030 (resting stops via MT5 SL), P7-T025 (recon side), P7-T051 (parity)

## Requirements

- Order types: market, limit, stop; SL/TP attached broker-side on entry (resting stops, P7-T030).
- Instrument mapping from MT5 symbols (FX, metals, index/commodity CFDs, ETF CFDs) to `market.instrument` with contract size, digits, swap.
- Fills/deals → `fill.{venue}`; swaps and commissions → journal + M16 cost events.
- Recon side adapter for P7-T025 (positions, orders, balances).
- Venue registry entry `fp_markets_mt5`; leverage capped by the registry (retail ASIC limits).
- Idempotent client order ids with restart epoch; reconnect with backoff; unconfirmed on disconnect.

## ToDo

- [ ] `packages/mt_engine/adapters/mt5/` exec + data clients.
- [ ] Symbol mapper + cost/swap ingestion.
- [ ] Recon side adapter.
- [ ] Tests (bridge fake + demo).
- [ ] Docs.

## Verification

### Tests
- Unit: symbol mapping, order translation, deal parsing (fixtures from demo).
- Integration (demo): full order lifecycle through M11; fill journalled; TCA computed; recon clean.

### Scenarios
- Given the bridge reports `broker_disconnected`, then the account becomes unconfirmed and entries are rejected.
- Given an MT5 deal with swap, then the journal records the swap as a funding/financing event.

### Stress / failure injection
- Replay 1 week of MasterTradingBot signals at 10× speed on demo: no dropped orders; adapter restart mid-run → no duplicates.

## Acceptance criteria

- [ ] Adapter passes demo integration through M11 → journal → TCA → recon.
- [ ] CI green.

## Exceptions & edge cases

- Hedging-mode vs netting-mode accounts: adapter reads account mode and maps positions accordingly; STP for strategies sharing an account (14 §4 pitfalls).

## Cardinal rules (do NOT)

- Do NOT route MT5 orders outside M11.
- Do NOT trade live on MT5 until P7-T051 parity passes.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT use keys that are not trade-only, IP-locked and withdrawal-disabled; no live money before the P7 gates pass.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/03-build-spec.md` M12: MT5 adapter details.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.24 when this item is done.

## Branch & PR

- Branch: `p7/P7-T036-mt5-engine-adapter`
- PR title: `P7-T036: mt_engine MT5 execution and data adapter via the bridge`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T036` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (deps on the deployed bridge (P7-T035) and P2-T021/T027; fields)
