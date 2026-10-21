---
id: P2-B056
kind: gap
title: Command catalogue lacks a leakage-waiver command and a tier-A training run
phase: 2
type: DOC
status: backlog
priority: medium
size: XS
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.43, R2.47]
roadmap_todos: []
modules: [M7, M21]
dashboards: [D04]
branch: p2/P2-B056-missing-lab-commands
pr: ""
doc_sync: [docs/02-v1-architecture.md]
doc_sync_status: n/a
found_in: docs/02-v1-architecture.md §7.2 (Lab, Agents & models groups); docs/14-strategy-evidence-and-validation.md §6 gate 1
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-B056 · Command catalogue lacks a leakage-waiver command and a tier-A training run

## Goal / expected outcome

The docs agree and part-B tasks can be built without guessing: every lab action the part-B UI issues has a catalogue entry with its confirmation level.

## Context & references

- [02 §7.2](../../../docs/02-v1-architecture.md#72-commands-rest-write) · [14 §6 gate 1](../../../docs/14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) · [14 §4 discipline](../../../docs/14-strategy-evidence-and-validation.md#4-trading-methods-enforced-in-code-defaults-user-editable-in-d06)
- Affects P2-T113, P2-T117, P2-T125, P2-T145; related part-A catalogue additions: flatten-and-halt as `position.close` + `halt=true` + reason (currently P2-T020) and `/approvals` (currently P2-T038)

## Requirements

- **Steps to reproduce:** 14 §6 requires that a 'present' leakage finding can be 'waived by you, with the waiver audited', but 02 §7.2 has no waiver command. R2.47 needs tier-A training/compile jobs, but the Lab group has only backtest/sweep/validate/generate/cancel and the models group only promote/rollback/bake-off. 14 §4's flatten-and-halt with a required reason is also not named in the catalogue (part A plans it as a `position.close` flag).
- **Expected:** every lab action the part-B UI issues has a catalogue entry with its confirmation level.
- **Actual:** see steps; the sources disagree or are silent.
- **Suggested fix:** Add `lab.leakage.waive` (C1, reason required, WORM-audited) and `lab.tier_a.train` (C1; covers train → calibrate → compile) to 02 §7.2; document `position.close {halt: true, reason}` as the flatten-and-halt form (coordinate wording with part A's catalogue edits).
- **Impact:** S3: the waiver and training flows would otherwise use undocumented endpoints.

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

- `docs/02-v1-architecture.md`: align with the decision.

## Branch & PR

- Branch: `p2/P2-B056-missing-lab-commands`
- PR title: `P2-B056: Command catalogue lacks a leakage-waiver command and a tier-A training run`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-B056` run

## Progress log

- 2026-10-21 00:00 · planner · opened
