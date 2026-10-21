---
id: P2-T168
kind: task
title: Verify UI real-time and degraded modes on D01/D03/D04/D05
phase: 2
type: VERIFY
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T142, P2-T147, P2-T149]
requirements: [R2.50, R2.51]
roadmap_todos: [T2.32]
modules: [M15]
dashboards: [D01, D03, D04, D05]
branch: p2/P2-T168-verify-ui-degraded-and-realtime
pr: ""
doc_sync: [docs/ui/README.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T168 · Verify UI real-time and degraded modes on D01/D03/D04/D05

## Goal / expected outcome

Evidence that the part-B dashboards behave correctly under WS gaps, mt-api restarts, stale data, Postgres read-only mode and Kill ON, and meet the live-update lag SLO (p95 < 500 ms).

## Context & references

- Roadmap: [R2.50, R2.51](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.32
- [ui §3.1 data states](../../../docs/ui/README.md#31-data-states-every-tile-implements-all-of-them) · [ui §3.4 real-time](../../../docs/ui/README.md#34-real-time) · [02 §9.2/9.3](../../../docs/02-v1-architecture.md#93-degraded-modes)

## Requirements

- WS gap (drop seq) → 'Re-syncing' chip → REST refetch → resume, on every live tile.
- mt-api restart → tiles recover without reload; actions disabled while down; Telegram alert path (part A) unaffected.
- Stale DQ on an instrument → stale chips + 'paused-by-DQ' strategy rows.
- Postgres read-only → grey banner, actions disabled except Kill.
- Kill ON → red banner, Safety red, trading actions disabled except cancel/flatten-via-kill, state reflected < 1 s after server ack.
- UI live update lag p95 < 500 ms measured by local client telemetry under 1 Hz portfolio + 4 Hz chart load.

## ToDo

- [ ] Playwright specs with fault fixtures (mock WS server + compose stop)
- [ ] Measure lag via client telemetry
- [ ] Record results; file bugs

## Verification

### Tests
- Playwright degraded-mode specs (nightly).

### Scenarios
- Given the approvals sheet is open when the WS drops, then countdowns continue from server time after re-sync (no stale TTLs).

### Stress / failure injection
- Background tab for 10 min then foreground: subscriptions resume from 0.2 Hz to full within 1 s.

## Acceptance criteria

- [ ] All degraded states render as specified
- [ ] Lag p95 < 500 ms measured
- [ ] Kill reflected < 1 s

## Exceptions & edge cases

- Offline PWA: shell shows 'Offline: data may be stale'; no actions queued except Kill attempts.

## Cardinal rules (do NOT)

- Do NOT hide errors behind spinners or blank tiles.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/ui/README.md` §3: confirm behaviours as implemented.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.32 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T168-verify-ui-degraded-and-realtime`
- PR title: `P2-T168: Verify UI real-time and degraded modes on D01/D03/D04/D05`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T168` run · Playwright viewport matrix + axe green

## Progress log

- 2026-10-21 00:00 · planner · created
