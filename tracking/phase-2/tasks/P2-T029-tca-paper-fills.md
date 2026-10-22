---
id: P2-T029
kind: task
title: TCA on paper fills and measured-cost feedback to the lab
phase: 2
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T021, P1-T038, P1-T039, P1-T040]
requirements: [R2.34]
roadmap_todos: [T2.26]
modules: [M16, M12]
dashboards: [D05]
tools: [uv]
mcp: []
env: []
services: [nats, postgres]
branch: p2/P2-T029-tca-paper-fills
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T029 · TCA on paper fills and measured-cost feedback to the lab

## Goal / expected outcome

`mt_monitor` computes implementation shortfall for every paper/testnet order (decision, arrival, fill VWAP, fees, funding → delay / spread-impact / fees), keeps the realised-vs-modelled cost ratio per strategy × venue × instrument, tells M11 to pause on blow-outs and publishes measured cost models the lab uses.

## Context & references

- Roadmap: [R2.34](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.26
- Spec: [03 M16 TCA](../../../docs/03-build-spec.md#m16-live-cost--data-quality-monitor--mt_monitor-always-on-autonomous) · Flow: [02 F2 step 8](../../../docs/02-v1-architecture.md#8-end-to-end-flows)
- Cross-phase (`depends_on`): TCA scaffolding + spreads (P1-T040), fees (P1-T038), funding/financing (P1-T039), all T1.28 / R1.11.
- Defaults: cost blow-out = realised ÷ modelled > **1.5× over the last 20 fills → pause the bot**, alert ([16 §2.1](../../../docs/16-configuration-and-safety-model.md#21-risk-sizing-and-drawdown)); the sleeve kill criterion "implementation shortfall > 2× modelled" is P7 (16 §2.6, R7.06).
- Consumers: lab cost models (P2-T102, R2.40); D05 TCA tab (P2-T147); weekly cost review (P2-T150).

## Requirements

- Per order: decision price (signal time mid), arrival price (mid at submit), fill VWAP, fees (actual), funding/financing accrued while open → IS bps split into delay, spread/impact, fees.
- Writes `audit.cost_event` (per order) and `market.cost_model` (rolling measured spread/slippage/fee per venue × instrument × hour-of-week) consumed by the lab.
- Rolling realised-vs-modelled ratio per bot × venue × instrument over the last 20 fills (window and threshold are L3 settings, defaults 20 fills / 1.5×); ratio > 1.5× → `cost.alert` → M11 pauses the affected **bot** (03 M16, 16 §2.1) and alerts.
- Prometheus metrics + `/data/costs?tca=1` for D05.

## ToDo

- [ ] `packages/mt_monitor/tca.py` consumer of `fill.*` + `ord.*`
- [ ] Cost model table + publisher
- [ ] M11 pause hook (`risk.event{type: cost_blowout}`)
- [ ] Tests
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Unit: IS decomposition on hand-worked examples.
- Integration: sandbox fills → cost events → ratio over 20 fills → bot paused at 1.6×; other bots on the same venue keep trading.
- Unit: funding accrual for a held perp position.

### Scenarios
- Given slippage doubles on ETHUSDT (sandbox replay), when the ratio over the last 20 fills crosses 1.5×, then the bot pauses and a warning alert names the bot/venue/instrument.

### Stress / failure injection
- Replay 50k fills: TCA lag < 5 s behind fills; no unbounded memory.

## Acceptance criteria

- [ ] Every paper/testnet order has a cost event
- [ ] Ratio-based pause works
- [ ] Measured costs available to the lab
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Missing decision price (manual orders): use arrival as decision; flagged.
- Venue fee tier changes: next fills use new tier; model window adapts.

## Cardinal rules (do NOT)

- Do NOT use fixed-bps slippage for illiquid assets in the cost model (14 §6).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- No paid data/APIs; free tiers only (03 §1).

## Doc sync on completion

- `docs/03-build-spec.md` M16: TCA fields and `market.cost_model` contract.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.26 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T029-tca-paper-fills`
- PR title: `P2-T029: TCA on paper fills and measured-cost feedback to the lab`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T029` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (cost blow-out per 16 §2.1 (1.5× over 20 fills → pause the bot), cross-phase cost deps)
