# D03 · Strategies

| | |
|---|---|
| **Routes** | `/strategies` (registry), `/strategies/new` (builder), `/strategies/:id` (detail), `/strategies/bots` (bots), `/strategies/settings` (strategy settings incl. hard ceilings) |
| **Modules** | M0 framework, M11 risk, M12 execution, M21 tier A |
| **Phase** | 2 (gate reports and go-live/capital-step view in 7) |
| **Mock-up reference** | None (new screen); visual language from Strategy Lab + Cockpit |

## Purpose

Create, configure, deploy and supervise **any strategy type on any timeframe**:
- a **strategy** is promoted through its lifecycle (draft → backtested → validated → paper → hitl → autonomous) by passing gates; the last three stages are the highest mode its bots may use;
- a **bot** (strategy version × market scope × venue/sleeve, [15 §1](../../15-bots-hitl-and-worm-audit.md#1-trading-bots)) is switched between the modes `paper` / `hitl` / `autonomous`. "approve"/"auto" are retired aliases.

## `/strategies`: registry

| Tier | Layout |
|---|---|
| ≥ xl | Filter bar (type, asset class, timeframe, lifecycle stage, mode, status) + `DataTable` |
| md–lg | Same, with P3 columns hidden |
| ≤ ph | Filter chips (scroll) + strategy cards |

**Table columns:**

| Priority | Columns |
|---|---|
| P1 | Name, lifecycle stage, highest allowed mode, bots (count by mode), status, today P&L |
| P2 | Type/template, instruments, timeframes, 30d P&L, Sharpe (live), drawdown, gate status |
| P3 | Last signal, owner notes, created |

**Actions:**

| Action | Command | Level |
|---|---|---|
| New strategy | navigate to builder | C0 |
| Clone | `strategy.clone` | C1 |
| Archive | `strategy.archive` | C1 |
| Bulk pause (selection) | `strategy.pause` | C1 |

## `/strategies/new`: builder

**Three ways in (tabs):**
1. **Template.** Pick a template, then fill in `ParamForm`. The list renders from `/strategies/templates` (no hard-coded list in the UI). Phase 2 set ([R2.02](../../roadmap/phase-2-strategies-risk-lab.md#3-requirements)): deterministic rule-based, scalping (tick/L2), intraday, EMA/MA cross, mean reversion, breakout, swing/position, grid/DCA, pairs/stat-arb, event/news-driven, ML-signal, funding carry, cross-sectional momentum, token unlock, memecoin momentum (paper-only). Later: market making (Nautilus or Hummingbot; Phase 6, optional) and LLM/decision-model signal (Phase 6), shown disabled with their phase until available.
2. **Code.** `CodeEditor` with the manifest + Strategy class skeleton. Desktop only for editing; read-only on phones with a "continue on desktop" note.
3. **Describe it.** Natural-language prompt → `lab.generate_strategy`.
   - Generated code runs in the **sandbox**.
   - The result shows code + manifest + a first backtest.
   - The user must review before saving.

**Common sections:**

| Section | Contents |
|---|---|
| Universe | Instruments (combobox), venues. Shows each instrument's **finest available resolution**; incompatible timeframes are flagged. |
| Data subscriptions | Ticks / quotes / L2 / bar specs (multi-timeframe allowed) |
| Features | From the feature library, incl. tier-B scores |
| Decision | Rules, tier-A model (from the registry) or tier-B question thresholds |
| Sizing | Fixed, fixed-fractional, vol-target, Kelly-capped (quarter-Kelly is a **ceiling**, never stacked on vol targeting), risk-parity. Defaults (risk per trade 1% of sleeve, max position 10%) are configurable ([16 §2.1](../../16-configuration-and-safety-model.md#21-risk-sizing-and-drawdown)) |
| Risk policy | Link to the policy (D06) + quick limits. The manifest's values are **proposals**: each shows next to your sleeve/system limits and the L0 ceiling; you accept or tighten, and anything looser than a parent layer is rejected ([16 §1](../../16-configuration-and-safety-model.md#1-configuration-layers-tighten-only-inheritance)) |
| Schedule / sessions | Trading hours; `event_sensitive` flag and calendar blackouts (default: no new entries 15 min before to 15 min after high-importance events; exits continue; configurable per bot and event type, [16 §2.8](../../16-configuration-and-safety-model.md#28-calendar-blackouts)) |
| Review | Manifest diff + validation of the manifest schema |

**Save:** `strategy.create` (C1). The strategy starts as `draft`, and the next suggested step is "Run backtest" (→ D04).

## `/strategies/:id`: detail

| Tier | Layout |
|---|---|
| ≥ xl | Header (name, stage stepper, highest allowed mode, status, Start/Pause/Stop) + tabs: Overview · Parameters · Performance · Positions & orders · Signals · Gates · Versions · Logs (+ Go-live from Phase 7) |
| ≤ ph | Header condensed; stage stepper as "Stage 4/6"; tabs as a select |

**Tabs:**

| Tab | Shows | Source |
|---|---|---|
| Overview | Live P&L, equity curve (live vs paper vs backtest expectation), drawdown, exposure, last signals, health (paused-by-DQ/risk reasons) | `/strategies/{id}`, `/strategies/{id}/runs`, WS `signals`, `positions` |
| Parameters | `ParamForm` (current version); edit → new version | `/strategies/{id}` |
| Performance | Metrics table (return, Sharpe, Sortino, max DD, hit rate, avg win/loss, turnover, **realised vs modelled costs**), distribution of returns, comparison with backtest (tracking error) | `/strategies/{id}/runs?metrics=1` |
| Positions & orders | Filtered blotter | `/positions?strategy=`, `/orders?strategy=` |
| Signals | Signal log with risk outcome + provenance | `/signals?strategy=` |
| **Gates** | `GateChecklist` for the strategy's gate profile ([16 §2.4](../../16-configuration-and-safety-model.md#24-validation-gates-per-strategy-gate-profile); defaults, configurable; loosening a gate is C3): deflated Sharpe **≥ 0.95** (a probability) with the trial counter; MC permutation p < 0.05; walk-forward ≥ 60% of folds positive and worst fold ≥ −(sleeve halt drawdown); cost stress profitable at 2× (3× reported); positive per year and per regime (bull/bear/chop, [16 §2.4.1](../../16-configuration-and-safety-model.md#241-regime-labels-for-per-regime-results)) or labelled single-regime; beats the passive benchmark; leakage review + look-ahead/recursive check clean or waived; post-cutoff LLM eval (if applicable); safety drills (kill switch, dead-man, restart) passed on the bot's venue; paper/HITL period elapsed / required (default ≥ 8 weeks **and** ≥ 50 trades; memecoin ≥ 300 trades; low-frequency ≥ 26 weeks); tracking error within tolerance | `/strategies/{id}?gates=1` |
| Versions | Version list with `DiffView`; rollback | `/strategies/{id}?versions=1` |
| Logs | `LogStream` for this strategy | Loki proxy via `/system/logs?strategy=` |

**Actions:**

| Control | Command | Level | Rule |
|---|---|---|---|
| Start (paper) | `strategy.start` | C1 | Needs stage ≥ validated, or a "paper from backtested" override |
| Pause / Resume / Stop | `strategy.pause` / `strategy.resume` / `strategy.stop` | C1 | — |
| Allow mode → hitl | `strategy.set_mode` (hitl) | C2 | Needs the paper-stage gates |
| Allow mode → **autonomous** | `strategy.set_mode` (autonomous) | **C3** | Disabled until all gates pass |
| Restrict to hitl / paper | `strategy.set_mode` | C1 | Tightening; bots above the new mode drop to it |
| Promote / demote stage | `strategy.promote` / `strategy.demote` | C1 (autonomous stage C3) | — |
| Edit params | `strategy.update_params` | C1 for paper; **C2** if live; **C3** if the change increases risk (size, leverage) | — |
| Flatten | `position.close` (strategy scope) | C2 | — |
| Run backtest / validation | `lab.backtest.run` / `lab.validate.run` | C1 | — |

## Additions from the CryptoTrader review

- **Manifest fields shown on the registry and detail:** `counterparty` (who pays you, the rule from [14 §3](../../14-strategy-evidence-and-validation.md#3-strategy-catalogue-evidence-ranked-templates)), `benchmark` (what it must beat, e.g. buy-and-hold BTC or cash yield), **priority** (P1 / P2 / P3 / X), `sleeve` and **kill criteria**.
- The builder refuses templates on the never-build list and shows why.
- Detail shows **per-year and per-regime** results, **2× and 3× cost stress**, the trial counter and the worst walk-forward fold (from the validation harness).

## `/strategies/settings`: strategy settings and hard ceilings

Settings that apply across strategies and bots, as `SettingField`s with the effective value, the layer and the default ([ui §3.7](../README.md#37-settings-show-configurable-defaults-and-their-layer)).

| Section | Contents |
|---|---|
| **Ceilings (L0)** | The absolute maxima that apply to **every bot**: e.g. crypto-derivatives leverage ≤ 2×, max daily loss, max per-transaction signer value. Editable here: **tightening is immediate (C1); loosening is C3** (Telegram approve + TOTP + cool-down). D06 shows the same ceilings on every field and links here. There is no host-only ceilings file |
| Bot defaults (L4) | Defaults new bots start with: decision deadlines (scalping 1 s · intraday 10 s · swing 5 min · position 1 h), HITL approval TTL (60 s · 15 min · 4 h), large-order threshold (> 2% of sleeve or > A$5,000), `on_system_failure` (default `flatten`; `cancel_orders_only`, `hold`), `auto_resume_after_crash` (default off), stale thresholds (2 s fast / 60 s slow) ([16 §2.2–§2.3](../../16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl), [§3.1](../../16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch)) |
| Gate profile | Default gate thresholds per strategy class ([16 §2.4](../../16-configuration-and-safety-model.md#24-validation-gates-per-strategy-gate-profile)); tightening free, loosening C3 |

Command: `risk.policy.update` (layer L0 for ceilings; tighten C1, loosen C3); bot defaults via `bot.update_params` (tighten C1, loosen C3).

## Go-live tab (Phase 7)

Per strategy going live:
- **Gate report:** generated from all gates + harness sections + paper tracking (`/strategies/{id}/gate-report`; `lab.gate_report.generate`, C1), with a pass/fail summary and a PDF/HTML export.
- **Per bot:** starting live allocation (set here when the bot goes live; default A$2,000, configurable), current capital step and clean weeks (`CapitalStepCard`, detail in D06 Live), kill criteria from the manifest and their state, last weekly review.

## Bots tab (`/strategies/bots`; see [15 §1](../../15-bots-hitl-and-worm-audit.md#1-trading-bots))

- **List:** bot, strategy version, market scope (instrument / list / dynamic selection), venue & sleeve, **mode chip (paper · HITL · autonomous)**, status, pending approvals, today P&L.
- **Create wizard:** strategy version → market scope → venue & sleeve → mode → approval policy (TTL, large-order threshold, escalation rules) → failure behaviour (`on_system_failure`, `auto_resume_after_crash`, `event_sensitive`) → review (risk preview). Every field prefills from the defaults above, shows its layer, and can only be tighter than the sleeve/system/ceiling.
- **Actions:** `bot.create` (C1); `bot.set_mode` → paper (C1), → hitl (**C2** from paper; C1 from autonomous), → **autonomous (C3, disabled while gates fail)**; `bot.pause`/`resume`/`stop` (C1); `bot.approval_policy.set` (tighten C1, loosen C3).
- **Auto-downgrade** (autonomous → hitl): decay alert, ladder rung ≥ 3, DQ degraded, model service down, venue registry change ([16 §2.6](../../16-configuration-and-safety-model.md#26-decay-and-kill-signals-one-meaning-each)). Upgrading back is C3.
- **Detail:** mode history (WORM), approvals (shown card, decision, latency, outcome), auto-downgrade events.

## Acceptance criteria

1. **Template coverage:** every template creates a valid manifest, which a backtest then runs.
2. **Autonomous mode:** can't be selected while gates fail; the UI shows exactly which gate fails and its threshold (default or overridden).
3. **Timeframe compatibility:** a strategy that subscribes to a resolution an instrument can't provide is blocked at save with a clear message.

## Backend contract

- **Queries:** `/strategies`, `/strategies/{id}` (+ `gates`, `versions`, `metrics`), `/strategies/templates`, `/strategies/{id}/runs`, `/strategies/{id}/gate-report` (P7), `/bots` (+ `/{id}`, `/{id}/approvals`), `/risk/policy` (ceilings, defaults), `/risk/capital-steps` (P7), `/signals`, `/system/logs`.
- **WebSocket topics:** `signals`, `positions`, `orders`, `lab.job`.
- **Commands:** `strategy.*`, `bot.*`, `risk.policy.update` (L0 ceilings), `lab.generate_strategy`, `lab.backtest.run`, `lab.validate.run`, `lab.gate_report.generate` (P7), `position.close`.
