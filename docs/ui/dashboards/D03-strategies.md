# D03 · Strategies

| | |
|---|---|
| **Routes** | `/strategies` (registry), `/strategies/new` (builder), `/strategies/:id` (detail) |
| **Modules** | M0 framework, M11 risk, M12 execution, M21 tier A |
| **Phase** | 2 |
| **Mock-up reference** | None (new screen); visual language from Strategy Lab + Cockpit |

## Purpose

Create, configure, deploy and supervise **any strategy type on any timeframe**, and move each strategy through its lifecycle (draft → backtested → validated → paper → approve → auto) with gates enforced.

## `/strategies`: registry

| Tier | Layout |
|---|---|
| ≥ xl | Filter bar (type, asset class, timeframe, lifecycle stage, mode, status) + `DataTable` |
| md–lg | Same, with P3 columns hidden |
| ≤ ph | Filter chips (scroll) + strategy cards |

**Table columns:**

| Priority | Columns |
|---|---|
| P1 | Name, lifecycle stage, mode chip, status, today P&L |
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
1. **Template.** Pick a template, then fill in `ParamForm`. Templates: scalping (tick/L2), intraday, EMA/MA cross, mean reversion, breakout, swing/position, grid/DCA, market making (Nautilus or Hummingbot), pairs/stat-arb, event/news-driven, ML-signal, LLM/decision-model signal.
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
| Sizing | Fixed, fixed-fractional, vol-target, Kelly-capped, risk-parity |
| Risk policy | Link to the strategy-level policy (D06) + quick limits |
| Schedule / sessions | Trading hours; calendar blackouts (e.g. no trading ±5 min around NFP) |
| Review | Manifest diff + validation of the manifest schema |

**Save:** `strategy.create` (C1). The strategy starts as `draft`, and the next suggested step is "Run backtest" (→ D04).

## `/strategies/:id`: detail

| Tier | Layout |
|---|---|
| ≥ xl | Header (name, stage stepper, mode switch, status, Start/Pause/Stop) + tabs: Overview · Parameters · Performance · Positions & orders · Signals · Gates · Versions · Logs |
| ≤ ph | Header condensed; stage stepper as "Stage 4/6"; tabs as a select |

**Tabs:**

| Tab | Shows | Source |
|---|---|---|
| Overview | Live P&L, equity curve (live vs paper vs backtest expectation), drawdown, exposure, last signals, health (paused-by-DQ/risk reasons) | `/strategies/{id}`, `/strategies/{id}/runs`, WS `signals`, `positions` |
| Parameters | `ParamForm` (current version); edit → new version | `/strategies/{id}` |
| Performance | Metrics table (return, Sharpe, Sortino, max DD, hit rate, avg win/loss, turnover, **realised vs modelled costs**), distribution of returns, comparison with backtest (tracking error) | `/strategies/{id}/runs?metrics=1` |
| Positions & orders | Filtered blotter | `/positions?strategy=`, `/orders?strategy=` |
| Signals | Signal log with risk outcome + provenance | `/signals?strategy=` |
| **Gates** | Checklist per DESIGN/spec §8: walk-forward OOS ✔/✖, MC p-value, deflated Sharpe, look-ahead/recursive check, post-cutoff LLM eval (if applicable), paper period elapsed / required, tracking error within tolerance, safety drills | `/strategies/{id}?gates=1` |
| Versions | Version list with `DiffView`; rollback | `/strategies/{id}?versions=1` |
| Logs | `LogStream` for this strategy | Loki proxy via `/system/logs?strategy=` |

**Actions:**

| Control | Command | Level | Rule |
|---|---|---|---|
| Start (paper) | `strategy.start` | C1 | Needs stage ≥ validated, or a "paper from backtested" override |
| Pause / Resume / Stop | `strategy.pause` / `strategy.resume` / `strategy.stop` | C1 | — |
| Mode → approve | `strategy.set_mode` | C2 | — |
| Mode → **auto** | `strategy.set_mode` | **C3** | Disabled until all gates pass |
| Promote / demote stage | `strategy.promote` / `strategy.demote` | C1 (auto stage C3) | — |
| Edit params | `strategy.update_params` | C1 for paper; **C2** if live; **C3** if the change increases risk (size, leverage) | — |
| Flatten | `position.close` (strategy scope) | C2 | — |
| Run backtest / validation | `lab.backtest.run` / `lab.validate.run` | C1 | — |

## Additions from the CryptoTrader review

- **Manifest fields shown on the registry and detail:** `counterparty` (who pays you, the rule from [14 §3](../../14-strategy-evidence-and-validation.md#3-strategy-catalogue-evidence-ranked-templates)), `benchmark` (what it must beat, e.g. buy-and-hold BTC or cash yield), **priority** (P1 / P2 / P3 / X), `sleeve` and **kill criteria**.
- The builder refuses templates on the never-build list and shows why.
- Detail shows **per-year and per-regime** results, **2× and 3× cost stress**, the trial counter and the worst walk-forward fold (from the validation harness).

## Bots tab (`/strategies/bots`; see [15 §1](../../15-bots-hitl-and-worm-audit.md#1-trading-bots))

- **List:** bot, strategy version, market scope (instrument / list / dynamic selection), venue & sleeve, **mode chip (paper · HITL · autonomous)**, status, pending approvals, today P&L.
- **Create wizard:** strategy version → market scope → venue & sleeve → mode → approval policy (TTL, large-order threshold, escalation rules) → review (risk preview).
- **Actions:** `bot.create` (C1), `bot.set_mode` → HITL/paper (C1), → **autonomous (C3, disabled while gates fail)**, `bot.pause`/`resume`/`stop` (C1), `bot.approval_policy.set` (tighten C1, loosen C3).
- **Detail:** mode history (WORM), approvals (shown card, decision, latency, outcome), auto-downgrade events.

## Acceptance criteria

1. **Template coverage:** every template creates a valid manifest, which a backtest then runs.
2. **Auto mode:** can't be selected while gates fail; the UI shows exactly which gate fails.
3. **Timeframe compatibility:** a strategy that subscribes to a resolution an instrument can't provide is blocked at save with a clear message.

## Backend contract

- **Queries:** `/strategies`, `/strategies/{id}` (+ `gates`, `versions`, `metrics`), `/strategies/templates`, `/strategies/{id}/runs`, `/signals`, `/system/logs`.
- **WebSocket topics:** `signals`, `positions`, `orders`, `lab.job`.
- **Commands:** `strategy.*`, `lab.generate_strategy`, `lab.backtest.run`, `lab.validate.run`, `position.close`.
