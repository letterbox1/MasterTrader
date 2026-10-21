---
id: P1-T034
kind: task
title: Add the cross-source divergence check
phase: 1
type: BUILD
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T030, P1-T011, P1-T016, P1-T017]
requirements: [R1.10]
roadmap_todos: [T1.27]
modules: [M16]
dashboards: [D07]
branch: p1/P1-T034-dq-check-cross-source-divergence
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/03-build-spec.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P1-T034 · Add the cross-source divergence check

## Goal / expected outcome

Mid prices of the same instrument from two free sources are compared continuously in bps; sustained divergence raises an incident and feeds the D07 divergence chart.

## Context & references

- Roadmap: requirements [R1.10](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.27](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M16](../../../docs/03-build-spec.md#m16-live-cost--data-quality-monitor--mt_monitor-always-on-autonomous) (DQ checks table) · flow [02 §8 F1](../../../docs/02-v1-architecture.md#8-end-to-end-flows) step 5 · subjects [02 §6](../../../docs/02-v1-architecture.md#6-messaging-nats) · degraded modes [02 §9.3](../../../docs/02-v1-architecture.md#93-degraded-modes) · UI [D07 Data & Quality](../../../docs/ui/dashboards/D07-data-quality.md) Quality tab (Binance vs Bybit/OKX/Coinbase; OANDA vs Dukascopy/IG)
- Risk table: "cross-source references for every critical feed" ([phase 1 §7 risks](../../../docs/roadmap/phase-1-data-and-monitoring.md#7-risks--open-questions))
- Depends on (this phase): P1-T030, P1-T011, P1-T016, P1-T017

## Requirements

- Pairs configured in `config/dq_checks.yaml` (e.g. BTCUSDT Binance↔OKX, Binance↔Coinbase (USD vs USDT basis tracked separately); EURUSD OANDA↔IG; nightly OANDA↔Dukascopy)
- Time-aligned mids (last quote within 500 ms on both sides); divergence bps = |m1 − m2| / avg · 1e4
- Thresholds per class (defaults: crypto 25 bps, FX majors 5 bps), sustained ≥ 5 s → `degraded`; ≥ 4× threshold → `bad` on the outlier side when a third source agrees with the other
- Stocks: compare Alpaca IEX vs Finnhub free quotes (60/min, P0 key) at low frequency, or record "single source" explicitly in D07
- Metric `mt_dq_divergence_bps{pair}` for the D07 chart

## ToDo

- [ ] Implement aligned-mid comparator and majority vote
- [ ] Configure pairs for the universe
- [ ] Fault injection: offset one source by 50 bps
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Fault injection: offset one source → incident within threshold window; majority picks the faulty side with 3 sources
- Unit: alignment rejects stale counterpart quotes

### Scenarios

- Given USDT trades at a 20 bps discount to USD, when comparing Binance USDT vs Coinbase USD, then the stablecoin basis is removed before comparing

### Stress / failure injection

- n/a beyond the fault-injection suite; the comparator runs on the same evaluation loop (load covered by P1-T030)

## Acceptance criteria

- [ ] Every major pair has a configured divergence pair (or an explicit single-source note) and the fault test passes
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- One side stale: divergence check suspended (stale wins), no double alert

## Cardinal rules (do NOT)

- Do NOT UPDATE or DELETE WORM rows (`audit.*`); resolutions and corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT let any path loosen DQ thresholds, risk or alert routing without C3 (Telegram + TOTP + cool-down); tightening is C1.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.27 once every task traced to it in PHASE.md is done; note P1-T034 next to it.
- `docs/03-build-spec.md` §M16: default divergence thresholds and pairs

## Branch & PR

- Branch: `p1/P1-T034-dq-check-cross-source-divergence`
- PR title: `P1-T034: Add the cross-source divergence check`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T034` run

## Progress log

- 2026-10-21 00:00 · planner · created
