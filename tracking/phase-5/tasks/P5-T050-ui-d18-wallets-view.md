---
id: P5-T050
kind: task
title: UI: D18 Wallets & Treasury — unified view (P5 scope)
phase: 5
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T011, P5-T021, P5-T022, P5-T024, P5-T027, P5-T020]
requirements: [R5.23, R5.05, R5.01]
roadmap_todos: [T5.31]
modules: [M15, M22, M16, M18]
dashboards: [D18]
branch: p5/P5-T050-ui-d18-wallets-view
pr: ""
doc_sync: [docs/ui/dashboards/D18-wallets-treasury.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P5-T050 · UI: D18 Wallets & Treasury — unified view (P5 scope)

## Goal / expected outcome

D18 `/wallets` and `/wallets/:walletId` show net worth (AUD and USD, 24h/7d/FY change), allocation (custody tier, venue, asset class, sleeve, concentration vs cap), the wallet table (tier, chain/venue, tag, balance, cap usage, last activity, recon status), internal transfers, venue health, on-chain alerts (approvals, depeg, nonce authority) and the cost-gate quotes widget; register/tag, revoke and sweep actions. Treasury/earn routes stay for P6.

## Context & references

- Roadmap: [R5.23](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md), R5.05 · ToDo T5.31 · USER P5-T005
- Spec: [D18](../../../docs/ui/dashboards/D18-wallets-treasury.md) (Phase 5 = unified view + monitors) · [13 §3](../../../docs/13-wallets-treasury-and-onchain.md#3-unified-wallet-view) · [DESIGN §6.8](../../../DESIGN.md#68-test-matrix-every-screen-must-pass)
- WS topics `wallet`, `alert`, `kill` (gap P5-B005)

## Requirements

- Acceptance (D18): every balance shows native, USD and AUD with rate source and timestamp; internal transfers never show as P&L/disposals and link both rows; works 240 → 2560 px.
- Vault/warm rows watch-only (no signing controls).
- Recon status per wallet from P5-T024 with link to the report.
- Actions: register C1 (with proof-of-control flow), tag C1, revoke approval C2, sweep to allow-listed vault C2.
- Depeg banner shows the action taken (from P5-T026).

## ToDo

- [ ] Build `/wallets` and `/wallets/:walletId` with grouping (`?group=`), wallet table/cards, transfers, alerts side column.
- [ ] Registration wizard implementing the three proof methods.
- [ ] Playwright flows + viewport matrix + axe; doc sync.

## Verification

### Tests
- Playwright: register an address via self-transfer proof (mocked indexer event) → verified.
- Playwright: internal transfer row links both wallets and has no P&L.
- Playwright: viewport matrix + axe.

### Scenarios
- Given a stale price (> 24 h), then the balance renders amber with the timestamp.
- Given kill ON, then sweep and revoke stay available (protective) while other moves are disabled.

### Stress / failure injection
- Wallet table with 300 rows and 1 Hz WS updates stays smooth (no layout thrash; ≤ 1 Hz table updates).

## Acceptance criteria

- [ ] Unified view per D18 P5 scope
- [ ] D18 acceptance 1, 2 and 4 met (3 belongs to P6 treasury moves)
- [ ] Viewport matrix + axe pass

## Exceptions & edge cases

- Indexer stale: global amber banner "balances as of …".

## Cardinal rules (do NOT)

- Do NOT render connect-wallet, sign-permit, approve-unknown-contract, seed/key entry, multi-wallet or automated-social controls anywhere (D12/D18 never-offered lists).
- Do NOT enforce confirmation levels only in the UI; the server enforces C0–C3 (02 §7.2).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order, including disposal-rule sells, goes through M11.
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/ui/dashboards/D18-wallets-treasury.md`: mark P5 parts implemented.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.31 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T050-ui-d18-wallets-view`
- PR title: `P5-T050: UI: D18 Wallets & Treasury — unified view (P5 scope)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T050` run

## Progress log

- 2026-10-21 00:00 · planner · created
