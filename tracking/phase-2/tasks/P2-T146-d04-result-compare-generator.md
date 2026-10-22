---
id: P2-T146
kind: task
title: D04 backtest result, compare view and generator panel
phase: 2
type: BUILD
status: backlog
priority: high
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T145, P2-T114, P2-T116]
requirements: [R2.50, R2.40, R2.42, R2.43, R2.45]
roadmap_todos: [T2.32]
modules: [M15, M7]
dashboards: [D04]
tools: [pnpm]
mcp: []
env: []
services: []
branch: p2/P2-T146-d04-result-compare-generator
pr: ""
doc_sync: [docs/ui/dashboards/D04-research-lab.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T146 · D04 backtest result, compare view and generator panel

## Goal / expected outcome

`/lab/backtests/:id` shows a result with Summary, Trades, Robustness, Bias checks, Costs, Gates and Reproduce tabs (incl. every harness section), `/lab/experiments/:id` compares up to 6 runs, and the generator panel shows sandboxed generations.

## Context & references

- Roadmap: [R2.40, R2.42, R2.43, R2.45, R2.50](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.32 · exit criterion 1 ('the validation report shows all harness sections')
- [D04 result/compare/generator](../../../docs/ui/dashboards/D04-research-lab.md) · tab contents decided ([17 §D P2-B052](../../../docs/17-decisions-register.md#d-other-decisions)): D04 now lists cost stress 2×/3×, per-year/per-regime, trial counter and worst fold

## Requirements

- Header: strategy@version, range, engine label ('Screener' vs 'Nautilus truth'), cost model + snapshot id, data hash; amber 'Unrealistic costs' chip on zero-cost runs (D04 acceptance 1–3).
- Summary: metrics, costs breakdown, equity vs benchmark, drawdown, monthly heatmap.
- Trades: DataTable (cards on phones); click → chart with entry/exit markers.
- Robustness: walk-forward folds incl. worst fold + positive share, purged K-fold, MC distribution with p-value, bootstrap CI, DSR with trial count, parameter-stability heatmap, per-year and per-regime tables.
- Bias checks: look-ahead/recursive/repaint results with offending signals; PIT audit; LLM leakage items with quoted lines and waive action (`lab.leakage.waive`, **C2**, reason required).
- Costs: modelled vs measured; sensitivity 0.5×/1×/2×/3× with the 2×/3× stress verdicts.
- Gates: which gates this run satisfies; Reproduce: code version, manifest, snapshots, seed, engine version, Re-run (C1); Export report (HTML/PDF).
- Compare: ≤ 6 runs, best values highlighted, overlaid equity, param diff, cost-assumption diff.
- Generator panel: prompt → progress → read-only code diff, sandbox log, first backtest; Save as draft (C1) with the sandbox banner.
- Every tile implements the [data states](../../../docs/ui/README.md#31-data-states-every-tile-implements-all-of-them) (loading skeleton ≤ 300 ms, live, stale chip, degraded, error card with retry → D16, empty with primary action, PAPER/LIVE markers, unconfirmed hatching).

## ToDo

- [ ] Routes `lab/backtests/$id.tsx`, `lab/experiments/$id.tsx`, generator panel component
- [ ] Tabs bound to `/lab/backtests/{id}` sections
- [ ] Export link
- [ ] Playwright + matrix; doc sync

## Verification

### Tests
- Playwright: DESIGN.md §6.8 viewport matrix (overflow + fixed-bar overlap checks) and axe on the new routes; Vitest + Testing Library for components.
- Playwright: validation fixture shows every harness section; Re-run produces `reproduced=true` badge.

### Scenarios
- Given a screener result, then the Gates tab says 'not eligible: screener' for every performance gate.
- Given a seeded look-ahead strategy, then Bias checks shows the analyser fail and the leakage item quoting the line.
- Given a 7th run selected for compare, then selection is refused with 'max 6'.

### Stress / failure injection
- Trade list of 100k trades: server-side pagination; tab switch < 300 ms.

## Acceptance criteria

- [ ] All D04 result tabs implemented incl. every harness section
- [ ] D04 acceptance 1–4 visible in UI
- [ ] Viewport matrix + axe green on result/compare routes
- [ ] CI green (lint, types, tests, viewport matrix where UI)

## Exceptions & edge cases

- Incomplete experiment (crashed section): tab shows error card, overall verdict 'fail'.
- Result for a deleted strategy version still renders from stored data.

## Cardinal rules (do NOT)

- Do NOT enforce confirmation levels only in the UI; C1–C3/Kill are enforced server-side by `mt_api`.
- Do NOT use `100vh`/`h-screen`, unprefixed multi-column grids or the Tailwind CDN (DESIGN.md §6.3–6.5).
- Do NOT sum or show paper and live money without a mode label.
- Do NOT show any gate as passed when its data is missing.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/ui/dashboards/D04-research-lab.md`: confirm tab contents as built.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.32 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T146-d04-result-compare-generator`
- PR title: `P2-T146: D04 backtest result, compare view and generator panel`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T146` run · Playwright viewport matrix + axe green

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (leakage waiver C2, D04 tabs per 17 §D P2-B052)
