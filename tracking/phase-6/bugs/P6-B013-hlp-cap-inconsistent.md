---
id: P6-B013
kind: gap
title: HLP cap stated three ways: '≤ 5–10% of portfolio / ≤ 10% of stables' vs '≤ 10% of stables' vs allocation table
phase: 6
type: DOC
status: backlog
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R6.20]
roadmap_todos: []
modules: []
dashboards: []
branch: p6/P6-B013-hlp-cap-inconsistent
pr: ""
doc_sync: [docs/13-wallets-treasury-and-onchain.md, docs/14-strategy-evidence-and-validation.md]
doc_sync_status: n/a
found_in: docs/13-wallets-treasury-and-onchain.md §4 vs docs/14-strategy-evidence-and-validation.md §3
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P6-B013 · HLP cap stated three ways: '≤ 5–10% of portfolio / ≤ 10% of stables' vs '≤ 10% of stables' vs allocation table

## Goal / expected outcome

The docs agree and are specific enough to build from: one HLP cap definition (both bounds, which applies first) used by the treasury policy.

## Context & references

- Found in: docs/13-wallets-treasury-and-onchain.md §4 vs docs/14-strategy-evidence-and-validation.md §3
- [13 §4](../../../docs/13-wallets-treasury-and-onchain.md#4-hold-and-earn-module-m22-mt_treasury) · [14 §3](../../../docs/14-strategy-evidence-and-validation.md#3-strategy-catalogue-evidence-ranked-templates)
- Affects: P6-T033, P6-T034

## Requirements

- **Steps to reproduce:** read docs/13-wallets-treasury-and-onchain.md §4 vs docs/14-strategy-evidence-and-validation.md §3 and compare it with the cross-referenced sections listed under Context.
- **Expected:** one HLP cap definition (both bounds, which applies first) used by the treasury policy.
- **Actual:** 13 §4 caps HLP at '≤ 5–10% of portfolio / ≤ 10% of stables'; 14 §3 says '≤ 10% of stables' and its allocation table says 'Hold-and-earn (HLP ≤ 10% of stables) 10% | 20–30%'.
- **Suggested fix:** Use both bounds: min(10% of stables, 5% of portfolio) as default; user may raise to 10% of portfolio via C3.
- **Impact:** Policy default ambiguity on a pooled-loss product (severity S3)

## ToDo

- [ ] Propose the unified wording.
- [ ] Update the docs listed under Doc sync and link the resolving commit here.

## Verification

### Tests
- Doc review: the affected sections state one consistent value/definition; relative links resolve.

### Scenarios
- Given a developer picks up the dependent P6 task cold, when they read the docs, then there is exactly one answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [ ] 13 §4 and 14 §3 agree.
- [ ] Root cause noted in the progress log.

## Exceptions & edge cases

- Until resolved, dependent tasks use the conservative interpretation stated under Suggested fix and note it in their progress log.

## Cardinal rules (do NOT)

- Do NOT silently pick a number in code; record the decision in the doc first.
- Do NOT edit docs owned by another phase's planner from a P6 branch without the owner's agreement; propose the change in the PR description.

## Doc sync on completion

- `docs/13-wallets-treasury-and-onchain.md`: resolve the inconsistency.
- `docs/14-strategy-evidence-and-validation.md`: resolve the inconsistency.

## Branch & PR

- Branch: `p6/P6-B013-hlp-cap-inconsistent`
- PR title: `P6-B013: HLP cap stated three ways: '≤ 5–10% of portfolio / ≤ 10% of stables' vs '≤ 10% of stables' vs allocation table`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-B013` run

## Progress log

- 2026-10-21 00:00 · planner · created
