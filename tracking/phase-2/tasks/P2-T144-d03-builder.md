---
id: P2-T144
kind: task
title: D03 strategy builder: template, code and describe-it
phase: 2
type: BUILD
status: backlog
priority: high
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T141, P2-T116, P2-T117]
requirements: [R2.50, R2.02, R2.03, R2.04, R2.05, R2.45]
roadmap_todos: [T2.32]
modules: [M15, M0, M7]
dashboards: [D03]
branch: p2/P2-T144-d03-builder
pr: ""
doc_sync: [docs/ui/dashboards/D03-strategies.md, docs/roadmap/phase-2-strategies-risk-lab.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P2-T144 · D03 strategy builder: template, code and describe-it

## Goal / expected outcome

`/strategies/new` lets you create a strategy three ways — template + `ParamForm`, code (manifest + class skeleton in `CodeEditor`), or 'describe it' via the sandboxed generator — with the common sections (universe, data subscriptions, features, decision, sizing, risk policy, schedule, review) and saves as `draft` via `strategy.create`.

## Context & references

- Roadmap: [R2.50, R2.02–R2.05, R2.45](../../../docs/roadmap/phase-2-strategies-risk-lab.md#3-requirements) · ToDo T2.32 · exit criterion 1 ('create a strategy from a template, from code and by describe it')
- [D03 builder](../../../docs/ui/dashboards/D03-strategies.md) · template list mismatch tracked in P2-B054
- Backend from part A (P2-T001–T099): `/strategies/templates`, manifest validator incl. never-build rules, `strategy.create` (T2.20/T2.21); generator from P2-T116

## Requirements

- Template tab lists templates from `/strategies/templates` with evidence + priority; never-build patterns are not offered and the validator explains refusals.
- Universe section shows each instrument's finest available resolution; incompatible timeframes flagged; saving a strategy that needs an unavailable resolution is blocked with a clear message (D03 acceptance 3).
- Data subscriptions: ticks/quotes/L2/any bar spec incl. tick/volume/value bars; multiple timeframes allowed.
- Decision section: rules, tier-A model from the registry (only `promotable` models), tier-B thresholds disabled until P4.
- Sizing: fixed, fixed-fractional, vol-target, Kelly-capped, risk-parity (as offered by part A's M11).
- Manifest required fields enforced in the Review step: counterparty sentence, sleeve, kill criteria, benchmark, risk-policy ref.
- Describe-it: prompt → progress via `lab.job` → code diff, manifest, sandbox log, first backtest, leakage review; banner 'Generated code ran in an isolated sandbox with no network or secrets.'; must review before save.
- Code tab editable ≥ md; read-only on phones.
- Every tile implements the [data states](../../../docs/ui/README.md#31-data-states-every-tile-implements-all-of-them) (loading skeleton ≤ 300 ms, live, stale chip, degraded, error card with retry → D16, empty with primary action, PAPER/LIVE markers, unconfirmed hatching).

## ToDo

- [ ] Route `apps/web/src/routes/strategies/new.tsx` with three tabs and common sections
- [ ] Resolution compatibility check using instrument metadata (`/markets/instruments`)
- [ ] Generator panel shared with D04 (P2-T146)
- [ ] Playwright: one strategy created each way; matrix; doc sync

## Verification

### Tests
- Playwright: DESIGN.md §6.8 viewport matrix (overflow + fixed-bar overlap checks) and axe on the new routes; Vitest + Testing Library for components.
- Playwright: create EMA template strategy → draft; create via code fixture; create via describe-it (recorded generator) → draft.

### Scenarios
- Given a manifest describing copy-trading, then save is refused with the never-build reason.
- Given a strategy subscribing to 1s bars on a daily-only instrument, then save is blocked naming the instrument and its finest resolution.
- Given the generator job fails in the sandbox, then the log is shown and nothing is saved.

### Stress / failure injection
- n/a: form flows; generator load covered by P2-T116/T165.

## Acceptance criteria

- [ ] D03 acceptance 1 and 3 pass
- [ ] All three creation paths produce a draft
- [ ] Viewport matrix + axe green on `/strategies/new`
- [ ] CI green (lint, types, tests, viewport matrix where UI)

## Exceptions & edge cases

- Unsaved builder state kept in session storage; leaving prompts a confirm.
- Template version changes while editing: warn and offer to rebase.

## Cardinal rules (do NOT)

- Do NOT enforce confirmation levels only in the UI; C1–C3/Kill are enforced server-side by `mt_api`.
- Do NOT use `100vh`/`h-screen`, unprefixed multi-column grids or the Tailwind CDN (DESIGN.md §6.3–6.5).
- Do NOT sum or show paper and live money without a mode label.
- Do NOT execute generated code in the browser or API; only display sandbox results.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/ui/dashboards/D03-strategies.md`: template list per P2-B054 resolution.
- `docs/roadmap/phase-2-strategies-risk-lab.md`: tick T2.32 once every task mapped to it (part A and part B) is done.

## Branch & PR

- Branch: `p2/P2-T144-d03-builder`
- PR title: `P2-T144: D03 strategy builder: template, code and describe-it`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P2-T144` run · Playwright viewport matrix + axe green

## Progress log

- 2026-10-21 00:00 · planner · created
