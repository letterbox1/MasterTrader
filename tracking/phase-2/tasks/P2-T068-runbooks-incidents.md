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
depends_on: [P2-T031, P2-T032, P2-T027, P2-T072, P2-T074]
requirements: [R2.18]
roadmap_todos: [T2.90]
modules: [M11, M12]
dashboards: []
tools: []
mcp: []
env: []
services: []
branch: p2/P2-T068-runbooks-incidents
pr: ""
doc_sync: [docs/runbooks/keys-leaked.md, docs/runbooks/server-down-open-positions.md, docs/runbooks/kill-switch-drill.md, docs/runbooks/bad-data.md, docs/07-security-notes.md, docs/roadmap/phase-2-strategies-risk-lab.md]
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

# P2-T068 · Runbooks: keys leaked, server down with open positions, kill-switch drill, bad data

## Goal / expected outcome

Four step-by-step runbooks in `docs/runbooks/` let you act correctly under stress from a phone: keys leaked, server down with open positions, kill-switch drill, bad data.

## Context & references

- Roadmap: ToDo T2.90 · [07 §9 runbook list](../../../docs/07-security-notes.md#9-monitoring--incident-response)
- Flows: [02 F6, F11](../../../docs/02-v1-architecture.md#8-end-to-end-flows) · [02 §9.3](../../../docs/02-v1-architecture.md#93-degraded-modes)
- Cross-phase: P0 runbooks (backup/restore, host rebuild, secret rotation and WORM incident: P0-T060, P0-T061).
- Decisions: three-layer dead-man and clean restart flat with bots paused ([16 §3.1](../../../docs/16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch)); fixed egress IP and fail-flat when the tunnel is down ([16 §3.2](../../../docs/16-configuration-and-safety-model.md#32-network-egress-and-ip-locked-keys)); key rotation every 90 days and after a suspected leak ([16 §2.3](../../../docs/16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl)); inline data age ([16 §2.2](../../../docs/16-configuration-and-safety-model.md#22-data-freshness-what-stale-means)).

## Requirements

- Each runbook: trigger/symptoms, first 5 minutes (phone-only steps), commands (`/kill`, D06 HALT, venue web UI links), verification, recovery, post-incident (audit/`risk.event` references, journal note).
- Keys leaked: `/kill` → revoke keys at each venue (links per venue), including the separate `deadman` keys → rotate in the sops file outside the repo → `mt keys audit` → check withdrawals history (withdrawals are disabled on every key; confirm).
- Server down with open positions: what each dead-man layer did (in-engine watchdog, `deadman` sidecar at 5 s cancel / 10 s `on_system_failure`, venue cancel-after timers + resting venue stops), check via venue web UIs, flatten per venue if anything remains; restart: the engine starts with every bot paused, reconciles, flattens/cancels residue and waits for your resume (C1) (P2-T027, P2-T074). Host/internet down: only venue timers and resting stops protect you.
- Kill-switch drill: the procedure from P2-T054 + how to resume via C3.
- Bad data: identify via D07/DQ alerts (stale orders are already rejected inline by M11), hold/halt affected bots (downgrade), switch feed source, verify recon before resuming.

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
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (runbooks reflect the three-layer dead-man, restart flat with bots paused, deadman keys, rotation and inline data age)
