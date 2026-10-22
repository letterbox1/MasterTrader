---
id: P3-T059
kind: task
title: Key rotation re-wraps data keys only and the hash chain still verifies
phase: 3
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T006, P3-T007, P3-T047, P0-T038]
requirements: [R3.N1, R3.02]
roadmap_todos: [T3.66]
modules: [M18, M17]
dashboards: [D16]
tools: [git, uv, docker, sops, age]
mcp: []
env: []
services: [postgres]
branch: p3/P3-T059-key-rotation-re-wraps-data-keys-only-and-the-has
pr: ""
doc_sync: [docs/roadmap/phase-3-journal-and-tax.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-22
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P3-T059 · Key rotation re-wraps data keys only and the hash chain still verifies

## Goal / expected outcome

A drill on a scratch database proves envelope-encryption rotation is WORM-safe: rotating the master key re-wraps every yearly data key in the non-WORM key table, no `journal.*` row changes (byte-identical, same `row_hash`), every encrypted column still decrypts, and `audit.verify` passes against the external seal.

## Context & references

- Roadmap: [R3.N1, T3.66](../../../docs/roadmap/phase-3-journal-and-tax.md)
- Decision: [17 §D P3-B009](../../../docs/17-decisions-register.md#d-other-decisions) · [07 §8](../../../docs/07-security-notes.md#8-data-protection-backups--audit) (key rotation without breaking WORM) · [15 §2 Encryption row](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)
- Under test: P3-T006 (master key + `ops.journal_data_key`), P3-T007 (encrypt/decrypt helpers), P3-T047 (WORM suite)
- Cross-phase prerequisite (depends_on): P0-T038 (`audit.verify` and the incident path)

## Requirements

- Scratch DB seeded with ≥ 3 FYs of synthetic events, encrypted columns (TFN canary, raw payloads, residency evidence) under three yearly data keys.
- Snapshot before: sha256 of every `journal.*` row's canonical JSON + `row_hash`, latest seal; key table contents.
- Rotate: new master key version in a scratch sops file; run the rotation CLI (`mtctl journal-keys rewrap`), which re-wraps each data key and records the rotation in `audit.command` (source `system`).
- Snapshot after: every `journal.*` row identical; only `ops.journal_data_key` rows show the new wrap/master version; old master key retired and removed from tmpfs.
- Decrypt every encrypted value with the new master key → plaintext identical; with the old master key removed → still decrypts (proves no row depended on it directly).
- `audit.verify` (full) passes; no `audit.integrity_incident` row.
- Negative test: a "rotation" implementation that re-encrypts rows is detected (UPDATE blocked by WORM trigger, test asserts the failure).

## ToDo

- [ ] Write `tests/security/test_key_rotation_worm.py` and the scratch seed
- [ ] Run the drill; record hashes before/after and the verify result in the progress log
- [ ] File bugs for any deviation

## Verification

### Tests
- The drill above, automated; negative test included.

### Scenarios
- Given the 90-day rotation reminder fires (16 §2.3), when you follow the runbook rotation, then reports for every past FY regenerate with identical hashes.

### Stress / failure injection
- Kill the rotation mid-way (after 1 of 3 keys) → re-run completes; no data key left unreadable; rows untouched.

## Acceptance criteria

- [ ] Zero `journal.*` row changes across rotation (hash comparison)
- [ ] All encrypted values decrypt after rotation
- [ ] `audit.verify` passes; rotation audited
- [ ] Results recorded in the progress log

## Exceptions & edge cases

- Run destructive and negative tests only on scratch DBs, never the live DB.

## Cardinal rules (do NOT)

- Do NOT re-encrypt or UPDATE WORM rows during rotation ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT use real keys or a real TFN in the drill.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.66 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T059-key-rotation-re-wraps-data-keys-only-and-the-has`
- PR title: `P3-T059: Key rotation re-wraps data keys only and the hash chain still verifies`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T059` run

## Progress log

- 2026-10-22 00:00 · aligner · created for R3.N1/T3.66 (docs/16–17 alignment; verifies the P3-B009 decision)
