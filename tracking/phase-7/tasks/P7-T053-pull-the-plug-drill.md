---
id: P7-T053
kind: task
title: Pull-the-plug drill with paper positions
phase: 7
type: USER
status: backlog
priority: critical
size: S
severity: ""
owner: user
claimed_by: ""
depends_on: [P7-T052]
requirements: [R7.11]
roadmap_todos: [T7.09]
modules: [M11]
dashboards: [D06]
branch: p7/P7-T053-pull-the-plug-drill
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

# P7-T053 · Pull-the-plug drill with paper positions

## Goal / expected outcome

You physically cut mains power and the fixed line with paper positions open, and the system fails flat (or holds safely on resting stops), recovers, reconciles and records the drill — the R7.11 verification.

## Context & references

- Roadmap: [R7.11 · ToDo T7.09](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [07 §5](../../../docs/07-security-notes.md#5-network--host) · Roadmap T7.09
- Related: P7-T052 (automated precursor), P7-T043 (`power-or-link-loss.md`), P7-T011 (drill log)

## Requirements

- Paper positions on at least two venues (one with `fail_flat: flatten`, one `cancel_only` with resting stop).
- Steps: unplug the fixed line → wait 2 min → unplug mains → wait for UPS low battery → observe fail-flat + shutdown → restore power/line → host boots → recon.
- Expected: Telegram/ntfy alerts received on the phone (via mobile data); positions flat or protected; after boot accounts `unconfirmed` → `confirmed`; drill recorded.

## ToDo

- [ ] Pick a 1-hour window outside high-volatility events.
- [ ] Open the paper positions via bots.
- [ ] Follow `docs/runbooks/power-or-link-loss.md` step by step.
- [ ] Record the drill in D16 (`ops.drill.record`) with timings and photos/screenshots (no secrets).
- [ ] Tell the planner of any surprise; it becomes a bug item.

## Verification

### Tests
- Evidence: alerts timeline, fail-flat timestamps, recon result after boot.

### Scenarios
- Given mains is cut, when the UPS reaches low battery, then positions are flat (flatten config) or protected by resting stops (cancel_only) before the host shuts down.

### Stress / failure injection
- This drill is the real-world failure injection.

## Acceptance criteria

- [ ] Drill recorded as `pass` with timings.
- [ ] No unprotected position at any time.

## Exceptions & edge cases

- Host fails to boot after power restore: follow the host-rebuild runbook; record as a failed drill and re-run.

## Cardinal rules (do NOT)

- Do NOT do this drill with live positions.
- Do NOT skip the recon step before resuming bots.
- Do NOT add discretionary overrides; the only manual action outside approve mode is flatten-and-halt with a required reason (14 §4).
- Do NOT commit secrets or paste them into chats, issues, PRs or logs; secrets live only in the sops/age file (07 §2).

## Doc sync on completion

- `docs/runbooks/power-or-link-loss.md`: fixes from the drill.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.09 when this item is done.

## Branch & PR

- Branch: `p7/P7-T053-pull-the-plug-drill`
- PR title: `P7-T053: Pull-the-plug drill with paper positions`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T053` run · evidence (redacted, no secrets) linked in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
