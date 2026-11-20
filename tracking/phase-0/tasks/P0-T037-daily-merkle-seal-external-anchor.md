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
depends_on: [P0-T031]
requirements: [R0.07, R0.N7]
roadmap_todos: [T0.23]
modules: [M17, mt-obs]
dashboards: []
tools: [git, cargo, supabase, docker]
mcp: []
env: []
services: [supabase-postgres, minio]
branch: p0/P0-T037-daily-merkle-seal-external-anchor
pr: ""
doc_sync: [docs/15-bots-hitl-and-worm-audit.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-11-20
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P0-T037 · Implement the daily Merkle seal with external anchoring

## Goal / expected outcome

The `mt-obs seal` job (Rust, [18 §2.1](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates)), scheduled daily (00:15 UTC) by a host timer (`infra/timers/`: a systemd timer on a Linux workstation, the launchd or Task Scheduler equivalent elsewhere; installed by `just timers-install`), writes, per WORM table per UTC day, a Merkle root over that day's `row_hash`es into `audit.seal`, then anchors the seal outside the database: (1) an object in the Object-Locked `mt-worm-seal` bucket (or append-only rest-server), (2) an optional OpenTimestamps proof, (3) a Telegram witness message to you.

## Context & references

- [Roadmap P0 R0.07](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [15 §2.2 layers](../../../docs/15-bots-hitl-and-worm-audit.md#22-layers) (Daily seal)
- [07 §8 backups & audit](../../../docs/07-security-notes.md#8-data-protection-backups--audit)
- Scheduling: a host timer, because P0 needs it before `mt-scheduler` exists and pg_cron can only run SQL inside Postgres, not upload to object storage or call Telegram; P1-T077 moves it onto `mt-scheduler` ([18 §2.1](../../../docs/18-platform-and-deployment.md#21-rust-cargo-workspace-crates), 17 §H). The seal job is idempotent per table and day, so the move is a re-registration only.
- Related: P0-T006 (real bucket), P0-T002 (real bot), P0-T038 (consumes seals), P0-T063 (soak: first real anchors and witnesses)
- Depends on: P0-T031. Build first, keys last: built and tested against MinIO with Object Lock and a mocked Telegram Bot API (no real keys); the real bucket and bot are exercised in the soak (P0-T063).

## Requirements

- Merkle tree: leaves = `row_hash` ordered by `(chain_id, seq)`; SHA-256; odd leaf duplicated; empty day → root = sha256("empty"‖table‖date). Also records `first_seq`, `last_seq`, `row_count`, `last_row_hash` per chain.
- `audit.seal` row (WORM, chained): `table_name`, `day`, `merkle_root`, chain summaries (jsonb), `anchor_s3_key`, `anchor_s3_version_id`, `ots_proof` (bytea, nullable), `telegram_message_id`, `sealed_at`.
- Anchor object `seals/<table>/<YYYY>/<MM>/<DD>.json` with the seal JSON (canonical) uploaded with Object Lock retention ≥ 2557 days; upload verified by re-download + hash compare; version id recorded.
- OpenTimestamps (free, optional, `ots_enabled` setting): `ots stamp` the seal file hash; upgrade proofs after ~24 h in the next run.
- Telegram witness: one message per day listing `table: root[:16]… rows` + link-free text; sent with the bot token from tmpfs to `owner_chat_id`; message id stored.
- The seal for day D runs only after D closes (UTC) and waits for late inserts with a 10 min grace (default, [16 §2.14](../../../docs/16-configuration-and-safety-model.md#214-platform--operations)); rows inserted for D after sealing are counted into D+1's chain summary and flagged (`late_rows`).
- Never on the order path: sealing reads replicas of data via `mt_jobs_rw` with `statement_timeout` 5 min; inserts never wait on seals (15 §2.4).
- Failure handling: any anchor step failing → seal row still written with `anchor_status=partial`, alert `alert.critical.seal_anchor_failed`, retry hourly for 24 h (default, [16 §2.14](../../../docs/16-configuration-and-safety-model.md#214-platform--operations)).

## ToDo

- [ ] Implement `mt_obs::worm::merkle` (pure Rust, tested) and the `mt-obs seal --day` command, wrapped by `just seal`.
- [ ] Implement S3 (`aws-sdk-s3` or `object_store`, B2 endpoint) and rest-server uploaders behind one `AnchorStore` trait.
- [ ] Implement the OTS step (the pinned `opentimestamps-client` CLI in the job image, called as a subprocess) behind a flag.
- [ ] Implement the Telegram witness via Bot API `sendMessage` (`reqwest`, no bot framework yet; `mt-telegram-bot` comes in P1).
- [ ] Schedule it with the host timer `mt-seal` (time from settings, catch-up on missed runs); create `infra/timers/` and `just timers-install` if no other P0 job has yet; expose last seal status to `/system/backups` and D16 Audit.
- [ ] Tests below.

## Verification

### Tests
- `cargo test -p mt-obs merkle`: Merkle root golden vectors (1, 2, 3, 1000 leaves); empty-day root.
- Integration (MinIO with object lock in CI as B2 stand-in): seal object written with retention; delete attempt fails; version id stored.
- Integration: Telegram call mocked (`wiremock`) → message id stored; failure → `partial` + alert.

### Scenarios
- Given B2 is unreachable at 00:15, then the seal row is `partial`, an alert fires, and the hourly retry anchors it later the same day.
- Given a row for yesterday arrives at 00:20 (after sealing), then it is flagged `late_rows` in today's seal and verify does not report a mismatch.

### Stress / failure injection
- Seal 5 M rows/day for one table in < 2 min; inserts into `audit.command` during sealing keep p99 < 5 ms (SLO, [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P0-B004; gated in P0-T066).

## Acceptance criteria

- [ ] Daily seal rows for every registered WORM table
- [ ] Anchor object present with compliance retention and recorded version id
- [ ] Telegram witness delivered to the mocked Bot API with the message id stored (the real-day witness is checked in P0-T063)
- [ ] Partial-anchor path alerts and retries (tested)
- [ ] CI green (clippy, cargo test, ruff, mypy, pytest, `supabase test db`, gitleaks, `pit` check)

## Exceptions & edge cases

- OTS calendars down: skip with `ots_status=pending`; never block the seal.
- Telegram rate limits: one message per day, so never near 30 msg/s.
- Workstation asleep or off at 00:15: the timer runs on wake (`Persistent=true` or the platform equivalent) and the job seals every closed, unsealed day in order.

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
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (keyless: MinIO + mocked Bot API, live anchors/witness move to P0-T063; seals never block inserts (R0.N7); run fields added)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (Merkle seal is Rust in `mt-obs` (Prefect only schedules it); boto3/httpx/respx → aws-sdk-s3/reqwest/wiremock)
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (Prefect removed: the seal runs from a host timer in P0 (pg_cron can't upload or call Telegram; `mt-scheduler` comes in P1-T077, which moves it); role `mt_jobs_rw`; catch-up on missed runs)
