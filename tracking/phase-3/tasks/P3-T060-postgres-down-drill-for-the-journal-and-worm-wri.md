---
id: P3-T060
kind: task
title: Postgres-down drill for the journal and WORM write path
phase: 3
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T057, P3-T013, P3-T009]
requirements: [R3.N3, R3.01, R3.02]
roadmap_todos: [T3.67]
modules: [M18, M17, M11]
dashboards: [D14, D16]
tools: [git, uv, docker, nats]
mcp: []
env: []
services: [postgres, nats, journal, engine, grafana]
branch: p3/P3-T060-postgres-down-drill-for-the-journal-and-worm-wri
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

# P3-T060 · Postgres-down drill for the journal and WORM write path

## Goal / expected outcome

A recorded drill on the staging stack with paper trading proves R3.N3: with Postgres stopped, journal and WORM writes buffer in JetStream; at 80% of the bound new entries stop while exits continue; and on recovery every buffered record lands exactly once with a verifying hash chain.

## Context & references

- Roadmap: [R3.N3, T3.67](../../../docs/roadmap/phase-3-journal-and-tax.md)
- Defaults: [16 §3.3](../../../docs/16-configuration-and-safety-model.md#33-records-the-write-path-vs-the-integrity-check) (1 GB or 24 h; new entries stop above 80%; exits continue; nothing executes without a record) · [02 §9.3](../../../docs/02-v1-architecture.md#93-degraded-modes)
- Under test: P3-T057 (stream, buffer library, M11 hook), P3-T013 (fills → journal), P3-T009 (journal consumers)
- Related: P3-T052 (general stress; this drill is the bound-specific one)

## Requirements

- Staging compose with the paper engine running a test bot on a testnet/sandbox venue (no money), the journal consumer and Grafana.
- Use a **test settings profile** with small bounds (e.g. 50 MB / 30 min) so 80% is reachable in minutes; production defaults remain 1 GB / 24 h.
- Steps: (1) baseline counts (`audit.fill`, `journal.event`, `seq` per chain); (2) stop Postgres; (3) generate fills and synthetic WORM writes until the buffer passes 80%; (4) attempt a new entry → rejected `worm_buffer_high`; trigger a protective stop/reduce-only close → executes and is buffered; (5) start Postgres; (6) wait for drain; (7) compare counts and run `audit.verify`.
- Pass: zero lost or duplicated records; `seq` contiguous; verify clean; alerts `worm_buffering`, `worm_buffer_high` observed on Telegram/ntfy/UI; UI red banner + read-only during the outage.
- Runbook section from P3-T057 followed as written; timings recorded.

## ToDo

- [ ] Script the drill `tests/chaos/journal/postgres_down_drill.py`
- [ ] Run it; capture Grafana screenshots, alert receipts and counts
- [ ] Record results and timings in the progress log; file bugs for deviations

## Verification

### Tests
- Automated assertions: counts before/after, duplicate check on idempotency keys, `seq` gaps = 0, `audit.verify` exit 0, M11 reason codes.

### Scenarios
- Given Postgres is down and the buffer is at 85%, when a strategy sends a new entry, then it is rejected while a protective exit executes and is recorded after recovery.
- Given Postgres returns, when the drainer finishes, then D14 shows every fill from the outage exactly once.

### Stress / failure injection
- This item is the failure injection for R3.N3; also kill the drainer once mid-drain.

## Acceptance criteria

- [ ] New entries stopped at ≥ 80% and exits continued
- [ ] Every buffered record landed exactly once; chain verifies
- [ ] Alerts and banner observed; results in the progress log

## Exceptions & edge cases

- If NATS itself is down too, the engine refuses new entries and spills exits locally (P3-T057); a variant of the drill covers this.

## Cardinal rules (do NOT)

- Do NOT run the drill against production data or with real money.
- Do NOT change production buffer defaults to make the drill faster; use the test profile.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT UPDATE or DELETE WORM rows; corrections are new rows ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.67 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T060-postgres-down-drill-for-the-journal-and-worm-wri`
- PR title: `P3-T060: Postgres-down drill for the journal and WORM write path`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T060` run

## Progress log

- 2026-10-22 00:00 · aligner · created for R3.N3/T3.67 (docs/16–17 alignment)
