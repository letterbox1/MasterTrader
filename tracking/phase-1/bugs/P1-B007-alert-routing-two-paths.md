---
id: P1-B007
kind: gap
title: Alert routing has two undefined paths (Grafana Alerting vs alert.* consumer)
phase: 1
type: DOC
status: done
priority: medium
size: S
severity: S3
owner: agent
claimed_by: ""
depends_on: []
requirements: [R1.14]
roadmap_todos: []
modules: []
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p1/P1-B007-alert-routing-two-paths
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/03-build-spec.md, docs/roadmap/phase-1-data-and-monitoring.md]
doc_sync_status: done
found_in: docs/03-build-spec.md §2 and M16; docs/02-v1-architecture.md §6; docs/roadmap/phase-1-data-and-monitoring.md R1.14 / T1.31
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: 2026-10-22
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P1-B007 · Alert routing has two undefined paths (Grafana Alerting vs alert.* consumer)

## Goal / expected outcome

One documented path: Grafana/Alertmanager → webhook → `alert.*` → notifier → Telegram/email/ntfy/notification centre

## Context & references

- Found in: 03 says "Grafana Alerting → Telegram"; R1.14 says "Grafana Alerting → Telegram + email + ntfy"; T1.31 says one `alert.{severity}.{kind}` consumer; [02 §6](../../../docs/02-v1-architecture.md#6-messaging-nats) lists `alert.*` consumers as only "telegram, UI"
- Related items: P1-T045, P1-T054, P1-T060

## Requirements

- **Where:** 03 says "Grafana Alerting → Telegram"; R1.14 says "Grafana Alerting → Telegram + email + ntfy"; T1.31 says one `alert.{severity}.{kind}` consumer; [02 §6](../../../docs/02-v1-architecture.md#6-messaging-nats) lists `alert.*` consumers as only "telegram, UI"
- **Expected:** One documented path: Grafana/Alertmanager → webhook → `alert.*` → notifier → Telegram/email/ntfy/notification centre
- **Actual:** Two paths would duplicate or drop alerts and make dedupe impossible
- **Suggested fix:** Adopt the single path implemented in P1-T045 and update 02 §6 consumers and 03 §2
- **Impact:** Duplicate or missing alerts (severity S3)

## ToDo

- [x] Decision recorded in docs/17 (17 §D P1-B007): one fan-out: Grafana alerts → webhook → the `alert.*` consumer → Telegram/ntfy/email
- [x] Aligned docs carry it: 02 §6 (`alert.{severity}.{kind}` row and "One alert path" rule), 03 M15 (Grafana), 07 §9; roadmap R1.14, T1.31
- [x] Affected P1 tasks updated in the 2026-10-22 task alignment: P1-T045, P1-T054, P1-T060

## Verification

### Tests

- Doc review: the edited sections agree with each other and with the affected task files

### Scenarios

- Given a developer picks up the related task cold, when they read the fixed docs, then there is exactly one interpretation

### Stress / failure injection

- n/a: documentation gap

## Acceptance criteria

- [x] Docs updated and consistent (02 §6 (`alert.{severity}.{kind}` row and "One alert path" rule), 03 M15 (Grafana), 07 §9; roadmap R1.14, T1.31)
- [x] Decision and owning tasks noted in the progress log

## Exceptions & edge cases

- Until fixed, related tasks follow the interim rule stated in their own files

## Cardinal rules (do NOT)

- Do NOT resolve by silently picking a number in code; the decision lands in the docs first
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.

## Doc sync on completion

- `docs/02-v1-architecture.md`: apply the fix above
- `docs/03-build-spec.md`: apply the fix above
- `docs/roadmap/phase-1-data-and-monitoring.md`: apply the fix above

## Branch & PR

- Branch: `p1/P1-B007-alert-routing-two-paths`
- PR title: `P1-B007: Alert routing has two undefined paths (Grafana Alerting vs alert.* consumer)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-B007` run

## Progress log

- 2026-10-21 00:00 · planner · opened
- 2026-10-22 00:00 · aligner · resolved by 17 §D P1-B007; docs carry it (02 §6 (`alert.{severity}.{kind}` row and "One alert path" rule), 03 M15 (Grafana), 07 §9; roadmap R1.14, T1.31); implementation owned by P1-T045, P1-T054, P1-T060
- 2026-10-22 02:08 · cloud:vm:be04b6ae61f8 · verified: decided in docs/17 (17 §D P1-B007); docs updated: 02 §6 (`alert.{severity}.{kind}` row and "One alert path" rule), 03 M15 (Grafana), 07 §9; roadmap R1.14, T1.31; implementation owned by P1-T045, P1-T054, P1-T060
- 2026-10-22 02:08 · cloud:vm:be04b6ae61f8 · done
- 2026-10-22 02:08 · cloud:vm:be04b6ae61f8 · doc sync done: docs updated in the alignment wave
