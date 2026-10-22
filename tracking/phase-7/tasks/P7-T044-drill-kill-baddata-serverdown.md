---
id: P7-T044
kind: task
title: Drill runbooks: kill, bad data, server down with open positions
phase: 7
type: VERIFY
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T043, P7-T011]
requirements: [R7.06, R7.11]
roadmap_todos: [T7.60]
modules: [M11, M16]
dashboards: [D06, D07, D16]
tools: [git, uv, docker]
mcp: []
env: []
services: [postgres, nats, mt-api, monitor, grafana]
branch: p7/P7-T044-drill-kill-baddata-serverdown
pr: ""
doc_sync: [docs/runbooks/, docs/roadmap/phase-7-prove-and-go-live.md]
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

# P7-T044 · Drill runbooks: kill, bad data, server down with open positions

## Goal / expected outcome

The kill, bad-data and server-down-with-open-positions runbooks are each drilled end to end with paper positions on the live-shaped setup, timings measured, and results recorded in `ops.drill_log` (entry criterion).

## Context & references

- Roadmap: [R7.06, R7.11 · ToDo T7.60](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Roadmap §2 entry criteria ([phase 7](../../../docs/roadmap/phase-7-prove-and-go-live.md)) · [07 §9](../../../docs/07-security-notes.md#9-monitoring--incident-response) · [02 §8 flows](../../../docs/02-v1-architecture.md#8-end-to-end-flows) F6 · [02 §9.2](../../../docs/02-v1-architecture.md#92-observability--slos) (kill → cancels < 1 s) · [16 §2.2](../../../docs/16-configuration-and-safety-model.md#22-data-freshness-what-stale-means) (stale flip ≤ 250 ms p99) · [16 §3.1](../../../docs/16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch) (dead-man, restart flat) · [16 §2.4](../../../docs/16-configuration-and-safety-model.md#24-validation-gates-per-strategy-gate-profile) (safety-drills gate)
- Cross-phase: P2-T054 (kill/dead-man drills on paper), repeated here on the live-shaped configuration.
- Related: P7-T043, P7-T011 (preflight reads the drill log), P7-T045

## Requirements

- Kill: `/kill` from phone → all cancels sent < 1 s; each bot's `on_system_failure` applied; new treasury/earn moves frozen ([17 §B](../../../docs/17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer)); kill OFF via C3 only.
- Bad data: inject a stale/bad feed on a traded instrument → `dq.status` flips ≤ 250 ms p99 after the threshold and M11 rejects orders on it inline (16 §2.2); affected strategies paused, autonomous bots downgraded; runbook steps (halt autonomous bots, switch feeds) followed.
- Server down: stop the host's `engine` + `mt-api` with paper positions open → the `deadman` sidecar cancels within 5 s and applies `on_system_failure` at 10 s (16 §3.1); you check each venue's web UI/terminal following the runbook; resting stops verified present; restart → bots paused → recon → confirmed → you resume (C1).
- Dead-man and restart drills also count for the gate's 'safety drills' (16 §2.4): record them per venue the first bots will trade on.
- Each drill recorded via `ops.drill.record` with start/end, result, evidence (Grafana snapshot links, redacted screenshots).

## ToDo

- [ ] Schedule a 2-hour drill window; open paper positions on two venues.
- [ ] Run the kill drill; record.
- [ ] Run the bad-data drill (DQ fault injector); record.
- [ ] Run the server-down drill (incl. dead-man and restart timings per venue); record.
- [ ] File bugs (P7-B…) for any step that failed or was unclear; update runbooks.

## Verification

### Tests
- Drill evidence: Prometheus timings for cancels and DQ pause; recon result after restart.

### Scenarios
- Given positions on two venues, when the engine is stopped, then you can flatten both from venue UIs within 10 minutes using only the runbook.

### Stress / failure injection
- The drills are the failure injection: process kill, feed corruption, kill-switch path under load (20 open orders).

## Acceptance criteria

- [ ] Three drills recorded as `pass` in `ops.drill_log`.
- [ ] Kill cancels < 1 s; `dq.status` flip ≤ 250 ms p99; sidecar cancel ≤ 5 s and `on_system_failure` ≤ 10 s measured.
- [ ] Any failures fixed and re-drilled.

## Exceptions & edge cases

- mt-api down during kill drill: Telegram `/kill` via NATS must still work (02 §9.3).
- A venue UI step changed: update the runbook before recording `pass`.

## Cardinal rules (do NOT)

- Do NOT drill with live money; paper positions only.
- Do NOT record a drill as pass with open follow-ups.
- Do NOT add discretionary overrides; the only manual trading action outside HITL approvals is flatten-and-halt with a required reason (14 §4).
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/runbooks/`: fixes from the drill.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.60 when this item is done.

## Branch & PR

- Branch: `p7/P7-T044-drill-kill-baddata-serverdown`
- PR title: `P7-T044: Drill runbooks: kill, bad data, server down with open positions`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T044` run · evidence (redacted, no secrets) linked in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (timings per 16 §2.2/§3.1; dead-man + restart drills count for the 16 §2.4 safety-drills gate; kill actions per 17 §B)
