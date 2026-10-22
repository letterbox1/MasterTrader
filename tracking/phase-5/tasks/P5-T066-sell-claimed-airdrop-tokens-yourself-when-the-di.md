---
id: P5-T066
kind: task
title: Sell claimed airdrop tokens yourself when the disposal task arrives (until the P7 gates)
phase: 5
type: USER
status: backlog
priority: medium
size: S
severity: ""
owner: user
claimed_by: ""
depends_on: [P5-T045, P5-T049, P5-T030]
requirements: [R5.17, R5.18]
roadmap_todos: [T5.09]
modules: [M4, M19, M18]
dashboards: [D12, D13]
tools: []
mcp: []
env: []
services: [telegram]
branch: p5/P5-T066-sell-claimed-airdrop-tokens-yourself-when-the-di
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

# P5-T066 · Sell claimed airdrop tokens yourself when the disposal task arrives (until the P7 gates)

## Goal / expected outcome

Until live execution passes the Phase 7 gates, the disposal rule never sells anything automatically. Instead it creates an `ONCHAIN_ACTION_MANUAL` "manual sale" task with the quantity and the cost-gate numbers. You know the procedure, you have worked the first such task end to end (sale done or deliberately skipped, then marked in D13/Telegram), and the outcome is journalled. Further disposal tasks keep arriving in the normal queue until the P7 gates switch the sale to an M11 order.

## Context & references

- Roadmap: [R5.17](../../../docs/roadmap/phase-5-airdrops-wallets-curation.md) · ToDo T5.09
- [08 wallet discipline: disposal rule](../../../docs/08-airdrops-and-token-launches.md#wallet-discipline) (default sell 50% on claim; before Phase 7 a USER task with the cost-gate numbers; from Phase 7 an order through M11) · [03 M4](../../../docs/03-build-spec.md#m4-airdrops-token-launches--icos--mt_airdrop)
- Decision P5-B010 ([17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer)); disposal % default in [16 §2.7](../../../docs/16-configuration-and-safety-model.md#27-wallets-signer-and-gas-13) (set by you in P5-T007)
- Task type `ONCHAIN_ACTION_MANUAL` ([03 M19](../../../docs/03-build-spec.md#m19-user-task-queue--community-curation--mt_curation))
- Depends on: P5-T045 (disposal flow creates the task), P5-T049 (D13), P5-T030 (Telegram task buttons incl. Details)

## Requirements

- The task shows: token, chain, wallet (identity), quantity to sell (disposal % × received), suggested venue(s) or DEX route, cost-gate estimate (gas, fees, impact) and the standing warnings.
- You sell from your own wallet app or exchange account. For a signer-held identity wallet, first sweep the tokens to the vault or an exchange you own (the system offers `wallet.sweep` C2 to the allow-listed vault); never import a signer key anywhere.
- After selling, mark the task Done and paste the tx hash or exchange order id (public data only) so the journal records the disposal; Skip if you decide to hold (the reason is recorded).
- The system never sells automatically in P5, whatever the token or venue.

## ToDo

- [ ] Read the first disposal task in D13 (it can come from the P5-T056 testnet claim, marked "test"; testnet tokens have no market, so record "skipped: test token").
- [ ] For a real disposal task: sell the stated quantity from your own wallet/exchange, following the task steps.
- [ ] Mark the task Done (with tx hash/order id) or Skip (with reason) from D13 or Telegram.
- [ ] Check D14 shows the disposal event linked to the campaign record, or the skip reason.
- [ ] Report "done" so T5.09 can be ticked; later disposal tasks continue in the queue until the P7 gates pass.

## Verification

### Tests
- Manual: the disposal task shows the quantity and cost-gate numbers.
- Manual: after Done with a tx hash, the journal has the disposal event linked to the campaign record (D14 drill-through).

### Scenarios
- Given a claim of 1,000 tokens with the default rule, when the claim finalises, then a manual-sale task for 500 tokens appears with cost numbers, and nothing is sold automatically.
- Given you choose to hold, when you tap Skip with "hold", then the task closes, the reason is stored and the tokens stay under the M22 rules.

### Stress / failure injection
- n/a: human action

## Acceptance criteria

- [ ] First disposal task worked (sold, or skipped with a reason) and marked in D13/Telegram
- [ ] Journal or task history shows the outcome
- [ ] You confirm you will handle disposal tasks manually until the P7 gates pass

## Exceptions & edge cases

- Token has no liquid market: Skip with "no market"; the task can be re-raised by a later rescore.
- Sale needs an approval on a DEX: do it from your own wallet, sized to the sale, and revoke afterwards; never from a system wallet.

## Cardinal rules (do NOT)

- Do NOT import a signer-held key into any wallet app or exchange; move tokens out only via `wallet.sweep` to the allow-listed vault.
- Do NOT sign Permit/Permit2 or unlimited approvals to sell; do NOT connect your vault to a website.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every system order goes through M11, and until the P7 live gates pass, disposal sales are manual USER tasks (never automated).
- Do NOT commit secrets or paste them into chats, issues or logs; secrets live only in the sops/age file or OpenBao (07 §2).

## Doc sync on completion

- No repo doc change; the agent ticks T5.09 once you confirm.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.09 when this lands.

## Branch & PR

- Branch: `p5/P5-T066-sell-claimed-airdrop-tokens-yourself-when-the-di`
- PR title: `P5-T066: Sell claimed airdrop tokens yourself when the disposal task arrives (until the P7 gates)`
- PR checklist: no PR (USER item); confirm in the progress log

## Progress log

- 2026-10-22 00:00 · aligner · created for docs/16–17 (T5.09: disposal manual until the P7 gates, P5-B010)
