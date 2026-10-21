---
id: P1-B007
kind: gap
title: Alert routing has two undefined paths (Grafana Alerting vs alert.* consumer)
phase: 1
type: DOC
status: backlog
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
branch: p1/P1-B007-alert-routing-two-paths
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/03-build-spec.md, docs/roadmap/phase-1-data-and-monitoring.md]
doc_sync_status: n/a
found_in: docs/03-build-spec.md §2 and M16; docs/02-v1-architecture.md §6; docs/roadmap/phase-1-data-and-monitoring.md R1.14 / T1.31
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
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

- [ ] Edit 02 §6, 03 §2 and R1.14 wording
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

- `docs/02-v1-architecture.md`: apply the fix above
- `docs/03-build-spec.md`: apply the fix above
- `docs/roadmap/phase-1-data-and-monitoring.md`: apply the fix above

## Branch & PR

- Branch: `p1/P1-B007-alert-routing-two-paths`
- PR title: `P1-B007: Alert routing has two undefined paths (Grafana Alerting vs alert.* consumer)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-B007` run

## Progress log

- 2026-10-21 00:00 · planner · opened
