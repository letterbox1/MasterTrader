---
id: P1-T048
kind: task
title: Build D07 Data & Quality with all six tabs
phase: 1
type: BUILD
status: backlog
priority: critical
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T046, P1-T047, P0-T049, P0-T050]
requirements: [R1.15, R1.08, R1.10, R1.11, R1.12, R1.13]
roadmap_todos: [T1.32]
modules: [M15, M16]
dashboards: [D07]
tools: [git, pnpm, node>=20]
mcp: []
env: []
services: [mt-api]
branch: p1/P1-T048-ui-d07-data-quality
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/ui/dashboards/D07-data-quality.md]
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

# P1-T048 · Build D07 Data & Quality with all six tabs

## Goal / expected outcome

`/data` renders the KPI strip and the Feeds, Quality, Costs, Quotas, Reconciliation and Storage tabs exactly as specified in D07, live over WebSocket, with every tile's data states and the actions at the right confirmation level, passing the viewport matrix.

## Context & references

- Roadmap: requirements [R1.15](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.08](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.10](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.11](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.12](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.13](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.32](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [D07 Data & Quality](../../../docs/ui/dashboards/D07-data-quality.md) (layout by tier, tabs & widgets, actions, acceptance) · components [ui components](../../../docs/ui/components.md) (`KpiStrip`, `DataTable`, `StatusChip`, `Heatmap`, `Sparkline`) · [ui §3.1 data states](../../../docs/ui/README.md#31-data-states-every-tile-implements-all-of-them) · [ui §3.3 confirmation](../../../docs/ui/README.md#33-actions--confirmation) · [DESIGN §6.8](../../../DESIGN.md#68-test-matrix-every-screen-must-pass)
- Venue health panel: R1.13 (`/venues/registry`)
- Depends on (this phase): P1-T046, P1-T047
- Cross-phase prerequisites (depends_on): P0-T049 (component library v0), P0-T050 (app shell)

## Requirements

- KPI strip (≥ 2xl): feeds ok/degraded/stale/bad, incidents 24 h, max divergence, min quota headroom, recon mismatches, storage used
- Feeds tab: per feed status (`ok/degraded/stale/closed/bad`), data age vs threshold (and the bots using it; none yet in P1), live-updating, msgs/s, latency p50/p99, reconnects 24 h, gaps 24 h, licence and cost tag, msg-rate sparkline; pause/resume (C1, shows dependent strategies)
- Quality tab: incident list with all D07 columns (incl. the threshold and the layer that set it, auto-action), divergence chart, clock-skew chart, nightly Pandera/Evidently results with report links, acknowledge via `data.incident.ack` (C0; a separate `audit.dq_ack` row)
- Costs tab: spread hour-of-week heatmap, fee tiers, funding predicted/realised, swap/financing, borrow; highlight spread > 3× normal (default, configurable)
- Quotas tab: limit, used, headroom %, throttle state, next reset, history chart, warnings at 80%
- Reconciliation tab: last run per scope (positions/open orders 60 s, balances 5 min, EOD), mismatches (ours, venue's, diff), status, explanation or "unexplained" with time left before the 24 h halt rule; "Run now" (C1). Venue health panel with measured withdrawal times, flags, notes and AUSTRAC check age (`VenueStatusChip`)
- Threshold adjust: link to `system.settings.update` (tighten C1; loosen C3, via the break-glass CLI in P1)
- Storage tab: catalog size by venue/type, hot/cold tiers, Timescale compression, backfill jobs with progress; "Run backfill" (C1)
- Data states on every tile (loading, live, stale, degraded, error, empty); `DataTable` priority columns and card renderer ≤ ph; nav badge for open DQ incidents; "Data degraded" global banner when any feed is stale/bad ([ui §2.2 banners](../../../docs/ui/README.md#22-global-banners-stacked-under-the-top-bar-highest-severity-first))
- D07 acceptance: the monitor publishes `stale` ≤ 250 ms p99 after the threshold and the UI shows it within the live-update lag (p95 < 500 ms); paid feed cannot be enabled (UI blocks, server rejects); quota warnings before throttling

## ToDo

- [ ] Build route `/data` with tabs and the KPI strip in `apps/web/src/routes/data/`
- [ ] Build tiles using the component library; wire TanStack Query + WS topics
- [ ] Actions with confirm sheets and idempotency keys
- [ ] Playwright: viewport matrix + axe + D07 acceptance tests
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Component (Vitest): each tile renders all data states
- Playwright: viewport matrix 240×320 → 2560×1440 portrait/landscape (no horizontal scroll, no overlap, kill switch visible)
- Playwright: inject a stale `dq.status` via the test hook → feed chip turns stale within the 500 ms live-update budget and the banner appears; a `closed` status shows the session label, not amber

### Scenarios

- Given a paid source in the registry, when you open its row, then the resume control is disabled with "paid feed: not allowed" and a forced API call returns 409
- Given quota headroom hits 20%, when the Quotas tab is open, then a warning shows before the throttle state changes

### Stress / failure injection

- Load: Feeds table with 200 feeds updating at 1 Hz stays responsive (virtualised; INP < 200 ms on a mid-range phone profile)

## Acceptance criteria

- [ ] All six tabs and the KPI strip implemented per D07; the three D07 acceptance criteria pass in Playwright
- [ ] CI green (lint, types, tests, Playwright viewport matrix 240→2560 px per DESIGN §6.8, axe)

## Exceptions & edge cases

- mt-api down: read-only banner and last-known values dimmed as stale
- Very narrow (240 px): segmented tabs scroll; feed cards with status chips only

## Cardinal rules (do NOT)

- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; research and backtest reads go through `pit` only.
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file (kept outside the repo) mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT let any path loosen DQ thresholds, risk or alert routing without C3 (Telegram + TOTP + cool-down; in P1 via the break-glass CLI `mtctl approve` + TOTP); tightening is C1.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.32 once every task traced to it in PHASE.md is done; note P1-T048 next to it.
- `docs/ui/dashboards/D07-data-quality.md`: adjust columns/actions to what shipped (e.g. acknowledge command)

## Branch & PR

- Branch: `p1/P1-T048-ui-d07-data-quality`
- PR title: `P1-T048: Build D07 Data & Quality with all six tabs`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T048` run · viewport matrix + axe green

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (data age vs threshold, closed state, ack via data.incident.ack, recon 16 §2.9 view, D07 acceptance at 250 ms + UI lag; P0 UI deps)
