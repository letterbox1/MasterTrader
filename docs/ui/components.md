# Component Library

These are shared components for `apps/web/src/components`. They're styled with the DESIGN.md v2 tokens and built on Radix primitives where interactive.

**Every component must:**
- implement the data states in [README §3.1](README.md#31-data-states-every-tile-implements-all-of-them);
- adapt via **container queries** (behaviour by its own width, not the viewport);
- pass the Playwright viewport matrix and axe checks.

Props are TypeScript-style. `?` means optional.

---

## 1. Shell & navigation

| Component | Purpose | Key props | Responsive behaviour |
|---|---|---|---|
| `AppShell` | Top bar + nav + content + status bar | `nav`, `banners` | Sidebar (≥ xl) → rail (md–lg) → bottom nav (< md); landscape-short → rail 56 |
| `TopBar` | §2.1 elements | `mode`, `killState`, `approvalsCount`, `notificationsCount`, `pulse` | Collapses search to an icon < lg; brand → mark only ≤ xs |
| `SideNav` / `NavRail` / `BottomNav` | Navigation | `groups[]`, `badges` | BottomNav: 5 items (4 + More at xxs) with safe-area padding |
| `MoreSheet` | Overflow nav on phones | `items[]` | Bottom sheet |
| `Banner` | Global banners | `severity: info\|warn\|critical`, `title`, `detail`, `action?`, `dismissible` | Text wraps; action becomes a full-width button < ph |
| `StatusBar` | Footer status | `items[]` | Hidden < md (moved into MoreSheet) |
| `CommandPalette` | ⌘K | `sources[]` (instruments, strategies, commands, routes) | Full-screen < md |
| `Breadcrumbs` | Sub-routes | `items[]` | Collapses middle items < md |
| `WorkspaceGrid` | Tile layout with saved layouts | `layouts{tier: Layout}`, `editable` | Per-tier layouts; drag/resize ≥ xl only |

## 2. Tiles & data display

| Component | Purpose | Key props | Notes |
|---|---|---|---|
| `Tile` | Base container | `title`, `live?`, `state`, `actions?`, `help?`, `span{tier}` | 32px header; window controls hidden ≤ ph |
| `KpiCard` | One metric | `label`, `value`, `unit?`, `delta?`, `deltaPct?`, `sparkline?`, `mode?: paper\|live`, `href?` | Value in `data-mono-xl`; tooltip shows the full value |
| `KpiStrip` | Row of KPIs | `items: KpiCard[]` | Grid ≥ md; snap scroller ph–sm; vertical stack at xxs |
| `StatusChip` | Status | `status: running\|idle\|degraded\|breach\|stale\|paper\|live\|approve`, `label` | Always has text |
| `HealthDot` | Heartbeat | `service`, `lastBeat`, `threshold` | Tooltip; pulses when live |
| `Delta` | Change display | `value`, `format`, `invert?` | Sign + ▲/▼ + colour |
| `Money` / `Qty` / `Price` | Formatters | `value: string(decimal)`, `ccy?`, `precision?`, `instrument?` | Tabular nums |
| `Timestamp` | Time | `ts`, `relative?` | Local time + UTC tooltip |
| `DataTable` | Tables | `columns[]` (with `priority: 1\|2\|3`), `rows`, `virtual?`, `rowActions?`, `cardRenderer` | Hides P3 columns < xl, P2 < md; **renders `cardRenderer` ≤ ph**; scrolls inside its own box |
| `LogStream` | Live logs | `source`, `filters`, `maxRows` | Virtualised; pause on hover/touch |
| `Sparkline` | Mini chart | `points`, `kind` | — |
| `Gauge` / `LimitBar` | Limit usage | `used`, `limit`, `warnAt`, `breachAt`, `label` | Colour + numeric text; the breach marker is labelled |
| `Heatmap` | Correlation, calendar, sentiment | `matrix`, `scale` | ECharts; scrolls inside its box < md |
| `EquityCurve` | Equity/drawdown | `series[]`, `benchmark?`, `drawdown?` | ECharts |
| `Distribution` | Histograms, MC results | `bins`, `markers` | ECharts |
| `EmptyState` / `ErrorState` / `Skeleton` | States | — | Required in every tile |

## 3. Trading components

| Component | Purpose | Key props | Notes |
|---|---|---|---|
| `PriceChart` | Candles/line with overlays | `instrumentId`, `spec` (tick, 1s…1W, tick/volume bars), `overlays[]` (indicators, fills, signals, decision nodes, events), `drawings?` | lightweight-charts; toolbar → menu < lg; full-screen mode; landscape-short fills height |
| `TimeframePicker` | Bar spec | `value`, `available` (from instrument min resolution) | Chips scroll horizontally on phones; unsupported resolutions disabled with a reason |
| `OrderBook` | L2 ladder | `instrumentId`, `levels`, `grouping` | Levels by tier (25/15/10/5); depth bars; spread row pinned |
| `TradesTape` | Recent trades | `instrumentId` | — |
| `OrderTicket` | Manual order entry | `instrumentId`, `side?`, `defaults` | Fields: side, type (market/limit/stop/stop-limit), qty or notional, price, TIF, reduce-only, brackets (TP/SL); **live risk preview** (`RiskPreview`); submit = C2 |
| `RiskPreview` | Pre-trade check preview | `intent` | Lists each check pass/fail, projected exposure, limits used, est. cost/slippage |
| `PositionRow` / `PositionCard` | Position | `position` | Actions: close (C2), reduce (C2), set brackets (C2) |
| `OrderRow` / `OrderCard` | Order | `order` | Actions: modify (C2), cancel (C1) |
| `ApprovalCard` | Approval request | `request` (intent, source, risk preview, TTL) | Approve (C2) / Reject; TTL countdown |
| `FillMarker` | Chart marker | `fill` | — |
| `ModeSwitch` | paper / approve / auto per strategy | `value`, `strategyId` | Changing to auto = C3 |
| `KillSwitchButton` | Global halt | `state` | Kill level; never hidden |

## 4. Forms & controls

| Component | Notes |
|---|---|
| `Field`, `NumberInput` (`inputmode="decimal"`, steppers ≥ 44px on touch), `Select`, `Combobox` (instrument search), `Toggle`, `Slider` (leverage, risk %), `DateRangePicker`, `TagInput`, `CodeEditor` (Monaco, read-only on phones), `JsonViewer` | Labels above inputs < md; validation from zod schemas |
| `ConfirmSheet` | Levels C1/C2; dialog ≥ md, bottom sheet < md, full screen at xxs; hold-to-confirm on touch |
| `C3Flow` | Shows the Telegram approval status → TOTP → cool-down timer → applied; cancellable |
| `DiffView` | Before/after for risk policy and strategy params; marks tighten (mint) vs loosen (flare) |
| `ParamForm` | Generated from a strategy manifest param schema (types, ranges, defaults) |

## 5. Intel, agents & records components

| Component | Purpose |
|---|---|
| `DocumentCard` | News/social item: source, time, tickers, sentiment, tier-B scores, relevance; open the original link |
| `EventCard` / `EventMap` | Geo event with severity and exposure (map: MapLibre, optional; list fallback < md) |
| `CalendarList` | Macro/earnings/IPO events with importance, consensus, actual, and **blackout** markers |
| `AgentTurn` | One agent's contribution: role, stance, confidence, cited sources (links to documents/bars) |
| `ConsensusBar` | Aggregated stance with confidence; shows the PM decision |
| `TierBScore` | Question → option probabilities bar + calibration badge + model version |
| `ProvenanceList` | Sources behind a signal/decision |
| `TaskCard` | Steps, verified links, deadline, scores; Done / Skip / Snooze / Details / Never |
| `RiskScoreBadge` | Airdrop/token risk 0–100 with top reasons |
| `JournalEntry` | Trade with rationale, signal, chart snapshot, notes, tags |
| `LotTable` | Lots and matches (method, holding days, discount eligibility) |
| `TaxSummaryCard` | FY figures with rule version + FX source |
| `AuditRow` | Command/audit entry with hash-chain status |
