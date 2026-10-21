---
id: P2-B053
kind: gap
title: Strategy/bot mode names differ across docs (approve/auto vs hitl/autonomous)
phase: 2
type: DOC
status: backlog
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
branch: p2/P2-B053-mode-vocabulary-mismatch
pr: ""
doc_sync: [docs/ui/dashboards/D01-cockpit.md, docs/ui/dashboards/D03-strategies.md, docs/ui/components.md, docs/ui/README.md, docs/03-build-spec.md]
doc_sync_status: n/a
found_in: docs/ui/dashboards/D01-cockpit.md, D03-strategies.md, docs/ui/components.md (ModeSwitch), docs/03-build-spec.md M0 manifest vs docs/15 §1.2, docs/02 §7.2, roadmap R2.20
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
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
