---
id: P5-T006
kind: task
title: Sign the first claim mandates (C3)
phase: 5
type: USER
status: backlog
priority: high
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: [P5-T043, P5-T048, P5-T004]
requirements: [R5.15]
roadmap_todos: [T5.05]
modules: [M4, M22]
dashboards: [D12]
branch: p5/P5-T006-sign-first-mandates
pr: ""
doc_sync: [docs/roadmap/phase-5-airdrops-wallets-curation.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P5-T006 · Sign the first claim mandates (C3)

## Goal / expected outcome

At least one active, expiring **mandate** per identity wallet you want automated: wallet, chain, allow-listed contracts and functions (e.g. a Merkle `claim(...)`), gas/value caps, expiry — created through `airdrop.mandate.create` (C3) so the claim executor (P5-T044) may act within it.

## Context & references

- Roadmap: ToDo T5.05 → [R5.15](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) · [08 what may run autonomously](../../../docs/08-airdrops-and-token-launches.md#what-may-run-autonomously)
- UI: [D12 /airdrops/wallet](../../../docs/ui/dashboards/D12-airdrops.md) (Create mandate = C3)
- Mandates are WORM (`curation.mandate`, [15 §2.1](../../../docs/15-bots-hitl-and-worm-audit.md#21-scope)); revocation is a new row
- Depends on: P5-T043 (mandate model), P5-T048 (D12 UI), P5-T004 (identity wallets exist)

## Requirements

- Start with a **testnet** mandate for the P5-T056 scenario (e.g. Sepolia identity wallet, test Merkle distributor), then mainnet mandates only for specific vetted claim contracts.
- Each mandate: one wallet, one chain, explicit contract address(es) + function selector(s), `msg.value = 0`, max gas per tx, max claims/day, expiry (suggest ≤ 30 days).
- Approve in Telegram with TOTP; it takes effect after the cool-down (default 15 min).

## ToDo

- [ ] In D12 `/airdrops/wallet` → Create mandate, fill the fields for the testnet scenario.
- [ ] Approve in Telegram (approve + TOTP); wait for the cool-down; confirm status "active".
- [ ] Create mainnet mandates only for opportunities D12 shows as "auto-claim eligible" (risk passed, ≥ 2 official sources).
- [ ] Report "done" so T5.05 can be ticked.

## Verification

### Tests
- Manual: D12 mandates widget shows the mandate active with the expiry you set.
- Manual: the mandate row appears in `/airdrops/mandates` with a row hash (WORM).

### Scenarios
- Given an expired mandate, when an eligible claim appears, then it becomes a `CLAIM_MANUAL` task instead of executing.

### Stress / failure injection
- n/a: human approval step

## Acceptance criteria

- [ ] Testnet mandate active (used by P5-T056)
- [ ] Any mainnet mandates limited to specific contracts/functions with caps and expiry

## Exceptions & edge cases

- Revoking a mandate is C1 and immediate; use it whenever in doubt.
- Mandates never cover permits, approvals or non-zero `msg.value` (rejected at creation, P5-T042).

## Cardinal rules (do NOT)

- Do NOT create open-ended mandates (no wildcard contracts or functions, no expiry > 90 days).
- Do NOT apply loosening (new mandate, higher caps, autonomous claims) without C3 (Telegram approve + TOTP + cool-down); protective actions (revoke, sweep, kill) never wait for approval.
- Do NOT UPDATE or DELETE WORM rows (`curation.mandate`, `curation.exec_log`, the signer ledger, `journal.*`, `audit.*`); corrections are new rows with `supersedes_id` (15 §2).

## Doc sync on completion

- No repo doc change; the agent ticks T5.05 once you confirm.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.05 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T006-sign-first-mandates`
- PR title: `P5-T006: Sign the first claim mandates (C3)`
- PR checklist: no PR (USER item); confirm in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
