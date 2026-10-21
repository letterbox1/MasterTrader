---
id: P2-T167
kind: task
title: Lab failure injection and load test
phase: 2
type: VERIFY
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T114, P2-T115, P2-T116, P2-T117]
requirements: [R2.40, R2.44, R2.45]
roadmap_todos: [T2.27]
modules: [M7]
dashboards: [D04]
branch: p2/P2-T167-verify-lab-failure-injection
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T167 · Lab failure injection and load test

## Goal / expected outcome

Evidence that the lab degrades safely: worker crashes, MLflow/Postgres/NATS/gateway outages and resource exhaustion never produce a false 'pass', never lose results, and never affect the trading engine.

## Context & references

- Roadmap: [R2.40, R2.44, R2.45](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.27
- [02 §9.3 degraded modes](../../../docs/02-v1-architecture.md#93-degraded-modes) (LLM gateway/budget exhausted → local models; Postgres down)

## Requirements

- Injections: kill `backtest-worker` mid-validation; stop MLflow 10 min; stop Postgres 2 min; drop NATS 30 s; exhaust the `lab-review`/`strategy-gen` gateway budget; fill `/tmp` in the worker; run 3 sweeps + 2 validations + 1 generation concurrently.
- Expected: jobs re-queued or failed with reason; no duplicate result rows; MLflow sync resumes; gates never 'pass' on missing sections; gateway falls back to local model and reports it; engine heartbeat and order path p99 unaffected (part A metrics).
- Load: 20 concurrent jobs with 4 workers on the host for 2 h without OOM; CPU isolation keeps engine cores free.

## ToDo

- [ ] Write chaos scripts (`tests/chaos/lab_*.sh`) using `docker compose stop/kill`
- [ ] Run, collect metrics, record results
- [ ] File bugs for any false pass or data loss

## Verification

### Tests
- Chaos suite (manual/nightly-weekly) with assertions on DB state after each injection.

### Scenarios
- Given MLflow down during a sweep, then trials still count in `strategy.trial` and sync later.
- Given the worker is OOM-killed, then the job is re-queued once and then failed with 'OOM' rather than looping.

### Stress / failure injection
- As listed in Requirements (this item is the stress test).

## Acceptance criteria

- [ ] No false pass, no lost results across all injections
- [ ] Engine SLOs unaffected during lab load
- [ ] Results recorded in the progress log

## Exceptions & edge cases

- Re-queue loops capped at 2 attempts per job.

## Cardinal rules (do NOT)

- Do NOT run chaos tests against live accounts; test profile or paper only.
- Do NOT touch live money; keys are trade-only, IP-locked, withdrawals disabled; live waits for the P7 gates.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/03-build-spec.md` M7: degraded behaviour.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.27 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T167-verify-lab-failure-injection`
- PR title: `P2-T167: Lab failure injection and load test`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T167` run

## Progress log

- 2026-10-21 00:00 · planner · created
