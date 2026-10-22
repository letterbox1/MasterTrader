---
id: P0-T040
kind: task
title: Implement the monthly immutable export of WORM tables
phase: 0
type: BUILD
status: backlog
priority: medium
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T031, P0-T037]
requirements: [R0.07, R0.N4]
roadmap_todos: [T0.23, T0.44]
modules: [M17]
dashboards: []
tools: [git, uv, python>=3.12, docker]
mcp: []
env: []
services: [postgres, minio, prefect-server]
branch: p0/P0-T040-monthly-immutable-worm-export
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

# P0-T040 · Implement the monthly immutable export of WORM tables

## Goal / expected outcome

On the 1st of each month a Prefect flow exports every WORM table's previous-month rows to Parquet with a manifest (row counts, first/last seq, per-file SHA-256, the month's seal roots) and uploads both to the Object-Locked `mt-worm-seal` bucket with ≥ 7-year retention.

## Context & references

- [Roadmap P0 R0.07](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [15 §2.2 layers](../../../docs/15-bots-hitl-and-worm-audit.md#22-layers) (Backups: monthly immutable export ≥ 7 years)
- [07 §8 backups & audit](../../../docs/07-security-notes.md#8-data-protection-backups--audit)
- Related: P0-T037, P0-T055 (re-verify from export)
- Depends on: P0-T031, P0-T037

## Requirements

- Path `exports/<table>/<YYYY>-<MM>/part-*.parquet` + `manifest.json` (canonical JSON, itself hashed and its hash sent in the Telegram witness of that day).
- Parquet schema mirrors the table incl. chain columns; `numeric` as decimal128 or string (no float), timestamps µs UTC.
- Upload with compliance retention 2557 days; verify by re-download hash.
- A `verify-export` mode recomputes the chain from Parquet alone and checks the manifest + seal roots (used by P0-T055 and auditors).
- Export reads via `mt_flows_rw` with a consistent snapshot (`REPEATABLE READ`).

## ToDo

- [ ] Implement the export flow + manifest + upload.
- [ ] Implement `verify-export`.
- [ ] Schedule monthly at 01:30 UTC on the 1st.
- [ ] Tests below.

## Verification

### Tests
- Integration (MinIO): export a fixture month → manifest hashes match; `verify-export` passes; tampered Parquet fails.
- Unit: decimal/timestamp round trip without precision loss.

### Scenarios
- Given the DB is lost entirely, when an auditor gets the exports + anchored seals, then they can verify the trail without our DB.

### Stress / failure injection
- Export 10 M rows in < 15 min with < 2 GiB RAM (row-group streaming).

## Acceptance criteria

- [ ] Monthly export flow scheduled and run once on fixture data
- [ ] Manifest + Parquet locked for 7 years
- [ ] `verify-export` detects tampering
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- Month with zero rows: manifest with `row_count: 0` still written (proves absence).

## Cardinal rules (do NOT)

- Do NOT write floats for money in exports.
- Do NOT export secrets (args are already redacted in audit rows).
- Do NOT UPDATE or DELETE WORM rows, ever; corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/15-bots-hitl-and-worm-audit.md` §2.2: document export layout and `verify-export`.
- `docs/roadmap/phase-0-foundations.md`: tick T0.23, T0.44 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T040-monthly-immutable-worm-export`
- PR title: `P0-T040: Implement the monthly immutable export of WORM tables`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T040` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (keyless: MinIO in CI/dev, real anchoring checked in the soak P0-T063; run fields added)
