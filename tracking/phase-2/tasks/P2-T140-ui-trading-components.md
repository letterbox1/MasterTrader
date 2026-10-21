---
id: P2-T140
kind: task
title: Trading components: RiskPreview, OrderTicket, position/order rows and cards, ModeSwitch
phase: 2
type: BUILD
status: backlog
priority: high
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.50, R2.51]
roadmap_todos: [T2.32]
modules: [M15]
dashboards: [D01, D03, D05]
branch: p2/P2-T140-ui-trading-components
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

# P2-T140 · Trading components: RiskPreview, OrderTicket, position/order rows and cards, ModeSwitch

## Goal / expected outcome

The Phase 2 trading components in `apps/web/src/components` that part B's dashboards need — `RiskPreview`, `OrderTicket`, `PositionRow/Card`, `OrderRow/Card`, `FillMarker`, `ModeSwitch` and `StatusChip` additions — built to DESIGN.md v2 with all data states, container queries and the C2 hold-to-confirm pattern. `ApprovalCard` + approvals sheet, `KillSwitchButton` wiring and `DiffView`/`C3Flow` are delivered by part A and reused here.

## Context & references

- Roadmap: [R2.50, R2.51](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.32
- [components §3 trading](../../../docs/ui/components.md) · [ui §3.3 confirmation](../../../docs/ui/README.md#33-actions--confirmation) · [DESIGN §6](../../../DESIGN.md#6-responsive-system-1920px--240px-portrait--landscape)
- Backend + shared components from part A (P2-T001–T099): `POST /risk/preview` and order commands (currently P2-T017/P2-T020), `ApprovalCard` + approvals sheet (P2-T038), `KillSwitchButton` wiring (P2-T042), `DiffView`/`C3Flow` (P2-T043); mode vocabulary conflict tracked in P2-B053
- Cross-phase: P0 T0.26 component library v0 (shell, tiles, data states, ConfirmSheet)

## Requirements

- `RiskPreview(intent)`: calls `POST /risk/preview` (debounced 250 ms); lists each check pass/fail with reason, projected exposure, limits used (`LimitBar`), est. cost/slippage; stale preview (> 5 s or inputs changed) blocks submit.
- `RiskPreview` is the same component part A's `ApprovalCard` embeds; agree its props with part A before building (one implementation).
- `OrderTicket`: side, type (market/limit/stop/stop-limit), qty or notional, price, TIF, reduce-only, TP/SL brackets; sleeve fixed to `manual`; `inputmode=decimal`; live `RiskPreview`; submit = C2.
- `ModeSwitch`: paper / hitl (approve) / autonomous (auto) per P2-B053 resolution; autonomous triggers the `C3Flow` and is disabled with the failing gate list while gates fail.
- Touch targets ≥ 44 px on touch; ≥ 8 px gap between destructive and safe actions; Flare styling + specific labels ('Cancel 3 orders').
- Every tile implements the [data states](../../../docs/ui/README.md#31-data-states-every-tile-implements-all-of-them) (loading skeleton ≤ 300 ms, live, stale chip, degraded, error card with retry → D16, empty with primary action, PAPER/LIVE markers, unconfirmed hatching).

## ToDo

- [ ] Implement the components with Radix primitives and DESIGN tokens; container-query layouts
- [ ] Storybook-style fixtures (Ladle/Vitest browser) for each state
- [ ] Hook to typed API client (`openapi-typescript`) and WS topics `orders`, `positions`, `kill`, `risk.event`
- [ ] Unit + interaction tests; axe on fixtures
- [ ] Update components.md with final props

## Verification

### Tests
- Playwright: DESIGN.md §6.8 viewport matrix (overflow + fixed-bar overlap checks) and axe on the new routes; Vitest + Testing Library for components.
- Interaction: hold-to-confirm cancels if released < 600 ms; double submit ignored (idempotency key reused).
- Unit: RiskPreview marks itself stale after 5 s or any input change and blocks submit.

### Scenarios
- Given the risk preview fails a check, when the user tries to submit the ticket, then submit is disabled and the failing check is named.
- Given a ModeSwitch change to autonomous while a gate fails, then the option is disabled and the failing gate is listed.
- Given `POST /risk/preview` times out, then the preview shows an error state and submit stays disabled.

### Stress / failure injection
- Render 200 `OrderRow`s updating at 1 Hz in a virtualised table: no dropped frames > 50 ms on a mid-range laptop.
- WS disconnect: components show 'Re-syncing', refetch via REST, then resume (ui §3.4).

## Acceptance criteria

- [ ] Components match components.md props and pass axe
- [ ] Hold-to-confirm and idempotency verified
- [ ] Viewport matrix green on fixture pages
- [ ] CI green (lint, types, tests, viewport matrix where UI)

## Exceptions & edge cases

- Kill ON: all trading actions disabled except cancel and flatten-via-kill.
- Unreconciled positions: close actions require reconciliation first unless via kill flatten (D05 rules).

## Cardinal rules (do NOT)

- Do NOT enforce confirmation levels only in the UI; C1–C3/Kill are enforced server-side by `mt_api`.
- Do NOT use `100vh`/`h-screen`, unprefixed multi-column grids or the Tailwind CDN (DESIGN.md §6.3–6.5).
- Do NOT sum or show paper and live money without a mode label.
- Do NOT allow the ticket to choose a sleeve other than `manual`.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT let any UI/API path loosen risk, enable autonomous mode or turn the kill switch off without C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/ui/components.md`: final props for the trading components.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.32 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T140-ui-trading-components`
- PR title: `P2-T140: Trading components: RiskPreview, OrderTicket, position/order rows and cards, ModeSwitch`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T140` run · Playwright viewport matrix + axe green

## Progress log

- 2026-10-21 00:00 · planner · created
