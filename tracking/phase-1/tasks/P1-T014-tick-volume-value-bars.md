---
id: P1-T014
kind: task
title: Add tick, volume and value bars
phase: 1
type: BUILD
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T013, P1-T012]
requirements: [R1.02]
roadmap_todos: [T1.21]
modules: [M1]
dashboards: [D02]
tools: [git, cargo, uv, docker]
mcp: []
env: []
services: [supabase-postgres]
branch: p1/P1-T014-tick-volume-value-bars
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/03-build-spec.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-11-19
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P1-T014 · Add tick, volume and value bars

## Goal / expected outcome

Information-driven bars (every N trades, every V units, every X notional) are available on demand from Parquet trades and live from the stream, for D02 charts and P2 strategies.

## Context & references

- Roadmap: requirements [R1.02](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.21](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Roadmap T1.21 ("tick/volume/value bar support") · [03 M1](../../../docs/03-build-spec.md#m1-market--macro-data--mt_datamarket) · UI [D02 Markets](../../../docs/ui/dashboards/D02-markets.md) (`PriceChart` incl. tick/volume bars)
- Depends on (this phase): P1-T013, P1-T012

## Requirements

- `mt-store` `bars::info_bars(instrument, kind = tick|volume|value, threshold, from, to)` (Rust, exposed to Python through the PyO3 module) built from Parquet trades
- Live variant in the `mt-recorder` bar builder for configured (instrument, kind, threshold) pairs, publishing `md.*.bar.{kind}{threshold}`
- Not stored in the partitioned bar tables by default (they are not time-based); cached results keyed by parameters
- Exact reproducibility: the same trades and threshold always give the same bars

## ToDo

- [ ] Implement batch builder over Parquet and the live incremental builder
- [ ] Spec grammar for `spec=` (`t500`, `v10`, `n1000000`) shared with the API
- [ ] Write the tests listed under Verification
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Property (`cargo test -p mt-store info_bars`, proptest): concatenating live bars equals batch bars over the same trade range; `uv run pytest -k info_bars` checks the binding
- Unit: threshold edge cases (a single trade larger than the volume threshold closes one bar)

### Scenarios

- Given a request for `t500` bars over a day, when served, then it streams from Parquet in < 2 s for a liquid symbol

### Stress / failure injection

- Load: one month of BTCUSDT trades → `v100` bars in < 60 s on the workstation

## Acceptance criteria

- [ ] Live and batch info bars match exactly in the property test
- [ ] D02 can request them via `/markets/{id}/bars?spec=t500`
- [ ] CI green (`cargo clippy`, `cargo test`, ruff, mypy, `uv run pytest`, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Instruments with no trades (FX quotes only) return a clear 422 "no trade data"

## Cardinal rules (do NOT)

- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT bypass `mt-api`, the risk manager (M11) or `pit(as_of)` (`mt-store`, also through its Python binding); research and backtest reads go through `pit` only.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.21 once every task traced to it in PHASE.md is done; note P1-T014 next to it.
- `docs/03-build-spec.md` §M1: document the info-bar spec grammar

## Branch & PR

- Branch: `p1/P1-T014-tick-volume-value-bars`
- PR title: `P1-T014: Add tick, volume and value bars`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T014` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (run fields)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (info bars in Rust `mt-store` (Python binding) and the `mt-recorder` live builder; no hypertables; tools cargo+uv; services supabase-postgres)
