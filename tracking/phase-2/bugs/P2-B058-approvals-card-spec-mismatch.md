---
id: P2-B058
kind: gap
title: D05/D01 approvals spec misses 15 §1.3 card actions and conflicts on bulk approve
phase: 2
type: DOC
status: backlog
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.51, R2.54]
roadmap_todos: []
modules: [M15]
dashboards: [D05, D01]
branch: p2/P2-B058-approvals-card-spec-mismatch
pr: ""
doc_sync: [docs/ui/dashboards/D05-execution.md, docs/ui/dashboards/D01-cockpit.md, docs/ui/components.md]
doc_sync_status: n/a
found_in: docs/ui/dashboards/D05-execution.md (Approvals), docs/ui/components.md (ApprovalCard) vs docs/15-bots-hitl-and-worm-audit.md §1.3
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-B058 · D05/D01 approvals spec misses 15 §1.3 card actions and conflicts on bulk approve

## Goal / expected outcome

The docs agree and part-B tasks can be built without guessing: the web `ApprovalCard` matches the Telegram card capabilities, and batching vs bulk approve is defined once.

## Context & references

- [15 §1.3](../../../docs/15-bots-hitl-and-worm-audit.md#13-hitl-approval-via-telegram) · [D05](../../../docs/ui/dashboards/D05-execution.md) · [components](../../../docs/ui/components.md)
- Affects P2-T140, P2-T149

## Requirements

- **Steps to reproduce:** 15 §1.3 defines Approve · Approve ½ · Reject · Pause bot, a large-order TOTP/hold requirement, and batched cards with per-line toggles for dynamic-selection bots. D05/components only have Approve/Reject (+ bulk approve ≤ 5 same strategy) and no Approve ½, Pause bot, large-order rule or per-line toggles.
- **Expected:** the web `ApprovalCard` matches the Telegram card capabilities, and batching vs bulk approve is defined once.
- **Actual:** see steps; the sources disagree or are silent.
- **Suggested fix:** Add Approve ½ (bot requests), Pause bot and the large-order hold-to-confirm rule to D05 and components; define bulk approve as 'up to 5 cards or one batched card with per-line toggles'; change the D01/D05 backend contracts from `/orders?status=pending_approval` to `/approvals` (added by part A, currently P2-T038).
- **Impact:** S3: web and Telegram approvals behave differently for the same request.

## ToDo

- [ ] Decide the resolution (owner: you, with the planner's suggestion as default)
- [ ] Edit the listed docs in one PR so they agree
- [ ] Update the affected part-B task files (Requirements/Acceptance) if the decision differs from the default
- [ ] Add/adjust the regression test named below where code depends on it

## Verification

### Tests
- Doc gap: reviewed diff; where code depends on it, the named test in the affected task asserts the decided value.

### Scenarios
- Given the decided value, when the affected task is implemented, then its tests assert that value (no hard-coded alternative).

### Stress / failure injection
- n/a: documentation/spec consistency item.

## Acceptance criteria

- [ ] Docs listed under Doc sync agree with each other
- [ ] Affected tasks reference the decision
- [ ] Root cause noted in the progress log

## Exceptions & edge cases

- Until resolved, implementations use the suggested default and keep the value configurable.

## Cardinal rules (do NOT)

- Do NOT close without a regression test (code) or a reviewed doc diff (doc gap).
- Do NOT silently pick a value in code without updating the docs.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/ui/dashboards/D05-execution.md`: align with the decision.
- `docs/ui/dashboards/D01-cockpit.md`: align with the decision.
- `docs/ui/components.md`: align with the decision.

## Branch & PR

- Branch: `p2/P2-B058-approvals-card-spec-mismatch`
- PR title: `P2-B058: D05/D01 approvals spec misses 15 §1.3 card actions and conflicts on bulk approve`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-B058` run

## Progress log

- 2026-10-21 00:00 · planner · opened
