---
id: P2-T104
kind: task
title: Vectorised screening backtest engine
phase: 2
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T102, P2-T103]
requirements: [R2.40, R2.41]
roadmap_todos: [T2.27]
modules: [M7]
dashboards: [D04]
tools: [uv]
mcp: []
env: []
services: []
branch: p2/P2-T104-screening-engine
pr: ""
doc_sync: [docs/03-build-spec.md, third_party/LICENSES.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T104 · Vectorised screening backtest engine

## Goal / expected outcome

A fast vectorised screener (vectorbt or a port of the MIT Vibe-Trading engines) for wide parameter scans that enforces next-bar action and measured costs, and whose results are always labelled 'Screener' and never count for promotion gates.

## Context & references

- Roadmap: [R2.40, R2.41](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.27
- Spec: [03 M7 two backtest paths](../../../docs/03-build-spec.md#m7-research-lab--mt_lab) · [01 §3.4 Vibe-Trading](../../../docs/01-repo-vetting-report.md#34-hkudsvibe-trading--research-and-strategy-generation-layer) (signals shifted one bar, next-open fills) · vectorbt is Apache-2.0 + Commons Clause (personal use only)
- [D04 acceptance 1–3](../../../docs/ui/dashboards/D04-research-lab.md): engine labelling, only truth results count for gates, costs on every result
- Depends on P2-T102 (costs), P2-T103 (datasets); strategy signal functions from part A's M0 templates (T2.20/T2.21)

## Requirements

- Input: a strategy's vectorisable signal function (template exposes `signals(df, params)`), a `Dataset` and a `CostModel`.
- Signals act on the next bar open (or next event); same-bar execution is impossible by construction (shift enforced in the engine, not by the strategy).
- Per-trade costs from `CostModel` (fees, spread, impact by size, funding/swap per holding period).
- Result row: `engine=screener`, `gate_eligible=false`, metrics (via P2-T106), trades list.
- Throughput target: ≥ 1,000 parameter sets/min for a 1h-bar, 2-year, single-instrument run on 4 cores.

## ToDo

- [ ] Pick vectorbt (pip, pinned) or port Vibe-Trading engine modules (MIT; keep NOTICE incl. Qlib Apache-2.0) into `mt_lab/screener/`; record in `third_party/LICENSES.md`
- [ ] Implement enforced next-bar shift and cost application
- [ ] Register a `screener` `JobRunner` (P2-T101)
- [ ] Label results and set `gate_eligible=false`
- [ ] Tests + benchmark

## Verification

### Tests
- Unit: a signal on bar t fills at bar t+1 open; cost totals match CostModel for a fixed trade list.
- Golden: EMA-cross on a fixture yields a stored trade list and equity curve.
- Benchmark test asserting the throughput target (marked slow).

### Scenarios
- Given a strategy that would profit only by trading at the signal bar's close, when screened, then the profit disappears (shift enforced).
- Given a screener result, when a promotion is attempted using it, then the gate evaluator rejects it as not truth.

### Stress / failure injection
- 10,000-trial sweep on the screener: memory stays bounded (chunked), no worker OOM.
- Strategy function raising mid-sweep: that trial fails, the sweep continues and records the error.

## Acceptance criteria

- [ ] Results labelled 'Screener' and `gate_eligible=false`
- [ ] Next-bar and cost golden tests pass
- [ ] Licence recorded in `third_party/LICENSES.md`
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Instruments with gaps: no fills inside bad-DQ periods.
- Tick/L2-only strategies (scalpers) are not vectorisable: the screener refuses them and points to truth.

## Cardinal rules (do NOT)

- Do NOT let screener results feed gates or lifecycle promotion.
- Do NOT import GPL code (freqtrade) into this engine.
- Do NOT read research/backtest data except through `mt_store.pit(as_of=…)`; the `pit` CI bypass test must stay green.
- Do NOT add telemetry or referral IDs via vendored code; pin images by digest; record vendored code in `third_party/LICENSES.md`.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/03-build-spec.md` M7: which screening engine was chosen.
- `third_party/LICENSES.md`: vendored engine + NOTICE.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.27 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T104-screening-engine`
- PR title: `P2-T104: Vectorised screening backtest engine`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T104` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (run fields (no decision change))
