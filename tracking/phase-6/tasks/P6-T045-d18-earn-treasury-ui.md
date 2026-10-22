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
depends_on: [P6-T038, P5-T050]
requirements: [R6.40, R6.20, R6.24]
roadmap_todos: [T6.29]
modules: [M15, M22]
dashboards: [D18]
tools: [git, pnpm, node>=20, playwright]
mcp: []
env: []
services: [mt-api]
branch: p6/P6-T045-d18-earn-treasury-ui
pr: ""
doc_sync: [docs/ui/dashboards/D18-wallets-treasury.md, docs/roadmap/phase-6-ai-models-treasury.md]
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

# P6-T045 · D18 treasury and hold-and-earn UI

## Goal / expected outcome

`/wallets/treasury` and `/wallets/earn` show the policy, allocation vs reserve, earn positions (net APY, lock-up, protocol risk, exit cost, P&L incl. rewards), rewards ledger, proposals and cost-gate quotes, with allocate/enter/exit actions that always preview the gate result.

## Context & references

- Roadmap: [R6.40](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.20](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.24](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.29
- UI: [D18](../../../docs/ui/dashboards/D18-wallets-treasury.md) (widgets, actions, rules & states, acceptance) · [DESIGN §6.8](../../../DESIGN.md#68-test-matrix-every-screen-must-pass)
- Decisions: [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) (P6-B007: WS topics `wallet`, `treasury`, `alert` in 02 §7.3) · [17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer) (P6-B008: one venue cap, default 25%, shown as the configured value; P6-B013 HLP cap)
- Cross-phase: P5-T050 (D18 unified view, P5 scope)
- Depends on (this phase): P6-T038

## Requirements

- Actions: `treasury.allocate` (C2 with gate preview; loosening policy C3), `treasury.earn.enter/exit` (C2), policy edit via P6-T033 commands.
- Kill switch ON: entries frozen, exits available at C2; depeg banner with the auto-reduce taken.
- Every balance native/USD/AUD with rate source and timestamp; vault/warm watch-only.
- Concentration widget shows the **configured** venue cap (default ≤ 25% of total equity, [16 §2.1](../../../docs/16-configuration-and-safety-model.md#21-risk-sizing-and-drawdown)), never a range; the HLP cap shows both bounds (≤ 10% of stables and ≤ 5% of portfolio, [16 §2.7](../../../docs/16-configuration-and-safety-model.md#27-wallets-signer-and-gas-13)).
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
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (WS topics (17 §D P6-B007), configured venue cap 25% and HLP cap (17 §B); dep P5-T050; run fields)
