---
id: P2-T068
kind: task
title: "Runbooks: keys leaked, server down with open positions, kill-switch drill, bad data"
phase: 2
type: DOC
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T031, P2-T032, P2-T027]
requirements: [R2.18]
roadmap_todos: [T2.90]
modules: [M11, M12]
dashboards: []
branch: p2/P2-T068-runbooks-incidents
pr: ""
doc_sync: [docs/runbooks/keys-leaked.md, docs/runbooks/server-down-open-positions.md, docs/runbooks/kill-switch-drill.md, docs/runbooks/bad-data.md, docs/07-security-notes.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T068 · Runbooks: keys leaked, server down with open positions, kill-switch drill, bad data

## Goal / expected outcome

Four step-by-step runbooks in `docs/runbooks/` let you act correctly under stress from a phone: keys leaked, server down with open positions, kill-switch drill, bad data.

## Context & references

- Roadmap: ToDo T2.90 · [07 §9 runbook list](../../../docs/07-security-notes.md#9-monitoring--incident-response)
- Flows: [02 F6, F11](../../../docs/02-v1-architecture.md#8-end-to-end-flows) · [02 §9.3](../../../docs/02-v1-architecture.md#93-degraded-modes)
- Cross-phase: P0 runbooks (backup/restore, host rebuild, secret rotation).

## Requirements

- Each runbook: trigger/symptoms, first 5 minutes (phone-only steps), commands (`/kill`, D06 HALT, venue web UI links), verification, recovery, post-incident (audit/`risk.event` references, journal note).
- Keys leaked: `/kill` → revoke keys at each venue (links per venue) → rotate in sops → `mt keys audit` → check withdrawals history.
- Server down with open positions: broker/venue web UI flatten per venue, check dead-man sidecar acted, resting broker-side stops, restart + reconcile (P2-T027).
- Kill-switch drill: the procedure from P2-T054 + how to resume via C3.
- Bad data: identify via D07/DQ alerts, hold/halt affected bots (downgrade), switch feed source, verify recon before resuming.

## ToDo

- [ ] Write the four runbooks
- [ ] Dry-run each on paper/testnet; fix gaps
- [ ] Link from D16 System and Telegram `/help`
- [ ] Update the docs listed under *Doc sync on completion* and tick the roadmap ToDo box(es) once every task mapped to them is done

## Verification

### Tests
- Tabletop walkthrough of each runbook on paper with timings recorded.

### Scenarios
- Given the host is unreachable, when you follow the runbook on your phone, then all paper positions are flat via venue UIs within 10 minutes.

### Stress / failure injection
- n/a: documentation; drills in P2-T054 and P7 T7.60.

## Acceptance criteria

- [ ] Four runbooks merged and each walked through once
- [ ] CI green: ruff, mypy, pytest (and the `mt_risk` golden suite, `pit` check, viewport matrix where relevant)

## Exceptions & edge cases

- Venue web UI unavailable: escalation contacts listed.

## Cardinal rules (do NOT)

- Do NOT include secrets, account numbers or recovery codes in runbooks.
- Do NOT commit secrets or paste them into chats/issues/logs; secrets live in the sops/age file (07 §2).

## Doc sync on completion

- `docs/07-security-notes.md` §9: link the runbooks.
- `docs/runbooks/*.md`: created.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.90 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T068-runbooks-incidents`
- PR title: `P2-T068: Runbooks: keys leaked, server down with open positions, kill-switch drill, bad data`
- PR checklist: tests added and green · docs synced · task file ticked · no secrets (gitleaks) · `./kanban done P2-T068` run

## Progress log

- 2026-10-21 00:00 · planner · created
