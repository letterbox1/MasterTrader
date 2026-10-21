---
id: P7-T059
kind: task
title: Run micro-live 4-week windows (each clean window allows one 25% step)
phase: 7
type: RUN
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T057]
requirements: [R7.05]
roadmap_todos: [T7.81]
modules: [M11, M16, M18]
dashboards: [D06, D03, D14]
branch: p7/P7-T059-run-micro-live-windows
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P7-T059 · Run micro-live 4-week windows (each clean window allows one 25% step)

## Goal / expected outcome

The first funded sleeve trades live in micro size for at least one full 4-week window with weekly reviews, kill/decay monitoring and recon all active; each clean 4-week window makes one 25% step eligible. Windows after the phase closes continue as standing operations.

## Context & references

- Roadmap: [R7.05 · ToDo T7.81](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- Spec: [14 §7](../../../docs/14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7) · Roadmap exit criteria 1 and 3
- Related: P7-T018, P7-T019, P7-T060, P7-T061

## Requirements

- Minimum for this item: one complete 4-week window on the first sleeve with all monitors active and every week reviewed (clean or not).
- Track per week: clean/dirty + reason, P&L vs band, shortfall ratio, recon breaks, approvals expired.
- If a kill criterion fires: follow the runbook, record, and the window restarts after a C3 restart (or the sleeve retires).

## ToDo

- [ ] Each Monday: copy the capital-step status line into the progress log.
- [ ] Ensure the weekly review is signed (P7-T060).
- [ ] At window end: record clean/dirty outcome; if clean, P7-T061 can approve the step.

## Verification

### Tests
- Evidence: weekly pack + capital-step log rows.

### Scenarios
- Given week 3 is dirty (recon break 14 h), then the window restarts from week 4 and the step is not eligible yet.

### Stress / failure injection
- n/a: elapsed-time item; failures handled by kill criteria.

## Acceptance criteria

- [ ] One full 4-week live window completed with all weeks reviewed and logged.
- [ ] Outcome (clean → step eligible, or dirty with reasons) recorded.

## Exceptions & edge cases

- Market closed weeks (FX holidays) count per the clean-week activity rule (P7-T018).

## Cardinal rules (do NOT)

- Do NOT override the system to place discretionary trades; only flatten-and-halt with a reason.
- Do NOT add discretionary overrides; the only manual action outside approve mode is flatten-and-halt with a required reason (14 §4).
- Do NOT weaken a gate, threshold or window to "get live sooner" (roadmap §1, Out).

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §7: none unless the clean-week rule needed change (then via P7-B003).
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.81 when this item is done.

## Branch & PR

- Branch: `p7/P7-T059-run-micro-live-windows`
- PR title: `P7-T059: Run micro-live 4-week windows (each clean window allows one 25% step)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T059` run · evidence (redacted, no secrets) linked in the progress log

## Progress log

- 2026-10-21 00:00 · planner · created
