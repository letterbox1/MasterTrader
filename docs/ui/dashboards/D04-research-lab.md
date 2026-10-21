# D04 · Research Lab

| | |
|---|---|
| **Routes** | `/lab` (jobs & experiments), `/lab/backtests/:id`, `/lab/experiments/:id` |
| **Modules** | M7 lab, M6 features, M16 measured costs, M21 tier-A training |
| **Phase** | 2 |
| **Mock-up reference** | `strategy-lab-nautilustrader-simulation.png` |

## Purpose

Backtest, validate, optimise and compare strategies, and understand them, using realistic **measured** costs and strict point-in-time data.

## `/lab`

| Tier | Layout |
|---|---|
| ≥ xl | Left: "New run" panel (8 col). Right: job queue (live) + recent experiments table (16 col). |
| md–lg | New run as a drawer; jobs + experiments stacked |
| ≤ ph | Jobs list + "New run" floating button → full-screen sheet. Editing complex runs is best on desktop, but it is possible on phones. |

**New run panel:**

| Field | Options |
|---|---|
| Strategy + version | Combobox |
| Run type | Backtest (fast vectorised screener **or** Nautilus "truth" engine), walk-forward, purged K-fold, Monte Carlo permutation, parameter sweep (Optuna), validation suite (all), distillation (tier A/B) |
| Data range | Date range + `as_of` (point-in-time); instruments; resolution (tick → 1D) |
| Cost model | **Measured (default)** or custom fees/slippage/latency/funding; shows which measured snapshot is used |
| Fill model (Nautilus) | L1/L2 replay, queue position, latency |
| Benchmark | Buy-and-hold, equal weight, custom |
| Sweep space | Param ranges from the manifest, objective, trials, complexity penalty |
| Resources | Max workers, time cap |

**Submit:** `lab.backtest.run` / `lab.sweep.run` / `lab.validate.run` (C1). The run shows in the queue with progress.

**Job queue:**
- **Columns:** status, type, strategy, progress, ETA, started.
- **Actions:** cancel (`lab.job.cancel`, C1), open.

**Experiments table:**
- **Columns:** MLflow-backed runs with key metrics.
- **Actions:** multi-select → **Compare**.

## `/lab/backtests/:id`: result

| Tier | Layout |
|---|---|
| ≥ xl | Header (strategy@version, range, engine, cost model, data hash) + KPI strip + tabs |
| ≤ ph | KPI scroller + tabs as accordions; charts full width |

**Tabs:**

| Tab | Shows |
|---|---|
| Summary | Return, CAGR, Sharpe, Sortino, Calmar, max DD, hit rate, profit factor, turnover, exposure, **costs breakdown** (fees, spread, slippage, funding/swap); equity curve vs benchmark; drawdown chart; monthly returns heatmap |
| Trades | Trade list (`DataTable`, card view on phones); click → chart with entry/exit markers |
| Robustness | Walk-forward folds table; MC permutation distribution with p-value marker; bootstrap Sharpe CI; deflated Sharpe; parameter-stability heatmap (sweeps) |
| Bias checks | Look-ahead & recursive analyser results (pass/fail with offending signals); point-in-time audit (any data with `ingest_time > as_of` → fail) |
| Costs | Modelled vs measured costs; sensitivity (results at 0.5×/1×/2× costs) |
| Gates | Which promotion gates this run satisfies (feeds D03 Gates) |
| Reproduce | Code version, manifest, data snapshot ids, seed, engine version; "Re-run" button |

**Actions:**

| Action | Command | Level |
|---|---|---|
| Re-run | `lab.backtest.run` | C1 |
| Promote strategy stage | `strategy.promote` | C1 |
| Export report (PDF/HTML) | — | C0 |
| Open in notebook | Deep link (desktop) | C0 |

## `/lab/experiments/:id`: compare

- Up to 6 runs side by side.
- Metric table with best values highlighted.
- Overlaid equity curves.
- Parameter diff.
- Cost assumptions diff.

## Strategy generator (sandbox) panel

Opened from D03 "Describe it", or from here:
- prompt → progress;
- generated code (read-only diff);
- sandbox log;
- first backtest.

**Save as draft:** `strategy.create` (C1). A banner states "Generated code ran in an isolated sandbox with no network or secrets."

## Acceptance criteria

1. **Engine labelling:** every result is clearly labelled "Screener" vs "Nautilus truth".
2. **Gate eligibility:** only truth results count for gates.
3. **Costs:** shown on every result. A result run with zero costs is flagged with an amber "Unrealistic costs" chip.
4. **Reproducibility:** re-running with the same inputs yields the same results (verified by data hash + seed).

## Backend contract

- **Queries:** `/lab/backtests`, `/lab/backtests/{id}`, `/lab/experiments`, `/lab/experiments/{id}`, `/lab/jobs`, `/data/costs?snapshot=`.
- **WebSocket topics:** `lab.job`.
- **Commands:** `lab.backtest.run`, `lab.sweep.run`, `lab.validate.run`, `lab.generate_strategy`, `lab.job.cancel`, `strategy.create`, `strategy.promote`.
