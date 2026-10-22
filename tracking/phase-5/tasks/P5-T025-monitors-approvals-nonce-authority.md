---
id: P5-T025
kind: task
title: Monitors: token approvals and nonce authority
phase: 5
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T023, P5-T013, P1-T045]
requirements: [R5.06, R5.03]
roadmap_todos: [T5.23]
modules: [M22, M16, M11, M19]
dashboards: [D18, D12]
tools: [uv, anvil, solana-test-validator]
mcp: []
env: []
services: [postgres, nats]
branch: p5/P5-T025-monitors-approvals-nonce-authority
pr: ""
doc_sync: [docs/13-wallets-treasury-and-onchain.md, docs/07-security-notes.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
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

# P5-T025 · Monitors: token approvals and nonce authority

## Goal / expected outcome

Every new token approval on any registered wallet raises an alert within one poll cycle; a weekly approvals audit (revoke.cash-style: Approval logs + GoPlus approval security) flags stale/risky approvals; hot-wallet risky approvals are auto-revoked (defensive), others become `REVOKE_APPROVAL` tasks; any change of a Solana nonce authority is a critical alert and freezes that wallet in the signer.

## Context & references

- Roadmap: [R5.06](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md), R5.03 (nonce-authority alerts) · ToDo T5.23
- [13 §6](../../../docs/13-wallets-treasury-and-onchain.md#6-monitors-feed-m16-and-m11) · [07 §4](../../../docs/07-security-notes.md#4-crypto-wallets-airdrops-on-chain-claims) (revoke weekly, alert on any new approval) · [07 §9](../../../docs/07-security-notes.md#9-monitoring--incident-response)
- Defensive actions allowed autonomously: [08 §What may run autonomously 3](../../../docs/08-airdrops-and-token-launches.md#what-may-run-autonomously)

## Requirements

- Approval sources: `ops.wallet_approval` from P5-T023, GoPlus approval-security API (within 150/min, 30K/day), built and tested on recorded fixtures without a key; the live keyed call is checked in P5-T068.
- Risk flags: unlimited allowance, spender unverified/blocklisted/not on allow-list, allowance older than 7 days on hot/burner, approval not created by our signer.
- Hot/burner/identity: flagged approvals → `revoke_approval` intent (cost-gate defensive bypass) automatically; vault/warm/user wallets → `REVOKE_APPROVAL` task with steps (watch-only).
- Nonce authority: on change (or nonce account not created by us appearing for a hot wallet) → `alert.critical.nonce_authority`, signer wallet freeze flag, wallet-drained runbook link (P5-T051).
- Weekly approvals audit included in the weekly digest (P5-T030).

## ToDo

- [ ] Implement `packages/mt_treasury/monitors/approvals.py` and `nonce_authority.py`, consuming `wallet.*.approval|nonce_authority`.
- [ ] Signer freeze flag API (per wallet) and auto-revoke intent producer.
- [ ] Weekly audit Prefect flow + report; D18/D12 approvals widgets data.
- [ ] Tests; doc sync.

## Verification

### Tests
- Integration (Anvil): create an unlimited approval from the hot wallet → alert ≤ 1 poll cycle and revoke intent signed + confirmed.
- Integration (`solana-test-validator`): change a nonce account authority → critical alert and signer refuses that wallet.
- Unit: risk flag rules table.

### Scenarios
- Given a user phone wallet grants an approval to a blocklisted spender, then a `REVOKE_APPROVAL` task with exact revoke steps appears and an instant Telegram alert is sent.
- Given the kill switch is ON, when a flagged hot-wallet approval appears, then the revoke still runs (protective).

### Stress / failure injection
- Burst of 100 approval events: all alerted, revokes rate-limited to the daily gas budget with overflow as tasks.

## Acceptance criteria

- [ ] New approvals alert within one poll cycle
- [ ] Weekly audit produced
- [ ] Hot-wallet risky approvals auto-revoked
- [ ] Nonce-authority change → critical alert + signer freeze

## Exceptions & edge cases

- Revoke fails (gas spike): retry with the cost-gate defensive path up to 3 times, then urgent task.
- GoPlus unavailable: rule-based flags still apply; audit marks source missing.

## Cardinal rules (do NOT)

- Do NOT auto-act on vault/warm/user wallets (watch-only); tasks only.
- Do NOT apply loosening (new mandate, higher caps, autonomous claims) without C3 (Telegram approve + TOTP + cool-down); protective actions (revoke, sweep, kill) never wait for approval.
- Do NOT commit secrets or paste them into chats, issues or logs; secrets live only in the sops/age file or OpenBao (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/13-wallets-treasury-and-onchain.md` §6: approvals/nonce rules.
- `docs/07-security-notes.md` §9: alert list includes nonce-authority change.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.23 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T025-monitors-approvals-nonce-authority`
- PR title: `P5-T025: Monitors: token approvals and nonce authority`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T025` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (keyless GoPlus fixtures, live in P5-T068; signer freeze API and P1 alert fan-out as deps)
