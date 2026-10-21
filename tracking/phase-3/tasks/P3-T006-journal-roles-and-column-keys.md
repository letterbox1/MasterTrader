---
id: P3-T006
kind: task
title: Insert-only journal role and column-encryption keys in sops
phase: 3
type: OPS
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T005]
requirements: [R3.02, R3.N1]
roadmap_todos: [T3.41]
modules: [M18]
dashboards: []
branch: p3/P3-T006-journal-roles-and-column-keys
pr: ""
doc_sync: [docs/07-security-notes.md, docs/roadmap/phase-3-journal-and-tax.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P3-T006 · Insert-only journal role and column-encryption keys in sops

## Goal / expected outcome

The `journal` container connects as an insert-only `journal_app` role, read paths use a `journal_ro` role, and the pgcrypto column key (versioned) is delivered from the sops file to tmpfs, so no running process can edit journal rows or read tax-sensitive columns without the key.

## Context & references

- Roadmap: [T3.41, R3.02, R3.N1](../../../docs/roadmap/phase-3-journal-and-tax.md)
- [07 §2 secrets](../../../docs/07-security-notes.md#2-secrets) · [07 §8](../../../docs/07-security-notes.md#8-data-protection-backups--audit) · [15 §2 privileges layer](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)
- Cross-phase prerequisites: P0 T0.43 (sops + age → tmpfs, per-service scoping), P0 T0.23 (`worm_owner` offline)
- Related: P3-T007 (encryption helpers), P3-T047 (WORM tests), P3-B009 (key rotation vs WORM)

## Requirements

- Roles: `journal_app` (INSERT, SELECT on `journal.*`), `journal_ro` (SELECT on non-sensitive columns + views; used by `mt-api` queries), `journal_decrypt` (function-level EXECUTE on decrypt helpers only, granted to `journal` and report generation). No role but offline `worm_owner` owns the tables.
- Keys: `JOURNAL_COLUMN_KEY_V1` (32-byte random, base64) in `secrets/journal.enc.yaml`; mounted only into `journal` (not `mt-api`, `agents`, `litellm`). Key id stored in each encrypted row (`key_id`).
- Rotation model: new key id for new rows; old keys retained read-only in sops (never re-encrypt WORM rows; see P3-B009).
- Grafana: alert if `journal` starts without a key (fail-closed: service refuses to start).

## ToDo

- [ ] Add role DDL migration `journal_0002_roles` (run as `worm_owner` from the offline secret)
- [ ] Add `journal` secrets stanza to `infra/sops/.sops.yaml` and the compose service's tmpfs mount
- [ ] Generate `JOURNAL_COLUMN_KEY_V1` on the host (`openssl rand -base64 32`) straight into `sops secrets/journal.enc.yaml`
- [ ] Ensure `mt-api`, `agents`, `litellm`, `decision-svc` have no access to the key (compose scoping test)
- [ ] Startup check in `mt_journal.app` that refuses to run without a key and logs only the key id
- [ ] Write tests; update docs

## Verification

### Tests

- Integration: as `journal_app`, INSERT ok, UPDATE/DELETE/TRUNCATE fail; as `journal_ro`, SELECT on encrypted columns denied.
- Config test: parse compose; only `journal` mounts the journal secrets file.
- gitleaks run on the PR.

### Scenarios

- Given the key file is missing, when `journal` starts, then it exits non-zero with `missing column key` and an alert fires.
- Given `mt-api` is compromised, when it queries `journal.raw_payload.blob`, then permission is denied.

### Stress / failure injection

- Restart `journal` 20× in a loop; key always loaded from tmpfs, never written to disk (check `docker diff`).

## Acceptance criteria

- [ ] Roles exist with exactly the grants above (grant snapshot test)
- [ ] Key only in sops + tmpfs; nothing in git
- [ ] Fail-closed startup verified
- [ ] CI green (lint, types, tests, `pit` check; `tax-golden` once P3-T045 lands)

## Exceptions & edge cases

- Lost age key → encrypted columns unreadable; the age key backup procedure from P0 applies (runbook link).
- Key rotation never touches existing rows.

## Cardinal rules (do NOT)

- Do NOT give `mt-api`, agents or the LLM gateway the column key.
- Do NOT re-encrypt existing WORM rows during rotation.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT expose tax-sensitive fields (TFN, addresses, raw statements) to any LLM prompt, RAG index or the LiteLLM gateway ([07 §8](../../../docs/07-security-notes.md#8-data-protection-backups--audit)).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/07-security-notes.md` §8: note the `journal_*` roles and key-id versioning.
- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.41 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T006-journal-roles-and-column-keys`
- PR title: `P3-T006: Insert-only journal role and column-encryption keys in sops`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T006` run

## Progress log

- 2026-10-21 00:00 · planner · created
