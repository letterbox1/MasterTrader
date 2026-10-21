---
id: P0-T009
kind: task
title: Open free demo, paper and testnet accounts
phase: 0
type: USER
status: ready
priority: medium
size: M
severity: ""
owner: user
claimed_by: ""
depends_on: []
requirements: []
roadmap_todos: [T0.09]
modules: [M1, M12]
dashboards: []
branch: p0/P0-T009-demo-practice-accounts
pr: ""
doc_sync: [docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P0-T009 · Open free demo, paper and testnet accounts

## Goal / expected outcome

Free practice/testnet accounts exist at OANDA (practice), IG (demo), Alpaca (paper), IBKR (paper), Binance Spot testnet and Bybit testnet, so P1 can stream and reconcile and P2 can paper-trade. No API keys yet (read-only keys are T1.02, trade-only keys T2.03).

## Context & references

- [Roadmap P0 T0.09](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [04 do-this-week](../../../docs/04-plan-of-action.md#️-do-this-week-regardless-of-phase)
- [07 §3 broker keys](../../../docs/07-security-notes.md#3-broker--exchange-keys)
- [12 §2 venue registry](../../../docs/12-policy-and-compliance.md#2-venue-access-registry)
- [P1 roadmap](../../../docs/roadmap/phase-1-data-and-monitoring.md) (T1.02 read-only keys)
- [P2 roadmap](../../../docs/roadmap/phase-2-strategies-risk-lab.md) (T2.03 trade-only keys)
- Unblocks: P1 entry criteria (T0.09), P2 paper trading

## Requirements

- Accounts: OANDA v20 **practice**, IG **demo**, Alpaca **paper**, IBKR **paper** (may require a live application first; log if blocked), Binance **Spot testnet**, Bybit **testnet**.
- Each with a unique strong password + 2FA where offered; account ids recorded (not secret).
- No real money deposited anywhere in P0.
- Outputs: logins in your password manager; any key you already created → the sops secrets file `/etc/mastertrader/secrets.sops.yaml` (created by the secrets task, P0-T022).

## ToDo

- [ ] Create each account and enable 2FA; log 'done' per venue.
- [ ] Note each account id and environment base URL in this log.
- [ ] If IBKR paper needs a live application, log the status and continue (P2 can start without IBKR).

## Verification

### Tests
- Confirmation: log in to each web UI once; on Binance/Bybit testnets the faucet balance is visible.

### Scenarios
- Given an account is unavailable to AU residents, then log it and check the venue registry (P0-T011) status; never misstate residency.

### Stress / failure injection
- n/a: account action.

## Acceptance criteria

- [ ] Six practice/testnet accounts exist with 2FA (or a logged reason why one can't)
- [ ] No real funds deposited
- [ ] Credentials only in password manager / secrets file

## Exceptions & edge cases

- Bybit is data/testnet only for AU; Bybit derivatives are **blocked** for live (12 §2).

## Cardinal rules (do NOT)

- Do NOT create withdrawal-capable or trading API keys now (P1/P2 do that with the right scopes).
- Do NOT misstate residency or wholesale status (12 §1).
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Keys are trade-only, IP-locked, withdrawals disabled; no live money before the P7 gates.

## Doc sync on completion

- None beyond this log.
- `docs/roadmap/phase-0-foundations.md`: tick T0.09 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T009-demo-practice-accounts`
- PR title: `P0-T009: Open free demo, paper and testnet accounts`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T009` run

## Progress log

- 2026-10-21 00:00 · planner · created
