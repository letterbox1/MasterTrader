# MasterTrader UI Scope

This is the complete frontend scope, ready for implementation. It defines what every screen shows, how it behaves, which components it uses, and which backend contract it depends on.

| Doc | What it covers |
|---|---|
| **This file** | Information architecture, routes, the app shell, global elements, cross-cutting UI rules |
| [components.md](components.md) | Component library: every shared component with its props, states and responsive rules |
| [dashboards/](dashboards/) | One spec per dashboard (D01–D17) using a fixed template |
| [mobile-and-telegram.md](mobile-and-telegram.md) | Phone-specific flows, PWA, Telegram bot and mini-app views |

**Sources of truth:**
- [../../DESIGN.md](../../DESIGN.md): visuals and responsive rules.
- [../02-v1-architecture.md §7](../02-v1-architecture.md#7-api-contract-mt_api): API, WebSocket topics and confirmation levels.
- [../03-build-spec.md](../03-build-spec.md): module behaviour.

Visual references are in [../../ui-examples/](../../ui-examples/README.md). Where those references conflict with these docs, these docs win.

---

## 1. Information architecture

| # | Dashboard | Route | Primary modules | Phase | Mock-up reference |
|---|---|---|---|---|---|
| D01 | [Cockpit](dashboards/D01-cockpit.md) | `/` | M11, M12, M16, M8, M21 | 2 | Cockpit |
| D02 | [Markets](dashboards/D02-markets.md) | `/markets`, `/markets/:instrumentId` | M1, M6, M16, M21 | 1 | Cross-Asset Terminal |
| D03 | [Strategies](dashboards/D03-strategies.md) | `/strategies`, `/strategies/:id` | M0, M11 | 2 | — (new) |
| D04 | [Research Lab](dashboards/D04-research-lab.md) | `/lab`, `/lab/backtests/:id`, `/lab/experiments/:id` | M7, M6 | 2 | Strategy Lab |
| D05 | [Execution](dashboards/D05-execution.md) | `/execution` | M12, M11, M16 (TCA) | 2 | Order Execution Hub |
| D06 | [Risk](dashboards/D06-risk.md) | `/risk` | M11, M16 | 2 | Risk Governor & Kill-Switch Hub |
| D07 | [Data & Quality](dashboards/D07-data-quality.md) | `/data` | M1, M16 | 1 | Free Data Pipeline Sentinel |
| D08 | [Intel](dashboards/D08-intel.md) | `/intel` | M2, M3, M5, M21 | 4 | Social/Macro/Geopolitical Firehose |
| D09 | [Agents & Decisions](dashboards/D09-agents.md) | `/agents`, `/agents/runs/:id` | M8, M9, M21 | 6 | Multi-Agent Debate |
| D10 | [Models & Memory](dashboards/D10-models-memory.md) | `/models` | M21, M9, M7 | 6 | — (new) |
| D11 | [Market Making](dashboards/D11-market-making.md) | `/mm` | M13 | 6 (optional) | Hummingbot MM Terminal |
| D12 | [Airdrops & Launches](dashboards/D12-airdrops.md) | `/airdrops`, `/airdrops/:id` | M4 | 5 | Launch Radar |
| D13 | [Tasks & Curation](dashboards/D13-tasks-curation.md) | `/tasks` | M19 | 5 | Launch Radar (manual queue) |
| D14 | [Journal](dashboards/D14-journal.md) | `/journal`, `/journal/trades/:id` | M18 | 3 | — (new) |
| D15 | [Tax & Reports](dashboards/D15-tax.md) | `/tax` | M18 | 3 | AU EOFY Tax Ledger |
| D16 | [System](dashboards/D16-system.md) | `/system` (+ `/system/audit`, `/system/settings`) | M17, ops | 0 | — (new) |
| D17 | [MCP Console](dashboards/D17-mcp-console.md) | `/mcp` | M20 | 8 (optional) | Claude MCP Control |

**Navigation groups** (sidebar order):
- **Trade:** Cockpit, Markets, Execution, Risk.
- **Build:** Strategies, Research Lab, Agents, Models & Memory, Market Making.
- **Intel:** Intel, Data & Quality.
- **Crypto:** Airdrops, Tasks.
- **Records:** Journal, Tax.
- **System:** System, MCP.

On phones the bottom nav shows **Cockpit · Markets · Execution · Tasks · More**; everything else is under More.

## 2. App shell (all routes)

Layouts per tier follow [DESIGN.md §6.4](../../DESIGN.md#64-app-shell-by-tier).

### 2.1 Top bar (always visible)

| Element | Content | Behaviour |
|---|---|---|
| Brand | Signal M mark + wordmark (mark only ≤ xs) | Links to `/` |
| Command palette trigger | Search box (≥ lg) / icon (< lg); `⌘/Ctrl+K` | Search instruments, strategies, commands, docs; recent items |
| **Mode badge** | `PAPER` (cobalt) / `APPROVE` (warn) / `LIVE AUTO` (mint) / mixed: `n LIVE` | Click → per-strategy mode summary sheet |
| **Kill switch** | `HALT` button (Flare) / when ON: solid red `HALTED` + reason | ON: one confirm (Kill level). OFF: C3 flow. Visible at **every** tier. |
| **Approvals** | Bell-like icon with count of pending approvals | Opens the approvals sheet (D05 §Approvals) |
| Notifications | Icon + unread count | Opens the notification centre (alerts, task digests, system) |
| System pulse | Engine / data / risk heartbeat dots (≥ md; condensed into one dot < md) | Tooltip with last heartbeat; click → D16 |
| Profile | Theme, density, timezone, logout | Settings shortcut |

### 2.2 Global banners (stacked under the top bar, highest severity first)

1. **Kill switch ON** (red): reason, triggered by, time, "Review" → D06.
2. **Dead-man's warning** (red): heartbeat missing for N s, countdown.
3. **Data degraded** (amber): n feeds stale/bad, affected strategies paused → D07.
4. **Budget / local-model fallback** (cobalt info) → D10.
5. **Read-only mode** (grey): API or DB degraded.

Banners are dismissible only when the condition is informational. Red banners persist until the condition clears.

### 2.3 Status bar (bottom, ≥ md; folded into the More sheet on phones)

The status bar shows:
- engine version;
- kernel latency (measured);
- feed status summary;
- risk state (`ARMED` / `HALTED`);
- journal sync status;
- backup age;
- the local clock with UTC on hover.

It must not overlay content: the bar is sticky with a reserved space, per DESIGN.md.

### 2.4 Navigation

- **Sidebar/rail/bottom nav** per tier.
- **Badges** show counts: pending approvals (Execution), open tasks (Tasks), DQ incidents (Data), unread alerts.
- **Workspaces** (≥ xl): users can save tile layouts per dashboard, with a "Reset layout" option.

## 3. Cross-cutting UI rules

### 3.1 Data states (every tile implements all of them)

| State | Visual | Notes |
|---|---|---|
| Loading | Skeleton matching the final layout (no spinners in tiles) | ≤ 300 ms before the skeleton shows |
| Live | Normal; a live dot pulses (respects reduced motion) | — |
| Stale | Values dimmed + amber "stale 12s" chip | From `dq.status` or WebSocket gap |
| Degraded | Amber outline + reason tooltip | E.g. one source down, a fallback in use |
| Error | Inline error card with retry and a link to D16 | Never a blank tile |
| Empty | Helpful empty state with a primary action ("Create strategy") | No fake data |
| Paper vs Live | Every money figure shows a mode marker where ambiguous: PAPER (cobalt outline) vs LIVE | Never mix paper and live totals without a label |
| Unconfirmed | Positions/orders awaiting reconciliation are shown with a hatched background + "unconfirmed" | From venue disconnects |

### 3.2 Numbers, time and currency

- **Numbers:**
  - JetBrains Mono, tabular figures, right-aligned in tables.
  - Precision per instrument.
  - Large numbers are abbreviated only in KPI tiles (1.48M), with the full value in a tooltip.
- **P&L and deltas:** a sign + ▲/▼ + colour, never colour alone.
- **Currency:** base currency (AUD by default) with an optional per-instrument quote currency. FX conversions show the rate source on hover.
- **Time:** local time with UTC on hover; relative times ("12s ago") update live; timestamps in logs show milliseconds.

### 3.3 Actions & confirmation

These map to the API confirmation levels ([architecture §7.2](../02-v1-architecture.md#72-commands-rest-write)).

| Level | UI pattern |
|---|---|
| C0 | Immediate; toast with undo where possible |
| C1 | Confirm sheet: title, consequence, Confirm / Cancel |
| C2 | Confirm sheet + **risk preview**: projected exposure, limits used, checks pass/fail, estimated cost. **Hold-to-confirm** (600 ms) on touch, Enter on desktop. |
| C3 | C2, then "Approval sent to Telegram" state with a countdown; waits for Telegram approval + TOTP; then shows a cool-down timer until it takes effect; can be cancelled |
| Kill | Single confirm with a large target; never behind a menu |

**Rules:**
- **Destructive buttons:** never adjacent to safe ones without at least 8px spacing. They use Flare styling and specific labels ("Cancel 3 orders", not "OK").
- **Idempotency:** each confirm sheet generates an idempotency key, and double-submits are ignored.
- **Feedback:** every command result shows a toast, links to its audit entry, and updates the affected tiles via WebSocket.

### 3.4 Real-time

- **Throttling:** charts ≤ 4 updates/s; tables ≤ 1/s with batched row updates; price-flash rules from DESIGN.md §8.
- **Gaps:** on a WebSocket gap or reconnect, show a "Re-syncing" chip, refetch via REST, then resume.
- **Background tabs:** subscriptions drop to 0.2 Hz except for alerts, approvals and kill state.

### 3.5 Accessibility & input

- Meets WCAG 2.2 AA as defined in DESIGN.md §9.
- **Keyboard shortcuts:**
  - `⌘K` palette;
  - `g c` Cockpit, `g m` Markets, `g e` Execution, `g r` Risk;
  - `b`/`s` open the order ticket (buy/sell) on Markets;
  - `Shift+Esc` opens the kill confirm.
- Shortcuts are listed in `?`.

### 3.6 Permissions & sessions

- **Single user.** The session times out after 12 h of inactivity (configurable), and re-login needs TOTP.
- **Re-auth:** any C3 action re-checks the session even if Telegram approves.

## 4. Implementation notes for the backend

Each dashboard spec ends with a **Backend contract** section:
- the REST queries and WebSocket topics it needs;
- the commands it issues.

Together these sections are the backlog for `mt_api`. The union of all of them must equal the catalogue in architecture §7 (CI check: an OpenAPI diff against `docs/ui/contract-index.json`, generated later).
