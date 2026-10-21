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
depends_on: [P2-T035, P2-T017, P2-T027]
requirements: [R2.52, R2.16, R2.32]
roadmap_todos: [T2.33]
modules: [M11, M12, M15]
dashboards: []
branch: p2/P2-T059-verify-degraded-modes
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T059 · Degraded-mode tests for risk, execution and Telegram

## Goal / expected outcome

Fault-injection tests prove the 02 §9.3 behaviours relevant to Phase 2: stale/bad feed pauses strategies, venue disconnect → unknown → reconcile, Postgres down → engine continues with risk limits then dead-man, mt-api down → Telegram `/kill` still works.

## Context & references

- Roadmap: [R2.52, R2.16](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.33
- Degraded modes: [02 §9.3](../../../docs/02-v1-architecture.md#93-degraded-modes) · [SPEC NN3](../../../SPEC.md#non-negotiable-requirements)
- Cross-phase: DQ fault injection tooling (P1 T1.61).

## Requirements

- Stale feed (stop a P1 feed) → `dq.status=stale` → new entries held within 2 s; exits still allowed.
- Bad tick injection → `bad` → hold.
- Venue disconnect (iptables drop) → orders `unknown` → reconcile on reconnect, positions 'unconfirmed' meanwhile.
- Postgres stop → engine keeps trading within limits, audit buffered to JetStream, dead-man after N s; on restore, audit flushed in order with hash chain intact.
- mt-api stop → `/kill` via NATS works; web unreachable.

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

- Dead-man N shorter than the Postgres test outage: test asserts the dead-man path instead.

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
