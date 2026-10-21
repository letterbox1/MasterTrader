# Phase 2 · Strategy Framework, Risk Manager & Research Lab

| | |
|---|---|
| **Goal** | You can create **any strategy type on any timeframe**, backtest it with **measured costs**, validate it, and run it on **paper behind the risk manager**, controlled from the web UI and Telegram. |
| **Duration** | Weeks 7–11 |
| **Depends on** | P0 (`mt_api`, audit, shell), P1 (data, DQ status, measured costs) |
| **Unlocks** | **The paper clock starts here** (P1 sleeves need ≥ 8 weeks of paper before P7). P3 (fills to journal), P6 (lab + tier A for distillation), P7 |
| **Modules** | M0 strategy framework, M11 risk manager, M12 execution, M7 research lab, M6 core features, M21 tier A, M15 UI v1 + Telegram bot v1, MasterTradingBot shared libraries |
| **Containers** | `engine`, `backtest-worker`, `sandbox`, `telegram-bot` (commands) |
| **Dashboards** | [D01](../ui/dashboards/D01-cockpit.md) Cockpit, [D03](../ui/dashboards/D03-strategies.md) Strategies, [D04](../ui/dashboards/D04-research-lab.md) Research Lab, [D05](../ui/dashboards/D05-execution.md) Execution, [D06](../ui/dashboards/D06-risk.md) Risk |
| **Primary docs** | [03 M0](../03-build-spec.md#m0-strategy-framework--mt_strategy-strategy-agnostic-any-timeframe) · [03 M11](../03-build-spec.md#m11-risk-manager--mt_risk-built-in-user-inputs-via-uitelegram-later-mcp) · [03 M12](../03-build-spec.md#m12-execution--mt_engine) · [03 M7](../03-build-spec.md#m7-research-lab--mt_lab) · [03 §8](../03-build-spec.md#8-promotion-gates-per-strategy-configurable) · [14 §3](../14-strategy-evidence-and-validation.md#3-strategy-catalogue-evidence-ranked-templates) · [14 §4](../14-strategy-evidence-and-validation.md#4-trading-methods-enforced-in-code-defaults-user-editable-in-d06) · [14 §5](../14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11) · [14 §6](../14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) · [12 §3](../12-policy-and-compliance.md#3-exchange-conduct--self-trade-prevention) · [10 §4.3 tier A](../10-memory-rag-and-models.md#43-design) |

## 1. Scope

**In:** the strategy manifest, templates and lifecycle; the full risk manager (policy levels, sizing, sleeves, defaults, fallback ladder, venue registry, 2× cap, STP, kill and dead-man switches, change control, hard ceilings); Nautilus paper/testnet execution with custom Alpaca/OANDA/IG adapters; the lab (screening + truth backtests, the validation suite and its extensions, optimisation, MLflow, sandboxed generator); core features; tier A pipeline; UI v1 and Telegram v1; shared libraries for MasterTradingBot strategies.

**Out:** live money (P7), text/agent signals (P4/P6), tier B (P4/P6), MT5/cTrader execution (P7).

## 2. Entry criteria

- P1 exit criteria met; DQ status and measured costs are flowing.
- Testnet/practice **trade-only** keys exist (T2.03).

## 3. Requirements

### Strategy framework (M0)
| ID | Requirement | Source | Verified by |
|---|---|---|---|
| R2.01 | Nautilus `Strategy`/`Actor` base: one class runs unchanged in backtest, sandbox/paper and live | [03 M0](../03-build-spec.md#m0-strategy-framework--mt_strategy-strategy-agnostic-any-timeframe) | Parity test |
| R2.02 | Templates: scalping, intraday, EMA/MA, mean reversion, breakout, swing/position, grid/DCA, pairs, event, ML-signal, **deterministic rule-based**, funding carry, cross-sectional momentum, token unlock, memecoin momentum (paper-only) | [03 M0](../03-build-spec.md#m0-strategy-framework--mt_strategy-strategy-agnostic-any-timeframe), [14 §3](../14-strategy-evidence-and-validation.md#3-strategy-catalogue-evidence-ranked-templates) | Template tests |
| R2.03 | Any timeframe: ticks/quotes/trades/book deltas or any bar spec (time, tick, volume, value), multi-timeframe in one strategy | [03 M0](../03-build-spec.md#m0-strategy-framework--mt_strategy-strategy-agnostic-any-timeframe) | Template tests |
| R2.04 | Manifest schema incl. **counterparty**, **sleeve**, **kill criteria**, **benchmark**, risk-policy ref, mode; evidence/priority shown | [03 M0](../03-build-spec.md#m0-strategy-framework--mt_strategy-strategy-agnostic-any-timeframe), [14 §3](../14-strategy-evidence-and-validation.md#3-strategy-catalogue-evidence-ranked-templates) | Schema tests |
| R2.05 | **Never-build validator** rejects X/Never patterns (sniping, latency arb, copy-trading, prediction-market bots, sandwiching) | [14 §3](../14-strategy-evidence-and-validation.md#3-strategy-catalogue-evidence-ranked-templates) | Validator tests |
| R2.06 | Lifecycle draft → backtested → validated → paper → approve → auto, gate-checked and audited; `auto` is C3 | [02 F7](../02-v1-architecture.md#8-end-to-end-flows) | Lifecycle tests |
| R2.07 | Experimentation: sweeps, A/B on identical data, **shadow mode** | [03 M0](../03-build-spec.md#m0-strategy-framework--mt_strategy-strategy-agnostic-any-timeframe) | Lab run |

### Risk manager (M11)
| ID | Requirement | Source | Verified by |
|---|---|---|---|
| R2.10 | Default-deny pre-trade layer in front of Nautilus `RiskEngine`; **every order passes through it** whatever its source | [SPEC NN2](../../SPEC.md#non-negotiable-requirements), [03 M11](../03-build-spec.md#m11-risk-manager--mt_risk-built-in-user-inputs-via-uitelegram-later-mcp) | Bypass tests |
| R2.11 | Versioned policy at global, venue, strategy, instrument and portfolio levels | [03 M11](../03-build-spec.md#m11-risk-manager--mt_risk-built-in-user-inputs-via-uitelegram-later-mcp) | Policy tests |
| R2.12 | Sizing models: fixed, fixed-fractional, vol target, stop-distance, Kelly (quarter-Kelly ceiling, never `2p−1`, never stacked on vol targeting), risk parity | [14 §4](../14-strategy-evidence-and-validation.md#4-trading-methods-enforced-in-code-defaults-user-editable-in-d06) | Golden tests |
| R2.13 | **Sleeves** with own limits/kill switches and a **two-stage drawdown** (default 10% de-risk / 15% halt, configurable); exposure **netted per asset across sleeves**; `manual` sleeve for manual tickets | [14 §5](../14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11) | Golden tests |
| R2.14 | Default hard limits table (risk/trade, max position, daily loss, DD 15% sleeve / 10% system, open positions, stale data, decision deadline, API-error pause, venue concentration, leverage) | [14 §5](../14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11) | Golden tests |
| R2.15 | **Fallback ladder** (6 rungs) live in D06 | [03 M11](../03-build-spec.md#m11-risk-manager--mt_risk-built-in-user-inputs-via-uitelegram-later-mcp), [14 §5](../14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11) | Ladder tests |
| R2.16 | Pre-trade checks: limits, price collar, liquidity/spread (M16), duplicate (idempotent IDs), event blackout hook, **DQ status** | [03 M11](../03-build-spec.md#m11-risk-manager--mt_risk-built-in-user-inputs-via-uitelegram-later-mcp), [SPEC NN3](../../SPEC.md#non-negotiable-requirements) | Unit tests |
| R2.17 | **Venue registry check** on every order; **2× crypto-derivatives cap** | [12 §2](../12-policy-and-compliance.md#2-venue-access-registry), [12 §1](../12-policy-and-compliance.md#1-australian-boundary-the-load-bearing-assumption) | Rejection tests |
| R2.18 | Kill switch (manual + automatic triggers) and **dead-man's switch** (heartbeats) | [02 F6](../02-v1-architecture.md#8-end-to-end-flows) | Drill |
| R2.19 | Change control: tighten instantly; loosen = C3 (Telegram + TOTP + cool-down); **hard-ceilings file no API can write**; versioned with rollback | [02 F5](../02-v1-architecture.md#8-end-to-end-flows), [07 §6](../07-security-notes.md#6-application-controls) | C3 tests |
| R2.20 | Modes per mandate/bot: paper / **hitl** (approval card per order, TTL, expiry = reject) / **autonomous** (C3, gates required); protective exits never wait for approval | [03 M11](../03-build-spec.md#m11-risk-manager--mt_risk-built-in-user-inputs-via-uitelegram-later-mcp) | Flow tests |
| R2.21 | Daily health check per sleeve (30-day Sharpe < ½ validated or DD > 1.5× backtest max → halt) and decay alerts (rolling 60-trade vs 5th percentile, CUSUM) | [14 §5](../14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11), [03 §8 item 8](../03-build-spec.md#8-promotion-gates-per-strategy-configurable) | Simulated decay |

### Execution (M12)
| ID | Requirement | Source | Verified by |
|---|---|---|---|
| R2.30 | Nautilus paper/sandbox on testnets/practice accounts; custom **Alpaca, OANDA, IG** adapters | [03 M12](../03-build-spec.md#m12-execution--mt_engine) | Adapter tests |
| R2.31 | **STP mode sent explicitly on every order**; STP cancels recorded as non-fills | [12 §3](../12-policy-and-compliance.md#3-exchange-conduct--self-trade-prevention) | Order audit |
| R2.32 | Idempotent client order IDs with a restart epoch; reconcile open orders before resuming | [03 M12](../03-build-spec.md#m12-execution--mt_engine) | Restart test |
| R2.33 | Execution methods: maker-first with timeout, TWAP/slicing > ~1% of 1-min volume, exit plan fixed at entry | [14 §4](../14-strategy-evidence-and-validation.md#4-trading-methods-enforced-in-code-defaults-user-editable-in-d06) | Sim tests |
| R2.34 | TCA per order (decision/arrival/VWAP, fees, funding) → realised-vs-modelled ratio | [03 M16](../03-build-spec.md#m16-live-cost--data-quality-monitor--mt_monitor-always-on-autonomous), [02 F2](../02-v1-architecture.md#8-end-to-end-flows) | TCA report |

### Research lab (M7), features (M6), tier A (M21)
| ID | Requirement | Source | Verified by |
|---|---|---|---|
| R2.40 | Screening (vectorised) + truth (Nautilus L1/L2 replay) backtests with **measured costs from M16** | [03 M7](../03-build-spec.md#m7-research-lab--mt_lab) | Parity test |
| R2.41 | Backtest rules: next-bar action, real fees/impact, fills only at existing prices/sizes, **survivorship-free universes**, one timezone/bar-close convention | [14 §6](../14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) | Harness tests |
| R2.42 | Validation: walk-forward (share of positive folds + **worst fold**), purged K-fold, MC permutation, bootstrap Sharpe, **deflated Sharpe **≥ 0.95** with automatic trial counter**, per-year/per-regime, **2×/3× cost stress**, benchmark | [03 §8](../03-build-spec.md#8-promotion-gates-per-strategy-configurable), [14 §6](../14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) | Harness tests |
| R2.43 | **LLM leakage review** quoting exact lines + vendored freqtrade look-ahead/recursive analysers; waivers audited | [14 §6](../14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) | Seeded-bug test |
| R2.44 | Optuna with complexity penalty; **MLflow** tracking (code version, params, data range, costs, results) | [03 M7](../03-build-spec.md#m7-research-lab--mt_lab) | MLflow runs |
| R2.45 | Sandboxed LLM strategy generator (gVisor / `--network none`, no secrets) | [03 M7](../03-build-spec.md#m7-research-lab--mt_lab), [SPEC NN4](../../SPEC.md#non-negotiable-requirements) | Escape test |
| R2.46 | Core features: TA-Lib, Alpha158, microstructure; IC/rank-IC/decay evaluator; versioned | [03 M6](../03-build-spec.md#m6-features--mt_features) | Feature tests |
| R2.47 | Tier A: train → calibrate (isotonic/Platt, Brier/ECE) → compile (ONNX/Treelite/lleaves) → in-process runtime; MLflow registry | [10 §4.3](../10-memory-rag-and-models.md#43-design), [03 M21](../03-build-spec.md#m21-decision-one--model-serving--mt_models) | Benchmark |
| R2.48 | **MasterTradingBot shared libraries**: pure indicator/signal library + sizing/risk library with **golden files** against its historical outputs | [14 §8](../14-strategy-evidence-and-validation.md#8-mastertradingbot-integration) | Golden tests |

### UI & Telegram (M15)
| ID | Requirement | Source | Verified by |
|---|---|---|---|
| R2.50 | D01 Cockpit, D03 Strategies (builder/registry, manifest fields, validation results), D04 Lab, D05 Execution (manual ticket = `manual` sleeve, flatten-and-halt with reason), D06 Risk (policy editor, sleeves, ladder, venue registry, kill switch) | [D01](../ui/dashboards/D01-cockpit.md) [D03](../ui/dashboards/D03-strategies.md) [D04](../ui/dashboards/D04-research-lab.md) [D05](../ui/dashboards/D05-execution.md) [D06](../ui/dashboards/D06-risk.md) | Playwright |
| R2.51 | Approvals queue (web + Telegram buttons, TTL); C3 approve + TOTP in Telegram | [mob §3](../ui/mobile-and-telegram.md#3-telegram-bot), [ui §3.3](../ui/README.md#33-actions--confirmation) | Flow tests |
| R2.53 | **Trading bots:** strategy version × market scope (instrument, list, dynamic selection) × venue/sleeve × mode × approval policy; `bot.*` commands; tighter-only risk overrides; escalation rules; **auto-downgrade** autonomous → HITL on decay/DQ/ladder ≥ 3/model down/registry change; mode history WORM | [15 §1](../15-bots-hitl-and-worm-audit.md#1-trading-bots) | Bot flow tests |
| R2.54 | **HITL via Telegram:** approval cards (risk preview, reasons, chart link, TTL), Approve / Approve ½ / Reject / Pause bot, TOTP for large orders, `/bots`, `/bot`, `/approvals`, mode commands (auto = C3); D03 Bots tab + wizard | [15 §1](../15-bots-hitl-and-worm-audit.md#13-hitl-approval-via-telegram), [mob §3](../ui/mobile-and-telegram.md#3-telegram-bot), [D03](../ui/dashboards/D03-strategies.md) | E2E approval test |
| R2.52 | Telegram v1: `/kill`, `/status`, `/pnl`, `/pause <strategy>`; works even if `mt-api` is down (bot → NATS) | [03 M15](../03-build-spec.md#m15-ui--alerts--mt_ui-calls-mt_api), [02 §9.3](../02-v1-architecture.md#93-degraded-modes) | Degraded test |

### Non-functional
| ID | Requirement | Source | Verified by |
|---|---|---|---|
| R2.N1 | Pre-trade risk check p99 < 1 ms; signal → order submitted p99 < 5 ms (excl. venue); tier A p99 < 50 µs; kill → all cancels < 1 s | [02 §9.2](../02-v1-architecture.md#92-observability--slos) | Benchmarks |
| R2.N2 | Risk-manager golden tests are mandatory for merge | [04 standing rules](../04-plan-of-action.md#standing-rules) | CI |
| R2.N3 | Trade-only keys, withdrawals disabled, IP allow-listed, separate sub-accounts per mode | [07 §3](../07-security-notes.md#3-broker--exchange-keys), [SPEC NN5](../../SPEC.md#non-negotiable-requirements) | Key audit |
| R2.55 | **Configuration layering:** L0 hard ceilings → L1 system → L2 venue → L3 sleeve → L4 bot; effective = strictest; manifest values are proposals only; versioned (WORM); save-time validation; UI shows which layer sets each limit | [16 §1](../16-configuration-and-safety-model.md#1-configuration-layers-tighten-only-inheritance) | Golden tests |
| R2.57 | D06 Stress tab: replay historical shocks against current positions and policy (`risk.stress.run`, C1) | [D06](../ui/dashboards/D06-risk.md), [14 §3](../14-strategy-evidence-and-validation.md#3-strategy-catalogue-evidence-ranked-templates) | Scenario test |
| R2.56 | **Three-layer dead-man:** in-engine watchdog + external `deadman` sidecar (own keys/connections) + venue-side cancel-after timers and resting venue stops on every position; per-bot `on_system_failure` (default `flatten`); restart reconciles, starts flat, bots paused until you resume (C1) | [16 §3.1](../16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch) | Kill-the-engine drill |

## 4. ToDo sets

### A. Your actions (`USER`)
- [ ] **T2.01** `USER` Write the **initial risk policy values** and the **hard-ceilings file** (only you edit it, on the host). Start from the 14 §5 defaults. → R2.14, R2.19
- [ ] **T2.02** `USER` Decide **sleeves** and their risk budgets (14 §3 allocation table is the suggested start). → R2.13
- [ ] **T2.03** `USER` Create **trade-only, IP-locked, no-withdrawal** keys on testnets/practice accounts, one sub-account per mode. → R2.N3
- [ ] **T2.04** `USER` Provide **MasterTradingBot** rule descriptions + historical signal/trade outputs for golden files. → R2.48
- [ ] **T2.05** `USER` Write your first strategy manifests (counterparty sentence, kill criteria, benchmark) for the P1 candidates: trend on majors, funding carry if access permits. → R2.04 · [14 §3](../14-strategy-evidence-and-validation.md#3-strategy-catalogue-evidence-ranked-templates)
- [ ] **T2.06** `USER` Take part in the **kill-switch drill** from your phone (Telegram `/kill`, then C3 to turn off). → R2.18
- [ ] **T2.07** `USER` Approve a test C3 loosening to prove the TOTP + cool-down path. → R2.19
- [ ] **T2.09** `USER` Create your first bots (scope + mode) and do one HITL approval from Telegram end to end. → R2.53, R2.54
- [ ] **T2.08** `USER` Start the **paper clock**: switch the validated P1 candidates to paper at the end of this phase. → unlocks P7

### B. Build (`BUILD`, code)
- [ ] **T2.20** `BUILD` `mt_strategy`: base classes, multi-timeframe helpers, manifest schema + validator (incl. never-build rules), registry, lifecycle state machine. → R2.01–R2.06
- [ ] **T2.21** `BUILD` Templates (all of R2.02) with parameter schemas driving UI forms and Optuna. → R2.02, R2.03
- [ ] **T2.22** `BUILD` `mt_risk` policy model + store + versioning/rollback; pre-trade checks; sizing models; sleeves + netting; default limits; ladder; venue registry + 2× cap; health check + decay alerts. → R2.10–R2.17, R2.21
- [ ] **T2.23** `BUILD` Kill switch (KV `kill`, triggers, actions) and dead-man watchdog on `sys.heartbeat.*`. → R2.18
- [ ] **T2.24** `BUILD` Change-control service: tighten/loosen classifier, C3 flow, hard-ceilings file reader, audit. → R2.19
- [ ] **T2.25** `BUILD` `mt_engine`: Nautilus TradingNode wrapper, testnet configs, Alpaca/OANDA/IG adapters, STP per venue, epoch-based client IDs, restart reconciliation, approve-mode routing. → R2.20, R2.30–R2.33
- [ ] **T2.26** `BUILD` TCA in `mt_monitor` on paper fills; feed measured costs back into lab cost models. → R2.34
- [ ] **T2.27** `BUILD` `mt_lab`: screening engine, Nautilus truth backtests, validation harness + extensions (trial counter, worst fold, per-year/regime, cost stress, benchmark), vendored freqtrade analysers, leakage review via the gateway, Optuna, MLflow. → R2.40–R2.44
- [ ] **T2.28** `BUILD` Sandbox runner + LLM strategy generator. → R2.45
- [ ] **T2.29** `BUILD` `mt_features` core + IC evaluator. → R2.46
- [ ] **T2.30** `BUILD` `mt_models` tier A: training pipeline, calibration, compile, in-process loader, latency histogram. → R2.47
- [ ] **T2.31** `BUILD` Shared indicator/signal + sizing libraries for MasterTradingBot strategies; "deterministic rule-based" template using them. → R2.48
- [ ] **T2.32** `BUILD` UI: D01, D03, D04, D05, D06 + approvals queue + manual ticket. → R2.50, R2.51
- [ ] **T2.33** `BUILD` Telegram v1 commands, approval buttons, C3 TOTP prompt; NATS fallback path for `/kill`. → R2.51, R2.52
- [ ] **T2.34** `BUILD` Trading bots: `strategy.bot`/`bot_version`, scope resolver (dynamic selections), `bot.*` commands, approval policy + escalation, auto-downgrade, HITL approval cards on Telegram + web, D03 Bots tab. → R2.53, R2.54
- [ ] **T2.37** `BUILD` Experimentation: parameter sweeps, A/B on identical data, shadow mode (live bot mirrored in paper). → R2.07
- [ ] **T2.38** `BUILD` D06 Stress tab + `risk.stress.run` (historical shock replay: May 2022, Nov 2022, Aug 2024, Feb–Mar 2026). → R2.57
- [ ] **T2.35** `BUILD` Config layering service in `mt_risk`: layer store, merge (strictest wins), validation, effective-limits API for D06/D03. → R2.55
- [ ] **T2.36** `BUILD` `deadman` sidecar + venue cancel-after timers + resting venue stops at entry + restart-flat/paused-resume flow. → R2.56

### C. Ops & config (`OPS`)
- [ ] **T2.40** `OPS` `engine`, `backtest-worker`, `sandbox` containers; gVisor runtime; resource limits. → R2.45
- [ ] **T2.41** `OPS` MLflow artefact storage + model registry stages. → R2.44, R2.47
- [ ] **T2.42** `OPS` Grafana: risk state, ladder rung, kill/dead-man, latency SLO panels, TCA. → R2.N1

### D. Verify & test (`VERIFY`)
- [ ] **T2.60** `VERIFY` Risk golden tests + property tests (no order bypasses M11 from strategy, agent, UI or Telegram). → R2.10, R2.N2
- [ ] **T2.61** `VERIFY` Kill drill: cancels < 1 s; dead-man drill (stop the engine heartbeat). → R2.18, R2.N1
- [ ] **T2.62** `VERIFY` Restart-duplicate test (crash mid-order, restart, no duplicates, open orders reconciled). → R2.32
- [ ] **T2.63** `VERIFY` STP present on every order in `audit.order` for each venue. → R2.31
- [ ] **T2.64** `VERIFY` Seeded look-ahead bug caught by both the analysers and the leakage review. → R2.43
- [ ] **T2.65** `VERIFY` Backtest ↔ paper parity on a simple template over the same week. → R2.01, R2.40
- [ ] **T2.66** `VERIFY` Latency benchmarks (risk p99 < 1 ms, tier A p99 < 50 µs, signal → order p99 < 5 ms). → R2.N1
- [ ] **T2.67** `VERIFY` MasterTradingBot golden files match. → R2.48
- [ ] **T2.68** `VERIFY` Viewport matrix + axe on D01/D03–D06. → R2.50
- [ ] **T2.69** `VERIFY` Bot scenarios: HITL approve / approve ½ / reject / expiry (never executes late); protective stop fires without approval; autonomous needs C3 and auto-downgrades on an injected DQ fault; two bots on one strategy with different modes stay isolated. → R2.53, R2.54
- [ ] **T2.70** `VERIFY` Kill-the-engine drill: SIGKILL the engine with paper positions → sidecar cancels in ≤ 5 s and flattens in ≤ 10 s; restart starts flat with bots paused. → R2.56

### E. Run / soak (`RUN`)
- [ ] **T2.80** `RUN` **Paper clock (starts now, runs through P3–P6):** P1 sleeves on paper for ≥ 8 weeks through the real policy/risk/execution path. → gates P7 · [14 §7](../14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7)
- [ ] **T2.81** `RUN` Weekly: five-worst-trades review, realised vs modelled costs. → [14 §4](../14-strategy-evidence-and-validation.md#4-trading-methods-enforced-in-code-defaults-user-editable-in-d06)

### F. Docs
- [ ] **T2.90** `BUILD` Runbooks: keys leaked, server down with open positions, kill-switch drill, bad data. → [07 §9](../07-security-notes.md#9-monitoring--incident-response)

## 5. Deliverables

Strategy framework + templates · risk manager · paper engine + adapters · lab + validation harness · tier A pipeline · shared MasterTradingBot libraries · D01/D03–D06 · Telegram v1 · runbooks.

## 6. Exit criteria (demo)

1. Create a strategy from a template, from code and by "describe it"; backtest with measured costs; the validation report shows all harness sections.
2. Run it on paper behind M11; an approve-mode order is approved from Telegram.
3. Kill drill passes from the phone; a C3 loosening needs TOTP + cool-down.
4. The P1 paper clock has started.

## 7. Risks & open questions

| Risk | Mitigation |
|---|---|
| Scope is the largest of any phase | Ship M11 + M12 + one template first; the lab extensions can trail by a week |
| AU derivatives access unclear (carry needs perps) | Carry stays paper until the venue registry allows it (12 §2) |
| Overfitting through many tweaks | Automatic trial counter feeds deflated Sharpe; worst-fold judging |
