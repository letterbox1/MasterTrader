# D01 · Cockpit

| | |
|---|---|
| **Route** | `/` |
| **Modules** | M11 risk, M12 execution, M16 monitor, M8 agents, M21 decision models, M19 tasks |
| **Phase** | 2 (shell + System tile from Phase 0) |
| **Mock-up reference** | `ui-examples/screenshots/autonomous-command-cockpit-quant-terminal.png` (see content corrections in ui-examples/README) |

## Purpose

The one-glance answer to five questions:
- Am I safe?
- What's running?
- What changed?
- What needs me?
- How am I doing?

The Cockpit is the default landing page on every device.

## Layout by tier

| Tier | Layout |
|---|---|
| 3xl/2xl | Row 1: KPI strip (6). Row 2: Safety tile (8 col) · Needs-you tile (8) · Strategy status (8). Row 3: Main chart (16) + Signals & decisions (8). Row 4: Live blotter (16) + Alerts feed (8). |
| xl/lg | KPI strip (4 + overflow) · Safety + Needs-you side by side · Strategy status · Chart · Blotter · Alerts |
| md | 2-column tiles; chart full width; blotter as table with P1/P2 columns |
| ≤ ph | Safety banner card → Needs-you → KPI snap scroller → Strategy cards → Chart (compact) → Blotter cards → Alerts |
| landscape-short | KPI strip as one scroll row; Safety + Needs-you in a 2-column row; chart fills height |

## Widgets

| Widget | Shows | Source | Update |
|---|---|---|---|
| **KPI strip** | Portfolio value (base ccy), P&L today ($ / %), open risk (exposure % of limit), drawdown from peak vs limit, margin used, realised fees + funding today; paper/live split shown | `GET /portfolio/summary`, WS `portfolio` | Live (1 Hz) |
| **Safety tile** | Kill switch state + button; risk state (ARMED/HALTED); daily-loss gauge; drawdown gauge; dead-man heartbeat countdown; feeds summary (ok/degraded/stale counts); last risk event | `/risk/state`, WS `risk.state`, `kill`, `heartbeat`, `dq.status` | Live |
| **Needs you** | Pending approvals (count + top 3 `ApprovalCard`s), urgent tasks (deadline < 48h), unacknowledged critical alerts, C3 changes awaiting Telegram | `/orders?status=pending_approval`, `/tasks?urgent=1`, `/notifications?severity=critical` | Live |
| **Strategy status** | Each active strategy: name, mode chip (paper/approve/auto), state (running/paused-by-DQ/paused-by-risk/stopped), today P&L, positions, last signal time; sort by attention | `/strategies?active=1`, WS `signals`, `positions` | Live |
| **Main chart** | Selected instrument (default: largest exposure) with fills, signals, decision nodes, calendar markers; timeframe picker | `/markets/{id}/bars`, WS `md.bar`, `fills`, `signals` | Live (≤ 4 Hz) |
| **Signals & decisions** | Latest signals (strategy / agent / tier B) with direction, conviction/probability, risk outcome (pass/veto/approval), provenance link | WS `signals`, `tierb`, `/signals?limit=20` | Live |
| **Live blotter** | Today's orders and fills: time, instrument, side, qty, price, status, strategy, slippage (bps) vs decision | `/orders`, `/fills`, WS `orders`, `fills` | Live |
| **Alerts feed** | Alerts (DQ, cost blow-outs, anomalies, risk events) with severity, time, deep link | WS `notifications` | Live |

## Actions

| Control | Location | Command | Level |
|---|---|---|---|
| HALT / resume | Safety tile + top bar | `risk.kill.on` / `risk.kill.off` | Kill / C3 |
| Approve / Reject order | Needs-you `ApprovalCard` | `approval.approve` / `approval.reject` | C2 / C1 |
| Pause / resume strategy | Strategy status row menu | `strategy.pause` / `strategy.resume` | C1 |
| Flatten strategy | Strategy row menu | `position.close` (all for strategy) | C2 |
| Acknowledge dead-man warning | Safety tile | `risk.deadman.ack` | C1 |
| Change chart instrument / timeframe | Chart | — (UI) | C0 |
| Open full screen | Each tile | — | C0 |
| Customise layout | Header "Edit layout" (≥ xl) | `system.settings.update` (prefs) | C0 |

## States & alerts

- **Kill ON:**
  - The Safety tile turns red with the reason and trigger source.
  - Strategy rows show "halted".
  - The chart is shaded.
- **No live strategies:** an empty state with "Create strategy" (→ D03) and "Run backtest" (→ D04).
- **Paper-only:** all money tiles show a PAPER marker.

## Acceptance criteria

1. **Speed:** the kill switch is reachable within one tap/click at every tier, and its state is reflected in < 1 s after the server acknowledges.
2. **Approvals:** these are actionable from the Cockpit without navigation.
3. **Paper vs live:** values are never summed without a label.
4. **Layout:** passes the DESIGN.md §6.8 matrix; at 320px, the Safety and Needs-you tiles are visible without scrolling past the KPIs.

## Backend contract

- **Queries:**
  - `/portfolio/summary`, `/risk/state`, `/strategies?active=1`;
  - `/orders`, `/fills`, `/signals`, `/tasks?urgent=1`, `/notifications`;
  - `/markets/{id}/bars`.
- **WebSocket topics:** `portfolio`, `positions`, `orders`, `fills`, `risk.state`, `kill`, `heartbeat`, `dq.status`, `signals`, `tierb`, `notifications`, `md.bar`.
- **Commands:** `risk.kill.on|off`, `approval.approve|reject`, `strategy.pause|resume`, `position.close`, `risk.deadman.ack`.
