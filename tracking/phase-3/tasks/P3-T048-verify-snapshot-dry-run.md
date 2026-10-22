---
id: P3-T048
kind: task
title: Snapshot dry run on a test date
phase: 3
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T029, P3-T030]
requirements: [R3.08]
roadmap_todos: [T3.62]
modules: [M18]
dashboards: [D15]
tools: [git, uv, docker]
mcp: []
env: []
services: [postgres, prefect-server, journal]
branch: p3/P3-T048-verify-snapshot-dry-run
pr: ""
doc_sync: [docs/roadmap/phase-3-journal-and-tax.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P3-T048 · Snapshot dry run on a test date

## Goal / expected outcome

The snapshot flow runs end-to-end in production configuration for a test valuation time (e.g. 2027-01-31 23:59:59 AEST, `kind = dry_run`) over the real paper-trading lots, proving completeness, idempotency, price-source recording and the AU_2027_REFORM comparison numbers well before 30 June 2027.

## Context & references

- Roadmap: [R3.08, T3.62](../../../docs/roadmap/phase-3-journal-and-tax.md) · job P3-T030 · runbook P3-T044

## Requirements

- Run via Prefect with `kind = dry_run` (separate key space; never confused with `reform_2027`).
- Checks: completeness = 100% of open lots; every row has price + source + method + timestamps per the [16 §4.2](../../../docs/16-configuration-and-safety-model.md#42-market-value-snapshot-30-june-2027-and-any-residency-change) convention (crypto rows show the 23:55:00–23:59:59 AEST VWAP window); re-run creates 0 rows; worker kill mid-run recovers; late-run (next day) gives identical values; AU_2027_REFORM comparison computes for a synthetic post-date disposal.
- Runbook steps exercised and timed.

## ToDo

- [ ] Schedule/run the dry run
- [ ] Run the checks and record results + timings in the progress log
- [ ] File bugs for any deviations

## Verification

### Tests

- Integration run as described.

### Scenarios

- Given the dry run completes, when D15 Lots is filtered to `dry_run`, then every open lot shows a snapshot value.

### Stress / failure injection

- Kill the worker twice mid-run; completes without duplicates.

## Acceptance criteria

- [ ] 100% completeness
- [ ] Idempotent and late-run-identical
- [ ] Runbook validated

## Exceptions & edge cases

- Dry-run rows remain in WORM tables tagged `dry_run`; reports ignore them.

## Cardinal rules (do NOT)

- Do NOT use `kind = reform_2027` for tests.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.62 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T048-verify-snapshot-dry-run`
- PR title: `P3-T048: Snapshot dry run on a test date`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T048` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (dry run checks the 16 §4.2 convention and method recording (P3-B002); fields filled)
