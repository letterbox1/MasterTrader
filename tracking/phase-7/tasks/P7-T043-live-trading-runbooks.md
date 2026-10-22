---
id: P7-T043
kind: task
title: Live-trading runbooks for Phase 7 incidents
phase: 7
type: DOC
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T022, P7-T027, P7-T033, P7-T035, P7-T066, P2-T068]
requirements: [R7.06, R7.09, R7.11, R7.14]
roadmap_todos: [T7.60]
modules: [M11, M16]
dashboards: [D06, D16]
tools: [git, uv]
mcp: []
env: []
services: []
branch: p7/P7-T043-live-trading-runbooks
pr: ""
doc_sync: [docs/runbooks/, docs/07-security-notes.md, docs/roadmap/phase-7-prove-and-go-live.md]
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

# P7-T043 · Live-trading runbooks for Phase 7 incidents

## Goal / expected outcome

`docs/runbooks/` gains live-specific runbooks and updates the existing five so they cover live sub-accounts, and the drills in P7-T044/P7-T045 can follow them step by step.

## Context & references

- Roadmap: [R7.06, R7.09, R7.11 · ToDo T7.60](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [07 §9](../../../docs/07-security-notes.md#9-monitoring--incident-response) (runbooks: keys leaked, server down with open positions, bad data, wallet drained) · [14 §7](../../../docs/14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7) (kill criteria) · [07 §5](../../../docs/07-security-notes.md#5-network--host) (fail flat)
- Cross-phase: P2-T068 (`depends_on`: keys leaked, server down with open positions, kill-switch drill, bad data runbooks), P0-T060/P0-T061, P1-T055 (data-operations runbooks); P5-T051 (wallet drained) only if a hot/burner wallet exists ([17 §D P7-B011](../../../docs/17-decisions-register.md#d-other-decisions)).
- Related: P7-T044, P7-T045, P7-T053

## Requirements

- New runbooks: `kill-criterion-fired.md` (sleeve halt, step-down, C3 restart), `system-drawdown-stages.md` (stage 1 no new entries; stage 2 flatten + 30-day review template; two-strike end; 16 §2.1), `recon-break-unexplained.md` (12 h warn / 24 h halt), `power-or-link-loss.md` (UPS/4G/fail-flat, 16 §3.1), `egress-tunnel-down.md` (exit node or tunnel down: venue timers + resting stops, rebuild the exit node, 16 §3.2), `mt5-vps-down.md` (rebuild procedure, broker web/terminal fallback; only if the MT5 route is used).
- Updates: `server-down-with-open-positions.md` and `keys-leaked.md` list each live venue's web UI steps (flatten, revoke key) and sub-account ids (no secrets).
- Every runbook: trigger, first 5 minutes, decision points, commands (`mt_api`/Telegram), verification, record-the-drill step (`ops.drill.record`).
- Plain English; each runbook ≤ 2 pages.

## ToDo

- [ ] Write the six new runbooks.
- [ ] Update the existing runbooks for live.
- [ ] Link runbooks from alert templates (deep link in Telegram critical alerts).
- [ ] Peer-read each runbook against the code paths (commands exist).

## Verification

### Tests
- Docs lint (markdown links resolve); a test asserts every critical alert kind maps to a runbook URL.

### Scenarios
- Given a `recon_unexplained_24h` alert, then its Telegram message links to `recon-break-unexplained.md`.

### Stress / failure injection
- n/a: documentation; exercised by the drills.

## Acceptance criteria

- [ ] Six new runbooks + updated existing ones merged.
- [ ] Every critical alert kind links to a runbook.
- [ ] CI green (link check).

## Exceptions & edge cases

- Runbook needs a secret (e.g. venue login): reference the sops key name only.

## Cardinal rules (do NOT)

- Do NOT put credentials, API keys or seed locations in runbooks.
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file (07 §2).
- Do NOT add discretionary overrides; the only manual trading action outside HITL approvals is flatten-and-halt with a required reason (14 §4).

## Doc sync on completion

- `docs/runbooks/`: new and updated runbooks.
- `docs/07-security-notes.md` §9: list the new runbooks.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.60 when this item is done.

## Branch & PR

- Branch: `p7/P7-T043-live-trading-runbooks`
- PR title: `P7-T043: Live-trading runbooks for Phase 7 incidents`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T043` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (system-drawdown-stages runbook (16 §2.1), egress-tunnel-down runbook (16 §3.2), wallet drained only if a hot/burner wallet exists (P7-B011); deps)
