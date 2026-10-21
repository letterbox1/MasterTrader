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
branch: p5/P5-T007-set-disposal-rule-ev-hurdle
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

# P5-T007 · Set the disposal rule and EV hurdle

## Goal / expected outcome

Your airdrop **disposal rule** (default: sell 50% on claim, via M11) and the **EV hurdle** (hurdle rate for `capital_lockup_cost` and your time value per minute) are set, so the EV gate and post-claim orders use your numbers.

## Context & references

- Roadmap: ToDo T5.06 → R5.14, R5.17
- [08 EV gate](../../../docs/08-airdrops-and-token-launches.md#expected-value-gate-airdrops-icosidos-points-programmes) · [08 wallet discipline](../../../docs/08-airdrops-and-token-launches.md#wallet-discipline)
- Gap P5-B012: the default hurdle references a treasury yield that 13 §5 does not define
- Depends on: P5-T040 (EV gate settings), P5-T045 (disposal rule)

## Requirements

- Disposal rule: percent to sell on claim (default 50%), what happens to the rest (hold under M22 rules), minimum order value below which it becomes a manual task.
- EV inputs: hurdle rate (% p.a.), your time value (AUD/min), default haircut.
- Changes that loosen (e.g. lower hurdle → more tasks) are recorded; settings via `system.settings.update` with section `airdrop`.

## ToDo

- [ ] Open D12 settings (or `/system/settings?section=airdrop`) and set disposal %, min order value, hurdle rate, time value, haircut.
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

- [ ] Disposal rule and EV inputs set and visible in D12
- [ ] Digest reflects the new EV values

## Exceptions & edge cases

- Disposal sells for tokens with no allowed venue become manual tasks until the P7 DEX path (P5-B010).

## Cardinal rules (do NOT)

- Do NOT set a disposal rule that bypasses M11 (all sells are orders through the risk manager).
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order, including disposal-rule sells, goes through M11.

## Doc sync on completion

- No repo doc change; the agent ticks T5.06 once you confirm.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.06 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T007-set-disposal-rule-ev-hurdle`
- PR title: `P5-T007: Set the disposal rule and EV hurdle`
- PR checklist: no PR (USER item); confirm in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
