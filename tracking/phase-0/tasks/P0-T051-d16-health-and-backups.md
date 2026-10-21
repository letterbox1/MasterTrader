---
id: P0-T051
kind: task
title: Build D16 System: Health and Backups pages
phase: 0
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T050, P0-T046]
requirements: [R0.11]
roadmap_todos: [T0.26]
modules: [M15, M17]
dashboards: [D16]
branch: p0/P0-T051-d16-health-and-backups
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

# P0-T051 · Build D16 System: Health and Backups pages

## Goal / expected outcome

`/system` shows the service grid (status, image digest, uptime, restarts, heartbeat, health), host panel (CPU, RAM, disk per volume, GPU, temps, NTP offset), SLO panel, Loki-backed log search with `trace_id` jump and Grafana deep links; `/system/backups` shows last backup, restore test, WAL lag, schedule, seal/verify status and the run-backup / run-restore-test actions (C1).

## Context & references

- [Roadmap P0 R0.11](../../../docs/roadmap/phase-0-foundations.md#3-requirements)
- [D16 System](../../../docs/ui/dashboards/D16-system.md) (Health, Backups)
- [ui §3.1 data states](../../../docs/ui/README.md#31-data-states-every-tile-implements-all-of-them)
- [02 §9.2 SLOs](../../../docs/02-v1-architecture.md#92-observability--slos)
- Backend: P0-T046
- Depends on: P0-T050, P0-T046

## Requirements

- Layout ≥ xl: service grid + host panel + SLO panel; ≤ ph: host summary card → service cards → SLOs (D16 table).
- Live via WS `system`/`heartbeat`; every tile implements all data states; stale after 15 s without updates.
- Logs: filters service, level, text, time range; virtualised `LogStream`; clicking a `trace_id` filters by it.
- Backups: KPIs (backup age, size, WAL lag, last restore test pass/fail + date), seal/verify last status, schedule; actions `system.backup.run` (C1), `system.restore.test` (C1) via `ConfirmSheet`; results toast with audit link.
- Restart buttons rendered disabled with reason while `system.service.restart` is 501 (P0-B012).
- Loads with Postgres down (read-only; D16 acceptance 1).

## ToDo

- [ ] Build Health route tiles and Backups route.
- [ ] Wire queries/WS and commands.
- [ ] Vitest tests; screenshots per tier.

## Verification

### Tests
- Unit: each tile in loading/live/stale/error states.
- Integration (Playwright): with Postgres paused, `/system` renders with read-only banner and live host data.

### Scenarios
- Given the last backup is 30 h old, then the backup KPI shows Warn styling + text 'overdue' and Grafana alert fired (cross-check).

### Stress / failure injection
- n/a: covered by WS fan-out test in P0-T036 and the matrix in P0-T053.

## Acceptance criteria

- [ ] Health + Backups pages implemented per D16
- [ ] Read-only on Postgres outage
- [ ] C1 actions work end to end with audit links
- [ ] CI green (ruff, mypy, pytest, gitleaks, `pit` check, Playwright viewport matrix)

## Exceptions & edge cases

- GPU absent: GPU tile shows 'No GPU' empty state, not an error.

## Cardinal rules (do NOT)

- Do NOT show secret values or raw connection strings anywhere.
- Do NOT poll faster than the WS/REST limits (≤ 1 Hz tables).
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT skip, weaken or delete a test to get CI green.

## Doc sync on completion

- `docs/ui/dashboards/D16-system.md`: tick which widgets exist in P0.
- `docs/roadmap/phase-0-foundations.md`: tick T0.26 when every item mapped to it is done.

## Branch & PR

- Branch: `p0/P0-T051-d16-health-and-backups`
- PR title: `P0-T051: Build D16 System: Health and Backups pages`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P0-T051` run

## Progress log

- 2026-10-21 00:00 · planner · created
