---
id: P2-T148
kind: task
title: D05 manual ticket (manual sleeve) and flatten-and-halt with reason
phase: 2
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T140, P2-T147]
requirements: [R2.50, R2.13]
roadmap_todos: [T2.32]
modules: [M15, M11, M12]
dashboards: [D05]
branch: p2/P2-T148-d05-manual-ticket-flatten-halt
pr: ""
doc_sync: [docs/ui/dashboards/D05-execution.md, docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T148 · D05 manual ticket (manual sleeve) and flatten-and-halt with reason

## Goal / expected outcome

Manual trading in D05 is limited to what 14 §4 allows: the `OrderTicket` places orders only in the `manual` sleeve (own limits, journal tag) through M11 with a C2 risk preview, and 'Flatten-and-halt' closes a strategy/sleeve's positions and halts it with a required reason.

## Context & references

- Roadmap: [R2.50, R2.13](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.32
- [14 §4 discipline](../../../docs/14-strategy-evidence-and-validation.md#4-trading-methods-enforced-in-code-defaults-user-editable-in-d06) (no discretionary overrides; only flatten-and-halt with a required reason; manual tickets are their own `manual` sleeve) · [D05 actions](../../../docs/ui/dashboards/D05-execution.md) · [components OrderTicket/RiskPreview](../../../docs/ui/components.md)
- Backend from part A (P2-T001–T099): `manual` sleeve limits (T2.22), `order.place` through M11 and flatten-and-halt as `position.close` with `halt=true` + required `reason` (currently P2-T020); catalogue doc gap noted in P2-B056

## Requirements

- Ticket: instrument combobox, side, type, qty/notional, price, TIF, reduce-only, brackets; sleeve locked to `manual`; tag `source=manual` on the order and (P3) journal.
- Submit = `order.place` C2: risk preview must pass; hold-to-confirm on touch; idempotency key per confirm sheet.
- Modify (C2), cancel (C1), close/reduce (C2), set brackets (C2) on manual positions; strategy positions only via close/flatten.
- Flatten-and-halt: scope strategy or sleeve; reason text required (min 10 chars); C2 confirm showing positions to close and orders to cancel; issues part A's `position.close` with `halt=true` and the reason (one atomic command, not a client-side two-step) which is written to `audit.command`.
- No other manual override (e.g. editing a strategy order) is offered in the UI.
- Shortcuts `b`/`s` open the ticket on desktop; phones use the sticky 'New order' button.

## ToDo

- [ ] Wire OrderTicket into D05 dock/drawer/sheet per tier
- [ ] Flatten-and-halt dialog with reason
- [ ] Playwright flows incl. rejection by M11
- [ ] Doc sync

## Verification

### Tests
- Playwright: DESIGN.md §6.8 viewport matrix (overflow + fixed-bar overlap checks) and axe on the new routes; Vitest + Testing Library for components.
- Playwright: manual order exceeding manual-sleeve max position → preview fails, submit disabled.
- Playwright: flatten-and-halt without reason → cannot confirm.

### Scenarios
- Given a passing preview, when the user confirms, then an order with `sleeve=manual` appears in Orders with a 'manual' source badge.
- Given a strategy with 3 positions, when flatten-and-halt is confirmed with a reason, then positions close, the strategy is halted and the audit entry contains the reason.
- Given Kill ON, then the ticket is disabled.

### Stress / failure injection
- Network drop during confirm: idempotency key prevents a duplicate order on retry.

## Acceptance criteria

- [ ] Manual orders always in the `manual` sleeve and through M11
- [ ] Flatten-and-halt requires a reason and is audited
- [ ] Viewport matrix + axe green
- [ ] CI green (lint, types, tests, viewport matrix where UI)

## Exceptions & edge cases

- Unreconciled position: close blocked until reconciled (except kill flatten).
- Phone landscape-short: ticket as full-height side sheet.

## Cardinal rules (do NOT)

- Do NOT enforce confirmation levels only in the UI; C1–C3/Kill are enforced server-side by `mt_api`.
- Do NOT use `100vh`/`h-screen`, unprefixed multi-column grids or the Tailwind CDN (DESIGN.md §6.3–6.5).
- Do NOT sum or show paper and live money without a mode label.
- Do NOT offer discretionary overrides beyond flatten-and-halt.
- Do NOT let a manual order bypass the risk preview/M11.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT update or delete WORM rows (`audit.*`); corrections are new rows referencing the original (15 §2).
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/ui/dashboards/D05-execution.md`: flatten-and-halt action row.
- `docs/14-strategy-evidence-and-validation.md` §4: link to the UI flow.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.32 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T148-d05-manual-ticket-flatten-halt`
- PR title: `P2-T148: D05 manual ticket (manual sleeve) and flatten-and-halt with reason`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T148` run · Playwright viewport matrix + axe green

## Progress log

- 2026-10-21 00:00 · planner · created
