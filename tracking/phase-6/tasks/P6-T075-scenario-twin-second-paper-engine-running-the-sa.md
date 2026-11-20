---
id: P6-T075
kind: task
title: Scenario twin: second paper engine running the same bots under injected scenarios
phase: 6
type: BUILD
status: backlog
priority: high
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P6-T050, P2-T021, P2-T023, P2-T036]
requirements: [R6.33, R6.34]
roadmap_todos: [T6.36]
modules: [M14, M12, M11, mt-crowdsim, mt-engine]
dashboards: [D14, D06]
tools: [git, cargo, docker, supabase]
mcp: []
env: []
services: [supabase-postgres, nats]
branch: p6/P6-T075-scenario-twin-second-paper-engine-running-the-sa
pr: ""
doc_sync: [docs/03-build-spec.md, docs/02-v1-architecture.md, docs/18-platform-and-deployment.md, docs/roadmap/phase-6-ai-models-treasury.md]
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

# P6-T075 · Scenario twin: second paper engine running the same bots under injected scenarios

## Goal / expected outcome

A **scenario twin** runs: a second, paper-only `mt-engine` on simulated venues replays the week's recorded live data with the `mt-crowdsim` scenarios (P6-T050) injected, runs the same bots (same pinned strategy versions, params and `mt-risk` policy) and writes a **weekly report per bot**: the twin's P&L, drawdown and risk rules hit under each scenario, next to the real paper run for the same week. The report feeds the P7 weekly review pack (R7.03) and the scenarios join the pre-live stress tests (R7.16). The twin never touches the real paper or live accounts and all its output is `synthetic = true`. It is built early (18 §2.4) so it can join the 8-week paper period from its first weeks.

## Context & references

