---
id: P0-T049
kind: task
title: Build component library v0 (tiles, states, chips, confirm sheets)
phase: 0
type: BUILD
status: backlog
priority: high
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T047]
requirements: [R0.11, R0.N6]
roadmap_todos: [T0.26]
modules: [M15]
dashboards: []
tools: [git, node>=20, pnpm, playwright]
mcp: []
env: []
services: []
branch: p0/P0-T049-component-library-v0
pr: ""
doc_sync: [docs/ui/components.md, docs/roadmap/phase-0-foundations.md]
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

# P0-T049 · Build component library v0 (tiles, states, chips, confirm sheets)

## Goal / expected outcome

`apps/web/src/components` has the v0 set needed by the shell and D16 — `Tile` (all data states), `KpiCard`, `KpiStrip`, `StatusChip`, `HealthDot`, `Delta`, `Money`/`Qty`/`Price`, `Timestamp`, `DataTable` (card list ≤ ph), `LogStream`, `Banner`, `Skeleton`/`EmptyState`/`ErrorState`, `ConfirmSheet` (C1/C2), `C3Flow`, `KillSwitchButton` — each container-query driven, accessible, and covered by Vitest + a Playwright component story page.

## Context & references

- [Roadmap P0 R0.11, R0.N6](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [components §1 shell](../../../docs/ui/components.md#1-shell--navigation)
- [components §2 tiles](../../../docs/ui/components.md#2-tiles--data-display)
- [components §4 forms](../../../docs/ui/components.md#4-forms--controls)
- [ui §3.1 data states](../../../docs/ui/README.md#31-data-states-every-tile-implements-all-of-them)
- [ui §3.3 confirmation](../../../docs/ui/README.md#33-actions--confirmation)
- [DESIGN §6.7 touch](../../../DESIGN.md#67-touch--input)
- [DESIGN §9 accessibility](../../../DESIGN.md#9-accessibility)
- [DESIGN §7 components](../../../DESIGN.md#7-components-carried-over-from-v1-unchanged-unless-noted)
- Depends on: P0-T047

## Requirements

- Data states on `Tile`: loading (skeleton ≤ 300 ms), live, stale (amber chip `stale 12s`), degraded (amber outline + reason), error (inline card + retry + D16 link), empty (helpful action), paper/live marker, unconfirmed (hatched).
- `StatusChip` always has text; up/down never colour-only (▲/▼ + sign) per DESIGN §2.
- `DataTable`: column priorities (hide P3 < xl, P2 < md), `cardRenderer` ≤ ph, own `overflow-x-auto` box with scroll shadow, TanStack Table + Virtual for > 200 rows.
- `ConfirmSheet`: dialog ≥ md, bottom sheet < md, full screen at xxs; hold-to-confirm 600 ms on touch, Enter on desktop; generates the idempotency key; destructive buttons Flare with ≥ 8px spacing and specific labels.
- `C3Flow`: states awaiting approval (countdown; in P0–P1 it reads 'Waiting for break-glass approval', ui §3.3) → TOTP prompt → cool-down timer (the configured cool-down, default 15 min, [16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl)) → applied; cancellable; matches the server state machine in P0-T035.
- `KillSwitchButton`: Flare `HALT` / solid `HALTED + reason`; reachable within 2 tabs of the top bar; opens a Kill-level confirm, never `window.confirm`.
- Touch targets ≥ 44px on `touch`, ≥ 32px desktop; min text 11px; contrast ≥ 4.5:1 (body); reduced motion removes pulses/glows.
- A dev route `/__components` renders every component in every state for Playwright + axe.

## ToDo

- [ ] Implement the components with Radix where interactive.
- [ ] Write Vitest tests per component (states, a11y roles, keyboard).
- [ ] Build `/__components` gallery (excluded from production nav, kept for tests).
- [ ] Update docs/ui/components.md with any prop changes.

## Verification

### Tests
- Unit (Vitest + Testing Library): each data state renders; `ConfirmSheet` hold-to-confirm timing; `C3Flow` transitions; `Delta` shows sign + arrow.
- a11y: axe on `/__components` → zero serious/critical violations (also in P0-T053).

### Scenarios
- Given a tile's data source errors, then the tile shows the error card with retry and a D16 link, never a blank tile.
- Given a touch device, when the user taps (not holds) a C2 confirm, then nothing executes.

### Stress / failure injection
- `DataTable` with 50k rows virtualised scrolls at ≥ 50 fps on a mid laptop (logged).

## Acceptance criteria

- [ ] All v0 components implemented with every data state
- [ ] Vitest + axe clean
- [ ] Gallery route covers all states
- [ ] Docs updated
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check, Playwright viewport matrix)

## Exceptions & edge cases

- Charts (lightweight-charts, ECharts) are P1+; not in v0.

## Cardinal rules (do NOT)

- Do NOT use colour alone for status or direction.
- Do NOT use `window.alert/confirm` for any confirmation.
- Do NOT use `100vh`/`h-screen` for full-height layouts.
- Loosening risk, autonomous mode and mandates are C3 (Telegram + TOTP + cool-down); Kill ON and protective exits never wait for approval.
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/ui/components.md`: reflect any prop/state changes made in v0.
- `docs/roadmap/phase-0-foundations.md`: tick T0.26 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T049-component-library-v0`
- PR title: `P0-T049: Build component library v0 (tiles, states, chips, confirm sheets)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T049` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (C3Flow break-glass state and cool-down from settings (16 §2.3, 17 §D P0-B002); run fields added)
