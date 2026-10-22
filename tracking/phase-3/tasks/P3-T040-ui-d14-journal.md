---
id: P3-T040
kind: task
title: D14 Journal dashboard
phase: 3
type: BUILD
status: backlog
priority: high
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T039, P0-T048, P0-T049, P0-T050]
requirements: [R3.13]
roadmap_todos: [T3.29]
modules: [M18, M15]
dashboards: [D14]
tools: [git, node>=20, pnpm]
mcp: []
env: []
services: [mt-api]
branch: p3/P3-T040-ui-d14-journal
pr: ""
doc_sync: [docs/ui/dashboards/D14-journal.md, docs/roadmap/phase-3-journal-and-tax.md]
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

# P3-T040 · D14 Journal dashboard

## Goal / expected outcome

`/journal` and `/journal/trades/:id` implement D14: KPI strip, filters, trades table, events list with home-currency values and FX source, trade review with chart snapshot, provenance chain, costs vs modelled, notes/tags/screenshots and review prompts, analytics, and reconciliation status — responsive across the full viewport matrix.

## Context & references

- Roadmap: [R3.13, T3.29](../../../docs/roadmap/phase-3-journal-and-tax.md) · dashboard spec [D14](../../../docs/ui/dashboards/D14-journal.md)
- Frontend stack [02 §10](../../../docs/02-v1-architecture.md#10-frontend-architecture) · viewport matrix [DESIGN §6.8](../../../DESIGN.md#68-test-matrix-every-screen-must-pass)
- Cross-phase prerequisites (depends_on): P0-T048 (typed API + WS client), P0-T049 (component library), P0-T050 (app shell); P1 lightweight-charts usage (D02) as reference

## Requirements

- Layout tiers: ≥ xl KPI strip (trades, win rate, avg R, fees, funding, net P&L; paper/live toggle) + filters + table + review panel; md–lg table with review drawer; ≤ ph period selector, `JournalEntry` cards, review page.
- Widgets per D14: Trades table (TanStack Table + Virtual), Events (all types, AUD + native + USD, FX source chip), Trade review (lightweight-charts with entry/exit/signal markers; provenance chain; costs vs modelled; notes/tags/screenshots; prompts "Followed plan?", "Mistake type"), Analytics (ECharts: P&L by strategy/instrument/weekday/hour/tag, mistake-tag frequency, expectancy), Reconciliation status linking to D07.
- Actions: add note/tag/screenshot (C0; attachment PNG/JPEG default ≤ 5 MB, uploaded and stored content-addressed by hash, P3-T039), add a manual journal event (`journal.manual_event.add`, **C2**, reason required), export CSV/Beancount (`tax.export`, C0), open in tax view (D15 Lots).
- No edit controls on records; correction chain displayed.
- Live: new events via WS `journal` appear without reload (D14 acceptance: each fill within 5 s end-to-end).
- Paper vs live separated by default with a toggle.

## ToDo

- [ ] Routes `apps/web/src/routes/journal/*`, tiles in `apps/web/src/tiles/journal/*`, `JournalEntry` card component
- [ ] Trade review page with chart snapshot (render from bars via API, no external chart services)
- [ ] Analytics tiles (ECharts)
- [ ] Playwright tests (viewport matrix + axe) and Vitest component tests
- [ ] Docs

## Verification

### Tests

- Vitest: table renders Decimal strings exactly; FX chip shows source + timestamp.
- Playwright: viewport matrix (240×320 → 2560×1440, portrait + landscape) with overflow checks; axe no serious violations.
- Playwright E2E: publish a test fill → row visible within 5 s.

### Scenarios

- Given a corrected event, when viewing the trade, then the correction chain shows original and superseding rows, both read-only.
- Given the WS drops, when it reconnects with a `seq` gap, then the page re-syncs via REST and shows no duplicates.
- Given Postgres is down, when the page loads, then the red system banner shows and the page is read-only.

### Stress / failure injection

- Render 50k-row trades table with virtualisation at 60 fps scroll on a mid laptop; ≤ 1 Hz table updates under a 2,000-fill burst.

## Acceptance criteria

- [ ] All D14 widgets and actions present per spec
- [ ] Viewport matrix + axe green in CI
- [ ] Fill-to-screen ≤ 5 s demonstrated
- [ ] Paper/live toggle works
- [ ] CI green (lint, types, tests, `pit` check, Playwright viewport matrix + axe; `tax-golden` once P3-T045 lands)

## Exceptions & edge cases

- Very long instrument ids/tags truncate with tooltip, no overflow.
- Timezone: UI renders in the user's timezone (default Australia/Sydney).

## Cardinal rules (do NOT)

- Do NOT render any edit control on journal records; corrections are server-side superseding events.
- Do NOT compute tax figures in the browser; the UI only displays server results.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/ui/dashboards/D14-journal.md`: tick acceptance criteria; note any deviations.
- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.29 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T040-ui-d14-journal`
- PR title: `P3-T040: D14 Journal dashboard`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T040` run · Playwright matrix screenshots attached

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (manual event action C2 (P3-B006) and content-addressed attachments (P3-B013) per D14; explicit P0 depends_on; tools/services filled)
