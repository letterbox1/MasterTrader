---
id: P2-B001
kind: gap
title: "Sleeve drawdown rule conflicts: halve exposure at 15% vs halt at 15%"
phase: 2
type: DOC
status: backlog
priority: high
size: XS
severity: S2
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.14]
roadmap_todos: []
modules: [M11]
dashboards: []
branch: p2/P2-B001-drawdown-derisk-vs-halt
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md]
doc_sync_status: n/a
found_in: docs/14-strategy-evidence-and-validation.md §4 and §5
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-B001 · Sleeve drawdown rule conflicts: halve exposure at 15% vs halt at 15%

## Goal / expected outcome

One unambiguous drawdown rule set per sleeve: a de-risking threshold and a halt threshold, both policy inputs, with defaults that don't collide.

## Context & references

- [14 §4 drawdown de-risking](../../../docs/14-strategy-evidence-and-validation.md#4-trading-methods-enforced-in-code-defaults-user-editable-in-d06) · [14 §5 default hard limits](../../../docs/14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11)
- Affects P2-T012, P2-T048, P2-T051.

## Requirements

- **Steps to reproduce:** Read 14 §4 'halve exposure when a sleeve is > 15% below its peak' and 14 §5 'Drawdown from peak 15% sleeve → Halt + alert + manual restart'.
- **Expected:** De-risk happens before the halt (e.g. halve at X%, halt at Y% with X < Y).
- **Actual:** Both trigger at 15%, so the halving rule can never act (the sleeve halts at the same point).
- **Suggested fix:** Default de-risk at 10% (halve), halt at 15% sleeve / 10% system; both editable (loosening = C3). P2-T012 implements both as separate policy fields; until decided, the halt at 15% wins (conservative).
- **Impact:** S2: a core risk default is ambiguous and golden tests can't be written without a decision.

## ToDo

- [ ] Decide the rule with the user (or record the decision taken in the linked task)
- [ ] Update the source doc(s) so they agree
- [ ] Update the affected task file(s) to match

## Verification

### Tests
- The affected task's tests encode the decided rule (named in that task).

### Scenarios
- Given a sleeve 12% below peak, when a new entry arrives, then size is halved (after fix) and no halt.

### Stress / failure injection
- n/a: documentation/specification gap

## Acceptance criteria

- [ ] Docs agree in one place, cross-linked from the others
- [ ] Affected tasks reference the decision

## Exceptions & edge cases

- Until resolved, the affected task implements the conservative option stated under Suggested fix.

## Cardinal rules (do NOT)

- Do NOT close without the doc fix merged and the dependent task(s) updated to match.
- Do NOT "fix" by silently picking a number in code; the decision is recorded in the doc and in the risk policy (user input).
- Do NOT edit WORM records to "fix" data; append a correction instead.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §4/§5: aligned thresholds.

## Branch & PR

- Branch: `p2/P2-B001-drawdown-derisk-vs-halt`
- PR title: `P2-B001: align drawdown de-risk and halt thresholds`

## Progress log

- 2026-10-21 00:00 · planner · opened
