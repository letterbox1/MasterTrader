---
id: P4-T052
kind: task
title: Blackout test: a scalper pauses around a seeded NFP event
phase: 4
type: VERIFY
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T038]
requirements: [R4.10]
roadmap_todos: [T4.62]
modules: [M5, M11]
dashboards: [D06, D08]
branch: p4/P4-T052-verify-blackout-nfp
pr: ""
doc_sync: [docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P4-T052 · Blackout test: a scalper pauses around a seeded NFP event

## Goal / expected outcome

An integration test (and a paper-mode demo) seeds an NFP release into `text.calendar_event`, runs a paper scalper on EURUSD/XAUUSD through the real engine + M11 path, and proves new entries are rejected with `blackout:NFP` inside the window, protective exits still execute, and trading resumes after the window — with D06/D08 showing the same window.

## Context & references

- Roadmap: [R4.10](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.62](../../../docs/roadmap/phase-4-intel.md#4-todo-sets) · Exit criterion 2
- Spec: [03 M5](../../../docs/03-build-spec.md#m5-calendars--mt_datacalendar) ('pause scalpers around NFP') · [03 M11](../../../docs/03-build-spec.md#m11-risk-manager--mt_risk-built-in-user-inputs-via-uitelegram-later-mcp)
- Cross-phase: P2 paper engine + scalper template (R2.02, R2.30).

## Requirements

- Simulated clock drives the engine through [T−30 min, T+30 min] around the seeded event.
- Assertions: entries at T−20 rejected; stop-loss/reduce-only at T−5 executes; entry at T+16 accepted (with the default 15/15 window).
- Audit: rejections in `audit.order` / risk events with reason; nothing bypasses M11.
- UI check: D06 active blackouts and D08 calendar marker show the same interval (Playwright).

## ToDo

- [ ] Seed fixtures + simulated-clock harness.
- [ ] Integration test in `tests/integration/test_blackout_nfp.py`.
- [ ] Playwright check.
- [ ] Demo script `ops/demo/blackout_nfp.sh` for the exit demo (paper mode).

## Verification

### Tests
- The integration test + Playwright check.

### Scenarios
- Given the event is superseded (moved +1 day), then the window moves and the old window no longer blocks.
- Given the calendar is stale, then the fail-safe blocks and alerts.

### Stress / failure injection
- Run 1,000 random order intents across the window: zero entries accepted inside, zero exits blocked.

## Acceptance criteria

- [ ] Integration test green
- [ ] Demo script runs on paper and shows the pause in D06/D08
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- DST weeks: included as a parameterised case.

## Cardinal rules (do NOT)

- Do NOT run this against live accounts.
- Do NOT relax the window to make the test pass.
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.
- Do NOT touch live money (P7 gates); keys stay trade-only, IP-locked, withdrawals disabled.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/roadmap/phase-4-intel.md`: tick T4.62; exit criterion 2 evidence link

## Branch & PR

- Branch: `p4/P4-T052-verify-blackout-nfp`
- PR title: `P4-T052: Blackout test: a scalper pauses around a seeded NFP event`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T052` run

## Progress log

- 2026-10-21 00:00 · planner · created
