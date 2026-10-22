---
id: P3-T047
kind: task
title: WORM test suite for journal tables
phase: 3
type: VERIFY
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T005, P3-T006, P3-T008, P0-T055, P0-T038]
requirements: [R3.02]
roadmap_todos: [T3.41]
modules: [M18]
dashboards: []
tools: [git, uv, docker]
mcp: []
env: []
services: [postgres]
branch: p3/P3-T047-verify-worm-journal-suite
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

# P3-T047 · WORM test suite for journal tables

## Goal / expected outcome

The 15 §2.4 WORM tests run against every `journal.*` table: app-role UPDATE/DELETE/TRUNCATE fail, a direct edit as `worm_owner` is detected by `audit.verify`, a seal mismatch triggers the incident path (the configured integrity action, default `block_new_entries`: no new entries, exits continue; an `audit.integrity_incident` row; cleared only by `audit.integrity.ack` (C3)), restore from immutable backup re-verifies, and insert throughput with hashing stays within SLOs.

## Context & references

- Roadmap: [R3.02, T3.41](../../../docs/roadmap/phase-3-journal-and-tax.md) · [15 §2.4 tests](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many) · [SPEC NN7](../../../SPEC.md#non-negotiable-requirements)
- Cross-phase prerequisites (depends_on): P0-T055 (WORM test suite framework), P0-T038 (`audit.verify` and incident path); P0-T040 (monthly immutable WORM export) for the restore drill
- Integrity action: [16 §2.11](../../../docs/16-configuration-and-safety-model.md#211-worm-integrity) · decision [17 §A P0-B001](../../../docs/17-decisions-register.md#a-s2-items-all-resolved)

## Requirements

- Parametrised over the table list discovered from the WORM registry (new journal tables are automatically included).
- Retention: no partition drop or retention policy on `journal.*` < 7 years (catalog check).
- Insert throughput: ≥ 500 journal events/s sustained with hashing on the target host, WORM insert p99 < 5 ms ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)); fills on the order path never wait on journal writes or seals (journal is async via NATS).
- The envelope-encryption key table `ops.journal_data_key` is asserted **not** WORM-registered (rotation re-wraps it) but every change to it appears in `audit.command`.

## ToDo

- [ ] Extend the P0 WORM suite with `tests/worm/test_journal_worm.py`
- [ ] Seal-mismatch drill on a scratch DB
- [ ] Restore drill from the immutable backup (scratch target)
- [ ] Record results

## Verification

### Tests

- As listed in Requirements.

### Scenarios

- Given a row edited as `worm_owner` in a scratch DB, when `audit.verify` runs, then a critical incident is raised, KV `audit.integrity` shows `block_new_entries` (default; options `alert_only` / `halt_all`), new entries are rejected while exits continue, and only `audit.integrity.ack` (C3) clears it.

### Stress / failure injection

- Sustained 500 events/s for 10 min; p99 insert latency recorded.

## Acceptance criteria

- [ ] All WORM checks pass for every journal table
- [ ] Throughput target met
- [ ] Drill results in progress log

## Exceptions & edge cases

- Run destructive drills only on scratch DBs, never the live DB.

## Cardinal rules (do NOT)

- Do NOT run tamper drills against the production database.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.41 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T047-verify-worm-journal-suite`
- PR title: `P3-T047: WORM test suite for journal tables`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T047` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (integrity action `block_new_entries` + C3 ack per 16 §2.11 (was halt); insert p99 < 5 ms; key table not WORM (P3-B009); explicit P0 depends_on; tools/services filled)
