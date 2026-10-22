---
id: P3-T006
kind: task
title: Insert-only journal role and envelope-encryption keys (master key in sops, yearly data keys)
phase: 3
type: OPS
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T005, P0-T022, P0-T024]
requirements: [R3.02, R3.N1]
roadmap_todos: [T3.41]
modules: [M18]
dashboards: []
tools: [git, uv, docker, sops, age, openssl]
mcp: []
env: []
services: [postgres]
branch: p3/P3-T006-journal-roles-and-column-keys
pr: ""
doc_sync: [docs/07-security-notes.md, docs/roadmap/phase-3-journal-and-tax.md]
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

# P3-T006 · Insert-only journal role and envelope-encryption keys (master key in sops, yearly data keys)

## Goal / expected outcome

The `journal` container connects as an insert-only `journal_app` role, read paths use a `journal_ro` role, and tax-sensitive columns use **envelope encryption**: a master key held in the sops/age secrets file and delivered to tmpfs, wrapping one data key per FY stored in the non-WORM key table `ops.journal_data_key`. Rotation re-wraps the data keys only, never rows, so no running process can edit journal rows or read sensitive columns without the key, and rotation never breaks WORM.

## Context & references

- Roadmap: [T3.41, R3.02, R3.N1](../../../docs/roadmap/phase-3-journal-and-tax.md)
- [07 §2 secrets](../../../docs/07-security-notes.md#2-secrets) · [07 §8](../../../docs/07-security-notes.md#8-data-protection-backups--audit) · [15 §2 privileges layer](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)
- Decision: [17 §D P3-B009](../../../docs/17-decisions-register.md#d-other-decisions) (yearly data keys wrapped by a master key; rotation re-wraps keys in a non-WORM key table, never rows) · [07 §8](../../../docs/07-security-notes.md#8-data-protection-backups--audit) · [15 §2 Encryption row](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many) · key rotation reminder every 90 days [16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl)
- Cross-phase prerequisites (depends_on): P0-T022 (sops + age → tmpfs, per-service scoping), P0-T024 (schemas, roles, Alembic); P0-T013 (`worm_owner` offline credential) is used to run the role migration
- Related: P3-T007 (encryption helpers), P3-T047 (WORM tests), P3-T059 (rotation drill, T3.66)

## Requirements

- Roles: `journal_app` (INSERT, SELECT on `journal.*`), `journal_ro` (SELECT on non-sensitive columns + views; used by `mt-api` queries), `journal_decrypt` (function-level EXECUTE on decrypt helpers only, granted to `journal` and report generation). No role but offline `worm_owner` owns the tables.
- **Master key** `JOURNAL_MASTER_KEY` (32-byte random, base64, versioned `mk_v<n>`) in the sops file outside the repo ([17 §D P0-B018](../../../docs/17-decisions-register.md#d-other-decisions)); mounted only into `journal` (not `mt-api`, `agents`, `litellm`, `decision-svc`).
- **Data keys:** one per FY (e.g. `dk_fy2026-27`), generated on first use, stored **wrapped** (AES-256-GCM under the master key) in `ops.journal_data_key` {`key_id`, `fy`, `wrapped_key`, `master_key_version`, `created_at`, `rewrapped_at`}. This table is **not** WORM (re-wrap is an UPDATE of the wrap only) but every change is recorded in `audit.command` (source `system`). Each encrypted row stores its `key_id`.
- **Rotation:** `mtctl journal-keys rewrap` (host CLI, TOTP) re-wraps every data key under a new master key version; it never decrypts/re-encrypts or updates a WORM row. Rotation reminder every 90 days by default ([16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl)) and immediately after any suspected leak.
- Fail-closed: `journal` refuses to start without the master key, logs only the key version, and raises an alert.

## ToDo

- [ ] Add role DDL migration `journal_0002_roles` (run as `worm_owner` from the offline secret)
- [ ] Migration for `ops.journal_data_key` (non-WORM, audited) and its grants (`journal` only)
- [ ] Add `journal` secrets stanza to `infra/sops/.sops.yaml` and the compose service's tmpfs mount
- [ ] Generate `JOURNAL_MASTER_KEY` on the host (`openssl rand -base64 32`) straight into the sops file; never echo it
- [ ] Implement data-key create/unwrap in `packages/mt_journal/keys.py` and the `mtctl journal-keys rewrap` CLI
- [ ] Ensure `mt-api`, `agents`, `litellm`, `decision-svc` have no access to the master key or the key table (compose scoping + grant test)
- [ ] Startup check in `mt_journal.app` that refuses to run without the master key and logs only its version
- [ ] Write tests; update docs

## Verification

### Tests

- Integration: as `journal_app`, INSERT ok, UPDATE/DELETE/TRUNCATE fail; as `journal_ro`, SELECT on encrypted columns denied.
- Config test: parse compose; only `journal` mounts the journal secrets file.
- Unit: data key wrap/unwrap round-trip; rewrap changes only `ops.journal_data_key` rows (full rotation drill in P3-T059).
- gitleaks run on the PR.

### Scenarios

- Given the key file is missing, when `journal` starts, then it exits non-zero with `missing column key` and an alert fires.
- Given `mt-api` is compromised, when it queries `journal.raw_payload.blob`, then permission is denied.

### Stress / failure injection

- Restart `journal` 20× in a loop; master key always loaded from tmpfs, never written to disk (check `docker diff`).
- Kill `mtctl journal-keys rewrap` mid-run → re-run completes; every data key unwraps.

## Acceptance criteria

- [ ] Roles exist with exactly the grants above (grant snapshot test)
- [ ] Master key only in sops + tmpfs; data keys stored only wrapped; nothing in git
- [ ] Rotation re-wraps data keys without touching any `journal.*` row
- [ ] Fail-closed startup verified
- [ ] CI green (lint, types, tests, `pit` check; `tax-golden` once P3-T045 lands)

## Exceptions & edge cases

- Lost age key → encrypted columns unreadable; the age key backup procedure from P0 applies (runbook link).
- Key rotation never touches existing rows; a lost master key with no backup makes data keys unrecoverable, so the age key backup (restic, 17 §D P0-B018) is part of the runbook.

## Cardinal rules (do NOT)

- Do NOT give `mt-api`, agents or the LLM gateway the column key.
- Do NOT re-encrypt or UPDATE existing WORM rows during rotation; only the wraps in `ops.journal_data_key` change.
- Do NOT store an unwrapped data key anywhere but process memory.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT expose tax-sensitive fields (TFN, addresses, raw statements) to any LLM prompt, RAG index or the LiteLLM gateway ([07 §8](../../../docs/07-security-notes.md#8-data-protection-backups--audit)).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/07-security-notes.md` §8: note the `journal_*` roles, the `ops.journal_data_key` table and the rewrap CLI.
- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.41 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T006-journal-roles-and-column-keys`
- PR title: `P3-T006: Insert-only journal role and column-encryption keys in sops`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T006` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (envelope encryption per P3-B009: master key in sops, yearly data keys wrapped in non-WORM `ops.journal_data_key`, rewrap-only rotation; explicit P0 depends_on; tools/services filled)
