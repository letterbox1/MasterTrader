---
id: P0-T055
kind: task
title: Run the full WORM test suite
phase: 0
type: VERIFY
status: backlog
priority: critical
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T038, P0-T040, P0-T041]
requirements: [R0.07, R0.12, R0.N7]
roadmap_todos: [T0.61]
modules: [M17]
dashboards: []
tools: [git, uv, python>=3.12, docker]
mcp: []
env: []
services: [postgres, nats, minio]
branch: p0/P0-T055-worm-test-suite
pr: ""
doc_sync: [docs/15-bots-hitl-and-worm-audit.md, docs/roadmap/phase-0-foundations.md]
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

# P0-T055 · Run the full WORM test suite

## Goal / expected outcome

A reusable WORM test suite (`tests/worm/`) proves every 15 §2.4 property for every table in `audit.worm_registry`: app-role UPDATE/DELETE/TRUNCATE fail; a direct edit as `worm_owner` or superuser is caught by `audit.verify`; a seal mismatch triggers the incident path and the integrity response (`audit.integrity` = `block_new_entries` by default); a restore from immutable backup re-verifies cleanly; insert throughput with hashing stays within target. Later phases re-run it automatically for their new WORM tables.

## Context & references

- [Roadmap P0 R0.07](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [Roadmap P0 T0.61](../../../docs/roadmap/phase-0-foundations.md#4-todo-sets)
- [15 §2.4 tests](../../../docs/15-bots-hitl-and-worm-audit.md#24-tests-part-of-every-phase-that-adds-a-worm-table)
- [15 §2.2 layers](../../../docs/15-bots-hitl-and-worm-audit.md#22-layers)
- [15 §2.3 threat coverage](../../../docs/15-bots-hitl-and-worm-audit.md#23-what-this-protects-against)
- [SPEC non-negotiables](../../../SPEC.md#non-negotiable-requirements) (NN7)
- Depends on: P0-T029, P0-T030, P0-T031, P0-T037, P0-T038, P0-T040, P0-T039

## Requirements

- Parametrised over `audit.worm_registry` so new tables are covered without new code.
- Privilege tests per table and per app role: UPDATE, DELETE, TRUNCATE, `ALTER TABLE DISABLE TRIGGER`, `DROP`, `DETACH PARTITION` → all fail; `SET ROLE worm_owner` from app roles fails.
- Owner tests: as `worm_owner`, UPDATE/DELETE → `MT001` (trigger).
- Tamper detection: as superuser with triggers disabled, (a) modify a payload field, (b) delete a middle row, (c) insert a forged row with recomputed chain, (d) rewrite a whole day consistently and the `audit.seal` row → `audit.verify` reports mismatch for each; (d) is caught **only** via the external anchor.
- Seal mismatch → `audit.integrity_incident` critical row, `alert.critical.audit_verify` published, KV `audit.integrity` = the configured action (default `block_new_entries`), `mt_risk.integrity_gate` rejects an entry and passes an exit, and only a C3 `audit.integrity.ack` clears it, as a new row (15 §2.4, [16 §2.11](../../../docs/16-configuration-and-safety-model.md#211-worm-integrity)); D16 banner data via `/audit/integrity`.
- Ack rows: an integrity ack adds a row and never updates the incident (15 §2.4).
- Restore re-verify: restore the latest pgBackRest backup to a scratch DB (P0-T041) and run `audit.verify` full → ok; also `verify-export` on the latest monthly export.
- No `ON DELETE CASCADE` reaches a WORM table (lint).
- Throughput: `audit.command` insert ≥ 1,000 rows/s, p99 < 5 ms while a seal runs (SLO, [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P0-B004; the gated benchmark is P0-T066).

## ToDo

- [ ] Write the parametrised suite and fixtures (MinIO object-lock for anchors in CI).
- [ ] Add a `make wormtest` target and CI job (nightly + on changes to `migrations/**`, `packages/mt_store/**`, `packages/mt_obs/**`).
- [ ] Run on the host against a scratch DB and log results.
- [ ] File bugs for any failure.

## Verification

### Tests
- The suite (≥ 40 parametrised cases across six tables).

### Scenarios
- Given an app bug issues `DELETE FROM audit.command WHERE ...`, then it fails and the error is logged with SQLSTATE.
- Given OS-root tampering rewrites a day and its DB seal, then verify detects it against the Object-Locked anchor.

### Stress / failure injection
- Throughput under concurrent seal + verify on 5 M rows (logged against the p99 < 5 ms SLO).

## Acceptance criteria

- [ ] Every 15 §2.4 test passes for every registered table
- [ ] External-anchor-only detection case (d) passes
- [ ] Restore re-verify passes
- [ ] Suite in CI and parametrised by registry
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- Superuser tampering is detected, not prevented (15 §2.3) — tests assert detection, not prevention.

## Cardinal rules (do NOT)

- Do NOT run tamper tests against production data; scratch DBs only.
- Do NOT exclude a table from the registry to make the suite pass.
- Do NOT UPDATE or DELETE WORM rows, ever; corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/15-bots-hitl-and-worm-audit.md` §2.4: link `tests/worm/` and the `make wormtest` target.
- `docs/roadmap/phase-0-foundations.md`: tick T0.61 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T055-worm-test-suite`
- PR title: `P0-T055: Run the full WORM test suite`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T055` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (integrity response (16 §2.11) replaces trading_halt; ack-as-new-row test; insert SLO (R0.N7); deps trimmed to true preconditions; run fields added)
