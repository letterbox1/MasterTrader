---
id: P5-T010
kind: task
title: WORM tables: mandates, exec log, signer ledger and airdrop income journal
phase: 5
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T009]
requirements: [R5.02, R5.15, R5.18]
roadmap_todos: [T5.20, T5.28, T5.29]
modules: [M4, M22, M18, M17]
dashboards: []
branch: p5/P5-T010-worm-mandate-execlog-ledger-income
pr: ""
doc_sync: [docs/15-bots-hitl-and-worm-audit.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P5-T010 · WORM tables: mandates, exec log, signer ledger and airdrop income journal

## Goal / expected outcome

`curation.mandate`, `curation.exec_log`, `audit.signer_ledger` and `journal.airdrop_income_journal` exist as WORM tables on the P0 WORM layer (owner role, blocking triggers, per-row hash chain, daily seal), with "current state" views, and pass the 15 §2.4 test set.

## Context & references

- Roadmap: R5.02 (ledger of signatures), R5.15 (mandates), R5.18 (income journal) · ToDos T5.20, T5.28, T5.29
- WORM design: [15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many) — scope explicitly lists `curation.mandate`, `curation.exec_log` and the signer's signature ledger
- P0 WORM layer (P0 T0.23 / R0.07) and test suite (P0 T0.61) are cross-phase prerequisites
- Journal: [09](../../../docs/09-journal-and-tax.md) airdrop event types (established vs initial allocation)

## Requirements

- `curation.mandate`: mandate_id, wallet_id, chain, allowed `(contract, selector)` list, value cap (always 0 for claims), gas cap/tx, max tx/day, valid_from, expires_at, created_by command id, `supersedes_id`, `status_event` ∈ created/revoked/expired; status is derived by view `curation.mandate_current` (latest row per mandate_id).
- `curation.exec_log`: intent id, opportunity id, mandate id, cost-gate quote id, simulation digest (balance diff JSON + hash), signer ledger ref, tx hash, outcome, journal event ref.
- `audit.signer_ledger`: signature id, wallet, chain, intent id + intent hash, decoded call summary, raw tx hash, simulation ref, caps snapshot, refusal reason (refusals are logged too).
- `journal.airdrop_income_journal`: event id, campaign record ref, wallet, chain, token, qty, AUD/USD value at receipt with FX/price source and timestamp, classification (`airdrop_established` | `airdrop_initial_allocation` | `staking_reward`), evidence refs.
- Retention ≥ 7 years; no `ON DELETE CASCADE` reaches these tables; inserts on the claim path never wait for seals.

## ToDo

- [ ] Alembic migrations (run as `worm_owner` from the offline secret) creating the four tables, registering them with the hash-chain trigger and daily seal job.
- [ ] Grant app roles INSERT/SELECT only; add BEFORE UPDATE/DELETE/TRUNCATE exception triggers.
- [ ] Create `*_current` views (latest row per key) used by APIs.
- [ ] Write repository functions in `mt_store` that only expose `append()`/`query()` (no update API).
- [ ] Extend the WORM test suite with these four tables.
- [ ] Update 15 §2.1 table names if they changed.

## Verification

### Tests
- Integration: UPDATE, DELETE, TRUNCATE by the app role fail on each table (15 §2.4).
- Integration: a direct edit as `worm_owner` is detected by `audit.verify`.
- Unit: revoking a mandate appends a `revoked` row and `mandate_current` reflects it; the original row is unchanged.
- Benchmark: 1,000 exec_log inserts/s with hashing stay within the P0 insert SLO.

### Scenarios
- Given an active mandate, when the user revokes it, then a new row with `supersedes_id` is written and the executor sees `revoked` on its next read.
- Given a mis-classified income row, when corrected, then a correction row supersedes it and both remain visible to audit.

### Stress / failure injection
- Concurrent inserts from 4 writers on one chain keep `seq` gap-free (advisory lock) — run 10k inserts.

## Acceptance criteria

- [ ] Four WORM tables live with chain + seal
- [ ] 15 §2.4 tests pass for all four
- [ ] No update API exposed in `mt_store`

## Exceptions & edge cases

- Seal job down: inserts continue; the next seal covers the gap; `audit.verify` flags a missing seal day as an incident.
- Clock skew: timestamps from `clock_timestamp()` with chrony; skew > 1 s raises a DQ alert (P1).

## Cardinal rules (do NOT)

- Do NOT add an UPDATE path "for convenience" (status changes are new rows).
- Do NOT store key material or full raw signed transactions with secrets in the ledger.
- Do NOT UPDATE or DELETE WORM rows (`curation.mandate`, `curation.exec_log`, the signer ledger, `journal.*`, `audit.*`); corrections are new rows with `supersedes_id` (15 §2).
- Do NOT commit secrets or paste them into chats, issues or logs; secrets live only in the sops/age file or OpenBao (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/15-bots-hitl-and-worm-audit.md` §2.1: confirm exact table names (`audit.signer_ledger`, `journal.airdrop_income_journal`).
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.20, T5.28, T5.29 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T010-worm-mandate-execlog-ledger-income`
- PR title: `P5-T010: WORM tables: mandates, exec log, signer ledger and airdrop income journal`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T010` run

## Progress log

- 2026-10-21 00:00 · planner · created
