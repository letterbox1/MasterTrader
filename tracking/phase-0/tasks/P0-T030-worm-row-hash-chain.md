---
id: P0-T030
kind: task
title: Implement the per-row hash chain trigger and canonical JSON
phase: 0
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T029]
requirements: [R0.07]
roadmap_todos: [T0.23]
modules: [M17, mt_store]
dashboards: []
branch: p0/P0-T030-worm-row-hash-chain
pr: ""
doc_sync: [docs/15-bots-hitl-and-worm-audit.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P0-T030 · Implement the per-row hash chain trigger and canonical JSON

## Goal / expected outcome

Every WORM row carries `chain_id`, `seq`, `prev_hash`, `row_hash = sha256(prev_hash ‖ canonical_json(row))` computed in a `BEFORE INSERT` trigger serialised per chain with an advisory lock, and a Python reference implementation (`mt_store.worm.canonical_json`, `recompute_chain`) produces byte-identical hashes for verification.

## Context & references

- [Roadmap P0 R0.07](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [15 §2.2 layers](../../../docs/15-bots-hitl-and-worm-audit.md#22-layers) (Row hash chain)
- [07 §8 backups & audit](../../../docs/07-security-notes.md#8-data-protection-backups--audit)
- [03 M17](../../../docs/03-build-spec.md#m17-observability--audit--mt_obs)
- Related: P0-T029, P0-T038 (uses `recompute_chain`)
- Depends on: P0-T029

## Requirements

- Columns added by the helper: `chain_id text NOT NULL`, `seq bigint NOT NULL`, `prev_hash bytea NOT NULL`, `row_hash bytea NOT NULL`, `recorded_at timestamptz NOT NULL DEFAULT clock_timestamp()`; `UNIQUE (chain_id, seq)`.
- Trigger `worm_chain()` (plpgsql, `pgcrypto` `digest()`): `pg_advisory_xact_lock(hashtext(table||chain_id))`, reads the chain head from `audit.chain_head` (WORM-exempt internal table updated only by the trigger function, `SECURITY DEFINER`) or the last row, sets `seq = head.seq + 1`, `prev_hash = head.row_hash` (genesis = 32 zero bytes), computes `row_hash`.
- **Canonical JSON** (spec written in `packages/mt_store/WORM_CANONICAL.md`): keys sorted, UTF-8, no whitespace, `numeric` as decimal strings without exponent, `timestamptz` as UTC `YYYY-MM-DDTHH:MM:SS.ffffffZ`, `bytea` hex, NULL as `null`, booleans lowercase; excludes `row_hash` itself; includes `chain_id`, `seq`, `prev_hash`, `recorded_at`.
- Timestamps from `clock_timestamp()` on a chrony-synced host (15 §2.2).
- Python: `canonical_json(row: Mapping) -> bytes`, `row_hash(prev, row)`, `recompute_chain(rows) -> list[Mismatch]` — must match SQL byte-for-byte (golden vectors committed under `tests/worm/vectors/`).
- Chain granularity: one chain per table by default; tables may declare a chain key (e.g. per `source`) to reduce lock contention.

## ToDo

- [ ] Implement `worm_chain()` and `audit.chain_head`; attach via `create_worm_table()`.
- [ ] Write `WORM_CANONICAL.md` (the spec) and the Python reference.
- [ ] Generate golden vectors from SQL and assert Python equality (and vice versa).
- [ ] Concurrency test: 16 writers × 5k rows into one chain → contiguous `seq`, valid chain.

## Verification

### Tests
- Golden: SQL vs Python hashes equal for 50 vectors covering numeric precision, unicode, NULLs, timestamps at µs.
- Property (hypothesis): random rows → Python recompute equals stored `row_hash`.
- Concurrency: no gaps or duplicate `seq` under 16 parallel writers; chain verifies.

### Scenarios
- Given a row's payload is altered by a superuser with triggers disabled, when `recompute_chain` runs, then the first altered `seq` is reported and every later row mismatches too.
- Given a transaction inserting into the chain rolls back, then `seq` has no gap (head updated in the same transaction).

### Stress / failure injection
- Throughput: ≥ 1,000 inserts/s sustained into one chain with p99 insert latency < 5 ms on the host (provisional target; see P0-B004); results logged for P0-T059.

## Acceptance criteria

- [ ] Trigger + chain head + Python reference implemented
- [ ] Golden and property tests pass (SQL ≡ Python)
- [ ] Concurrency test passes
- [ ] Throughput numbers logged against the provisional target
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- Clock jump backwards: `recorded_at` may be non-monotonic; ordering is by `seq`, never by time.
- Large `jsonb` payloads: canonicalise with sorted keys recursively; arrays keep order.

## Cardinal rules (do NOT)

- Do NOT compute hashes in the application only (the trigger is authoritative).
- Do NOT change the canonical JSON spec without a versioned migration and a new chain epoch.
- Do NOT UPDATE or DELETE WORM rows, ever; corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/15-bots-hitl-and-worm-audit.md` §2.2: link `WORM_CANONICAL.md` from the Row hash chain row.
- `docs/roadmap/phase-0-foundations.md`: tick T0.23 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T030-worm-row-hash-chain`
- PR title: `P0-T030: Implement the per-row hash chain trigger and canonical JSON`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T030` run

## Progress log

- 2026-10-21 00:00 · planner · created
