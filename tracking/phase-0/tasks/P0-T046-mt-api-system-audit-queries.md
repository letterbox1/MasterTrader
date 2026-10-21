---
id: P0-T046
kind: task
title: Implement the System and audit queries for D16
phase: 0
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T032, P0-T036, P0-T023, P0-T038]
requirements: [R0.08, R0.11]
roadmap_todos: [T0.24, T0.26]
modules: [mt_api, M17]
dashboards: [D16]
branch: p0/P0-T046-mt-api-system-audit-queries
pr: ""
doc_sync: [docs/ui/dashboards/D16-system.md, docs/roadmap/phase-0-foundations.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P0-T046 · Implement the System and audit queries for D16

## Goal / expected outcome

mt-api serves the D16 backend contract: `/system/health` (+ `?slo=1`), `/system/services`, `/system/logs` (Loki proxy), `/system/backups`, `/system/keys` (masked metadata only), `/system/settings`, `/audit/log` with chain-verification status, and the `system` WS topic — all working read-only when Postgres is down.

## Context & references

- [Roadmap P0 R0.11](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [D16 System](../../../docs/ui/dashboards/D16-system.md) (Backend contract)
- [02 §7 API contract](../../../docs/02-v1-architecture.md#7-api-contract-mt_api) (§7.1 System queries)
- [02 §9.2 SLOs](../../../docs/02-v1-architecture.md#92-observability--slos)
- Related: P0-T051, P0-T052
- Depends on: P0-T032, P0-T036, P0-T023, P0-T038

## Requirements

- `/system/health`: host CPU/RAM/disk/GPU/temps/chrony offset via Prometheus HTTP API queries (no Docker socket); `slo=1` returns each 02 §9.2 SLO with `value|null` + status (`n/a` until its phase).
- `/system/services`: one row per container from 02 §3.2 present in P0: status/health, image digest, uptime, restarts (cAdvisor/Prometheus), heartbeat age (NATS KV `heartbeat`).
- `/system/logs`: Loki proxy with server-side allow-listed LogQL (service, level, text contains, time range ≤ 24 h, limit ≤ 1,000), never raw LogQL from the client; responses pass through the secret redactor again.
- `/system/backups`: last backup per kind, WAL lag, last restore test, last seal + verify status (from `ops.backup_run`, `ops.restore_test`, `audit.seal`, `audit.verify_run`).
- `/system/keys`: from `key_age.prom` and secrets **metadata** only: name, service, created, age, rotate_due — **never values** (D16 acceptance 2).
- `/system/settings`: read `ops.setting`/`ops.user_pref`; writes go through `system.settings.update`.
- `/audit/log`: filters source/command/date, cursor paging, columns per D16 incl. `hash` and per-row chain status from the latest `audit.verify_run`.
- Postgres down: `/system/health` and `/system/services` still answer from Prometheus/NATS with a `db: down` flag (D16 acceptance 1).

## ToDo

- [ ] Implement endpoints + response schemas (OpenAPI).
- [ ] Implement Prometheus and Loki clients with timeouts (2 s) and caching (5 s).
- [ ] Publish `system` WS topic updates every 5 s.
- [ ] Tests below.

## Verification

### Tests
- Integration: each endpoint returns schema-valid data on the running stack.
- Security: `/system/keys` response contains no secret values (scan against the real tmpfs values in a test fixture).
- Degraded: with Postgres paused, health/services still 200 with `db: down`.

### Scenarios
- Given Loki is down, when D16 Logs is opened, then `/system/logs` returns 503 problem+json and the tile shows its error state with a link (ui §3.1).
- Given a client sends a LogQL injection in `text`, then it's treated as a literal filter.

### Stress / failure injection
- 20 clients polling `/system/health` every 2 s → Prometheus load stays low thanks to the 5 s cache (logged).

## Acceptance criteria

- [ ] All D16 backend contract queries implemented and documented in OpenAPI
- [ ] No secret value can be returned (tested)
- [ ] Postgres-down read-only behaviour proven
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check)

## Exceptions & edge cases

- `system.service.restart` stays 501 until P0-B012 is resolved; D16 shows the button disabled with the reason.

## Cardinal rules (do NOT)

- Do NOT mount the Docker socket into mt-api.
- Do NOT render or log secret values; metadata only.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/ui/dashboards/D16-system.md`: mark which widgets are live in P0 and the restart-button status.
- `docs/roadmap/phase-0-foundations.md`: tick T0.24, T0.26 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T046-mt-api-system-audit-queries`
- PR title: `P0-T046: Implement the System and audit queries for D16`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T046` run

## Progress log

- 2026-10-21 00:00 · planner · created
