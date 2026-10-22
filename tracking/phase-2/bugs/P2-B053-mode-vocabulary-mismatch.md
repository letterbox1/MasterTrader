---
id: P2-B053
kind: gap
title: Strategy/bot mode names differ across docs (approve/auto vs hitl/autonomous)
phase: 2
type: DOC
status: done
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.20, R2.50]
roadmap_todos: []
modules: [M0, M15]
dashboards: [D01, D03, D05]
tools: []
mcp: []
env: []
services: []
branch: p2/P2-B053-mode-vocabulary-mismatch
pr: ""
doc_sync: [docs/ui/dashboards/D01-cockpit.md, docs/ui/dashboards/D03-strategies.md, docs/ui/components.md, docs/ui/README.md, docs/03-build-spec.md]
doc_sync_status: done
found_in: docs/ui/dashboards/D01-cockpit.md, D03-strategies.md, docs/ui/components.md (ModeSwitch), docs/03-build-spec.md M0 manifest vs docs/15 §1.2, docs/02 §7.2, roadmap R2.20
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P2-B053 · Strategy/bot mode names differ across docs (approve/auto vs hitl/autonomous)

## Goal / expected outcome

The docs agree and part-B tasks can be built without guessing: one enum used in the API, manifest, UI chips and Telegram, with display labels mapped once.

## Context & references

- [15 §1](../../../docs/15-bots-hitl-and-worm-audit.md#1-trading-bots) · [02 §7.2](../../../docs/02-v1-architecture.md#72-commands-rest-write) · [D03](../../../docs/ui/dashboards/D03-strategies.md) · [components](../../../docs/ui/components.md)
- Affects P2-T140, P2-T142, P2-T143

## Requirements

- **Steps to reproduce:** D01/D03/components/top-bar badge use `paper / approve / auto` (`APPROVE`, `LIVE AUTO`); 03 M0 manifest mode is `backtest/paper/approve/auto`; 15 §1.2, 02 §7.2 `strategy.set_mode` and R2.20 use `paper / hitl / autonomous`.
- **Expected:** one enum used in the API, manifest, UI chips and Telegram, with display labels mapped once.
- **Actual:** see steps; the sources disagree or are silent.
- **Suggested fix:** API/manifest enum `paper | hitl | autonomous` (matching 15 and the command catalogue); UI labels 'Paper', 'Approve (HITL)', 'Autonomous'; update D01/D03/components/ui README and 03 M0.
- **Impact:** S3: mismatched enums between part A's API and part B's UI cause wrong chips or rejected commands.

## ToDo

- [x] Decision recorded: modes are `paper` / `hitl` / `autonomous`, set per bot; "approve"/"auto" are retired aliases; a strategy is promoted through gates, a bot is switched between modes
- [x] Docs agree: 15 §1.2, D03, components, 03 M0
- [x] Tasks updated: P2-T004, P2-T007, P2-T033, P2-T140

## Verification

### Tests
- Doc gap: reviewed diff; where code depends on it, the named test in the affected task asserts the decided value.

### Scenarios
- Given the decided value, when the affected task is implemented, then its tests assert that value (no hard-coded alternative).

### Stress / failure injection
- n/a: documentation/spec consistency item.

## Acceptance criteria

- [x] Docs agree in one place, cross-linked from the others (15 §1.2; D03 lines on strategy vs bot modes; components `StatusChip`/`ModeSwitch` (labels "Paper", "Approve (HITL)", "Autonomous"); 03 M0 manifest and lifecycle)
- [x] Affected tasks reference the decision (P2-T004, P2-T007, P2-T033, P2-T140)

## Exceptions & edge cases

- Until resolved, implementations use the suggested default and keep the value configurable.

## Cardinal rules (do NOT)

- Do NOT close without a regression test (code) or a reviewed doc diff (doc gap).
- Do NOT silently pick a value in code without updating the docs.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/ui/dashboards/D01-cockpit.md`: align with the decision.
- `docs/ui/dashboards/D03-strategies.md`: align with the decision.
- `docs/ui/components.md`: align with the decision.
- `docs/ui/README.md`: align with the decision.
- `docs/03-build-spec.md`: align with the decision.

## Branch & PR

- Branch: `p2/P2-B053-mode-vocabulary-mismatch`
- PR title: `P2-B053: Strategy/bot mode names differ across docs (approve/auto vs hitl/autonomous)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-B053` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (resolved by 17 §B (P2-B053); docs carry it (15 §1.2; D03 lines on strategy vs bot modes; components `StatusChip`/`ModeSwitch` (labels "Paper", "Approve (HITL)", "Autonomous"); 03 M0 manifest and lifecycle); implementation owned by P2-T004, P2-T007, P2-T033, P2-T140)
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §B (P2-B053)); docs updated: 15 §1.2; D03 lines on strategy vs bot modes; components `StatusChip`/`ModeSwitch` (labels "Paper", "Approve (HITL)", "Autonomous"); 03 M0 manifest and lifecycle; implementation owned by P2-T004, P2-T007, P2-T033, P2-T140
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:14 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
