---
id: P6-T077
kind: task
title: D14 scenario-twin report view and recent simulator runs
phase: 6
type: BUILD
status: backlog
priority: medium
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T075, P0-T048, P0-T049, P3-T040]
requirements: [R6.40, R6.33]
roadmap_todos: [T6.37]
modules: [M14, M15, M18]
dashboards: [D14]
tools: [git, pnpm, playwright]
mcp: []
env: []
services: [mt-api]
branch: p6/P6-T077-d14-scenario-twin-report-view-and-recent-simulat
pr: ""
doc_sync: [docs/ui/dashboards/D14-journal.md, docs/roadmap/phase-6-ai-models-treasury.md]
doc_sync_status: n/a
found_in: ""
created: 2026-11-20
updated: 2026-11-20
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P6-T077 · D14 scenario-twin report view and recent simulator runs

## Goal / expected outcome

D14 gets the **Scenario twin** view (`/journal/reviews/scenario-twin`): per bot and per simulated scenario for each week, the scenario (source event, sentiment path, injected shocks), the twin's P&L, drawdown and risk rules hit next to the real paper run, plus a list of recent simulator runs. Everything is labelled **Simulated** and stays out of journal totals, so the weekly review (P7) can read it and exit criterion 5 can be shown.

## Context & references

- Roadmap: [R6.40](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.33](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.37 · exit criterion 5
- UI: [D14](../../../docs/ui/dashboards/D14-journal.md) (Scenario twin section, route `/journal/reviews/scenario-twin`, query `/sim/twin/reports`; rule 4 "Simulated stays separate")
- Canonical: [18 §2.4](../../../docs/18-platform-and-deployment.md#24-scenario--crowd-simulator-m14-a-go-live-tool) · [16 §2.14b](../../../docs/16-configuration-and-safety-model.md#214b-scenario--crowd-simulator-m14)
- Cross-phase: P0-T048 (typed API + WS client), P0-T049 (component library: tiles, states, chips), P3-T040 (D14 Journal page)
- Depends on (this phase): P6-T075 (reports and `/sim/twin/reports`); P6-T050's `/sim/runs` for the runs list

## Requirements

- Route `/journal/reviews/scenario-twin` in D14; week picker; per-bot table (scenario, twin P&L, max drawdown, rules hit, time to flat, vs baseline and real paper); per-scenario detail (source event, sentiment path chart, shock vector and any clamp).
- "Recent simulator runs" list from `GET /sim/runs` (seed, event, status, wall time).
- Every number labelled **Simulated** (chip + legend); never summed into journal totals, analytics, exports or tax (D14 rule 4).
- States: empty ("Scenario twin not running yet"), loading, error, and "baseline mismatch" flag.
- Read-only view: no commands except opening the scenario in D06 Stress when that tab exists (P7).
- Viewport matrix and axe like every D-screen.

## ToDo

- [ ] Route, week picker, per-bot table and scenario detail using the generated API client.
- [ ] Simulated chip/legend in the component library if missing.
- [ ] Recent simulator runs list.
- [ ] Empty/loading/error/mismatch states.
- [ ] Playwright + axe tests; docs.

## Verification

### Tests
- `pnpm test` (components, Simulated labelling) and `pnpm playwright` (view on fixture reports; viewport matrix; axe).

### Scenarios
- Given two bots and three scenarios in a week, when the view opens, then six rows show with Simulated labels and the real paper column alongside.
- Given no twin reports yet, then the empty state reads "Scenario twin not running yet".
- Given the journal totals page, then no twin number appears there.

### Stress / failure injection
- 52 weeks × 20 bots × 4 replays of fixture data: the table paginates and stays responsive (first paint < 1 s on the dev workstation).

## Acceptance criteria

- [ ] D14 shows the scenario-twin report per bot and per scenario, labelled Simulated.
- [ ] Recent simulator runs listed.
- [ ] Twin numbers never appear in journal totals (test).
- [ ] CI green (`pnpm test`, `pnpm playwright`, axe, viewport matrix).

## Exceptions & edge cases

- Weeks before the twin existed show the empty state, not zeros.
- A bot deleted since the week ran is still shown by its version id.

## Cardinal rules (do NOT)

- Do NOT mix simulated numbers into journal totals, analytics, exports or tax.
- Do NOT add commands that could trade or change risk from this view.
- Do NOT call the database from the browser; everything goes through `mt-api`.
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral/broker IDs in vendored code.

## Doc sync on completion

- `docs/ui/dashboards/D14-journal.md`: remove the "_(added)_" marks once built; confirm fields.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.37 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T077-d14-scenario-twin-report-view-and-recent-simulat`
- PR title: `P6-T077: D14 scenario-twin report view and recent simulator runs`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T077` run

## Progress log

- 2026-11-20 01:11 · cloud:vm:be04b6ae61f8 · created
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (new task for the scenario & crowd simulator workstream, 18 §2.4)
