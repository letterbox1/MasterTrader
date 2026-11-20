---
id: P7-T069
kind: task
title: Stress replay of the four historical shocks plus simulated scenarios before the first funding
phase: 7
type: VERIFY
status: backlog
priority: critical
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P7-T068, P7-T014, P6-T075, P6-T050]
requirements: [R7.16]
roadmap_todos: [T7.66]
modules: [M11, M7]
dashboards: [D06, D03]
tools: [git, cargo]
mcp: []
env: []
services: [supabase-postgres, nats, mt-api, backtest-worker]
branch: p7/P7-T069-stress-replay-of-the-four-historical-shocks-befo
pr: ""
doc_sync: [docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-7-prove-and-go-live.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-22
updated: 2026-11-20
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P7-T069 · Stress replay of the four historical shocks plus simulated scenarios before the first funding

## Goal / expected outcome

Before any money is funded (P7-T057), each bot going live is replayed through the four historical shocks **and the simulated `mt-crowdsim` scenarios** (R6.32, from the scenario twin P6-T075) at its starting allocation, together with the portfolio as it will stand after funding, and the results are attached to that strategy's gate report so you fund knowing the worst historical outcome and how the bot fares under shocks the market hasn't produced yet. The historical replay must pass; simulated results are reported alongside and don't gate (16 §2.14b).

## Context & references

- Roadmap: [R7.16 · ToDo T7.66](../../../docs/roadmap/phase-7-prove-and-go-live.md) (run before live capital; results attached to the gate report)
- Spec: [14 §3](../../../docs/14-strategy-evidence-and-validation.md#3-strategy-catalogue-evidence-ranked-templates) (stress-test against May 2022, Nov 2022, Aug 2024, Feb–Mar 2026) · [16 §2.1](../../../docs/16-configuration-and-safety-model.md#21-risk-sizing-and-drawdown) (drawdown stages and basis) · [16 §2.5](../../../docs/16-configuration-and-safety-model.md#25-capital-steps-per-sleevebot) (starting allocation default A$2,000 per bot)
- Related: P7-T068 (stress engine), P7-T014 (gate report storage), P7-T057 (funding waits on this), P7-T067 (D06 Live shows the attached result)
- Simulated scenarios: P6-T075 (scenario twin, R6.33) exports the latest `mt-crowdsim` scenarios in the `risk.stress.run` format ([18 §2.4](../../../docs/18-platform-and-deployment.md#24-scenario--crowd-simulator-m14-a-go-live-tool) · [16 §2.14b](../../../docs/16-configuration-and-safety-model.md#214b-scenario--crowd-simulator-m14))

## Requirements

- For each bot planned for funding: `risk.stress.run` with all four historical scenarios plus the simulated scenarios the twin recorded during the bot's paper period (`crowdsim.scenarios_per_week` a week, each capped by `crowdsim.max_shock`; no new setting), `positions: hypothetical_allocation` at the bot's starting allocation (from its strategy settings; default A$2,000), plus one portfolio run including existing live positions (none for the first funding).
- Attach the run ids to the latest gate report (a new gate-report row referencing them; never an edit) and show them in D03 Gates / D06 Live.
- Simulated results are shown in a separate **Simulated** block of the gate report: informational, flagged red/amber the same way so you can see them, but they never block funding (16 §2.14b sets no gate).
- Flag in red any historical scenario whose replay crosses the system stage-2 drawdown (default 25%) or the sleeve halt (default 15%) at the planned allocation; you see the flags before funding and can tighten the allocation or limits (tightening is free). Thresholds are read from the effective policy, never hard-coded.
- Re-run whenever the strategy version, starting allocation or risk policy changes before funding.

## ToDo

- [ ] Run the replay (historical + simulated) for each bot planned in P7-T057 and the portfolio run.
- [ ] Attach run ids to the gate report (new row) and confirm D03/D06 show them.
- [ ] Record per scenario: P&L, peak-to-trough, limits that would fire, proxies used, in the progress log.
- [ ] File a bug for any `incomplete` scenario (missing data without proxy) before funding.

## Verification

### Tests
- Integration: the gate-report row for the strategy references four historical `risk.stress_run` ids plus the simulated run ids (labelled Simulated) with matching policy version and allocation.
- Check: the funding check reads only the historical results; a red simulated result shows in P7-T057's checklist as information, not a blocker.
- Check: every scenario `complete` (no silent zero P&L; proxies labelled).

### Scenarios
- Given trend-on-majors at A$2,000, when the Nov 2022 replay shows a 12% drawdown, then it is shown amber (below the 15% sleeve halt) and funding can proceed.
- Given a replay crosses the 25% system stage 2, then the gate report shows it red and P7-T057 lists it in the pre-funding checklist.

### Stress / failure injection
- n/a: this item is itself the stress exercise; engine failure modes are covered by P7-T068's tests.

## Acceptance criteria

- [ ] All four historical scenarios and the simulated scenarios replayed for every bot planned for funding and for the portfolio; results attached to the gate reports, simulated ones labelled.
- [ ] Any red flag acknowledged in the progress log before P7-T057 starts.

## Exceptions & edge cases

- Scenario window data missing for a new instrument: proxy per P7-T068 (labelled); if no sensible proxy, the bot is not funded until resolved.
- Strategy version changes after the replay: the old results no longer count; re-run.

## Cardinal rules (do NOT)

- Do NOT fund (P7-T057) before the replay results are attached.
- Do NOT weaken a gate, threshold or window to "get live sooner" (roadmap §1, Out).
- Do NOT update or delete WORM rows; corrections are new rows with `supersedes_id` (15 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.
- Do NOT use keys that are not trade-only, IP-locked and withdrawal-disabled; no live money before the P7 gates pass.

## Doc sync on completion

- `docs/14-strategy-evidence-and-validation.md` §3: note that the replay runs before each funding (no figures beyond the report).
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.66 when this item is done.

## Branch & PR

- Branch: `p7/P7-T069-stress-replay-of-the-four-historical-shocks-befo`
- PR title: `P7-T069: Stress replay of the four historical shocks plus simulated scenarios before the first funding`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T069` run

## Progress log

- 2026-10-22 02:12 · cloud:vm:be04b6ae61f8 · created
- 2026-10-22 00:00 · aligner · created for docs/16–17 (R7.16/T7.66: stress replay before the first funding at the per-bot starting allocation, results attached to the gate report)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (services supabase-postgres)
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (R7.03/R7.16/T7.66: simulated `mt-crowdsim` scenarios from the twin run alongside the four historical shocks (+P6-T075), reported, not gating; title; tools uv → cargo)
- 2026-11-20 00:00 · main · depends on P6-T050 (scenario simulator / weekly twin run) per 17 §H.
