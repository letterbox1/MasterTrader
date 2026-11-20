---
id: P7-T068
kind: task
title: D06 Stress tab and risk.stress.run: historical shock replay plus simulated mt-crowdsim scenarios
phase: 7
type: BUILD
status: backlog
priority: high
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P2-T043, P2-T015, P2-T103]
requirements: [R7.16]
roadmap_todos: [T7.27]
modules: [M11, M7, M15]
dashboards: [D06]
tools: [git, cargo, pnpm, node>=20, docker, supabase]
mcp: []
env: []
services: [supabase-postgres, nats, mt-api, backtest-worker]
branch: p7/P7-T068-d06-stress-tab-and-risk-stress-run-historical-sh
pr: ""
doc_sync: [docs/ui/dashboards/D06-risk.md, docs/03-build-spec.md, docs/14-strategy-evidence-and-validation.md, docs/roadmap/phase-7-prove-and-go-live.md]
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

# P7-T068 · D06 Stress tab and risk.stress.run: historical shock replay plus simulated mt-crowdsim scenarios

## Goal / expected outcome

The D06 Stress tab replaces the Phase 2 placeholder: `risk.stress.run` (C1) replays the four historical shocks (May 2022, Nov 2022, Aug 2024, Feb–Mar 2026) **plus simulated scenarios from the scenario & crowd simulator** (`mt-crowdsim`, R6.32, capped by `crowdsim.max_shock`) against **current positions and the current risk policy**, and shows P&L impact by position/bot/sleeve/venue, which limits would trigger, liquidation distances and hedge coverage, with every run stored for the gate report. Simulated results are labelled as such and reported alongside; only the historical replay is a pass/fail input (16 §2.14b sets no gate on simulated results).

## Context & references

