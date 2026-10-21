---
id: P6-B008
kind: gap
title: Venue concentration cap conflict: D18 '≤ 25–30%' vs 13 §6 '≤ 25% equity per exchange'
phase: 6
type: DOC
status: backlog
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R6.22, R6.24]
roadmap_todos: []
modules: []
dashboards: []
branch: p6/P6-B008-venue-concentration-cap-conflict
pr: ""
doc_sync: [docs/ui/dashboards/D18-wallets-treasury.md, docs/13-wallets-treasury-and-onchain.md]
doc_sync_status: n/a
found_in: docs/ui/dashboards/D18-wallets-treasury.md (Allocation widget) vs docs/13-wallets-treasury-and-onchain.md §6
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P6-B008 · Venue concentration cap conflict: D18 '≤ 25–30%' vs 13 §6 '≤ 25% equity per exchange'

## Goal / expected outcome

The docs agree and are specific enough to build from: one venue cap value (and where it lives: risk policy vs treasury policy).

## Context & references

- Found in: docs/ui/dashboards/D18-wallets-treasury.md (Allocation widget) vs docs/13-wallets-treasury-and-onchain.md §6
- [D18](../../../docs/ui/dashboards/D18-wallets-treasury.md) · [13 §6](../../../docs/13-wallets-treasury-and-onchain.md#6-monitors-feed-m16-and-m11) · [14 §3](../../../docs/14-strategy-evidence-and-validation.md#3-strategy-catalogue-evidence-ranked-templates)
- Affects: P6-T033, P6-T037, P6-T060

## Requirements

- **Steps to reproduce:** read docs/ui/dashboards/D18-wallets-treasury.md (Allocation widget) vs docs/13-wallets-treasury-and-onchain.md §6 and compare it with the cross-referenced sections listed under Context.
- **Expected:** one venue cap value (and where it lives: risk policy vs treasury policy).
- **Actual:** D18 shows 'concentration vs venue cap (≤ 25–30%)'; 13 §6 says '≤ 25% equity per exchange'.
- **Suggested fix:** Use 25% (the stricter value) as the default in the risk policy; D18 displays the configured value rather than a range.
- **Impact:** Risk limit ambiguity (severity S3)

## ToDo

- [ ] Confirm with 14 §5 / P2 risk defaults.
- [ ] Propose the D18 wording.
- [ ] Update the docs listed under Doc sync and link the resolving commit here.

## Verification

### Tests
- Doc review: the affected sections state one consistent value/definition; relative links resolve.

### Scenarios
- Given a developer picks up the dependent P6 task cold, when they read the docs, then there is exactly one answer.

### Stress / failure injection
- n/a: documentation gap.

## Acceptance criteria

- [ ] D18 and 13 §6 agree.
- [ ] Root cause noted in the progress log.

## Exceptions & edge cases

- Until resolved, dependent tasks use the conservative interpretation stated under Suggested fix and note it in their progress log.

## Cardinal rules (do NOT)

- Do NOT silently pick a number in code; record the decision in the doc first.
- Do NOT edit docs owned by another phase's planner from a P6 branch without the owner's agreement; propose the change in the PR description.

## Doc sync on completion

- `docs/ui/dashboards/D18-wallets-treasury.md`: resolve the inconsistency.
- `docs/13-wallets-treasury-and-onchain.md`: resolve the inconsistency.

## Branch & PR

- Branch: `p6/P6-B008-venue-concentration-cap-conflict`
- PR title: `P6-B008: Venue concentration cap conflict: D18 '≤ 25–30%' vs 13 §6 '≤ 25% equity per exchange'`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-B008` run

## Progress log

- 2026-10-21 00:00 · planner · created
