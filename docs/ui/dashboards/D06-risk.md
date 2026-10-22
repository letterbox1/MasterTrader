# D06 · Risk

| | |
|---|---|
| **Route** | `/risk` (tabs: Overview · Policy · Events · Stress · Changes · Live (Phase 7)) |
| **Modules** | M11 risk manager, M16 monitor, M5 calendar (blackouts) |
| **Phase** | 2 (Stress tab per R2.57; Live tab: capital steps, kill criteria, weekly reviews in 7) |
| **Mock-up reference** | `autonomous-risk-governor-kill-switch-hub.png` (fix: status-bar overlap, full-height sidebar, native `confirm()` → `ConfirmSheet`) |

## Purpose

See and control the system's risk:
- current limit usage and the kill/dead-man state;
- the **risk policy** (user inputs at every level);
- the events log;
- stress tests;
- the audited history of every change;
- from Phase 7, live capital steps, kill-criteria state, gate reports and weekly reviews.

Every number on this page is a **configurable default** from [16](../../16-configuration-and-safety-model.md), shown with the layer that set its effective value ([ui §3.7](../README.md#37-settings-show-configurable-defaults-and-their-layer)).

## Layout by tier

| Tier | Layout |
|---|---|
| ≥ 2xl | Row 1: Kill switch tile (8) · Dead-man tile (8) · Risk state tile (8). Row 2: limit gauges grid (24). Row 3: exposure breakdown (12) + recent risk events (12). |
| xl/lg | Kill + dead-man side by side; gauges 3-up; breakdown + events stacked |
| md | 2-column |
| ≤ ph | Kill switch card (full width, large) → dead-man → gauges list → events |

## Overview widgets

| Widget | Shows | Source |
|---|---|---|
| **Kill switch** | State (ARMED/HALTED), last trigger (reason, source, time), big HALT button, and what happens on halt: stops new trading, cancels orders, applies each bot's `on_system_failure` (default `flatten`), freezes new treasury/earn moves, and (from Phase 5, default on) sweeps hot trading balances to the vault address. Protective exits continue | WS `kill`, `/risk/state` |
| **Dead-man** | The three layers ([16 §3.1](../../16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch)): **1. in-engine watchdog** (feeds, risk, DB, NATS heartbeats); **2. external `deadman` sidecar** (watches the engine's own heartbeat with its own keys and connections); **3. venue-side** cancel-after timers (refresh/timeout per venue) and resting venue stops per position. Per heartbeat: last beat and threshold; countdown when one is late; next action (defaults: cancel open orders at 5 s, apply each bot's `on_system_failure` at 10 s; configurable). Shows positions missing a resting venue stop as a breach | WS `heartbeat`, `/risk/state` |
| **Risk state** | Bot mode summary (paper / hitl / autonomous counts), trading allowed (Y/N + reasons), current ladder rung, system drawdown stage, audit-integrity status (`ok` / mismatch + action), egress IP/country check, active blackouts (calendar), DQ-paused instruments | `/risk/state`, WS `risk.state`, `dq.status`, `cal` |
| **Limit gauges** (`LimitBar`) | Global: daily loss, drawdown from peak with **both stages** marked (system defaults: 10% → no new entries; 25% → flatten to stablecoins/AUD + 30-day review lock), gross/net exposure, leverage, open orders, order rate. Per sleeve: drawdown with its two stages (defaults 10% → halve new sizes; 15% → halt). Per venue: concentration vs cap (default ≤ 25% of total equity). Per venue/bot/asset-class: top consumers. Each shows used / limit / warn / breach and the layer that set the limit. | `/risk/state`, WS `risk.state` |
| **Exposure breakdown** | By asset class, currency, venue, strategy, correlated cluster (USD, crypto beta); VaR/ES estimate | `/risk/state?breakdown=1` |
| **Recent risk events** | Vetoes, approvals required, breaches, auto-pauses, kill triggers, with reasons + links to orders/strategies | `/risk/events`, WS `risk.event` |

## Policy tab: risk policy editor (user inputs)

**Policy tree** (left; a select on phones), mapped to the configuration layers ([16 §1](../../16-configuration-and-safety-model.md#1-configuration-layers-tighten-only-inheritance)):
- Hard ceilings (L0): shown here; edited in the **Ceilings section of the strategy settings** ([D03 `/strategies/settings`](D03-strategies.md#strategiessettings-strategy-settings-and-hard-ceilings)), which applies to every bot
- Global (L1): system drawdown stages, failure behaviour, audit-integrity action, venue concentration
- Venues / accounts (L2): notional, leverage, allowed products, price collar, API-error pause (also the venue registry below)
- Sleeves (L3): capital, risk budget, daily loss, drawdown stages, capital-step plan, kill criteria
- Bots (L4): per-bot overrides (tighter only); edited in D03 Bots, shown here read-through
- Instruments / asset classes
- Portfolio (correlation, VaR)
- Sizing defaults (risk per trade, max position, quarter-Kelly ceiling)
- Data freshness (stale thresholds per bot class)
- Blackouts (calendar rules)
- Dead-man / kill configuration (watchdog timers, `on_system_failure`, `auto_resume_after_crash`, venue cancel-after timers)

**Each node shows a form (`SettingField`, `NumberInput`/`Slider`/`Toggle`) with:**
- the **effective value** and the layer that set it (`LayerBadge`): effective = the strictest across layers;
- the **L0 hard ceiling** with an "Edit ceilings" link to the strategy settings Ceilings section. Ceilings are no longer read-only or file-based: tightening a ceiling is immediate (C1); loosening one is C3 (Telegram approve + TOTP + cool-down) like every other loosening;
- the **default** from [16 §2](../../16-configuration-and-safety-model.md#2-default-values-all-configurable) with a link ("Default: 3% of sleeve");
- inheritance ("inherits L1 system: 3%", plus an override toggle);
- help text.

**Defaults shown on first install** (all configurable; [16 §2.1](../../16-configuration-and-safety-model.md#21-risk-sizing-and-drawdown)): risk per trade 1% of sleeve; max position 10% of sleeve (memecoin 2%); daily loss 3% of sleeve; open positions 10 per sleeve; leverage 1× until you approve more (crypto derivatives ≤ 2× as an L0 ceiling); venue concentration ≤ 25% of total equity (range 10–30%); price collar 2% crypto majors / 0.5% FX majors / 1% ETFs; API/RPC errors 5 in 60 s → pause that venue 10 min; cost blow-out > 1.5× modelled over 20 fills → pause the bot; stale data 2 s fast / 60 s slow bots ([16 §2.2](../../16-configuration-and-safety-model.md#22-data-freshness-what-stale-means)); blackouts 15 min before to 15 min after high-importance events for `event_sensitive` bots, exits continue ([16 §2.8](../../16-configuration-and-safety-model.md#28-calendar-blackouts)).

**Saving:**
- **Save** produces a `DiffView`. Each change is tagged **tighten** (mint) or **loosen** (flare).
- The submit path is decided per diff:
  - only tightenings → C1, applied immediately;
  - any loosening → **C3** (`C3Flow`: Telegram approve + TOTP → cool-down timer → applied);
  - above a ceiling → blocked, with an explanation and a link to loosen the ceiling itself (C3);
  - inconsistent values (e.g. sleeve de-risk drawdown ≥ halt drawdown, per-transaction cap > 24 h cap) → rejected at save with the reason.
- Pending C3 changes show at the top with a countdown and **Cancel**.

**Import/export:** policy as YAML (C0 export; import goes through the same diff/C3 path).

## Events tab

`DataTable` of `risk.event`s:
- **Columns:** time, type (veto / breach / pause / approval-required / kill / dead-man), scope, rule, observed vs limit, action taken, related order/strategy.
- **Filters:** type, scope, date.
- **Rows:** expand to show full context + an audit hash.

## Stress tab

- **Phase:** Phase 2 ships the tab as a **placeholder** (empty state: "Stress tests aren't available yet", no sample numbers) until the stress engine lands. The historical shock replay (May 2022, Nov 2022, Aug 2024, Feb–Mar 2026) is planned as R2.57; custom/preset hypothetical shocks are optional and must exist before live capital (Phase 7).
- **Scenarios:** historical replays; later, presets (e.g. −15% crypto in 60 s, USD +3%, gap-down at open, venue outage, stablecoin de-peg) or custom shocks per asset class/instrument.
- **Run:** `risk.stress.run` (C1), enabled once available.
- **Results:** P&L impact by position/bot/sleeve/venue, limits breached, liquidation distances, hedge coverage.
- **History** of runs.

## Changes tab

`risk.change` audit:
- **Columns:** who (web/telegram/mcp/system), when, diff, classification, status (applied / pending cool-down / rejected / cancelled), hash.
- **Columns** also show the **layer** changed (L0–L4) and the setting's default.
- **Rollback** to any previous version: a new change, with the same tighten/loosen rules applied.

## Live tab (Phase 7)

The live-capital state from [16 §2.5–§2.6](../../16-configuration-and-safety-model.md#25-capital-steps-per-sleevebot) and [14 §7](../../14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7). Hidden until the first bot goes live.

| Widget | Shows | Source |
|---|---|---|
| **Capital steps** (`CapitalStepCard` per sleeve/bot) | Starting allocation (set per bot when it goes live; default A$2,000), current allocation and step, clean weeks in a row (default 4 needed), clean-week checklist for the current week (no kill-criterion breach, no unexplained recon mismatch, no S1/S2 incident, shortfall ≤ 1.5× modelled, weekly P&L inside the backtest 5th–95th band), next step (default +25% of current, up to the sleeve cap), step-down history | `/risk/capital-steps` |
| **Kill criteria** | Per sleeve/bot: each criterion (written in the manifest before deployment) with observed vs threshold and state (ok / warning / halted). Decay signals with one meaning each ([16 §2.6](../../16-configuration-and-safety-model.md#26-decay-and-kill-signals-one-meaning-each)): rolling 60-trade Sharpe/hit rate or CUSUM → downgrade to HITL; daily health check fail → halt the bot; kill criterion → halt the sleeve + step down; unexplained reconciliation mismatch > 24 h → halts everything | `/risk/kill-criteria`, WS `risk.event` |
| **Kill and lock state** | Current kill state and reason; system drawdown stage; the 30-day review lock countdown after a stage-2 system drawdown; count of stage-2 events (two end the trading programme; capital moves to hold-and-earn) | `/risk/state`, WS `kill` |
| **Gate reports** | Latest gate report per strategy/bot going live (link to D03 Gates) | `/strategies/{id}/gate-report` |
| **Weekly reviews** | The weekly review per live sleeve: tracking error vs backtest, realised vs modelled costs, DQ incidents, journal reconciliation, five worst trades; open/closed status; your sign-off (recorded in D14) | `/journal/reviews` |

| Control | Command | Level |
|---|---|---|
| Fund the starting allocation | `risk.capital.fund` | C3 |
| Approve a capital step | `risk.capital_step.approve` | C3 |
| Step down (manual) | `risk.policy.update` (sleeve allocation, tighten) | C1 |
| Restart a halted sleeve | `risk.sleeve.restart` | C3 |
| Close a review lock / weekly review | `risk.review.close` | C3 |
| Sign off a weekly review | `journal.review.signoff` (→ D14) | C1 |

## Actions summary

| Control | Command | Level |
|---|---|---|
| HALT | `risk.kill.on` | Kill |
| Resume trading | `risk.kill.off` | C3 (requires the cause cleared) |
| Edit an L0 ceiling | → D03 strategy settings, Ceilings (`risk.policy.update`, layer L0) | Tighten C1 (immediate); loosen C3 |
| Acknowledge an audit-integrity incident | `audit.integrity.ack` (→ D16 Audit) | C3 |
| Ack dead-man | `risk.deadman.ack` | C1 |
| Save policy (tighten only) | `risk.policy.update` | C1 |
| Save policy (any loosen) | `risk.policy.update` | C3 |
| Cancel pending change | `risk.policy.update` (cancel) | C1 |
| Run stress test | `risk.stress.run` | C1 (once available) |

## Additions from the CryptoTrader review

| Widget | Shows |
|---|---|
| **Sleeves** | Sleeves come from your policy, not a fixed list (example from [14 §3](../../14-strategy-evidence-and-validation.md#3-strategy-catalogue-evidence-ranked-templates): trend, carry, hold-and-earn, memecoin, unlock/event, plus the `manual` sleeve for D05 tickets). Per sleeve: capital, risk budget, usage, drawdown vs its two stages (defaults 10% de-risk / 15% halt), daily loss, status |
| **Fallback ladder** (`LadderIndicator`) | Current rung of the six ([14 §5](../../14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11)): **1 normal** · **2 half size / observe** · **3 hold** (decision late or feed stale) · **4 rules only** (exits managed, no new entries) · **5 halt sleeve** · **6 kill**, and what triggered it. Rung ≥ 3 auto-downgrades autonomous bots to HITL. Manual step down (C1), step up (C3). Rungs and sleeves render from the API, never hard-coded |
| **Venue registry** | Venue, products allowed for your residency, max leverage (crypto derivatives ≤ **2×**, an L0 ceiling), STP mode sent (`n/a (netting)` for netting brokers: OANDA, IG, Alpaca, IBKR), AUSTRAC check date, concentration vs cap (default ≤ 25% of total equity, range 10–30%), cancel-after timer support, status (`allowed` / `read_only` / `blocked`; `paper_ok` marks blocked products allowed on paper) |

Commands: `risk.ladder.set` (down = C1, up = C3), `venue.registry.update` (tighten C1, allow C3). Source: `/risk/state?ladder=1`, `/venues/registry`.

## Acceptance criteria

1. **Policy classification:** the UI never lets a loosening apply without C3; the server independently enforces this (test both).
2. **Ceilings:** visible on every field, with the layer that set each effective value; loosening an L0 ceiling goes through C3 (test web and server).
3. **Kill switch:** the HALT button is ≥ 56px tall on touch and works from a cold load in one tap + confirm.
4. **Dead-man countdown:** accurate to ±1 s against the server.
5. **No hard-coded numbers:** every limit, stage, timer and allocation shown comes from the API (effective value + layer + default), never from UI constants.
6. **Stress placeholder:** until `risk.stress.run` exists, the Stress tab shows an empty state, never sample results.

## Backend contract

- **Queries:** `/risk/policy` (effective values with layer and default), `/risk/state` (+ `breakdown`, `ladder`), `/risk/events`, `/risk/changes`, `/risk/stress`, `/venues/registry`; Phase 7: `/risk/capital-steps`, `/risk/kill-criteria`, `/strategies/{id}/gate-report`, `/journal/reviews`.
- **WebSocket topics:** `kill`, `heartbeat`, `risk.state`, `risk.event`, `dq.status`, `cal`.
- **Commands:** `risk.kill.on|off`, `risk.deadman.ack`, `risk.policy.update` (all layers incl. L0), `risk.stress.run`, `risk.ladder.set`, `venue.registry.update`, `audit.integrity.ack`; Phase 7: `risk.capital.fund`, `risk.capital_step.approve`, `risk.sleeve.restart`, `risk.review.close`, `journal.review.signoff`.
