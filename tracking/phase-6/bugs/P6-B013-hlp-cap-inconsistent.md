---
id: P6-B013
kind: gap
title: HLP cap stated three ways: '≤ 5–10% of portfolio / ≤ 10% of stables' vs '≤ 10% of stables' vs allocation table
phase: 6
type: DOC
status: done
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
tools: []
mcp: []
env: []
services: []
branch: p6/P6-B013-hlp-cap-inconsistent
pr: ""
doc_sync: [docs/13-wallets-treasury-and-onchain.md, docs/14-strategy-evidence-and-validation.md]
doc_sync_status: done
found_in: docs/13-wallets-treasury-and-onchain.md §4 vs docs/14-strategy-evidence-and-validation.md §3
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
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

- [x] Decision recorded in docs/17 (17 §B P6-B013): HLP cap ≤ 10% of stablecoins and ≤ 5% of total portfolio, whichever is smaller (raising is C3)
- [x] Owning docs carry it: 16 §2.7 HLP row; 13 §4 HLP row; 14 §3 HLP row and allocation table; roadmap R6.20 and T6.03
- [x] Affected tasks aligned in the 2026-10-22 task-alignment wave; implementation owned by P6-T033 (policy), P6-T034 (your approval), P6-T036 (allocator), P6-T060 (verification)
- [x] Decision and source noted in the progress log

## Verification

### Tests
- Doc review: the affected sections state one consistent value/definition; relative links resolve.

### Scenarios
- Given a developer picks up the dependent P6 task cold, when they read the docs, then there is exactly one answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [x] Decision recorded in the owning docs (16 §2.7 HLP row; 13 §4 HLP row; 14 §3 HLP row and allocation table; roadmap R6.20 and T6.03)
- [x] Affected tasks consistent with it (P6-T033 (policy), P6-T034 (your approval), P6-T036 (allocator), P6-T060 (verification))
- [x] Root cause noted in the progress log

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
- 2026-10-22 00:00 · aligner · resolved by docs/17 §B P6-B013: HLP cap ≤ 10% of stablecoins and ≤ 5% of total portfolio, whichever is smaller (raising is C3). Docs now carry it: 16 §2.7 HLP row; 13 §4 HLP row; 14 §3 HLP row and allocation table; roadmap R6.20 and T6.03. Implementation owned by P6-T033 (policy), P6-T034 (your approval), P6-T036 (allocator), P6-T060 (verification). Root cause: 13 and 14 stated the cap differently.
- 2026-10-22 02:20 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §B P6-B013); docs updated: 16 §2.7 HLP row, 13 §4 HLP row, 14 §3 HLP row and allocation table, roadmap R6.20/T6.03; implementation owned by P6-T033, P6-T034, P6-T036, P6-T060
- 2026-10-22 02:20 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:20 · cloud:vm:be04b6ae61f8 · doc sync done: docs already updated in this wave
