---
id: P7-T067
kind: task
title: Phase 7 API surface and D06 Live and D03 Go-live views
phase: 7
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T011, P7-T014, P7-T016, P7-T019, P7-T020, P7-T022]
requirements: [R7.15]
roadmap_todos: [T7.26]
modules: [M15, M11, M17]
dashboards: [D06, D03, D14, D16]
tools: [git, uv, pnpm, node>=20, docker]
mcp: []
env: []
services: [postgres, nats, mt-api]
branch: p7/P7-T067-phase-7-api-surface-and-d06-live-and-d03-go-live
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/ui/dashboards/D06-risk.md, docs/ui/dashboards/D03-strategies.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-22
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P7-T067 · Phase 7 API surface and D06 Live and D03 Go-live views

## Goal / expected outcome

Every piece of Phase 7 state (capital steps, kill-criteria state, kill and lock state, gate reports, weekly reviews, preflight) is reachable through `mt_api` exactly as catalogued in 02 §7, contract-tested with the right confirmation levels, and shown in the **D06 Live tab** and the **D03 Go-live tab**, on desktop and phone.

## Context & references

- Roadmap: [R7.15 · ToDo T7.26](../../../docs/roadmap/phase-7-prove-and-go-live.md)
- API: [02 §7](../../../docs/02-v1-architecture.md#7-api-contract-mt_api) queries `/risk/capital-steps`, `/risk/kill-criteria`, `/strategies/{id}/gate-report`, `/journal/reviews`, `/system/preflight`; commands `lab.gate_report.generate` (C1), `risk.capital.fund` (C3), `risk.capital_step.approve` (C3), `risk.sleeve.restart` (C3), `risk.review.close` (C3), `journal.review.signoff` (C1), `ops.drill.record` (C1) · [02 §7.2](../../../docs/02-v1-architecture.md#72-commands-rest-write) (C1–C3 tokens)
- UI: [D06 Live tab](../../../docs/ui/dashboards/D06-risk.md) (CapitalStepCard, Kill criteria, Kill and lock state, Gate reports; hidden until the first bot goes live) · [D03](../../../docs/ui/dashboards/D03-strategies.md) Go-live tab (per bot: starting allocation, current step, clean weeks, kill criteria, last weekly review) · [D14](../../../docs/ui/dashboards/D14-journal.md) Weekly reviews · [DESIGN.md §6.8](../../../DESIGN.md#68-test-matrix-every-screen-must-pass)
- Defaults shown: [16 §2.5](../../../docs/16-configuration-and-safety-model.md#25-capital-steps-per-sleevebot) (starting allocation default A$2,000 per bot; clean week; +25% of current; step-down) · [16 §2.6](../../../docs/16-configuration-and-safety-model.md#26-decay-and-kill-signals-one-meaning-each) · [16 §2.1](../../../docs/16-configuration-and-safety-model.md#21-risk-sizing-and-drawdown) (system drawdown stages, 30-day lock)
- Decision: [17 §D P7-B008](../../../docs/17-decisions-register.md#d-other-decisions)
- Related (they build the pieces this task composes): P7-T011 (preflight + `ops.drill.record`), P7-T014 (gate report API + D03 Gates), P7-T016 (`/journal/reviews`, D14 Reviews), P7-T018/T019 (capital steps, `CapitalStepCard`, C3 approval), P7-T020 (kill-criteria evaluations), P7-T022 (lock state, `risk.review.close`)

## Requirements

- **Query `/risk/kill-criteria`** (new here): per sleeve and bot, each written criterion (from the manifest) with observed vs threshold, state `ok | warning | halted`, last evaluation, plus the decay signals with their single meaning (rolling 60-trade Sharpe/hit rate or CUSUM or 5 losses → downgrade to HITL; health check fail → halt the bot; kill criterion → halt the sleeve + step down; unexplained recon > 24 h → halt everything).
- **Query `/risk/capital-steps`** read model published from P7-T018 state: starting allocation (per bot, from its strategy settings, default A$2,000), current allocation, step, clean weeks in a row (of 4), current-week checklist, next step (+25% of current, capped at the sleeve target), step-down history.
- **`/risk/state`** carries the kill and lock state: system drawdown stage (none / 1 / 2), 30-day review-lock countdown, count of stage-2 events.
- **Contract tests** for every Phase 7 query and command in 02 §7: schema, auth, and server-computed confirmation level (C3 commands reject without the Telegram + TOTP + cool-down path; `428` without a confirm token).
- **WebSocket:** Phase 7 events ride the existing `risk.event` and `kill` topics (step proposed/applied/stepped-down, criterion warning/breach, lock start/end); no new topic unless 02 §7.3 lists it.
- **D06 Live tab** (`/risk` → Live): `CapitalStepCard` per sleeve/bot, Kill-criteria table, Kill-and-lock panel, Gate-reports list (links to D03 Gates); actions: fund the starting allocation (`risk.capital.fund`, C3), approve a step (`risk.capital_step.approve`, C3), restart a sleeve (`risk.sleeve.restart`, C3), close a review lock (`risk.review.close`, C3). Hidden until the first bot goes live.
- **D03 Go-live tab** per bot: starting allocation field (an L4 strategy setting, default A$2,000, suggested A$2–5k; set when the bot goes live; tighten C1, loosen C3), current step, clean weeks, kill criteria and state, last weekly review link, preflight status.
- Every value renders from the API with its layer and default (16 §1); nothing hard-coded in the UI.

## ToDo

- [ ] `/risk/kill-criteria` endpoint + OpenAPI schema; `/risk/state` lock fields.
- [ ] `/risk/capital-steps` read model wiring (from P7-T018 tables) + OpenAPI.
- [ ] Contract test suite `tests/api/test_phase7_catalogue.py` covering all Phase 7 queries/commands and their confirmation levels.
- [ ] D06 Live tab route and panels, composing `CapitalStepCard` (P7-T019) and the kill-criteria panel (P7-T020).
- [ ] D03 Go-live tab (starting allocation setting via `risk.policy.update` on L4, step, kill criteria, review link, preflight).
- [ ] Playwright for both tabs on the §6.8 viewport matrix + axe; phone ≤ 3 taps to the C3 confirmation for a step.
- [ ] Docs.

## Verification

### Tests
- Contract: every Phase 7 endpoint in 02 §7 exists with the documented confirmation level; a command missing from the catalogue fails the test.
- Integration: `/risk/kill-criteria` returns `warning` when shortfall is 1.6× modelled and `halted` after a breach (fixture evaluations from P7-T020).
- Integration: raising a bot's starting allocation above the current value is classified C3; lowering it is C1 and immediate.
- Playwright: D06 Live and D03 Go-live at 280×653, 375×667, 568×320 and desktop; axe clean.

### Scenarios
- Given no bot is live, when you open D06, then the Live tab is hidden.
- Given a sleeve in a 30-day review lock, then the Kill-and-lock panel shows the countdown and `risk.review.close` is disabled until day 30.
- Given a step proposal, when you tap it on the phone, then the C3 flow (Telegram approve + TOTP) starts within 3 taps.

### Stress / failure injection
- `mt-api` restart while the Live tab is open: WS gap re-sync (seq) restores state with no stale counts; 50 sleeves × 10 criteria render < 1 s.

## Acceptance criteria

- [ ] All Phase 7 queries/commands from 02 §7 implemented and contract-tested with the right confirmation levels.
- [ ] D06 Live and D03 Go-live tabs live on the viewport matrix.
- [ ] Starting allocation is a per-bot setting with default A$2,000 (16 §2.5), never hard-coded.
- [ ] CI green.

## Exceptions & edge cases

- Bot moved to another sleeve: capital-step history stays with the bot; the sleeve view shows both.
- Gate report stale (> 7 days): Live tab shows it amber with "regenerate" (`lab.gate_report.generate`, C1).

## Cardinal rules (do NOT)

- Do NOT add API paths or commands that aren't in 02 §7; raise a doc gap instead.
- Do NOT let loosening risk, autonomous mode or a capital step apply without C3 (Telegram + TOTP + cool-down); protective exits never wait for approval.
- Do NOT bypass `mt_api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT update or delete WORM rows; corrections are new rows with `supersedes_id` (15 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/02-v1-architecture.md` §7: confirm the Phase 7 entries match what shipped.
- `docs/ui/dashboards/D06-risk.md`: Live tab as built.
- `docs/ui/dashboards/D03-strategies.md`: Go-live tab as built.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.26 when this item is done.

## Branch & PR

- Branch: `p7/P7-T067-phase-7-api-surface-and-d06-live-and-d03-go-live`
- PR title: `P7-T067: Phase 7 API surface and D06 Live and D03 Go-live views`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T067` run

## Progress log

- 2026-10-22 02:12 · cloud:vm:be04b6ae61f8 · created
- 2026-10-22 00:00 · aligner · created for docs/16–17 (R7.15/T7.26: Phase 7 API catalogue + D06 Live / D03 Go-live, 17 §D P7-B008, starting allocation per bot default A$2,000)
