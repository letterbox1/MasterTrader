---
id: P0-T037
kind: task
title: Implement the daily Merkle seal with external anchoring
phase: 0
type: BUILD
status: backlog
priority: critical
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T031, P0-T022, P0-T006, P0-T002]
requirements: [R0.07]
roadmap_todos: [T0.23]
modules: [M17]
dashboards: []
branch: p0/P0-T037-daily-merkle-seal-external-anchor
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

# P0-T037 · Implement the daily Merkle seal with external anchoring

## Goal / expected outcome

A Prefect flow runs daily (00:15 UTC) and writes, per WORM table per UTC day, a Merkle root over that day's `row_hash`es into `audit.seal`, then anchors the seal outside the database: (1) an object in the Object-Locked `mt-worm-seal` bucket (or append-only rest-server), (2) an optional OpenTimestamps proof, (3) a Telegram witness message to you.

## Context & references

- [Roadmap P0 R0.07](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [15 §2.2 layers](../../../docs/15-bots-hitl-and-worm-audit.md#22-layers) (Daily seal)
- [07 §8 backups & audit](../../../docs/07-security-notes.md#8-data-protection-backups--audit)
- Related: P0-T006 (bucket), P0-T002 (bot), P0-T038 (consumes seals)
- Depends on: P0-T031, P0-T022, P0-T006, P0-T002

## Requirements

- Merkle tree: leaves = `row_hash` ordered by `(chain_id, seq)`; SHA-256; odd leaf duplicated; empty day → root = sha256("empty"‖table‖date). Also records `first_seq`, `last_seq`, `row_count`, `last_row_hash` per chain.
- `audit.seal` row (WORM, chained): `table_name`, `day`, `merkle_root`, chain summaries (jsonb), `anchor_s3_key`, `anchor_s3_version_id`, `ots_proof` (bytea, nullable), `telegram_message_id`, `sealed_at`.
- Anchor object `seals/<table>/<YYYY>/<MM>/<DD>.json` with the seal JSON (canonical) uploaded with Object Lock retention ≥ 2557 days; upload verified by re-download + hash compare; version id recorded.
- OpenTimestamps (free, optional, `ots_enabled` setting): `ots stamp` the seal file hash; upgrade proofs after ~24 h in the next run.
- Telegram witness: one message per day listing `table: root[:16]… rows` + link-free text; sent with the bot token from tmpfs to `owner_chat_id`; message id stored.
- The seal for day D runs only after D closes (UTC) and waits for late inserts with a 10 min grace; rows inserted for D after sealing are counted into D+1's chain summary and flagged (`late_rows`).
- Never on the order path: sealing reads replicas of data via `mt_flows_rw` with `statement_timeout` 5 min; inserts never wait on seals (15 §2.4).
- Failure handling: any anchor step failing → seal row still written with `anchor_status=partial`, alert `alert.critical.seal_anchor_failed`, retry hourly for 24 h.

## ToDo

- [ ] Implement `mt_obs.worm.merkle` (pure Python, tested) and the Prefect flow `seal_daily`.
- [ ] Implement S3 (boto3, B2 endpoint) and rest-server uploaders behind one `AnchorStore` interface.
- [ ] Implement the OTS step (opentimestamps-client pinned) behind a flag.
- [ ] Implement the Telegram witness via Bot API `sendMessage` (httpx, no bot framework yet).
- [ ] Schedule in Prefect; expose last seal status to `/system/backups` and D16 Audit.
- [ ] Tests below.

## Verification

### Tests
- Unit: Merkle root golden vectors (1, 2, 3, 1000 leaves); empty-day root.
- Integration (MinIO with object lock in CI as B2 stand-in): seal object written with retention; delete attempt fails; version id stored.
- Integration: Telegram call mocked (respx) → message id stored; failure → `partial` + alert.

### Scenarios
- Given B2 is unreachable at 00:15, then the seal row is `partial`, an alert fires, and the hourly retry anchors it later the same day.
- Given a row for yesterday arrives at 00:20 (after sealing), then it is flagged `late_rows` in today's seal and verify does not report a mismatch.

### Stress / failure injection
- Seal 5 M rows/day for one table in < 2 min on the host; inserts into `audit.command` during sealing keep p99 < 5 ms (provisional, P0-B004).

## Acceptance criteria

- [ ] Daily seal rows for every registered WORM table
- [ ] Anchor object present with compliance retention and recorded version id
- [ ] Telegram witness received for a real day (log)
- [ ] Partial-anchor path alerts and retries (tested)
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- OTS calendars down: skip with `ots_status=pending`; never block the seal.
- Telegram rate limits: one message per day, so never near 30 msg/s.

## Cardinal rules (do NOT)

- Do NOT store the only copy of seals in the database.
- Do NOT use Object Lock governance mode for seals.
- Do NOT put any Telegram text into models (witness is outbound only).
- Do NOT UPDATE or DELETE WORM rows, ever; corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT put Telegram text into any model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/15-bots-hitl-and-worm-audit.md` §2.2: document object key layout, grace period and `late_rows`.
- `docs/roadmap/phase-0-foundations.md`: tick T0.23 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T037-daily-merkle-seal-external-anchor`
- PR title: `P0-T037: Implement the daily Merkle seal with external anchoring`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T037` run

## Progress log

- 2026-10-21 00:00 · planner · created
