---
id: P2-T145
kind: task
title: D04 Research Lab: new run panel, job queue, experiments
phase: 2
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T141, P2-T117]
requirements: [R2.50, R2.40, R2.44]
roadmap_todos: [T2.32]
modules: [M15, M7]
dashboards: [D04]
branch: p2/P2-T145-d04-lab-jobs-and-experiments
pr: ""
doc_sync: [docs/ui/dashboards/D04-research-lab.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T145 · D04 Research Lab: new run panel, job queue, experiments

## Goal / expected outcome

`/lab` lets you start any lab run (screener/truth backtest, walk-forward, purged K-fold, MC permutation, sweep, full validation suite, tier-A training), watch the live job queue and browse MLflow-backed experiments with multi-select compare.

## Context & references

- Roadmap: [R2.50, R2.40, R2.44](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.32
- [D04 /lab spec](../../../docs/ui/dashboards/D04-research-lab.md) · commands via P2-T117

## Requirements

- New run panel fields per D04: strategy+version, run type, data range + `as_of`, instruments, resolution, cost model (measured default, shows snapshot id; custom flagged), fill model, benchmark, sweep space (from ParamForm), resources (max workers, time cap).
- Distillation run type hidden until P6 (D04 lists it; see P2-B059).
- Submit = C1 confirm; job appears in the queue with progress/ETA via WS `lab.job`.
- Job queue columns status, type, strategy, progress, ETA, started; cancel (C1).
- Experiments table from `/lab/experiments`; multi-select → Compare (≤ 6).
- Layouts: ≥ xl two-pane; md–lg drawer; ≤ ph floating 'New run' → full-screen sheet.
- Every tile implements the [data states](../../../docs/ui/README.md#31-data-states-every-tile-implements-all-of-them) (loading skeleton ≤ 300 ms, live, stale chip, degraded, error card with retry → D16, empty with primary action, PAPER/LIVE markers, unconfirmed hatching).

## ToDo

- [ ] Route `apps/web/src/routes/lab/index.tsx`
- [ ] New run form with zod schema from OpenAPI
- [ ] Queue + experiments tables
- [ ] Playwright + matrix; doc sync

## Verification

### Tests
- Playwright: DESIGN.md §6.8 viewport matrix (overflow + fixed-bar overlap checks) and axe on the new routes; Vitest + Testing Library for components.
- Playwright: submit a truth backtest fixture → progress → done row; cancel a running job.

### Scenarios
- Given 'custom' costs with zeros, then the form warns 'Unrealistic costs' before submit.
- Given the worker is offline, then the job shows 'queued (no worker)' and no spinner forever (ETA unknown).

### Stress / failure injection
- Queue with 100 jobs updating: table updates batched ≤ 1 Hz; no layout thrash.

## Acceptance criteria

- [ ] All run types (except P6 distillation) submittable
- [ ] Viewport matrix + axe green on `/lab`
- [ ] CI green (lint, types, tests, viewport matrix where UI)

## Exceptions & edge cases

- `as_of` later than now rejected; `as_of` earlier than data start warns.

## Cardinal rules (do NOT)

- Do NOT enforce confirmation levels only in the UI; C1–C3/Kill are enforced server-side by `mt_api`.
- Do NOT use `100vh`/`h-screen`, unprefixed multi-column grids or the Tailwind CDN (DESIGN.md §6.3–6.5).
- Do NOT sum or show paper and live money without a mode label.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/ui/dashboards/D04-research-lab.md`: run-type availability per phase.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.32 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T145-d04-lab-jobs-and-experiments`
- PR title: `P2-T145: D04 Research Lab: new run panel, job queue, experiments`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T145` run · Playwright viewport matrix + axe green

## Progress log

- 2026-10-21 00:00 · planner · created
