---
id: P2-T064
kind: task
title: Take part in the kill-switch drill from your phone
phase: 2
type: USER
status: backlog
priority: critical
size: XS
severity: ""
owner: user
claimed_by: ""
depends_on: [P2-T054]
requirements: [R2.18]
roadmap_todos: [T2.06]
modules: [M11]
dashboards: [D06]
branch: p2/P2-T064-user-kill-drill-phone
pr: ""
doc_sync: [docs/runbooks/kill-switch-drill.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T064 · Take part in the kill-switch drill from your phone

## Goal / expected outcome

You personally halt paper trading from your phone with Telegram `/kill`, see it take effect within 1 s, and turn it back off through the C3 path — exit criterion 3 (kill part).

## Context & references

- Roadmap: [R2.18](../../../docs/roadmap/phase-2-strategies-risk-lab.md) · ToDo T2.06 · exit criterion 3
- [mob §4 acceptance 1](../../../docs/ui/mobile-and-telegram.md#4-acceptance-criteria)
- Runbook: `docs/runbooks/kill-switch-drill.md` (P2-T068).

## Requirements

- Paper positions/orders open (agent seeds them).
- Phone only; no desktop.
- Turn-off requires Approve + TOTP + cool-down and the cause cleared.

## ToDo

- [ ] Agree a 15-min slot; agent seeds orders
- [ ] Send `/kill` and tap Confirm; note the bot's reply time
- [ ] Check D06 on the phone: HALTED, orders cancelled
- [ ] Request resume (D06 Resume or Telegram), approve, enter TOTP, wait the cool-down
- [ ] Note anything confusing for the runbook
- [ ] Record completion in the progress log (no secrets) and run `./kanban done P2-T064`

## Verification

### Tests
- Agent reads `mt_kill_to_cancels_seconds` for your drill (< 1 s).

### Scenarios
- Given open paper orders, when you send `/kill` and confirm, then everything halts within 1 s and the bot confirms.

### Stress / failure injection
- Optional second run with mt-api stopped by the agent (NATS path).

## Acceptance criteria

- [ ] Kill < 1 s from your tap (metric)
- [ ] Resume completed via C3 on the phone

## Exceptions & edge cases

- Telegram unreachable: use the web HALT; record it.

## Cardinal rules (do NOT)

- Do NOT run the drill with live money (none exists in P2).
- Loosening risk, autonomous mode and mandates are C3 (Telegram approve + TOTP + cool-down); protective exits never wait for approval.

## Doc sync on completion

- `docs/runbooks/kill-switch-drill.md`: add your notes.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.06 when all tasks mapped to it are done.

## Branch & PR

- Branch: `p2/P2-T064-user-kill-drill-phone` (only if a repo change results, e.g. non-secret config or manifests; secrets never go in git)
- PR title: `P2-T064: Take part in the kill-switch drill from your phone`
- PR checklist: no secrets in diff (gitleaks clean) · task file ticked · `./kanban done P2-T064` run

## Progress log

- 2026-10-21 00:00 · planner · created
