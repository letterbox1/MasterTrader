---
id: P5-B006
kind: gap
title: Exchange concentration cap: ≤ 25% (13 §6) vs 25–30% (14 §5, D18)
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
dashboards: [D18]
branch: p5/P5-B006-exchange-concentration-cap-conflict
pr: ""
doc_sync: [docs/13-wallets-treasury-and-onchain.md, docs/14-strategy-evidence-and-validation.md, docs/ui/dashboards/D18-wallets-treasury.md]
doc_sync_status: n/a
found_in: "docs/13-wallets-treasury-and-onchain.md §6; docs/14-strategy-evidence-and-validation.md §5"
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P5-B006 · Exchange concentration cap: ≤ 25% (13 §6) vs 25–30% (14 §5, D18)

## Goal / expected outcome

One default concentration cap per exchange across docs.

## Context & references

- 13 §6: "≤ 25% equity per exchange"
- 14 §5: "25–30% of total capital per venue"; D18: "≤ 25–30%"
- Task P5-T027 uses the stricter 25% until resolved

## Requirements

- **Steps to reproduce:** Read the three sections.
- **Expected:** A single default (user-editable, loosening = C3).
- **Actual:** A range in two places and a single value in another; also equity vs total capital wording.
- **Suggested fix:** Set default 25% of total capital per venue; allow raising to 30% via C3; align wording in 13/14/D18.
- **Impact:** S3: ambiguous limit for M11 and D18.

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
- `docs/14-strategy-evidence-and-validation.md`: align with the resolution
- `docs/ui/dashboards/D18-wallets-treasury.md`: align with the resolution

## Branch & PR

- Branch: `p5/P5-B006-exchange-concentration-cap-conflict`
- PR title: `P5-B006: Exchange concentration cap: ≤ 25% (13 §6) vs 25–30% (14 §5, D18)`

## Progress log

- 2026-10-21 00:00 · planner · opened
