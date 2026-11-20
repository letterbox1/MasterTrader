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
depends_on: [P2-T102, P2-T103, P2-T203]
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
updated: 2026-11-20
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P2-T104 · Vectorised screening backtest engine

## Goal / expected outcome

A fast vectorised screener in **`mt_research` (Python, research only)**, on vectorbt (Apache-2.0 + Commons Clause ⚑, [19 §2](../../../docs/19-third-party-register.md#2-python-libraries-we-keep-only-where-absolutely-required-18-22)) or a port of the MIT Vibe-Trading engines, for wide parameter scans that enforces next-bar action and measured costs, and whose results are always labelled 'Screener' and never count for promotion gates.

## Context & references

- Roadmap: [R2.40, R2.41](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.27
- Spec: [03 M7 two backtest paths](../../../docs/03-build-spec.md#m7-research-lab--mt_lab) · [01 §3.4 Vibe-Trading](../../../docs/01-repo-vetting-report.md#34-hkudsvibe-trading--research-and-strategy-generation-layer) (signals shifted one bar, next-open fills) · vectorbt is Apache-2.0 + Commons Clause ⚑ (research only, never in the runtime; dropped from any commercial build, 19 §2/§4)
- [D04 acceptance 1–3](../../../docs/ui/dashboards/D04-research-lab.md): engine labelling, only truth results count for gates, costs on every result
- Depends on P2-T102 (costs) and P2-T103 (datasets), both reached through the `mt-lab-core` binding (P2-T203); strategy signal functions from part A's Rust templates (T2.20/T2.21), exposed as a batch `signals(bars, params)` call through the binding

## Requirements

- Input: a strategy's vectorisable signal function (each Rust template exports a batch `signals(bars, params)` through the binding; Python research strategies expose `signals(df, params)` directly), a `Dataset` and a `CostModel` (both from `mt-lab-core` via the binding).
- Signals act on the next bar open (or next event); same-bar execution is impossible by construction (shift enforced in the engine, not by the strategy).
- Per-trade costs from `CostModel` (fees, spread, impact by size, funding/swap per holding period).
- Result row: `engine=screener`, `gate_eligible=false`, metrics (via P2-T106), trades list.
- Throughput target: ≥ 1,000 parameter sets/min for a 1h-bar, 2-year, single-instrument run on 4 cores.

## ToDo

- [ ] Pick vectorbt (pinned in the uv lock) or port Vibe-Trading engine modules (MIT; keep NOTICE incl. Qlib Apache-2.0) into `packages/mt_research/screener/`; record in `third_party/LICENSES.md` and keep vectorbt's ⚑ row in docs/19
- [ ] Implement enforced next-bar shift and cost application
- [ ] Register a `screener` external job kind (P2-T101 `ExternalJobRunner`, an `mt_research` job container)
- [ ] Label results and set `gate_eligible=false`
- [ ] Tests + benchmark

## Verification

### Tests
- Commands: `uv run pytest packages/mt_research -k screening`.
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
- [ ] CI green: ruff, mypy, `uv run pytest packages/mt_research`, `pit` check

## Exceptions & edge cases

- Instruments with gaps: no fills inside bad-DQ periods.
- Tick/L2-only strategies (scalpers) are not vectorisable: the screener refuses them and points to truth.

## Cardinal rules (do NOT)

- Do NOT let screener results feed gates or lifecycle promotion.
- Do NOT import GPL code (freqtrade) into this engine.
- Do NOT read research/backtest data except through `pit(as_of)` (the `mt-store` crate; the `mt_store` binding on the Python side); the `pit` CI bypass test must stay green.
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
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (stays Python (uv); `pit` via the `mt_store` binding of `mt-store`; Supabase Postgres; commands line)
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (screener stays Python but moves from `mt_lab` to `mt_research` (vectorbt ⚑ research-only per 19 §2); costs/datasets/signals reached through the `mt-lab-core` binding; depends_on + P2-T203; tools unchanged [uv])
