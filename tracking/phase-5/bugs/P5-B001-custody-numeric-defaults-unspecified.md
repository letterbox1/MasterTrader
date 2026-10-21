---
id: P5-B001
kind: gap
title: Custody-tier floats, per-tx/24h caps and daily gas budgets have no specified values
phase: 5
type: DOC
status: backlog
priority: high
size: XS
severity: S2
owner: agent
claimed_by: ""
depends_on: []
requirements: [R5.01, R5.04, R5.07]
roadmap_todos: []
modules: [M22]
dashboards: []
branch: p5/P5-B001-custody-numeric-defaults-unspecified
pr: ""
doc_sync: [docs/13-wallets-treasury-and-onchain.md, docs/08-airdrops-and-token-launches.md]
doc_sync_status: n/a
found_in: "docs/13-wallets-treasury-and-onchain.md §1, §7; docs/08 §What may run autonomously"
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P5-B001 · Custody-tier floats, per-tx/24h caps and daily gas budgets have no specified values

## Goal / expected outcome

The docs state default (user-overridable) values for each tier's float, per-transaction cap, rolling-24h cap, gas reserve, minimum sweep value and per-module daily gas budget, so the signer, sweeps and cost gate have something concrete to enforce.

## Context & references

- Found in: [13 §1](../../../docs/13-wallets-treasury-and-onchain.md#1-custody-tiers) ("per-transaction and rolling 24h caps", "tiny float") and [13 §7](../../../docs/13-wallets-treasury-and-onchain.md#7-on-chain-cost-gate--dex-execution-extends-m12--m16) ("daily gas spend per module") — no numbers
- Affects P5-T004, P5-T012, P5-T020, P5-T028

## Requirements

- **Steps to reproduce:** Read 13 §1/§7, 07 §4 and 08: caps, floats and budgets are named but never quantified.
- **Expected:** A defaults table (AUD and USD) per tier, e.g. burner float ≈ gas for 5 txs, hot per-tx and 24h caps, identity caps, daily gas budget per module, all marked user-editable (loosening = C3).
- **Actual:** No values anywhere; the signer would ship with arbitrary or no limits.
- **Suggested fix:** Add a defaults table to 13 §1 with conservative placeholders; P5-T012 ships them as `UNSET_REQUIRES_USER` and P5-T004 has you set the real numbers.
- **Impact:** S2: signing cannot be enabled safely without numbers; blocks auto-claims and sweeps.

## ToDo

- [ ] Agree the resolution with the user (or record the decision in the progress log)
- [ ] Edit the source docs listed under Doc sync so they agree
- [ ] Update the affected P5 task files if the numbers/names change

## Verification

### Tests
- Doc review: every listed doc states the same value/name after the fix; `python3 tools/kanban/kanban.py validate` stays at 0 errors

### Scenarios
- Given the fixed docs, when a developer picks up the affected P5 tasks, then there is exactly one authoritative answer to follow

### Stress / failure injection
- n/a: documentation/spec gap

## Acceptance criteria

- [ ] Docs listed under Doc sync are consistent
- [ ] Affected P5 tasks reference the resolved value/name
- [ ] Resolution recorded in the progress log

## Exceptions & edge cases

- Until resolved, implementers use the suggested fix as the default and flag it in their PR description

## Cardinal rules (do NOT)

- Do NOT resolve by silently picking a looser (less safe) value; when in doubt choose the stricter option.
- Do NOT edit WORM records to "fix" data; append a correction instead.

## Doc sync on completion

- `docs/13-wallets-treasury-and-onchain.md`: align with the resolution
- `docs/08-airdrops-and-token-launches.md`: align with the resolution

## Branch & PR

- Branch: `p5/P5-B001-custody-numeric-defaults-unspecified`
- PR title: `P5-B001: Custody-tier floats, per-tx/24h caps and daily gas budgets have no specified values`

## Progress log

- 2026-10-21 00:00 · planner · opened
