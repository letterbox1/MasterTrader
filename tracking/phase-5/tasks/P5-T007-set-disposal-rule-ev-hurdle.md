---
id: P5-T007
kind: task
title: Set the disposal rule and EV hurdle
phase: 5
type: USER
status: backlog
priority: medium
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: [P5-T040, P5-T045]
requirements: [R5.14, R5.17]
roadmap_todos: [T5.06]
modules: [M4]
dashboards: [D12]
tools: []
mcp: []
env: []
services: [telegram]
branch: p5/P5-T007-set-disposal-rule-ev-hurdle
pr: ""
doc_sync: [docs/roadmap/phase-5-airdrops-wallets-curation.md]
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

# P5-T007 · Set the disposal rule and EV hurdle

## Goal / expected outcome

You have reviewed the airdrop **disposal rule** (default: sell 50% on claim; until the P7 gates each disposal is a manual-sale USER task, P5-T066) and the **EV hurdle** (default 5% p.a. on capital locked, plus your time value per minute) and kept or changed them as settings, so the EV gate and disposal tasks use your numbers.

## Context & references

- Roadmap: ToDo T5.06 → R5.14, R5.17
- [08 EV gate](../../../docs/08-airdrops-and-token-launches.md#expected-value-gate-airdrops-icosidos-points-programmes) · [08 wallet discipline](../../../docs/08-airdrops-and-token-launches.md#wallet-discipline)
- Defaults: [16 §2.7](../../../docs/16-configuration-and-safety-model.md#27-wallets-signer-and-gas-13) (EV hurdle 5% p.a. on capital locked, an AUD cash-rate proxy; decision P5-B012) and [08 wallet discipline](../../../docs/08-airdrops-and-token-launches.md#wallet-discipline) (disposal 50%); both are settings ([17 §E](../../../docs/17-decisions-register.md#e-ratification-2026-10-22)); loosening is C3
- Disposal before P7: manual-sale task (decision P5-B010, [17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer))
- Depends on: P5-T040 (EV gate settings), P5-T045 (disposal rule)

## Requirements

- Disposal rule: percent to sell on claim (default 50%) and what happens to the rest (hold under M22 rules). Before the P7 gates every disposal is a manual-sale `ONCHAIN_ACTION_MANUAL` task; from P7 it becomes an M11 order.
- EV inputs: hurdle rate (default 5% p.a.), your time value (AUD/min), default haircut.
- Changes via `system.settings.update` section `airdrop`: tightening applies at once; loosening (e.g. a lower hurdle → more tasks) is C3 ([02 §7.2](../../../docs/02-v1-architecture.md#72-commands-rest-write); 08 principle 5).

## ToDo

- [ ] Open D12 settings (or `/system/settings?section=airdrop`); keep or change disposal %, hurdle rate (default 5% p.a.), time value and haircut (a loosening asks for C3 in Telegram).
- [ ] Check the next daily digest: EV values recalculate with your numbers.
- [ ] Report "done" so T5.06 can be ticked.

## Verification

### Tests
- Manual: an opportunity's EV breakdown in D12 shows your hurdle and time value.

### Scenarios
- Given hurdle 8% p.a. and time value A$1/min, when a 60-minute task's EV falls below 0, then it drops out of the digest.

### Stress / failure injection
- n/a: human setting

## Acceptance criteria

- [ ] Disposal rule and EV inputs reviewed (kept or changed) and visible in D12
- [ ] Digest reflects the new EV values

## Exceptions & edge cases

- Every disposal is a manual-sale task until the P7 gates pass (P5-B010), whatever the venue; the rule here only sets the quantity.

## Cardinal rules (do NOT)

- Do NOT set up any automated sale path before the P7 gates; after them, every sale is an order through M11.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, and until the P7 live gates pass, disposal sales are manual USER tasks (never automated).

## Doc sync on completion

- No repo doc change; the agent ticks T5.06 once you confirm.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.06 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T007-set-disposal-rule-ev-hurdle`
- PR title: `P5-T007: Set the disposal rule and EV hurdle`
- PR checklist: no PR (USER item); confirm in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (EV hurdle default 5% p.a. per 16 §2.7/P5-B012; disposal = manual-sale task until P7 per P5-B010; loosening C3)
