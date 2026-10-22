---
id: P5-T065
kind: task
title: Review and confirm the wallet, signer and gas limits to enable signing
phase: 5
type: USER
status: backlog
priority: critical
size: S
severity: ""
owner: user
claimed_by: ""
depends_on: [P5-T012, P5-T050, P2-T035]
requirements: [R5.24, R5.01, R5.04]
roadmap_todos: [T5.08]
modules: [M22]
dashboards: [D18]
tools: []
mcp: []
env: []
services: [telegram]
branch: p5/P5-T065-review-and-confirm-the-wallet-signer-and-gas-lim
pr: ""
doc_sync: [docs/roadmap/phase-5-airdrops-wallets-curation.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-22
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P5-T065 · Review and confirm the wallet, signer and gas limits to enable signing

## Goal / expected outcome

You have reviewed the prefilled wallet, signer and gas limits (floats, per-transaction and rolling 24 h caps, daily gas budgets, cost-gate margin, gas window, EV hurdle) and confirmed them, or your own tighter numbers, through the C3 flow. Until you do this, the signer refuses every intent with `limits_unconfirmed`. This is the switch that lets any claim, sweep or testnet drill sign.

## Context & references

- Roadmap: [R5.24](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) · ToDo T5.08
- Defaults: [16 §2.7](../../../docs/16-configuration-and-safety-model.md#27-wallets-signer-and-gas-13) (hot float ≤ A$500 per chain, identity ≤ A$300 per chain, burner ≤ A$50, signer A$250 per transaction and A$1,000 per rolling 24 h per wallet, gas budgets airdrops A$20/day and DEX trading A$50/day with alert at 80% and stop at 100%, cost-gate margin 2×, gas window 7-day p30 unless deadline < 48 h, EV hurdle 5% p.a.)
- Rule: "signing stays disabled until you confirm these numbers on first setup" ([16 §2.7](../../../docs/16-configuration-and-safety-model.md#27-wallets-signer-and-gas-13), [13 §1](../../../docs/13-wallets-treasury-and-onchain.md#1-custody-tiers), [D18 rules](../../../docs/ui/dashboards/D18-wallets-treasury.md)); decision P5-B001 in [17 §A](../../../docs/17-decisions-register.md#a-s2-items-all-resolved)
- Change levels: tighten immediate, loosen C3 ([16 §1](../../../docs/16-configuration-and-safety-model.md#1-configuration-layers-tighten-only-inheritance)); C3 = Telegram approve + TOTP + 15 min cool-down ([16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl))
- Depends on: P5-T012 (limits model with the signing-enabled flag), P5-T050 (D18 limits form), P2-T035 (Telegram C3 prompt with TOTP)
- Unblocks: P5-T004 (key creation), P5-T056 (testnet claim), P5-T058 (kill drill on testnet)

## Requirements

- Review every value on the D18 limits form; each shows its default, the accepted range and the 16 §2.7 link.
- You may keep the defaults or tighten them. Anything looser than a parent layer (L0 hard ceiling, e.g. max per-transaction signer value) is rejected at save time with the reason.
- The first confirmation flips `signing_enabled` from false to true. Because enabling signing is a loosening, it is C3 (Telegram approve + TOTP + cool-down).
- The confirmed set is stored as a new version row (WORM history) with your command id; later tightening is immediate, later loosening is C3.

## ToDo

- [ ] Open D18 → Limits (first-setup form) and read each prefilled value against 16 §2.7.
- [ ] Change any value you want tighter; leave the rest at the defaults.
- [ ] Submit; approve the C3 prompt in Telegram (approve + TOTP); wait for the 15 min cool-down.
- [ ] Confirm D18 shows "Signing enabled" with the confirmed version, timestamp and values.
- [ ] Report "done" so T5.08 can be ticked.

## Verification

### Tests
- Manual: before confirmation, D18 shows "Signing disabled until you confirm limits" and a test intent (P5-T013) is refused `limits_unconfirmed`.
- Manual: after the cool-down, D18 shows the confirmed version and the signer accepts a testnet intent within the caps.

### Scenarios
- Given you set the per-transaction cap above the L0 ceiling, when you submit, then the form rejects it with the reason and nothing changes.
- Given you lower the burner float after confirmation, when you save, then it applies immediately (tightening) without a C3 prompt.

### Stress / failure injection
- n/a: one-off human confirmation (signer enforcement is tested in P5-T013 and P5-T062)

## Acceptance criteria

- [ ] All 16 §2.7 wallet, signer and gas values reviewed and confirmed (or tightened) via C3
- [ ] D18 shows "Signing enabled" with the confirmed version
- [ ] Confirmation recorded as a version row with your command id

## Exceptions & edge cases

- Kill switch ON during the cool-down: the confirmation stays pending until kill is OFF (C3); signing stays disabled meanwhile.
- If you never confirm, all signing stays off: claims become `CLAIM_MANUAL` tasks and sweeps are listed as manual steps.

## Cardinal rules (do NOT)

- Do NOT paste keys, seeds or TOTP secrets anywhere; only the numbers are entered.
- Do NOT apply loosening (enabling signing, higher caps, bigger gas budgets) without C3 (Telegram approve + TOTP + cool-down); protective actions (revoke, sweep, kill) never wait for approval.
- Do NOT treat the defaults as advice to raise limits; when unsure, choose the stricter value.
- Do NOT commit secrets or paste them into chats, issues or logs; secrets live only in the sops/age file or OpenBao (07 §2).

## Doc sync on completion

- No repo doc change; the agent ticks T5.08 once you confirm.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.08 when this lands.

## Branch & PR

- Branch: `p5/P5-T065-review-and-confirm-the-wallet-signer-and-gas-lim`
- PR title: `P5-T065: Review and confirm the wallet, signer and gas limits to enable signing`
- PR checklist: no PR (USER item); confirm in the progress log

## Progress log

- 2026-10-22 00:00 · aligner · created for docs/16–17 (R5.24 / T5.08: signing disabled until you confirm the 16 §2.7 limits)
