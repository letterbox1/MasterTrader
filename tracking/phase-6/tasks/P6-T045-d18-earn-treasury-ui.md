---
id: P6-T045
kind: task
title: D18 treasury and hold-and-earn UI
phase: 6
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T038]
requirements: [R6.40, R6.20, R6.24]
roadmap_todos: [T6.29]
modules: [M15, M22]
dashboards: [D18]
branch: p6/P6-T045-d18-earn-treasury-ui
pr: ""
doc_sync: [docs/ui/dashboards/D18-wallets-treasury.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P6-T045 · D18 treasury and hold-and-earn UI

## Goal / expected outcome

`/wallets/treasury` and `/wallets/earn` show the policy, allocation vs reserve, earn positions (net APY, lock-up, protocol risk, exit cost, P&L incl. rewards), rewards ledger, proposals and cost-gate quotes, with allocate/enter/exit actions that always preview the gate result.

## Context & references

- Roadmap: [R6.40](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.20](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.24](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.29
- UI: [D18](../../../docs/ui/dashboards/D18-wallets-treasury.md) (widgets, actions, rules & states, acceptance) · [DESIGN §6.8](../../../DESIGN.md#68-test-matrix-every-screen-must-pass)
- Gaps: P6-B007 (WS topics), P6-B008 (venue cap)
- Depends on (this phase): P6-T038

## Requirements

- Actions: `treasury.allocate` (C2 with gate preview; loosening policy C3), `treasury.earn.enter/exit` (C2), policy edit via P6-T033 commands.
- Kill switch ON: entries frozen, exits available at C2; depeg banner with the auto-reduce taken.
- Every balance native/USD/AUD with rate source and timestamp; vault/warm watch-only.
- Responsive 240 → 2560 px (cards ≤ ph, table ≥ md).

## ToDo

- [ ] Treasury + earn routes and widgets.
- [ ] Gate preview sheet.
- [ ] Playwright + viewport matrix.
- [ ] Docs.

## Verification

### Tests
- Playwright: enter position shows gate result before confirm; kill ON hides enter.
- Viewport matrix.

### Scenarios
- Given a rejected gate quote, then Confirm is disabled and the reason shows.
- Given a depeg event, then the banner and the auto-reduce entry appear.

### Stress / failure injection
- n/a: low-volume screens; WS throttled ≤ 1 Hz.

## Acceptance criteria

- [ ] D18 acceptance 1–4 pass for treasury/earn routes.
- [ ] Viewport matrix green.

## Exceptions & edge cases

- Stale yields: earn screen shows stale badge and disables new entries.

## Cardinal rules (do NOT)

- Do NOT offer seed/key entry, unlimited approvals or non-allow-listed destinations.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order and on-chain move goes through M11.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/ui/dashboards/D18-wallets-treasury.md`: mark earn/treasury implemented.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.29 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T045-d18-earn-treasury-ui`
- PR title: `P6-T045: D18 treasury and hold-and-earn UI`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T045` run

## Progress log

- 2026-10-21 00:00 · planner · created
