---
id: P2-B011
kind: gap
title: Decay monitoring and health check are required in both P2 (R2.21) and P7 (R7.07/T7.22)
phase: 2
type: DOC
status: backlog
priority: low
size: XS
severity: S4
owner: agent
claimed_by: ""
depends_on: []
requirements: [R2.21]
roadmap_todos: []
modules: [M11]
dashboards: []
branch: p2/P2-B011-decay-monitoring-p2-p7-overlap
pr: ""
doc_sync: [docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: docs/roadmap/phase-2-strategies-risk-lab.md R2.21; docs/roadmap/phase-7-prove-and-go-live.md R7.07/T7.22
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-B011 · Decay monitoring and health check are required in both P2 (R2.21) and P7 (R7.07/T7.22)

## Goal / expected outcome

P7's item is scoped as live hardening of the P2 jobs, not a second build.

## Context & references

- [R2.21](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · [R7.07 / T7.22](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Affects P2-T034, P2-T060.

## Requirements

- **Steps to reproduce:** Both phases have a BUILD ToDo for the same rolling 60-trade/CUSUM/health-check jobs.
- **Expected:** P2 builds and runs them on paper; P7 extends them to live sub-accounts and kill-criteria wiring.
- **Actual:** Duplicate scope; risk of rebuilding.
- **Suggested fix:** Reword T7.22 to 'extend P2 decay jobs to live accounts and kill criteria (R7.06)'.
- **Impact:** S4: planning duplication only.

## ToDo

- [ ] Decide the rule with the user (or record the decision taken in the linked task)
- [ ] Update the source doc(s) so they agree
- [ ] Update the affected task file(s) to match

## Verification

### Tests
- The affected task's tests encode the decided rule (named in that task).

### Scenarios
- n/a: documentation.

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

- `docs/roadmap/phase-7-prove-and-go-live.md` T7.22 wording (via the Phase 7 planner).

## Branch & PR

- Branch: `p2/P2-B011-decay-monitoring-p2-p7-overlap`
- PR title: `P2-B011: scope P7 decay item as live hardening`

## Progress log

- 2026-10-21 00:00 · planner · opened
