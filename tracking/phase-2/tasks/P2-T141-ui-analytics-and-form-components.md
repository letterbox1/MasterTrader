---
id: P2-T141
kind: task
title: Analytics and form components: EquityCurve, Distribution, Heatmap, ParamForm, CodeEditor
phase: 2
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.50]
roadmap_todos: [T2.32]
modules: [M15]
dashboards: [D03, D04]
branch: p2/P2-T141-ui-analytics-and-form-components
pr: ""
doc_sync: [docs/ui/components.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T141 · Analytics and form components: EquityCurve, Distribution, Heatmap, ParamForm, CodeEditor

## Goal / expected outcome

The analytics (ECharts) and form components D03/D04 need — `EquityCurve`, `Distribution`, `Heatmap`, `Gauge/LimitBar` polish, `ParamForm` generated from a manifest parameter JSON schema and `CodeEditor` (Monaco, read-only on phones). `DiffView`/`C3Flow` come from part A (currently P2-T043).

## Context & references

- Roadmap: [R2.50](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.32
- [components §2 and §4](../../../docs/ui/components.md) · [02 §10 frontend choices](../../../docs/02-v1-architecture.md#10-frontend-architecture) (ECharts Apache-2.0, react-hook-form + zod from OpenAPI)
- Parameter schema format from part A's templates (T2.21 in part A (P2-T001–T099))

## Requirements

- `EquityCurve(series[], benchmark?, drawdown?)`: strategy vs benchmark vs backtest expectation bands; drawdown sub-chart; PAPER/LIVE labels.
- `Distribution(bins, markers)`: MC permutation histogram with observed-Sharpe marker and p-value label; bootstrap CI band.
- `Heatmap(matrix, scale)`: monthly returns and parameter-stability slices; scrolls inside its own box < md; colour + numeric text (never colour alone).
- `ParamForm(schema)`: renders types/ranges/defaults/conditional params from the manifest JSON schema; zod validation; shows sweep-range mode for D04.
- `CodeEditor`: Monaco, lazy-loaded; read-only on phones with a 'continue on desktop' note; code/manifest diffs reuse part A's `DiffView` (Monaco diff mode for code).
- ECharts throttled to ≤ 4 Hz updates; reduced-motion respected.
- Every tile implements the [data states](../../../docs/ui/README.md#31-data-states-every-tile-implements-all-of-them) (loading skeleton ≤ 300 ms, live, stale chip, degraded, error card with retry → D16, empty with primary action, PAPER/LIVE markers, unconfirmed hatching).

## ToDo

- [ ] Implement components + fixtures
- [ ] Lazy-load Monaco and ECharts chunks (bundle budget: route chunk ≤ 300 KB gzip excluding Monaco)
- [ ] Tests + axe
- [ ] Update components.md

## Verification

### Tests
- Playwright: DESIGN.md §6.8 viewport matrix (overflow + fixed-bar overlap checks) and axe on the new routes; Vitest + Testing Library for components.
- Unit: ParamForm round-trips a schema with conditional params; invalid range shows inline error.

### Scenarios
- Given a phone viewport, when opening code, then the editor is read-only and the note shows.
- Given a param edit that increases risk (size/leverage), then ParamForm reports `risk_increasing=true` so the parent shows DiffView flare and requests C3.

### Stress / failure injection
- Heatmap of 60 × 60 cells and an equity curve of 500k points (downsampled LTTB) render < 500 ms.

## Acceptance criteria

- [ ] Components implemented with fixtures and axe-clean
- [ ] Bundle budget met
- [ ] CI green (lint, types, tests, viewport matrix where UI)

## Exceptions & edge cases

- Empty series: `EmptyState` with the next action, never a blank chart.
- Very long parameter names truncate with tooltip (no overflow).

## Cardinal rules (do NOT)

- Do NOT enforce confirmation levels only in the UI; C1–C3/Kill are enforced server-side by `mt_api`.
- Do NOT use `100vh`/`h-screen`, unprefixed multi-column grids or the Tailwind CDN (DESIGN.md §6.3–6.5).
- Do NOT sum or show paper and live money without a mode label.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/ui/components.md`: final props for analytics/form components.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.32 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T141-ui-analytics-and-form-components`
- PR title: `P2-T141: Analytics and form components: EquityCurve, Distribution, Heatmap, ParamForm, CodeEditor`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T141` run · Playwright viewport matrix + axe green

## Progress log

- 2026-10-21 00:00 · planner · created
