---
id: P5-B009
kind: gap
title: Depeg "auto-reduce" has no defined action path before P6 treasury / P7 DEX
phase: 5
type: DOC
status: backlog
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R5.06]
roadmap_todos: []
modules: [M22, M11]
dashboards: []
branch: p5/P5-B009-depeg-auto-reduce-action-undefined-p5
pr: ""
doc_sync: [docs/13-wallets-treasury-and-onchain.md]
doc_sync_status: n/a
found_in: "docs/13-wallets-treasury-and-onchain.md §6; docs/roadmap/phase-5-airdrops-wallets-curation.md R5.06"
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P5-B009 · Depeg "auto-reduce" has no defined action path before P6 treasury / P7 DEX

## Goal / expected outcome

13 §6 defines what auto-reduce does per holding location and phase.

## Context & references

- 13 §6: "Auto-reduce beyond 50 bps deviation"
- In P5 there is no treasury allocator (P6) and no DEX execution (P7)
- Task P5-T026 implements: M11 block new exposure; reduce exchange-held balances via M11 orders; on-chain holdings → urgent task

## Requirements

- **Steps to reproduce:** Ask: what does auto-reduce sell, where, and through which path in P5?
- **Expected:** A per-location action table.
- **Actual:** Unspecified.
- **Suggested fix:** Adopt the P5-T026 behaviour in 13 §6, with P6/P7 extending it to on-chain swaps via the cost gate and DEX path.
- **Impact:** S3: ambiguous behaviour for a protective monitor.

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

## Branch & PR

- Branch: `p5/P5-B009-depeg-auto-reduce-action-undefined-p5`
- PR title: `P5-B009: Depeg "auto-reduce" has no defined action path before P6 treasury / P7 DEX`

## Progress log

- 2026-10-21 00:00 · planner · opened
