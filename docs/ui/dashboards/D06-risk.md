# D06 · Risk

| | |
|---|---|
| **Route** | `/risk` (tabs: Overview · Policy · Events · Stress · Changes) |
| **Modules** | M11 risk manager, M16 monitor, M5 calendar (blackouts) |
| **Phase** | 2 |
| **Mock-up reference** | `autonomous-risk-governor-kill-switch-hub.png` (fix: status-bar overlap, full-height sidebar, native `confirm()` → `ConfirmSheet`) |

## Purpose

See and control the system's risk:
- current limit usage and the kill/dead-man state;
- the **risk policy** (user inputs at every level);
- the events log;
- stress tests;
- the audited history of every change.

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
| **Kill switch** | State (ARMED/HALTED), last trigger (reason, source, time), what happens on halt (cancel all; flatten yes/no per config), big HALT button | WS `kill`, `/risk/state` |
| **Dead-man** | Heartbeats per critical service (engine, monitor, risk, postgres, nats) with last beat and threshold; countdown when one is late; action configured (cancel / cancel + flatten) | WS `heartbeat` |
| **Risk state** | Mode summary (paper / approve / auto counts), trading allowed (Y/N + reasons), active blackouts (calendar), DQ-paused instruments | `/risk/state`, WS `risk.state`, `dq.status`, `cal` |
| **Limit gauges** (`LimitBar`) | Global: daily loss, drawdown (trailing/peak), gross/net exposure, leverage, open orders, order rate. Per venue/strategy/asset-class: top consumers. Each shows used / limit / warn / breach. | `/risk/state`, WS `risk.state` |
| **Exposure breakdown** | By asset class, currency, venue, strategy, correlated cluster (USD, crypto beta); VaR/ES estimate | `/risk/state?breakdown=1` |
| **Recent risk events** | Vetoes, approvals required, breaches, auto-pauses, kill triggers, with reasons + links to orders/strategies | `/risk/events`, WS `risk.event` |

## Policy tab: risk policy editor (user inputs)

**Policy tree** (left; a select on phones):
- Global
- Venues / accounts
- Strategies
- Instruments / asset classes
- Portfolio (correlation, VaR)
- Sizing defaults
- Blackouts (calendar rules)
- Dead-man / kill configuration

**Each node shows a form (`Field`/`NumberInput`/`Slider`/`Toggle`) with:**
- current value;
- **hard ceiling** (read-only, from the ceilings file, with a lock icon);
- inheritance ("inherits global: 3%", plus an override toggle);
- help text.

**Saving:**
- **Save** produces a `DiffView`. Each change is tagged **tighten** (mint) or **loosen** (flare).
- The submit path is decided per diff:
  - only tightenings → C1, applied immediately;
  - any loosening → **C3** (`C3Flow`: Telegram approve + TOTP → cool-down timer → applied);
  - above a ceiling → blocked, with an explanation.
- Pending C3 changes show at the top with a countdown and **Cancel**.

**Import/export:** policy as YAML (C0 export; import goes through the same diff/C3 path).

## Events tab

`DataTable` of `risk.event`s:
- **Columns:** time, type (veto / breach / pause / approval-required / kill / dead-man), scope, rule, observed vs limit, action taken, related order/strategy.
- **Filters:** type, scope, date.
- **Rows:** expand to show full context + an audit hash.

## Stress tab

- **Scenarios:** preset (e.g. −15% crypto in 60 s, USD +3%, gap-down at open, venue outage, stablecoin de-peg) or custom shocks per asset class/instrument.
- **Run:** `risk.stress.run` (C1).
- **Results:** P&L impact by position/strategy/venue, limits breached, liquidation distances, hedge coverage.
- **History** of runs.

## Changes tab

`risk.change` audit:
- **Columns:** who (web/telegram/mcp/system), when, diff, classification, status (applied / pending cool-down / rejected / cancelled), hash.
- **Rollback** to any previous version: a new change, with the same tighten/loosen rules applied.

## Actions summary

| Control | Command | Level |
|---|---|---|
| HALT | `risk.kill.on` | Kill |
| Resume trading | `risk.kill.off` | C3 (requires the cause cleared) |
| Ack dead-man | `risk.deadman.ack` | C1 |
| Save policy (tighten only) | `risk.policy.update` | C1 |
| Save policy (any loosen) | `risk.policy.update` | C3 |
| Cancel pending change | `risk.policy.update` (cancel) | C1 |
| Run stress test | `risk.stress.run` | C1 |

## Additions from the CryptoTrader review

| Widget | Shows |
|---|---|
| **Sleeves** | Capital per sleeve (core / carry / momentum / experimental), usage, drawdown vs sleeve stop |
| **Fallback ladder** | Current rung (normal → reduced size → close-only → flat → kill) and what triggered it; manual step down (C1), step up (C3) |
| **Venue registry** | Venue, products allowed for your residency, max leverage (crypto derivatives capped at **2×**), STP mode sent, AUSTRAC check date, concentration vs cap, status (`allowed` / `read_only` / `blocked`) | 

Commands: `risk.ladder.set` (down = C1, up = C3), `venue.registry.update` (tighten C1, allow C3). Source: `/risk/state?ladder=1`, `/venues/registry`.

## Acceptance criteria

1. **Policy classification:** the UI never lets a loosening apply without C3; the server independently enforces this (test both).
2. **Ceilings:** visible on every field.
3. **Kill switch:** the HALT button is ≥ 56px tall on touch and works from a cold load in one tap + confirm.
4. **Dead-man countdown:** accurate to ±1 s against the server.

## Backend contract

- **Queries:** `/risk/policy`, `/risk/state` (+ `breakdown`), `/risk/events`, `/risk/changes`, `/risk/stress`.
- **WebSocket topics:** `kill`, `heartbeat`, `risk.state`, `risk.event`, `dq.status`, `cal`.
- **Commands:** `risk.kill.on|off`, `risk.deadman.ack`, `risk.policy.update`, `risk.stress.run`.
