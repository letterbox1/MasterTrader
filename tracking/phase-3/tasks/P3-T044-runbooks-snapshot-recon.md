---
id: P3-T044
kind: task
title: Runbooks for the 2027 snapshot and reconciliation breaks
phase: 3
type: DOC
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T030, P3-T034]
requirements: [R3.08, R3.11]
roadmap_todos: [T3.25, T3.28]
modules: [M18]
dashboards: []
branch: p3/P3-T044-runbooks-snapshot-recon
pr: ""
doc_sync: [docs/runbooks/journal-snapshot-2027-06-30.md, docs/runbooks/journal-recon-break.md, docs/roadmap/phase-3-journal-and-tax.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P3-T044 · Runbooks for the 2027 snapshot and reconciliation breaks

## Goal / expected outcome

Two runbooks exist in `docs/runbooks/`: "30 June 2027 snapshot" (pre-checks, verify, late run, missing prices, re-valuation by superseding row) and "Journal reconciliation break" (triage, explain vs correct, escalation), so either can be followed cold by you or an agent.

## Context & references

- Roadmap: [R3.08, R3.11, T3.25, T3.28](../../../docs/roadmap/phase-3-journal-and-tax.md)
- Runbook convention: [07 §9](../../../docs/07-security-notes.md#9-monitoring--incident-response) · related jobs P3-T030, P3-T034 · diary P3-T004

## Requirements

- `docs/runbooks/journal-snapshot-2027-06-30.md`: T-30 days checks (backups, price feeds, Prefect schedule, P3-T002 answer), on-the-day verification (completeness query, D15 Lots), host-down recovery (late run is identical), `needs_valuation` handling (manual valuation via audited command with evidence), never edit rows.
- `docs/runbooks/journal-recon-break.md`: read the break, common causes (late funding, venue delay, missing ledger type, unmatched transfer), explain (annotation) vs correct (superseding event), when to escalate (> 2 days, any WORM verify failure → halt per 15 §2).
- Each runbook has exact commands/queries and links to Grafana panels.

## ToDo

- [ ] Write both runbooks
- [ ] Link them from D15 Lots banner and D14 recon widget help
- [ ] Peer-check by dry-running against P3-T048 and a seeded break in P3-T052

## Verification

### Tests

- Doc test: runbook commands executed during P3-T048/P3-T052 runs succeed as written.

### Scenarios

- Given a seeded recon break, when the runbook is followed, then the break is resolved without editing any journal row.

### Stress / failure injection

- n/a: documentation

## Acceptance criteria

- [ ] Both runbooks merged and linked
- [ ] Exercised once each (progress log)

## Exceptions & edge cases

- Runbook must cover the case where the WORM verify fails during an investigation (halt + incident).

## Cardinal rules (do NOT)

- Do NOT instruct anyone to UPDATE/DELETE journal rows in a runbook.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/runbooks/`: two new runbooks; `docs/roadmap/README.md` §5 Runbooks row for P3 (generated/main-agent maintained) should list them.
- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.25, T3.28 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T044-runbooks-snapshot-recon`
- PR title: `P3-T044: Runbooks for the 2027 snapshot and reconciliation breaks`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T044` run

## Progress log

- 2026-10-21 00:00 · planner · created
