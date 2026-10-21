---
id: P1-T055
kind: task
title: Write data-operations runbooks
phase: 1
type: DOC
status: backlog
priority: medium
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T048, P1-T052, P1-T045]
requirements: [R1.10, R1.12, R1.N3]
roadmap_todos: []
modules: [M1, M16]
dashboards: [D07]
branch: p1/P1-T055-runbooks-data-ops
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/runbooks/data-feeds.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P1-T055 · Write data-operations runbooks

## Goal / expected outcome

`docs/runbooks/data-feeds.md` explains how to triage a stale/bad feed, run and verify a backfill, handle a recon mismatch or testnet reset, respond to a quota exhaustion, and recover from a full disk, using the D07 controls and CLI commands built in P1.

## Context & references

- Roadmap: requirements [R1.10](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.12](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.N3](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements)
- Runbooks home: [07 §9](../../../docs/07-security-notes.md#9-monitoring--incident-response) (P2 adds "bad data" for trading impact) · [D07 Data & Quality](../../../docs/ui/dashboards/D07-data-quality.md) actions
- Depends on (this phase): P1-T048, P1-T052, P1-T045

## Requirements

- One section per scenario: symptoms (alert text, D07 view), checks, commands (`mt-data`, `mt-monitor`, D07 actions), escalation, how to confirm resolved
- Covers: stale feed, divergence incident, clock skew/chrony, gap + backfill, quota exhausted, recon mismatch/testnet reset, disk > 85%, alert channel down, provider API change
- No secrets or account numbers in the runbook

## ToDo

- [ ] Write the runbook
- [ ] Dry-run each procedure once on the dev stack and note results in the progress log
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Review: each command in the runbook executed once against the dev stack (recorded)

### Scenarios

- Given a stale-feed alert at 3 am, when you follow the runbook from your phone, then you can pause the feed from D07 and know whether trading would be affected

### Stress / failure injection

- n/a: documentation

## Acceptance criteria

- [ ] Runbook covers all nine scenarios and every command was executed once
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- P2 will extend "bad data" with strategy pause/flatten steps; link forward

## Cardinal rules (do NOT)

- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: no ToDo box of its own; note P1-T055 as evidence under the requirements it verifies (R1.10, R1.12, R1.N3).
- `docs/runbooks/data-feeds.md`: new file

## Branch & PR

- Branch: `p1/P1-T055-runbooks-data-ops`
- PR title: `P1-T055: Write data-operations runbooks`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T055` run

## Progress log

- 2026-10-21 00:00 · planner · created