- Roadmap: [R7.16 · ToDo T7.27](../../../docs/roadmap/phase-7-prove-and-go-live.md) (replaces the P2 placeholder R2.57/T2.38)
- UI: [D06 Stress tab](../../../docs/ui/dashboards/D06-risk.md) (scenarios, run `risk.stress.run` C1, results, history; placeholder never shows sample numbers)
- Spec: [14 §3](../../../docs/14-strategy-evidence-and-validation.md#3-strategy-catalogue-evidence-ranked-templates) (stress-test trend and carry against May 2022, Nov 2022, Aug 2024, Feb–Mar 2026) · [02 §7](../../../docs/02-v1-architecture.md#7-api-contract-mt_api) (`/risk/stress`, `risk.stress.run` C1) · [16 §2.1](../../../docs/16-configuration-and-safety-model.md#21-risk-sizing-and-drawdown) (sleeve and system drawdown stages, daily loss, venue concentration used for "limits triggered")
- Decision: [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) (stress tab moved to P7) · [17 §H](../../../docs/17-decisions-register.md#h-rust-max-borrowed-code-rebuilt-in-rust-scenario-simulator-copyleft-register-2026-11-20) (simulator is a go-live tool; its scenarios join the stress tests)
- Simulator: [18 §2.4](../../../docs/18-platform-and-deployment.md#24-scenario--crowd-simulator-m14-a-go-live-tool) · [16 §2.14b](../../../docs/16-configuration-and-safety-model.md#214b-scenario--crowd-simulator-m14) · scenarios produced by P6-T050 (`mt-crowdsim`) and exported by the scenario twin (P6-T075) in the format this task defines (T6.36)
- Cross-phase: P2-T043 (Stress tab placeholder and route), P2-T015 (portfolio risk: clusters, concentration, VaR/ES), P2-T103 (point-in-time dataset builder); historical bars come from the P1 backfills via `pit(as_of)`.
- Related: P7-T069 (VERIFY: replay before the first funding, results attached to the gate report), P7-T014 (gate report)

## Requirements

- **Scenarios** in `config/stress_scenarios.yaml` (configurable defaults, versioned): `may_2022` (Terra/LUNA), `nov_2022` (FTX), `aug_2024` (yen carry unwind), `feb_mar_2026`; each = date window + asset-class coverage. Exact window dates are defaults to confirm (U) from recorded data before first use; changing them is a recorded settings change.
- **Simulated scenarios:** `kind: simulated` entries read from the shared `Scenario` type in `mt-core` (sentiment path + price, volatility, spread and liquidity shocks, seed and run id); every shock is clamped to `crowdsim.max_shock` (default price ±15%, volatility ×3, spread ×5, liquidity ÷5, read from settings, never hard-coded); results carry `synthetic = true` and the label **Simulated**. Built and tested on fixture scenarios; real ones arrive from P6-T075, so this task doesn't wait on Phase 6.
- **Replay method:** for each current position, apply the instrument's own historical return path over the window (from `pit` bars); instruments without history in the window use a labelled proxy (beta to BTC/ETH or the asset-class index), never silently zero. Replay runs the **current** risk policy (sleeve/system drawdown stages, daily loss, venue cap, stops at their current levels with gap-through at the bar's worst price) to report which rules would fire and when.
- **Simulated replay:** apply the scenario's shocks to each position's current price, volatility, spread and depth over the scenario's horizon, running the same dry-run M11 evaluators; liquidity ÷N widens slippage and stop gap-through accordingly.
- **Outputs** per run: P&L by position/bot/sleeve/venue, peak-to-trough on the 16 §2.1 drawdown basis, limits that would trigger (with time), liquidation distances for leveraged positions, hedge coverage, proxies used. Stored in `risk.stress_run` (WORM: inputs hash, policy version, positions snapshot, results).
- **API:** `risk.stress.run {scenarios[], scope: portfolio|sleeve|bot, positions: current|hypothetical_allocation}` (C1); `/risk/stress` (runs, results). `hypothetical_allocation` lets P7-T069 replay a bot at its starting allocation before it holds live positions.
- **UI:** D06 Stress tab: scenario picker (Historical / Simulated groups), run button (C1), results table + per-sleeve bars, limits-triggered timeline, history; phone shows the summary card. Hypothetical preset shocks (e.g. −15% crypto in 60 s) are a later addition per D06, not in this task.
- Runs on the backtest worker; a 4-scenario portfolio run completes < 2 min; uses only PIT reads.

## ToDo

- [ ] `crates/mt-risk/src/stress/` (scenario loader for historical windows and simulated `mt-crowdsim` scenarios, replay engine, proxy mapper, `crowdsim.max_shock` clamp, limit-trigger simulator using the M11 evaluators in dry-run mode).
- [ ] SQL migration (`supabase/migrations/`) `risk.stress_run` (WORM) + `risk.stress.run` command + `/risk/stress` query.
- [ ] `config/stress_scenarios.yaml` with the four windows (dates marked U until confirmed from recorded data).
- [ ] D06 Stress tab (replace the placeholder), viewport matrix + axe.
- [ ] Tests; docs.

## Verification

### Tests
- `cargo test -p mt-risk stress` and `cargo clippy`; `supabase test db` (WORM on `risk.stress_run`); `pnpm test` and `pnpm playwright` (Stress tab).
- Golden: a fixture portfolio (BTC long, ETH long, AUD/JPY long) replayed over `aug_2024` reproduces the fixture P&L to the cent and flags the expected limit (sleeve stage 1).
- Unit: a simulated scenario with a −40% price shock is clamped to the `crowdsim.max_shock` cap (−15% by default) and the result is labelled Simulated with `synthetic = true`; simulated runs never set the pass/fail flag used by P7-T069.
- Unit: proxy mapping labels every proxied instrument; a missing-data instrument without a proxy fails the run (`incomplete`), never a zero P&L.
- Property: replay never mutates live state (M11 evaluators run in dry-run; no orders, no `risk.event` except `stress_run`).
- Playwright: Stress tab at §6.8 viewports; placeholder text gone; axe clean.

### Scenarios
- Given current positions on two venues, when you run all four scenarios, then the results show P&L by venue and which venue-concentration or drawdown rule would have fired.
- Given a bot with no live positions yet, when P7-T069 runs it at its starting allocation (A$2,000 default), then the replay sizes positions by the bot's sizing model at that allocation.
- Given a fixture `mt-crowdsim` scenario (exchange-hack headline: price −12%, spread ×4, liquidity ÷3), when you run it with the four historical shocks, then its results show under Simulated next to them and the limits it would trigger are listed.
- Given the scenario window has no recorded bars for an instrument, then the run shows the proxy used (or `incomplete`), never a silent zero.

### Stress / failure injection
- Run 4 scenarios × 50 positions × 5 sleeves concurrently with another lab job: < 2 min p95; backtest worker killed mid-run → run marked `failed`, nothing partial stored as complete.

## Acceptance criteria

- [ ] `risk.stress.run` (C1) and `/risk/stress` live; runs stored WORM with inputs hash and policy version.
- [ ] D06 Stress tab shows real results for the four historical shocks; no sample numbers ever.
- [ ] Simulated `mt-crowdsim` scenarios run through the same engine, clamped to `crowdsim.max_shock`, labelled Simulated and never used as a gate.
- [ ] Scenario windows are configuration, not code.
- [ ] CI green.

## Exceptions & edge cases

- Venue closed in part of the window (FX weekend, ETF holidays): gaps applied at reopen price.
- Leveraged positions: liquidation distance uses the venue's maintenance-margin rules from the registry; crypto derivatives remain ≤ 2× (L0).
- Hold-and-earn and vault excluded from the drawdown basis (16 §2.1), shown separately.

## Cardinal rules (do NOT)

- Do NOT place orders or change any live state from a stress run.
- Do NOT read data outside `pit(as_of)`, and do NOT use paid data to fill gaps.
- Do NOT show sample or made-up results in the UI.
- Do NOT present simulated results as historical, let them gate funding, or write them anywhere features, training or RAG read (18 §2.4).
- Do NOT bypass `mt-api`, the risk manager (M11) or `pit(as_of)`; every order goes through M11.
- Do NOT update or delete WORM rows; corrections are new rows with `supersedes_id` (15 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/ui/dashboards/D06-risk.md`: Stress tab as built (and the phase line now says P7, R7.16).
- `docs/03-build-spec.md` M11: stress replay.
- `docs/14-strategy-evidence-and-validation.md` §3: the confirmed scenario windows.
- `docs/roadmap/phase-7-prove-and-go-live.md`: tick T7.27 when this item is done.

## Branch & PR

- Branch: `p7/P7-T068-d06-stress-tab-and-risk-stress-run-historical-sh`
- PR title: `P7-T068: D06 Stress tab and risk.stress.run: historical shock replay plus simulated mt-crowdsim scenarios`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P7-T068` run

## Progress log

- 2026-10-22 02:12 · cloud:vm:be04b6ae61f8 · created
- 2026-10-22 00:00 · aligner · created for docs/16–17 (R7.16/T7.27: full D06 Stress tab + `risk.stress.run`, moved from the P2 placeholder per 17 §D)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (stress replay in Rust `crates/mt-risk/src/stress/` (M11 evaluators in dry-run); SQL migration in `supabase/`; tools cargo/supabase)
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (R7.16/T7.27: engine also replays simulated `mt-crowdsim` scenarios (clamped by `crowdsim.max_shock`, labelled Simulated, not a gate); fixture scenarios so no P6 dependency; title)
