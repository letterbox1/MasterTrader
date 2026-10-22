---
id: P5-B006
kind: gap
title: Exchange concentration cap: ≤ 25% (13 §6) vs 25–30% (14 §5, D18)
phase: 5
type: DOC
status: done
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
tools: []
mcp: []
env: []
services: []
branch: p5/P5-B006-exchange-concentration-cap-conflict
pr: ""
doc_sync: [docs/13-wallets-treasury-and-onchain.md, docs/14-strategy-evidence-and-validation.md, docs/ui/dashboards/D18-wallets-treasury.md]
doc_sync_status: done
found_in: "docs/13-wallets-treasury-and-onchain.md §6; docs/14-strategy-evidence-and-validation.md §5"
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
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

- [x] Resolution recorded: Decided (17 §B P5-B006): one venue concentration default, ≤ 25% of total equity per venue (range 10–30%), L1 policy, loosening C3
- [x] Docs carry it: 16 §2.1 (venue concentration row), 13 §6 (concentration monitor), 14 §5 (risk table), D18 allocation widget
- [x] P5 tasks aligned: P5-T027

## Verification

### Tests
- Doc review: every listed doc states the same value/name after the fix; `python3 tools/kanban/kanban.py validate` stays at 0 errors

### Scenarios
- Given the fixed docs, when a developer picks up the affected P5 tasks, then there is exactly one authoritative answer to follow

### Stress / failure injection
- n/a: documentation/spec gap

## Acceptance criteria

- [x] Docs listed under Doc sync (and the other docs named in the ToDo) state the decided value/name
- [x] Affected P5 tasks reference the decided value/name and an owning task exists
- [x] Resolution recorded in the progress log

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
- 2026-10-22 00:00 · aligner · aligned for docs/16–17: Decided (17 §B P5-B006): one venue concentration default, ≤ 25% of total equity per venue (range 10–30%), L1 policy, loosening C3. Docs checked: 16 §2.1 (venue concentration row), 13 §6 (concentration monitor), 14 §5 (risk table), D18 allocation widget. Implementation owned by P5-T027
- 2026-10-22 02:10 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §B P5-B006); docs updated: 16 §2.1 (venue concentration row), 13 §6 (concentration monitor), 14 §5 (risk table), D18 allocation widget; implementation owned by P5-T027
- 2026-10-22 02:10 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:10 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
