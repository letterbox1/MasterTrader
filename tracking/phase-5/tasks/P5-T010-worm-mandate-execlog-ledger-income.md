---
id: P5-T010
kind: task
title: WORM tables: mandates, exec log and signer ledger
phase: 5
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P5-T009, P0-T029, P0-T030, P0-T037]
requirements: [R5.02, R5.15]
roadmap_todos: [T5.20, T5.28]
modules: [M4, M22, M18, M17]
dashboards: []
tools: [uv, docker]
mcp: []
env: []
services: [postgres]
branch: p5/P5-T010-worm-mandate-execlog-ledger-income
pr: ""
doc_sync: [docs/15-bots-hitl-and-worm-audit.md, docs/02-v1-architecture.md, docs/roadmap/phase-5-airdrops-wallets-curation.md]
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

# P5-T010 · WORM tables: mandates, exec log and signer ledger

## Goal / expected outcome

`curation.mandate`, `curation.exec_log` and `audit.signer_ledger` exist as WORM tables on the P0 WORM layer (owner role, blocking triggers, per-row hash chain, daily seal), with "current state" views, and pass the 15 §2.4 test set. Airdrop income is **not** a separate table: it is a `journal.event` row (P3 WORM table) linked to the campaign record, written by P5-T046 ([08 data model](../../../docs/08-airdrops-and-token-launches.md#data-model-postgres)).

## Context & references

- Roadmap: R5.02 (ledger of signatures), R5.15 (mandates) · ToDos T5.20, T5.28
- WORM design: [15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many) — scope explicitly lists `curation.mandate`, `curation.exec_log` and the signer's signature ledger
- P0 WORM layer: P0-T029 (privileges and blocking triggers), P0-T030 (per-row hash chain), P0-T037 (daily seal); the test pattern follows P0-T055
- Journal: airdrop income goes to `journal.event` (P3), owned by P5-T046; the signer ledger name `audit.signer_ledger` follows the singular `audit.*` naming (17 §B) and still needs to be written into 15 §2.1 / 02 §5

## Requirements

- `curation.mandate`: mandate_id, wallet_id, chain, allowed `(contract, selector)` list, value cap (always 0 for claims), gas cap/tx, max tx/day, valid_from, expires_at, created_by command id, `supersedes_id`, `status_event` ∈ created/revoked/expired; status is derived by view `curation.mandate_current` (latest row per mandate_id).
- `curation.exec_log`: intent id, opportunity id, mandate id, cost-gate quote id, simulation digest (balance diff JSON + hash), signer ledger ref, tx hash, outcome, journal event ref.
- `audit.signer_ledger`: signature id, wallet, chain, intent id + intent hash, decoded call summary, raw tx hash, simulation ref, caps snapshot, refusal reason (refusals are logged too).
- Retention ≥ 7 years; no `ON DELETE CASCADE` reaches these tables; inserts on the claim path never wait for seals.

## ToDo

- [ ] Alembic migrations (run as `worm_owner` from the offline secret) creating the three tables, registering them with the hash-chain trigger and daily seal job.
- [ ] Grant app roles INSERT/SELECT only; add BEFORE UPDATE/DELETE/TRUNCATE exception triggers.
- [ ] Create `*_current` views (latest row per key) used by APIs.
- [ ] Write repository functions in `mt_store` that only expose `append()`/`query()` (no update API).
- [ ] Extend the WORM test suite with these three tables.
- [ ] Update 15 §2.1 table names if they changed.

## Verification

### Tests
- Integration: UPDATE, DELETE, TRUNCATE by the app role fail on each table (15 §2.4).
- Integration: a direct edit as `worm_owner` is detected by `audit.verify`.
- Unit: revoking a mandate appends a `revoked` row and `mandate_current` reflects it; the original row is unchanged.
- Benchmark: 1,000 exec_log inserts/s with hashing stay within the P0 insert SLO (WORM insert p99 < 5 ms, 17 §D P0-B004).

### Scenarios
- Given an active mandate, when the user revokes it, then a new row with `supersedes_id` is written and the executor sees `revoked` on its next read.
- Given a mis-recorded exec_log outcome, when corrected, then a correction row supersedes it and both remain visible to audit.

### Stress / failure injection
- Concurrent inserts from 4 writers on one chain keep `seq` gap-free (advisory lock) — run 10k inserts.

## Acceptance criteria

- [ ] Three WORM tables live with chain + seal
- [ ] 15 §2.4 tests pass for all three
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

- `docs/15-bots-hitl-and-worm-audit.md` §2.1 and `docs/02-v1-architecture.md` §5: name the signer ledger table `audit.signer_ledger`.
- `docs/roadmap/phase-5-airdrops-wallets-curation.md`: tick T5.20, T5.28 when this lands (with the other tasks sharing that ToDo).

## Branch & PR

- Branch: `p5/P5-T010-worm-mandate-execlog-ledger-income`
- PR title: `P5-T010: WORM tables: mandates, exec log and signer ledger`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P5-T010` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (no separate airdrop income table: income is `journal.event` per 08 data model, owned by P5-T046; P0 WORM deps added)
