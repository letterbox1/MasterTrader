---
id: P2-T059
kind: task
title: Degraded-mode tests for risk, execution and Telegram
phase: 2
type: VERIFY
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T035, P2-T017, P2-T027, P2-T070, P1-T057]
requirements: [R2.52, R2.16, R2.32]
roadmap_todos: [T2.33]
modules: [M11, M12, M15]
dashboards: []
tools: [uv, docker]
mcp: []
env: []
services: [nats, postgres]
branch: p2/P2-T059-verify-degraded-modes
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T059 · Degraded-mode tests for risk, execution and Telegram

## Goal / expected outcome

Fault-injection tests prove the 02 §9.3 / 16 §2–§3 behaviours relevant to Phase 2: stale data is rejected inline on every order and the monitor pauses strategies, venue disconnect → unknown → reconcile, Postgres down → bounded JetStream buffer and the layer-1 dead-man, WORM verify mismatch → `block_new_entries`, egress mismatch → new orders blocked, mt-api down → Telegram `/kill` still works.

## Context & references

- Roadmap: [R2.52, R2.16](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.33
- Degraded modes: [02 §9.3](../../../docs/02-v1-architecture.md#93-degraded-modes) · [SPEC NN3](../../../SPEC.md#non-negotiable-requirements)
- Cross-phase (`depends_on`): DQ fault-injection tooling (P1-T057, T1.61).
- Defaults: [16 §2.2](../../../docs/16-configuration-and-safety-model.md#22-data-freshness-what-stale-means) (inline data age; monitor flips `dq.status` ≤ 250 ms p99 after the threshold) · [16 §3.3](../../../docs/16-configuration-and-safety-model.md#33-records-the-write-path-vs-the-integrity-check) (buffer 1 GB / 24 h; above 80% new entries stop) · [16 §2.11](../../../docs/16-configuration-and-safety-model.md#211-worm-integrity) · [16 §3.2](../../../docs/16-configuration-and-safety-model.md#32-network-egress-and-ip-locked-keys).
- Related: P2-T070/P2-T076 (safety-state checks and goldens), P2-T075 (engine down), gap P2-B015 (Postgres-down wording differs between 02 §9.3 and 16 §3.1).

## Requirements

- Stale feed (stop a P1 feed) → the next order on that instrument is rejected inline (data older than the bot's threshold, default 2 s fast / 60 s slow) and the ladder holds; the monitor flips `dq.status=stale` within 250 ms p99 of the threshold and strategies pause; exits still allowed.
- Bad tick injection → `bad` → hold.
- Venue disconnect (iptables drop) → orders `unknown` → reconcile on reconnect, positions 'unconfirmed' meanwhile.
- Postgres stop → engine keeps risk limits in memory, audit buffered to JetStream (bound 1 GB / 24 h; above 80% new entries stop, exits continue; nothing executes without a record); the layer-1 watchdog treats the DB heartbeat per 16 §3.1 (5 s / 10 s); on restore, audit flushed in order with hash chain intact.
- WORM verify mismatch injected (`audit.integrity = block_new_entries`) → new entries rejected, exits and protective orders pass; `halt_all` stops everything.
- Egress status mismatch injected → new orders blocked + alert.
- mt-api stop → `/kill` via NATS (`kill.set` only) works and the engine writes the WORM kill event with source `telegram`; web unreachable.

## ToDo

- [ ] Toxiproxy/iptables fault scripts
- [ ] Test cases per row
- [ ] Report
- [ ] Record results (numbers, run IDs, screenshots) in the progress log and tick the roadmap ToDo box

## Verification

### Tests
- Each degraded row as an automated e2e test on the compose test stack.

### Scenarios
- Given Postgres stops for 30 s (< N), when fills occur, then they are written after restore with a valid hash chain and no gaps.

### Stress / failure injection
- Combined: feed stale + venue disconnect at once; system holds and recovers without duplicates.

## Acceptance criteria

- [ ] Every row passes and is automated
- [ ] Hash chain verified after Postgres outage

## Exceptions & edge cases

- Postgres outage longer than the 5 s layer-1 threshold: test asserts the dead-man path (cancel, then `on_system_failure`).

## Cardinal rules (do NOT)

- Do NOT treat a hold as a failure to be retried around; holds are the intended behaviour.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11, whatever its source.
- Do NOT skip, weaken or delete a test to get green; risk-manager golden tests are mandatory for merge.
- Do NOT UPDATE or DELETE WORM rows (`audit.*`, `risk.change`, `risk.approval`, `strategy.bot_version`); corrections are new rows with `supersedes_id` (15 §2).

## Doc sync on completion

- `docs/02-v1-architecture.md` §9.3: link tests per row.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.33 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T059-verify-degraded-modes`
- PR title: `P2-T059: Degraded-mode tests for risk, execution and Telegram`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T059` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (inline data age + 250 ms monitor flip, buffer bounds, integrity and egress rows, kill.set-only NATS path)
