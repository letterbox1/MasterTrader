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
branch: p7/P7-T044-drill-kill-baddata-serverdown
pr: ""
doc_sync: [docs/runbooks/, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-T044 · Drill runbooks: kill, bad data, server down with open positions

## Goal / expected outcome

The kill, bad-data and server-down-with-open-positions runbooks are each drilled end to end with paper positions on the live-shaped setup, timings measured, and results recorded in `ops.drill_log` (entry criterion).

## Context & references

- Roadmap: [R7.06, R7.11 · ToDo T7.60](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Roadmap §2 entry criteria ([phase 7](../../../docs/roadmap/phase-7-prove-and-go-live.md)) · [07 §9](../../../docs/07-security-notes.md#9-monitoring--incident-response) · [02 §8 flows](../../../docs/02-v1-architecture.md#8-end-to-end-flows) F6 · [02 §9.2](../../../docs/02-v1-architecture.md#92-observability--slos) (kill → cancels < 1 s; feed stale → paused < 2 s)
- Cross-phase: P2 T2.61 (kill/dead-man drills on paper) — repeated here on the live configuration.
- Related: P7-T043, P7-T011 (preflight reads the drill log), P7-T045

## Requirements

- Kill: `/kill` from phone → all cancels sent < 1 s, flatten per config, kill OFF via C3 only.
- Bad data: inject a stale/bad feed on a traded instrument → affected strategies paused < 2 s, autonomous bots downgraded, no orders on that instrument; runbook steps (halt auto mandates, switch feeds) followed.
- Server down: stop the host's `engine` + `mt-api` with paper positions open → you flatten via each venue's web UI/terminal following the runbook; resting stops verified present; restart → unconfirmed → recon → confirmed.
- Each drill recorded via `ops.drill.record` with start/end, result, evidence (Grafana snapshot links, redacted screenshots).

## ToDo

- [ ] Schedule a 2-hour drill window; open paper positions on two venues.
- [ ] Run the kill drill; record.
- [ ] Run the bad-data drill (DQ fault injector); record.
- [ ] Run the server-down drill; record.
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
- [ ] Kill cancels < 1 s; DQ pause < 2 s measured.
- [ ] Any failures fixed and re-drilled.

## Exceptions & edge cases

- mt-api down during kill drill: Telegram `/kill` via NATS must still work (02 §9.3).
- A venue UI step changed: update the runbook before recording `pass`.

## Cardinal rules (do NOT)

- Do NOT drill with live money; paper positions only.
- Do NOT record a drill as pass with open follow-ups.
- Do NOT add discretionary overrides; the only manual action outside approve mode is flatten-and-halt with a required reason (14 §4).
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
