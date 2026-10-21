---
id: P1-B009
kind: gap
title: Loosening DQ thresholds is C3, but the Telegram approval path arrives in P2
phase: 1
type: DOC
status: backlog
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R1.10]
roadmap_todos: []
modules: []
dashboards: []
branch: p1/P1-B009-c3-path-missing-in-p1
pr: ""
doc_sync: [docs/ui/dashboards/D07-data-quality.md, docs/roadmap/phase-1-data-and-monitoring.md]
doc_sync_status: n/a
found_in: docs/ui/dashboards/D07-data-quality.md Actions; docs/roadmap/phase-2-strategies-risk-lab.md T2.33; docs/roadmap/phase-1-data-and-monitoring.md T1.04
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P1-B009 · Loosening DQ thresholds is C3, but the Telegram approval path arrives in P2

## Goal / expected outcome

A documented interim path for P1 threshold loosening that keeps the C3 intent

## Context & references

- Found in: [D07 Data & Quality](../../../docs/ui/dashboards/D07-data-quality.md) makes loosening DQ thresholds C3 (Telegram approve + TOTP + cool-down); T1.04 asks you to tune noisy thresholds in P1; the Telegram C3 prompt is built in P2 (T2.33)
- Related items: P1-T030, P1-T046, P1-T066

## Requirements

- **Where:** [D07 Data & Quality](../../../docs/ui/dashboards/D07-data-quality.md) makes loosening DQ thresholds C3 (Telegram approve + TOTP + cool-down); T1.04 asks you to tune noisy thresholds in P1; the Telegram C3 prompt is built in P2 (T2.33)
- **Expected:** A documented interim path for P1 threshold loosening that keeps the C3 intent
- **Actual:** No way to apply a C3 change in P1 unless P0's confirmation engine already supports Telegram approval
- **Suggested fix:** Either (a) P0 T0.24 includes the Telegram approve + TOTP leg, or (b) during P1 thresholds live in `config/dq_checks.yaml` and loosening needs a reviewed PR approved by you; document in D07 and 02 §7.2
- **Impact:** Threshold tuning (P1-T066) blocked or done without the intended control (severity S3)

## ToDo

- [ ] Decide (a) or (b) with the user
- [ ] Edit D07 actions and the P1/P2 roadmap notes
- [ ] Update the affected P1 task files if the decision changes their requirements

## Verification

### Tests

- Doc review: the edited sections agree with each other and with the affected task files

### Scenarios

- Given a developer picks up the related task cold, when they read the fixed docs, then there is exactly one interpretation

### Stress / failure injection

- n/a: documentation gap

## Acceptance criteria

- [ ] Docs updated and consistent
- [ ] Root cause and decision noted in the progress log

## Exceptions & edge cases

- Until fixed, related tasks follow the interim rule stated in their own files

## Cardinal rules (do NOT)

- Do NOT resolve by silently picking a number in code; the decision lands in the docs first
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.

## Doc sync on completion

- `docs/ui/dashboards/D07-data-quality.md`: apply the fix above
- `docs/roadmap/phase-1-data-and-monitoring.md`: apply the fix above

## Branch & PR

- Branch: `p1/P1-B009-c3-path-missing-in-p1`
- PR title: `P1-B009: Loosening DQ thresholds is C3, but the Telegram approval path arrives in P2`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-B009` run

## Progress log

- 2026-10-21 00:00 · planner · opened
