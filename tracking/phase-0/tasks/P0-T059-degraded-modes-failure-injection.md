---
id: P0-T059
kind: task
title: Failure-inject degraded modes and stress the P0 stack
phase: 0
type: VERIFY
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T051, P0-T042, P0-T043, P0-T044, P0-T039, P0-T038, P0-T045]
requirements: [R0.02, R0.07, R0.08, R0.09, R0.10, R0.N7]
roadmap_todos: [T0.41, T0.24, T0.45]
modules: [ops, mt_api, M17, M21]
dashboards: [D16]
tools: [docker, uv, tc]
mcp: []
env: []
services: [postgres, nats, loki, litellm, tei-embed, llm-local, minio]
branch: p0/P0-T059-degraded-modes-failure-injection
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/roadmap/phase-0-foundations.md]
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

# P0-T059 · Failure-inject degraded modes and stress the P0 stack

## Goal / expected outcome

A scripted chaos/stress run (`tools/chaos/p0.sh`) injects the P0-relevant failures from 02 §9.3 and measures the stack's behaviour and recovery, plus load on the audit/command path, proving the platform degrades predictably before any trading exists.

## Context & references

- [02 §9.3 degraded modes](../../../docs/02-v1-architecture.md#93-degraded-modes)
- [02 §9.2 SLOs](../../../docs/02-v1-architecture.md#92-observability--slos)
- [Roadmap P0 R0.02, R0.07–R0.10](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- SLOs (02 §9.2, [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P0-B004): WORM insert p99 < 5 ms, command bus p99 < 50 ms excl. handler; the order path never waits on seals. Postgres-down behaviour per [16 §3.3](../../../docs/16-configuration-and-safety-model.md#33-records-the-write-path-vs-the-integrity-check).
- Depends on: P0-T046, P0-T051, P0-T042, P0-T043, P0-T044, P0-T039, P0-T038, P0-T036, P0-T045

## Requirements

- Faults (each: inject → observe → recover → assert): Postgres stopped 5 min (mt-api read-only, 503 on non-Kill writes, D16 loads, Kill ON still works and its record buffers in JetStream `WORM_BUFFER` then drains in order, alert fires, recovery automatic); WORM buffer filled past 80 % of a small test bound (new entries refused, Kill still recorded, alert); NATS stopped 2 min (heartbeats stale, WS snapshot on recovery, KV `kill` preserved); Loki stopped 10 min (no log loss via Vector buffer); LiteLLM budget exhausted + (mock) Anthropic unreachable (fallback to `local-advisor`, marked `fallback_used`); TEI killed (embedding calls fail fast with 503, recover); B2 unreachable 1 h (WAL queues, lag alert, catch-up); clock step +2 s via chrony test (TOTP still valid, alerts on offset); disk 85 % on NVMe (alert).
- Load: 200 commands/s for 10 min → `audit.command` chain valid, p99 command latency < 50 ms (SLO); WS fan-out 50 clients; seal + verify running concurrently.
- Container restart storm: restart every service once in random order → `docker compose ps` all healthy within 180 s.
- Results table (fault, expected, observed, recovery time) committed under `docs/runbooks/evidence/p0-chaos-<date>.md`.

## ToDo

- [ ] Write `tools/chaos/p0.sh` (bash + `docker compose pause/stop`, `tc` for latency where useful).
- [ ] Run on the host; capture Grafana screenshots and the results table.
- [ ] File bugs for any deviation.
- [ ] Update 02 §9.3 with observed P0 behaviour.

## Verification

### Tests
- The fault matrix and load runs above.

### Scenarios
- Given Postgres is down, when you press HALT, then KV `kill` is set, the banner shows, and the audit row appears after recovery.
- Given Anthropic is unreachable, when a chat call is made, then `local-advisor` answers and the 'Local models' badge data is available.

### Stress / failure injection
- Everything in Requirements is a stress/failure item; durations as listed.

## Acceptance criteria

- [ ] Every fault behaves as specified and recovers without manual steps (or a bug is filed)
- [ ] Load targets met or deviations filed as bugs
- [ ] Results table committed
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- Faults that need a later-phase component (engine, feeds) are out of scope here and listed as such in the table.

## Cardinal rules (do NOT)

- Do NOT run chaos against the off-site buckets' contents (network faults only).
- Do NOT edit WORM rows to 'reset' after tests; use scratch DBs.
- Do NOT UPDATE or DELETE WORM rows, ever; corrections are new rows with `supersedes_id` ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/02-v1-architecture.md` §9.3: add the P0 degraded-mode observations.
- `docs/roadmap/phase-0-foundations.md`: tick T0.41, T0.24, T0.45 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T059-degraded-modes-failure-injection`
- PR title: `P0-T059: Failure-inject degraded modes and stress the P0 stack`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T059` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (Postgres-down WORM buffer behaviour (16 §3.3), SLOs from 02 §9.2 (17 §D P0-B004) replace provisional targets; deps trimmed; run fields added)
