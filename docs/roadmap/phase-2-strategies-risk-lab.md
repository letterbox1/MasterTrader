# Phase 2 · Strategy Framework, Risk Manager & Research Lab

| | |
|---|---|
| **Goal** | You can create **any strategy type on any timeframe**, backtest it with **measured costs**, validate it, and run it on **paper behind the risk manager**, controlled from the web UI and Telegram. |
| **Duration** | Weeks 7–11 |
| **Depends on** | P0 (`mt_api`, audit, shell), P1 (data, DQ status, measured costs) |
| **Unlocks** | **The paper clock starts here** (P1 sleeves need ≥ 8 weeks of paper before P7). P3 (fills to journal), P6 (lab + tier A for distillation), P7 |
| **Modules** | M0 strategy framework, M11 risk manager, M12 execution, M7 research lab, M6 core features, M21 tier A, M15 UI v1 + Telegram bot v1, MasterTradingBot shared libraries |
| **Containers** | `engine`, `deadman`, `backtest-worker`, `sandbox`, `telegram-bot` (commands) |
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
| R2.06 | Strategy lifecycle draft → backtested → validated → promoted, gate-checked and audited. A strategy is promoted through gates; a **bot** is switched between modes `paper` / `hitl` / `autonomous` (R2.20; "approve"/"auto" are retired aliases) | [02 F7](../02-v1-architecture.md#8-end-to-end-flows), [17 §B](../17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer) | Lifecycle tests |
| R2.07 | Experimentation: sweeps, A/B on identical data, **shadow mode** | [03 M0](../03-build-spec.md#m0-strategy-framework--mt_strategy-strategy-agnostic-any-timeframe) | Lab run |

### Risk manager (M11)
| ID | Requirement | Source | Verified by |
|---|---|---|---|
| R2.10 | Default-deny pre-trade layer in front of Nautilus `RiskEngine`; **every order passes through it** whatever its source | [SPEC NN2](../../SPEC.md#non-negotiable-requirements), [03 M11](../03-build-spec.md#m11-risk-manager--mt_risk-built-in-user-inputs-via-uitelegram-later-mcp) | Bypass tests |
| R2.11 | Versioned policy at global, venue, strategy, instrument and portfolio levels | [03 M11](../03-build-spec.md#m11-risk-manager--mt_risk-built-in-user-inputs-via-uitelegram-later-mcp) | Policy tests |
| R2.12 | Sizing models: fixed, fixed-fractional, vol target, stop-distance, Kelly (quarter-Kelly ceiling, never `2p−1`, never stacked on vol targeting), risk parity | [14 §4](../14-strategy-evidence-and-validation.md#4-trading-methods-enforced-in-code-defaults-user-editable-in-d06) | Golden tests |
| R2.13 | **Sleeves** with own limits/kill switches and a **two-stage drawdown** (default 10% de-risk / 15% halt, configurable); exposure **netted per asset across sleeves**; `manual` sleeve for manual tickets | [14 §5](../14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11) | Golden tests |
| R2.14 | Default limits table (risk/trade, max position, daily loss, two-stage sleeve drawdown 10%/15%, system drawdown 10% no new entries / 25% flatten + 30-day lock, open positions, stale data, decision deadline, price collar, API-error pause, cost blow-out, venue concentration 25%, leverage): all defaults, configurable | [14 §5](../14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11), [16 §2.1–§2.3](../16-configuration-and-safety-model.md#21-risk-sizing-and-drawdown) | Golden tests |
| R2.15 | **Fallback ladder** (6 rungs) live in D06 | [03 M11](../03-build-spec.md#m11-risk-manager--mt_risk-built-in-user-inputs-via-uitelegram-later-mcp), [14 §5](../14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11) | Ladder tests |
| R2.16 | Pre-trade checks: limits, price collar, liquidity/spread (M16), duplicate (idempotent IDs), event blackout hook, **DQ status** | [03 M11](../03-build-spec.md#m11-risk-manager--mt_risk-built-in-user-inputs-via-uitelegram-later-mcp), [SPEC NN3](../../SPEC.md#non-negotiable-requirements) | Unit tests |
| R2.17 | **Venue registry check** on every order; **2× crypto-derivatives cap**; paper/testnet orders are allowed on venues/products marked `allowed` or `read_only`, and on `blocked` products only if marked `paper_ok` | [12 §2](../12-policy-and-compliance.md#2-venue-access-registry), [12 §1](../12-policy-and-compliance.md#1-australian-boundary-the-load-bearing-assumption) | Rejection tests |
| R2.18 | Kill switch (manual + automatic triggers): stops new trading, cancels orders, applies each bot's `on_system_failure`, freezes new treasury/earn moves (no vault sweep in P2; it arrives in P5); **dead-man's switch** (three layers, R2.56) | [02 F6](../02-v1-architecture.md#8-end-to-end-flows), [17 §B](../17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer) | Drill |
| R2.19 | Change control: tighten instantly; loosen = C3 (Telegram + TOTP + cool-down); **L0 hard ceilings** are edited in the agent/bot strategy settings (the ceilings section applies to every bot): tightening is immediate, loosening is C3; versioned with rollback. Telegram C3 replaces the P0 break-glass CLI | [02 F5](../02-v1-architecture.md#8-end-to-end-flows), [07 §6](../07-security-notes.md#6-application-controls), [16 §1](../16-configuration-and-safety-model.md#1-configuration-layers-tighten-only-inheritance), [17 §E](../17-decisions-register.md#e-ratification-2026-10-22) | C3 tests |
| R2.20 | Modes per bot: `paper` / **`hitl`** (approval card per order, TTL default 60 s intraday · 15 min swing · 4 h position, expiry = reject) / **`autonomous`** (gates required). paper → HITL is C2, HITL → autonomous C3, any downgrade C1 ([16 §2.3](../16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl)); protective exits never wait for approval | [03 M11](../03-build-spec.md#m11-risk-manager--mt_risk-built-in-user-inputs-via-uitelegram-later-mcp) | Flow tests |
| R2.21 | Decay and health signals, one meaning each ([16 §2.6](../16-configuration-and-safety-model.md#26-decay-and-kill-signals-one-meaning-each)): rolling 60-trade Sharpe/hit rate below the backtest 5th percentile (26-week window for low-frequency bots), a CUSUM break or 5 consecutive losing trades → alert + downgrade autonomous → HITL; daily health check fails (30-day Sharpe < ½ validated or drawdown > 1.5× backtest max) → halt the bot. Built here for paper; P7 extends it to live with kill criteria | [14 §5](../14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11), [03 §8 item 8](../03-build-spec.md#8-promotion-gates-per-strategy-configurable) | Simulated decay |

### Execution (M12)
| ID | Requirement | Source | Verified by |
|---|---|---|---|
| R2.30 | Nautilus paper/sandbox on testnets/practice accounts; custom **Alpaca, OANDA, IG** adapters | [03 M12](../03-build-spec.md#m12-execution--mt_engine) | Adapter tests |
| R2.31 | **STP mode sent explicitly on every order** where the venue has an STP field; STP cancels recorded as non-fills. Netting brokers (OANDA, IG, Alpaca, IBKR) are marked `stp: n/a (netting)` in the venue registry and run one strategy per account/sub-account where netting would merge bots | [12 §3](../12-policy-and-compliance.md#3-exchange-conduct--self-trade-prevention) | Order audit |
| R2.32 | Idempotent client order IDs `{bot}-{engine_epoch}-{seq}` (a signal hash is stored separately for idempotency); reconcile open orders before resuming | [03 M12](../03-build-spec.md#m12-execution--mt_engine) | Restart test |
| R2.33 | Execution methods: maker-first with timeout, TWAP/slicing > ~1% of 1-min volume, exit plan fixed at entry | [14 §4](../14-strategy-evidence-and-validation.md#4-trading-methods-enforced-in-code-defaults-user-editable-in-d06) | Sim tests |
| R2.34 | TCA per order (decision/arrival/VWAP, fees, funding) → realised-vs-modelled ratio | [03 M16](../03-build-spec.md#m16-live-cost--data-quality-monitor--mt_monitor-always-on-autonomous), [02 F2](../02-v1-architecture.md#8-end-to-end-flows) | TCA report |

### Research lab (M7), features (M6), tier A (M21)
| ID | Requirement | Source | Verified by |
|---|---|---|---|
| R2.40 | Screening (vectorised) + truth (Nautilus L1/L2 replay) backtests with **measured costs from M16** | [03 M7](../03-build-spec.md#m7-research-lab--mt_lab) | Parity test |
| R2.41 | Backtest rules: next-bar action, real fees/impact, fills only at existing prices/sizes, **survivorship-free universes**, one timezone/bar-close convention | [14 §6](../14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) | Harness tests |
| R2.42 | Validation: walk-forward (share of positive folds + **worst fold**), purged K-fold, MC permutation, bootstrap Sharpe, **deflated Sharpe ≥ 0.95 with automatic trial counter**, per-year/per-regime (regime labels per [16 §2.4.1](../16-configuration-and-safety-model.md#241-regime-labels-for-per-regime-results)), **2×/3× cost stress**, benchmark. Gate values are defaults, configurable ([16 §2.4](../16-configuration-and-safety-model.md#24-validation-gates-per-strategy-gate-profile)); loosening a gate is C3 | [03 §8](../03-build-spec.md#8-promotion-gates-per-strategy-configurable), [14 §6](../14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8) | Harness tests |
| R2.43 | **LLM leakage review** quoting exact lines + freqtrade look-ahead/recursive analysers, vendored under `third_party/` with their GPL licence and isolated in `mt_lab` (personal, never-distributed use); each finding waived via `lab.leakage.waive` (C2, audited) | [14 §6](../14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8), [17 §A](../17-decisions-register.md#a-s2-items-all-resolved) | Seeded-bug test |
| R2.44 | Optuna with complexity penalty; **MLflow** tracking (code version, params, data range, costs, results) | [03 M7](../03-build-spec.md#m7-research-lab--mt_lab) | MLflow runs |
| R2.45 | Sandboxed LLM strategy generator (gVisor / `--network none`, no secrets) | [03 M7](../03-build-spec.md#m7-research-lab--mt_lab), [SPEC NN4](../../SPEC.md#non-negotiable-requirements) | Escape test |
| R2.46 | Core features: TA-Lib, Alpha158, microstructure; IC/rank-IC/decay evaluator; versioned | [03 M6](../03-build-spec.md#m6-features--mt_features) | Feature tests |
| R2.47 | Tier A: train → calibrate (isotonic/Platt, Brier/ECE) → compile (ONNX/Treelite/lleaves) → in-process runtime; MLflow registry. Until the P6 teacher exists, tier A trains on forward-return / triple-barrier labels from market data; training runs via `models.tiera.train` (C1) | [10 §4.3](../10-memory-rag-and-models.md#43-design), [03 M21](../03-build-spec.md#m21-decision-one--model-serving--mt_models) | Benchmark |
| R2.48 | **MasterTradingBot shared libraries**: pure indicator/signal library + sizing/risk library with **golden files** against its historical outputs | [14 §8](../14-strategy-evidence-and-validation.md#8-mastertradingbot-integration) | Golden tests |

### UI & Telegram (M15)
| ID | Requirement | Source | Verified by |
|---|---|---|---|
| R2.50 | D01 Cockpit, D03 Strategies (builder/registry, manifest fields, validation results), D04 Lab, D05 Execution (manual ticket = `manual` sleeve, flatten-and-halt with reason), D06 Risk (policy editor, sleeves, ladder, venue registry, kill switch) | [D01](../ui/dashboards/D01-cockpit.md) [D03](../ui/dashboards/D03-strategies.md) [D04](../ui/dashboards/D04-research-lab.md) [D05](../ui/dashboards/D05-execution.md) [D06](../ui/dashboards/D06-risk.md) | Playwright |
| R2.51 | Approvals queue (web + Telegram buttons, TTL); C3 approve + TOTP in Telegram; no bulk approve (except the batched dynamic-selection card, [15 §1.3](../15-bots-hitl-and-worm-audit.md#13-hitl-approval-via-telegram)) | [mob §3](../ui/mobile-and-telegram.md#3-telegram-bot), [ui §3.3](../ui/README.md#33-actions--confirmation) | Flow tests |
| R2.53 | **Trading bots:** strategy version × market scope (instrument, list, dynamic selection) × venue/sleeve × mode × approval policy; `bot.*` commands; tighter-only risk overrides; escalation rules; **auto-downgrade** autonomous → HITL on decay/DQ/ladder ≥ 3/model down/registry change; mode history WORM | [15 §1](../15-bots-hitl-and-worm-audit.md#1-trading-bots) | Bot flow tests |
| R2.54 | **HITL via Telegram:** approval cards (risk preview, reasons, chart link, TTL), Approve / Approve ½ / Reject / Pause bot, TOTP for large orders, `/bots`, `/bot`, `/approvals`, mode commands (autonomous = C3); D03 Bots tab + wizard | [15 §1](../15-bots-hitl-and-worm-audit.md#13-hitl-approval-via-telegram), [mob §3](../ui/mobile-and-telegram.md#3-telegram-bot), [D03](../ui/dashboards/D03-strategies.md) | E2E approval test |
| R2.52 | Telegram v1: `/kill`, `/status`, `/pnl`, `/pause <strategy>`; works even if `mt-api` is down (bot → NATS, with NATS credentials limited to publishing `kill.set`; the engine writes the kill event to WORM with source `telegram`) | [03 M15](../03-build-spec.md#m15-ui--alerts--mt_ui-calls-mt_api), [02 §9.3](../02-v1-architecture.md#93-degraded-modes) | Degraded test |

### Non-functional
| ID | Requirement | Source | Verified by |
|---|---|---|---|
| R2.N1 | Pre-trade risk check p99 < 1 ms; signal → order submitted p99 < 5 ms (excl. venue); tier A p99 < 50 µs; kill → all cancels < 1 s | [02 §9.2](../02-v1-architecture.md#92-observability--slos) | Benchmarks |
| R2.N2 | Risk-manager golden tests are mandatory for merge | [04 standing rules](../04-plan-of-action.md#standing-rules) | CI |
| R2.N3 | Trade-only keys, withdrawals disabled, IP allow-listed, separate sub-accounts per mode | [07 §3](../07-security-notes.md#3-broker--exchange-keys), [SPEC NN5](../../SPEC.md#non-negotiable-requirements) | Key audit |
| R2.55 | **Configuration layering:** L0 hard ceilings → L1 system → L2 venue → L3 sleeve → L4 bot; effective = strictest; manifest values are proposals only; versioned (WORM); save-time validation; UI shows which layer sets each limit | [16 §1](../16-configuration-and-safety-model.md#1-configuration-layers-tighten-only-inheritance) | Golden tests |
| R2.57 | D06 Stress tab ships as a **placeholder** in P2 ("arrives in P7"); the historical shock replay against current positions and policy (`risk.stress.run`, C1) is built in P7 before live capital (R7.16) | [D06](../ui/dashboards/D06-risk.md), [14 §3](../14-strategy-evidence-and-validation.md#3-strategy-catalogue-evidence-ranked-templates), [17 §D](../17-decisions-register.md#d-other-decisions) | Placeholder present |
| R2.56 | **Three-layer dead-man:** in-engine watchdog + external `deadman` sidecar (own keys/connections) + venue-side cancel-after timers and resting venue stops on every position; per-bot `on_system_failure` (default `flatten`); restart reconciles, starts flat, bots paused until you resume (C1) | [16 §3.1](../16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch) | Kill-the-engine drill |
| R2.58 | **Pre-trade safety state, checked inline on every order:** data age vs the bot's threshold (default 2 s fast / 60 s slow); WORM integrity status `audit.integrity` (R0.12: `block_new_entries` rejects entries while exits continue, `halt_all` stops all); egress status (R1.16); decision deadline (late decisions dropped). A failing check rejects the order and the ladder holds | [16 §2.2](../16-configuration-and-safety-model.md#22-data-freshness-what-stale-means), [16 §2.11](../16-configuration-and-safety-model.md#211-worm-integrity), [17 §A](../17-decisions-register.md#a-s2-items-all-resolved) | Golden tests |

## 4. ToDo sets

### A. Your actions (`USER`)
- [ ] **T2.01** `USER` Review the prefilled defaults ([16 §2](../16-configuration-and-safety-model.md#2-default-values-all-configurable)) and set the **initial risk policy values** and the **L0 hard ceilings** in the agent/bot strategy settings (the ceilings section applies to every bot). Every value stays a setting you can change; loosening is C3. → R2.14, R2.19
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
- [ ] **T2.23** `BUILD` Kill switch (KV `kill`, triggers, actions: stop, cancel, per-bot failure policy, freeze treasury moves) and the in-engine dead-man watchdog (layer 1) on `sys.heartbeat.*`. → R2.18
- [ ] **T2.24** `BUILD` Change-control service: tighten/loosen classifier, C3 flow, L0 hard-ceilings section in the strategy settings (applies to every bot), audit; retire the P0 break-glass C3 path once Telegram C3 passes (T2.07). → R2.19
- [ ] **T2.25** `BUILD` `mt_engine`: Nautilus TradingNode wrapper, testnet configs, Alpaca/OANDA/IG adapters, STP per venue (`stp: n/a (netting)` for netting brokers), client IDs `{bot}-{engine_epoch}-{seq}` + signal hash, restart reconciliation, HITL routing; built and tested against recorded fixtures and emulators (live testnet run in T2.72). → R2.20, R2.30–R2.33
- [ ] **T2.26** `BUILD` TCA in `mt_monitor` on paper fills; feed measured costs back into lab cost models. → R2.34
- [ ] **T2.27** `BUILD` `mt_lab`: screening engine, Nautilus truth backtests, validation harness + extensions (trial counter, worst fold, per-year/regime, cost stress, benchmark), vendored freqtrade analysers (GPL, `third_party/`, isolated in `mt_lab`), leakage review via the gateway + `lab.leakage.waive` (C2), Optuna, MLflow. → R2.40–R2.44
- [ ] **T2.28** `BUILD` Sandbox runner + LLM strategy generator. → R2.45
- [ ] **T2.29** `BUILD` `mt_features` core + IC evaluator. → R2.46
- [ ] **T2.30** `BUILD` `mt_models` tier A: training pipeline on forward-return / triple-barrier labels (until the P6 teacher), `models.tiera.train` (C1), calibration, compile, in-process loader, latency histogram. → R2.47
- [ ] **T2.31** `BUILD` Shared indicator/signal + sizing libraries for MasterTradingBot strategies; "deterministic rule-based" template using them. → R2.48
- [ ] **T2.32** `BUILD` UI: D01, D03, D04, D05, D06 + approvals queue + manual ticket. → R2.50, R2.51
- [ ] **T2.33** `BUILD` Telegram v1 commands, approval buttons, C3 TOTP prompt; NATS fallback path for `/kill` (credentials limited to `kill.set`; WORM kill event with source `telegram`). → R2.51, R2.52
- [ ] **T2.34** `BUILD` Trading bots: `strategy.bot`/`bot_version`, scope resolver (dynamic selections), `bot.*` commands, approval policy + escalation, auto-downgrade, HITL approval cards on Telegram + web, D03 Bots tab. → R2.53, R2.54
- [ ] **T2.37** `BUILD` Experimentation: parameter sweeps, A/B on identical data, shadow mode (live bot mirrored in paper). → R2.07
- [ ] **T2.38** `BUILD` D06 Stress tab placeholder ("arrives in P7"); the shock replay and `risk.stress.run` are built in P7 (T7.27). → R2.57
- [ ] **T2.35** `BUILD` Config layering service in `mt_risk`: layer store, merge (strictest wins), validation, effective-limits API for D06/D03. → R2.55
- [ ] **T2.36** `BUILD` `deadman` sidecar + venue cancel-after timers + resting venue stops at entry + restart-flat/paused-resume flow. → R2.56
- [ ] **T2.39** `BUILD` Inline pre-trade safety-state checks in `mt_risk`: data age vs the bot's threshold, `audit.integrity` status, `egress.status`, decision deadline. → R2.58

### C. Ops & config (`OPS`)
- [ ] **T2.40** `OPS` `engine`, `backtest-worker`, `sandbox` containers; gVisor runtime; resource limits. → R2.45
- [ ] **T2.41** `OPS` MLflow artefact storage + model registry stages. → R2.44, R2.47
- [ ] **T2.42** `OPS` Grafana: risk state, ladder rung, kill/dead-man, latency SLO panels, TCA. → R2.N1

### D. Verify & test (`VERIFY`)
- [ ] **T2.60** `VERIFY` Risk golden tests + property tests (no order bypasses M11 from strategy, agent, UI or Telegram). → R2.10, R2.N2
- [ ] **T2.61** `VERIFY` Kill drill: cancels < 1 s; dead-man drill (stop the engine heartbeat). → R2.18, R2.N1
- [ ] **T2.62** `VERIFY` Restart-duplicate test (crash mid-order, restart, no duplicates, open orders reconciled). → R2.32
- [ ] **T2.63** `VERIFY` STP present on every order in `audit.order` for each STP-capable venue; netting venues run one strategy per account/sub-account. → R2.31
- [ ] **T2.64** `VERIFY` Seeded look-ahead bug caught by both the analysers and the leakage review. → R2.43
- [ ] **T2.65** `VERIFY` Backtest ↔ paper parity on a simple template over the same week. → R2.01, R2.40
- [ ] **T2.66** `VERIFY` Latency benchmarks (risk p99 < 1 ms, tier A p99 < 50 µs, signal → order p99 < 5 ms). → R2.N1
- [ ] **T2.67** `VERIFY` MasterTradingBot golden files match. → R2.48
- [ ] **T2.68** `VERIFY` Viewport matrix + axe on D01/D03–D06. → R2.50
- [ ] **T2.69** `VERIFY` Bot scenarios: HITL approve / approve ½ / reject / expiry (never executes late); protective stop fires without approval; autonomous needs C3 and auto-downgrades on an injected DQ fault; two bots on one strategy with different modes stay isolated. → R2.53, R2.54
- [ ] **T2.70** `VERIFY` Kill-the-engine drill: SIGKILL the engine with paper positions → sidecar cancels in ≤ 5 s and flattens in ≤ 10 s; restart starts flat with bots paused. → R2.56
- [ ] **T2.71** `VERIFY` Safety-state golden tests: an order on data older than the bot's threshold, an entry while `audit.integrity` = `block_new_entries` (an exit still passes), and an order with a bad egress status are all rejected and the ladder holds. → R2.58
- [ ] **T2.72** `VERIFY` Testnet/practice end-to-end with your trade-only keys (after T2.03): one order per venue passes M11, fills, lands in `audit.order`/`audit.fill` and reconciles. → R2.30, R2.N3

### E. Run / soak (`RUN`)
- [ ] **T2.80** `RUN` **Paper clock (starts now, runs through P3–P6):** P1 sleeves on paper for ≥ 8 weeks through the real policy/risk/execution path. → gates P7 · [14 §7](../14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7)
- [ ] **T2.81** `RUN` Weekly: five-worst-trades review, realised vs modelled costs. → [14 §4](../14-strategy-evidence-and-validation.md#4-trading-methods-enforced-in-code-defaults-user-editable-in-d06)

### F. Docs
- [ ] **T2.90** `BUILD` Runbooks: keys leaked, server down with open positions, kill-switch drill, bad data. → [07 §9](../07-security-notes.md#9-monitoring--incident-response)

## 5. Deliverables

Strategy framework + templates · risk manager · paper engine + adapters · lab + validation harness · tier A pipeline · shared MasterTradingBot libraries · D01/D03–D06 · Telegram v1 · runbooks.

## 6. Exit criteria (demo)

1. Create a strategy from a template, from code and by "describe it"; backtest with measured costs; the validation report shows all harness sections.
2. Run it on paper behind M11; a HITL order is approved from Telegram.
3. Kill drill passes from the phone; a C3 loosening needs TOTP + cool-down.
4. The P1 paper clock has started.

## 7. Risks & open questions

| Risk | Mitigation |
|---|---|
| Scope is the largest of any phase | Ship M11 + M12 + one template first; the lab extensions can trail by a week |
| AU derivatives access unclear (carry needs perps) | Carry stays paper until the venue registry allows it (12 §2) |
| Overfitting through many tweaks | Automatic trial counter feeds deflated Sharpe; worst-fold judging |