- Roadmap: [R6.33](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · [R6.34](../../../docs/roadmap/phase-6-ai-models-treasury.md#3-requirements) · ToDo T6.36 · exit criterion 5 ([§6](../../../docs/roadmap/phase-6-ai-models-treasury.md#6-exit-criteria-demo))
- Canonical: [18 §2.4](../../../docs/18-platform-and-deployment.md#24-scenario--crowd-simulator-m14-a-go-live-tool) · defaults [16 §2.14b](../../../docs/16-configuration-and-safety-model.md#214b-scenario--crowd-simulator-m14) (`crowdsim.scenario_twin.enabled`, `crowdsim.scenarios_per_week`, `crowdsim.max_shock`) · decision [17 §H](../../../docs/17-decisions-register.md#h-rust-max-borrowed-code-rebuilt-in-rust-scenario-simulator-copyleft-register-2026-11-20)
- Spec: [03 M14](../../../docs/03-build-spec.md#m14-scenario--crowd-simulator-go-live-tool) · flow [02 F12](../../../docs/02-v1-architecture.md#8-end-to-end-flows) steps 3–4 · data rules [12 §5](../../../docs/12-policy-and-compliance.md#5-data-provenance-tagging-one-mechanism-for-all-data-terms) (synthetic rows)
- UI: [D14](../../../docs/ui/dashboards/D14-journal.md) Scenario twin (`/sim/twin/reports`, P6-T077) · [D06](../../../docs/ui/dashboards/D06-risk.md) Stress tab (simulated scenarios, P7-T068)
- Cross-phase: P2-T021 (`mt-engine` TradingNode wrapper, intent actor), P2-T023 (sandbox simulated venue), P2-T036 (bot model and versions). The recorded Parquet catalog from P1 and the P2 replay path (P2-T105) are reused where present
- Depends on (this phase): P6-T050 (scenarios)
- Downstream: P6-T076 (containers, network isolation, settings seed), P6-T077 (D14 view), P6-T078 (isolation tests), P6-T079 (dry run), P6-T080 (weekly runs), P7-T015 (weekly review pack reads the reports), P7-T069 (stress replay uses the scenarios)

## Requirements

- **Engine:** a separate `mt-engine` instance in `scenario-twin` mode: sandbox simulated venues only (P2-T023 fill model), no venue adapters with keys, the same `mt-risk` crate linked in, its own NATS account and its own database role.
- **Same bots:** at the start of each twin week it snapshots every active paper bot (strategy version, params, scope, sleeve, risk policy version) read-only; the twin runs those versions unchanged. Bot changes during the week are picked up next week.
- **Replay:** the week's recorded market data (Parquet catalog and bars through `pit(as_of)`) replayed in time order; each scenario's shock vector applied from its onset with its decay (price path shift, volatility scaling, spread widening, depth reduction), clamped again to `crowdsim.max_shock` (defence in depth).
- **Runs per week:** one baseline replay (no shock; it must track the real paper run within the P2 parity tolerance, else the report is flagged) plus one replay per scenario (default 3, `crowdsim.scenarios_per_week`).
- **Report per bot:** per scenario: P&L, max drawdown, exposure peaks, risk rules hit (M11 rejects, kill-criteria trips, protective exits), time to flat, vs the baseline and the real paper run; stored in `risk.twin_report` (insert-only, `synthetic = true`, `train_ok = false`, `model_input_ok = false`); `GET /sim/twin/reports` through `mt-api`; `sim.twin.report.ready` event for the weekly review pack.
- **Boundaries (R6.34):** it never trades the real paper or live accounts; it holds no venue keys and has no route to the signer; it cannot publish to the real engine's `ord.*` subjects; twin numbers never enter the journal, analytics, tax, features, training or RAG.
- **Settings:** runs only while `crowdsim.scenario_twin.enabled` is on (default: during the paper period and before live); nothing hard-coded.
- **Gate status:** an extra input, never a gate unless 16 says so.

## ToDo

- [ ] `scenario-twin` engine mode in `mt-engine` (sandbox venues only; startup refuses if any keyed adapter or signer endpoint is configured).
- [ ] Weekly bot snapshot (read-only) and replay driver over the week's data.
- [ ] Shock injector (price/volatility/spread/liquidity with onset and decay) with the second clamp.
- [ ] Baseline replay and parity check against the real paper run.
- [ ] SQL migration in `supabase/migrations/` for `risk.twin_run` and `risk.twin_report` (insert-only, synthetic flags with check constraints); twin database role limited to those tables.
- [ ] Report builder per bot; `/sim/twin/reports` query in `mt-api`; `sim.twin.report.ready` event.
- [ ] Tests (see Verification); docs.

## Verification

### Tests
- `cargo test -p mt-engine scenario_twin` and `cargo test -p mt-crowdsim`; `cargo clippy`; `supabase test db` (twin role can't write `journal.*`, `strategy.*` or real `risk.*` policy tables; synthetic flags enforced).
- Unit: shock injector on a fixture bar series (each shock kind, onset, decay, clamp).
- Integration: one fixture day, two bots, one scenario → a baseline run, a shocked run and two report rows; the real paper engine's orders and fills are untouched.
- Startup guard: twin mode with a keyed venue adapter configured refuses to start.

### Scenarios
- Given a −12% price shock with spread ×3 on BTC, when the twin replays the week, then a trend bot's report shows the drawdown, the M11 rules it hit and its time to flat, labelled Simulated.
- Given a scenario whose shock exceeds `crowdsim.max_shock`, then the injector clamps it and records the clamp.
- Given the baseline replay drifts from the real paper run beyond the parity tolerance, then the week's report is flagged "baseline mismatch" rather than hidden.

### Stress / failure injection
- One week × 10 bots × 4 replays completes within the weekly window on the workstation CPU profile; record wall time.
- Kill the twin mid-replay: it restarts the interrupted replay from the start (idempotent by run id) and writes no partial report.

## Acceptance criteria

- [ ] The twin runs the same bot versions on replayed data with scenarios injected and writes one report row per bot per scenario.
- [ ] No twin output reaches the real paper/live accounts, the journal or any training/feature/RAG path (tests).
- [ ] Reports are readable through `/sim/twin/reports`.
- [ ] CI green (`cargo test`, `cargo clippy`, `supabase test db`, `pit` bypass check).

## Exceptions & edge cases

- A bot whose venue has no recorded data that week is reported as "no replay data", not as flat P&L.
- Paper weeks before the twin exists simply have no twin report (18 §2.4).
- A strategy in Python on the Python node (research only): the twin runs it on the same node type; if that node isn't available it is listed as skipped.

## Cardinal rules (do NOT)

- Do NOT give the twin venue keys, a signer route or the real engine's order subjects; it never trades real paper or live accounts.
- Do NOT bypass `mt-risk`: the twin runs the same risk checks as the real engine.
- Do NOT let twin numbers enter the journal, analytics, exports, tax, features, model training, RAG or memory (`synthetic = true`).
- Do NOT inject shocks outside `crowdsim.max_shock` or hard-code any setting.
- Do NOT UPDATE or DELETE WORM rows (`audit.*`, `journal.*`, policy changes); corrections are new rows referencing the original (15 §2).
- Do NOT commit secrets or paste them into chats/issues/PRs; secrets live only in the sops/age file (07 §2).
- Do NOT skip, weaken or delete a test to get green; pin images by digest.

## Doc sync on completion

- `docs/03-build-spec.md` M14: twin runs per week, report fields.
- `docs/02-v1-architecture.md` §5/§7 and F12: `risk.twin_run`, `risk.twin_report`, `/sim/twin/reports`, `sim.twin.*` subjects.
- `docs/18-platform-and-deployment.md` §2.4: confirm the twin boundaries as built.
- `docs/roadmap/phase-6-ai-models-treasury.md`: tick T6.36 (and note this task ID) once all items covering it are done.

## Branch & PR

- Branch: `p6/P6-T075-scenario-twin-second-paper-engine-running-the-sa`
- PR title: `P6-T075: Scenario twin: second paper engine running the same bots under injected scenarios`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P6-T075` run

## Progress log

- 2026-11-20 01:08 · cloud:vm:be04b6ae61f8 · created
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (filled from the stub: scenario twin per 18 §2.4 and 16 §2.14b; depends on P6-T050 and the P2 paper engine, sandbox venue and bots only)
