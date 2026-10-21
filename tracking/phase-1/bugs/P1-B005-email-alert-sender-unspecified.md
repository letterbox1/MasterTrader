---
id: P1-B005
kind: gap
title: Email alert channel has no defined sender or SMTP provider
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
branch: p1/P1-B005-email-alert-sender-unspecified
pr: ""
doc_sync: [docs/07-security-notes.md, docs/roadmap/phase-1-data-and-monitoring.md]
doc_sync_status: n/a
found_in: docs/07-security-notes.md §9; docs/roadmap/phase-1-data-and-monitoring.md R1.14 / T1.03
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P1-B005 · Email alert channel has no defined sender or SMTP provider

## Goal / expected outcome

The docs name how email is sent (e.g. an SMTP account on a free plan or your mail provider's SMTP with an app password), where credentials live (sops), and deliverability expectations

## Context & references

- Found in: [07 §9](../../../docs/07-security-notes.md#9-monitoring--incident-response) lists email as an alert channel; T1.03 only confirms the destination address
- Related items: P1-T003, P1-T045, P1-T060

## Requirements

- **Where:** [07 §9](../../../docs/07-security-notes.md#9-monitoring--incident-response) lists email as an alert channel; T1.03 only confirms the destination address
- **Expected:** The docs name how email is sent (e.g. an SMTP account on a free plan or your mail provider's SMTP with an app password), where credentials live (sops), and deliverability expectations
- **Actual:** No sender, provider or credential location is defined
- **Suggested fix:** Add an `alerts.email` section to 07 §9: SMTP host, TLS, app password in sops, sender address, SPF/DKIM if a custom domain; add a USER step to create the app password (can be folded into P1-T003)
- **Impact:** Alert path test (P1-T060) cannot pass on email (severity S3)

## ToDo

- [ ] Decide the provider with the user
- [ ] Edit 07 §9 and T1.03 wording
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

- `docs/07-security-notes.md`: apply the fix above
- `docs/roadmap/phase-1-data-and-monitoring.md`: apply the fix above

## Branch & PR

- Branch: `p1/P1-B005-email-alert-sender-unspecified`
- PR title: `P1-B005: Email alert channel has no defined sender or SMTP provider`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-B005` run

## Progress log

- 2026-10-21 00:00 · planner · opened
