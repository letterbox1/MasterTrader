---
id: P3-T007
kind: task
title: pgcrypto column encryption and prompt exclusion for tax-sensitive fields
phase: 3
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T005, P3-T006]
requirements: [R3.N1]
roadmap_todos: [T3.41]
modules: [M18]
dashboards: []
branch: p3/P3-T007-column-encryption-prompt-exclusion
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

# P3-T007 · pgcrypto column encryption and prompt exclusion for tax-sensitive fields

## Goal / expected outcome

Tax-sensitive fields (TFN, postal/residential address, raw statement payloads, counterparty personal details, residency evidence notes) are encrypted with pgcrypto using the versioned key, and every such column plus all `journal.*` rows are tagged `model_input_ok = false` so the LLM/RAG paths refuse them.

## Context & references

- Roadmap: [R3.N1, T3.41](../../../docs/roadmap/phase-3-journal-and-tax.md) · verified by P3-T050 (prompt audit)
- [07 §8](../../../docs/07-security-notes.md#8-data-protection-backups--audit) · provenance mechanism [12 §5](../../../docs/12-policy-and-compliance.md#5-data-provenance-tagging-one-mechanism-for-all-data-terms)
- Cross-phase: P0 R0.05 provenance columns; P6 agents will read journal summaries only through allowed views

## Requirements

- Encrypted columns: `journal.taxpayer_profile.tfn`, `.address`, `journal.raw_payload.blob`, `journal.residency_period.evidence_notes`, `journal.event.counterparty_name` (if present); stored as `bytea` via `pgp_sym_encrypt(text, key)` with a `key_id` column.
- New table `journal.taxpayer_profile` (append-only; latest row wins) for TFN/address used only by the accountant pack and myTax worksheet.
- Python helper `mt_journal.crypto.encrypt/decrypt` that pulls the key from tmpfs; decrypt only inside the `journal` service.
- Provenance: every `journal.*` row sets `model_input_ok = false`, `train_ok = false`; a DB view `journal.llm_safe_summary` (aggregates only: P&L by strategy/period, no identifiers) is the only object `agents`' role may read.
- Logging: structlog processor redacts any field named in a deny-list (`tfn`, `address`, `raw_payload`, `evidence_notes`).

## ToDo

- [ ] Migration `journal_0003_taxpayer_profile` + encrypted column types
- [ ] Implement `packages/mt_journal/crypto.py` (encrypt/decrypt, key-id lookup, constant-time compare not needed)
- [ ] Add the structlog redaction processor to `mt_obs` config for the `journal` service
- [ ] Create `journal.llm_safe_summary` view and grant it to the agents role (only object granted)
- [ ] Unit + integration tests; docs

## Verification

### Tests

- Unit: round-trip encrypt/decrypt with key v1 and v2; wrong key fails closed.
- Integration: a raw SELECT of `journal.taxpayer_profile` as `journal_ro` returns ciphertext/permission denied.
- Unit: log redaction test (log a dict containing `tfn`; output shows `***`).

### Scenarios

- Given a statement is ingested, when stored, then `raw_payload.blob` is ciphertext and `raw_payload_hash` is the sha256 of the plaintext.
- Given the agents role, when it queries `journal.event`, then permission is denied; `journal.llm_safe_summary` works.

### Stress / failure injection

- Encrypt/decrypt 10k payloads; record p95 latency (informational; ingest path budget 5 s end-to-end per D14).

## Acceptance criteria

- [ ] Every listed column is ciphertext at rest (DB test)
- [ ] All `journal.*` rows have `model_input_ok = false`
- [ ] Agents role can read only `journal.llm_safe_summary`
- [ ] Log redaction proven by test
- [ ] CI green (lint, types, tests, `pit` check; `tax-golden` once P3-T045 lands)

## Exceptions & edge cases

- Hash of raw payload is computed on plaintext before encryption (so duplicates are detected without decrypting).
- Key rotation: old rows keep their `key_id`; decrypt picks the right key.

## Cardinal rules (do NOT)

- Do NOT log decrypted values; do NOT add decrypt grants to any role other than `journal`.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT expose tax-sensitive fields (TFN, addresses, raw statements) to any LLM prompt, RAG index or the LiteLLM gateway ([07 §8](../../../docs/07-security-notes.md#8-data-protection-backups--audit)).
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set (12 §4–5).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/07-security-notes.md` §8: list the encrypted columns and `journal.llm_safe_summary`.
- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.41 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T007-column-encryption-prompt-exclusion`
- PR title: `P3-T007: pgcrypto column encryption and prompt exclusion for tax-sensitive fields`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T007` run

## Progress log

- 2026-10-21 00:00 · planner · created
