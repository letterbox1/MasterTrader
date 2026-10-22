---
id: P1-B009
kind: gap
title: Loosening DQ thresholds is C3, but the Telegram approval path arrives in P2
phase: 1
type: DOC
status: done
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
tools: []
mcp: []
env: []
services: []
branch: p1/P1-B009-c3-path-missing-in-p1
pr: ""
doc_sync: [docs/ui/dashboards/D07-data-quality.md, docs/roadmap/phase-1-data-and-monitoring.md]
doc_sync_status: done
found_in: docs/ui/dashboards/D07-data-quality.md Actions; docs/roadmap/phase-2-strategies-risk-lab.md T2.33; docs/roadmap/phase-1-data-and-monitoring.md T1.04
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
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

- [x] Decision recorded in docs/17 (17 §D P0-B002/P1-B009): until Telegram C3 exists (P2), C3 commands complete through the host-only break-glass CLI `mtctl approve <id>` + TOTP, audited
- [x] Aligned docs carry it: 02 §7.2 ("Before Telegram C3 exists"); D07 actions (Adjust DQ thresholds); roadmap R1.10
- [x] Affected P1 tasks updated in the 2026-10-22 task alignment: P1-T030, P1-T046, P1-T066 (CLI built in P0-T035)

## Verification

### Tests

- Doc review: the edited sections agree with each other and with the affected task files

### Scenarios

- Given a developer picks up the related task cold, when they read the fixed docs, then there is exactly one interpretation

### Stress / failure injection

- n/a: documentation gap

## Acceptance criteria

- [x] Docs updated and consistent (02 §7.2 ("Before Telegram C3 exists"); D07 actions (Adjust DQ thresholds); roadmap R1.10)
- [x] Decision and owning tasks noted in the progress log

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
- 2026-10-22 00:00 · aligner · resolved by 17 §D P0-B002/P1-B009; docs carry it (02 §7.2 ("Before Telegram C3 exists"); D07 actions (Adjust DQ thresholds); roadmap R1.10); implementation owned by P1-T030, P1-T046, P1-T066 (CLI built in P0-T035)
- 2026-10-22 02:08 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D P0-B002/P1-B009); docs updated: 02 §7.2 ("Before Telegram C3 exists"); D07 actions (Adjust DQ thresholds); roadmap R1.10; implementation owned by P1-T030, P1-T046, P1-T066 (CLI built in P0-T035)
- 2026-10-22 02:08 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:08 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
