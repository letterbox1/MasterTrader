---
id: P3-T057
kind: task
title: JetStream buffer bounds for the journal and WORM write path
phase: 3
type: OPS
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T008, P0-T020, P0-T031, P1-T004, P2-T017]
requirements: [R3.N3, R3.02]
roadmap_todos: [T3.42]
modules: [M18, M17, M11, nats]
dashboards: [D16]
tools: [git, uv, docker, nats]
mcp: []
env: []
services: [nats, postgres, grafana, alertmanager]
branch: p3/P3-T057-jetstream-buffer-bounds-for-the-journal-and-worm
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/15-bots-hitl-and-worm-audit.md, docs/roadmap/phase-3-journal-and-tax.md]
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

# P3-T057 · JetStream buffer bounds for the journal and WORM write path

## Goal / expected outcome

When Postgres is unreachable, journal and WORM writes buffer in a bounded NATS JetStream stream (default **1 GB or 24 h**, configurable), the buffer level is published so M11 stops **new entries above 80%** while exits and protective orders continue, an alert fires, and on recovery every buffered record lands exactly once. Nothing executes without a record.

## Context & references

- Roadmap: [R3.N3, T3.42](../../../docs/roadmap/phase-3-journal-and-tax.md) · drill P3-T060 (T3.67)
- Defaults: [16 §3.3](../../../docs/16-configuration-and-safety-model.md#33-records-the-write-path-vs-the-integrity-check) · decision [17 §C P3-B015](../../../docs/17-decisions-register.md#c-defaults-that-were-n-or-unspecified)
- Architecture: [02 §5.1 stores](../../../docs/02-v1-architecture.md#51-stores) (JetStream bound) · [02 §9.3 degraded modes](../../../docs/02-v1-architecture.md#93-degraded-modes) (Postgres down row) · [15 §2 write path](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many) (insert p99 < 5 ms; never waits on seals)
- Setting surface: D16 Settings → Failure behaviour (NATS buffer bound) [D16](../../../docs/ui/dashboards/D16-system.md)
- Cross-phase prerequisites (depends_on): P0-T020 (nats JetStream in compose), P0-T031 (P0 WORM audit tables and writers), P1-T004 (P1 JetStream streams and limits conventions), P2-T017 (default-deny pre-trade RiskGate that reads KV status)
- Related: P3-T008 (journal writer acks only after commit), P3-T009 (journal container consumers), P3-T060 (drill)

## Requirements

- Stream `WORM_BUFFER` (subjects `worm.buffer.>`, file storage, `max_bytes` = 1 GB, `max_age` = 24 h, discard policy **new** so nothing already buffered is evicted); limits read from the L1 system policy setting `failure.worm_buffer` (defaults from 16 §3.3), never constants.
- Writer library `mt_store.worm.buffer`: when a WORM insert (`audit.*`, `journal.*`) fails with a connection-class error, the canonical row (with its idempotency key) is published to `worm.buffer.<table>` and the caller gets "recorded (buffered)"; a drainer replays in order per chain on recovery, idempotent on the key, so the hash chain is built at insert time with no gaps.
- Buffer level → NATS KV `worm_buffer` {`bytes_used`, `age_s`, `ratio`, `state`: `ok` | `buffering` | `high` | `full`}; `high` at ≥ 80% of either bound (default).
- M11 pre-trade hook: `state ∈ {high, full}` → reject new entries with reason `worm_buffer_high`; reduce-only exits and protective orders always pass. Mirrors how M11 reads KV `audit.integrity`.
- If the buffer itself cannot accept a record (`full` or NATS down) → the order path refuses new entries (nothing executes without a record); exits still go out and are recorded in the engine's local spill file, replayed first on recovery.
- Alerts via the single `alert.*` path: `alert.warning.worm_buffering` when buffering starts, `alert.critical.worm_buffer_high` at 80%, `alert.critical.worm_buffer_full`; Grafana panel for level, age and drain rate.
- Loosening the bound (bigger/longer) is a loosening of L1 failure policy → C3; tightening is immediate (16 §1).

## ToDo

- [ ] Stream + KV bucket definitions in `infra/nats/streams/worm_buffer.json` (bounds templated from settings)
- [ ] `packages/mt_store/worm/buffer.py` (publish on failure, drainer, idempotency) used by the journal writer and the P0 audit writers
- [ ] KV status publisher + M11 hook `packages/mt_risk/checks/worm_buffer.py` with reason code
- [ ] Setting `failure.worm_buffer` wired to D16 Settings (`system.settings.update`; loosen = C3)
- [ ] Grafana panel + alert rules; runbook section "Postgres down: write-path buffer" in `docs/runbooks/`
- [ ] Unit + integration tests; docs

## Verification

### Tests
- Unit: connection error on insert → record published to `worm.buffer.<table>`; other errors (constraint, WORM trigger) are **not** buffered and surface as errors.
- Unit (M11): `worm_buffer.state = high` → new entry rejected; reduce-only close passes.
- Integration: stop Postgres, write 10k journal events, start Postgres → drainer lands all 10k once, hash chain verifies (`audit.verify`).

### Scenarios
- Given Postgres is down, when a fill arrives, then it is buffered, the UI shows the red banner and read-only mode, and the fill appears in the journal once Postgres returns.
- Given the buffer reaches 80% of 1 GB, when a strategy sends a new entry, then M11 rejects it with `worm_buffer_high` while a protective stop still executes.
- Given you raise the bound to 2 GB, when saved, then a C3 approval is required before it applies.

### Stress / failure injection
- Fill the buffer synthetically to 79%, 80% and 100% (small test bounds, e.g. 10 MB / 10 min) → state transitions and alerts at each step; discard-new never evicts buffered rows.
- Kill the drainer mid-replay 3× → no duplicates, no gaps in `seq`.

## Acceptance criteria

- [ ] Bounded stream live with defaults 1 GB / 24 h from settings
- [ ] M11 stops new entries at ≥ 80% (default) and never blocks exits
- [ ] Every buffered record lands exactly once after recovery; chain verifies
- [ ] Alerts and Grafana panel provisioned; runbook section written
- [ ] CI green (lint, types, tests, `pit` check)

## Exceptions & edge cases

- Postgres flaps (up/down every few seconds) → drainer backs off; ordering per chain preserved.
- Clock: `age_s` uses the host monotonic clock (chrony-synced), not message timestamps.
- Disk for JetStream nearly full before 1 GB → the host disk alert (P1 storage alerts) fires; the stream refuses new data rather than corrupting.

## Cardinal rules (do NOT)

- Do NOT execute any order without a record (buffered or written).
- Do NOT block protective exits or reduce-only orders because of the buffer.
- Do NOT evict or drop buffered records (discard policy must be `new`).
- Do NOT hard-code the 1 GB / 24 h / 80% values; read the configured defaults ([16 §3.3](../../../docs/16-configuration-and-safety-model.md#33-records-the-write-path-vs-the-integrity-check)).
- Do NOT UPDATE or DELETE `journal.*` / `audit.*` (WORM) rows; corrections are new rows ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test to get green; pin images by digest.

## Doc sync on completion

- `docs/02-v1-architecture.md` §6: add the `worm.buffer.>` subjects and KV `worm_buffer` (M11 reads it pre-trade).
- `docs/15-bots-hitl-and-worm-audit.md` §2: name the stream and the drainer behaviour.
- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.42 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T057-jetstream-buffer-bounds-for-the-journal-and-worm`
- PR title: `P3-T057: JetStream buffer bounds for the journal and WORM write path`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T057` run

## Progress log

- 2026-10-22 00:00 · aligner · created for R3.N3/T3.42 (docs/16–17 alignment; implementation owner for P3-B015)
