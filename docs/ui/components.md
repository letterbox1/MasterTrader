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
| `StatusChip` | Status | `status: running\|idle\|degraded\|breach\|stale\|paper\|hitl\|autonomous\|live`, `label` | Always has text. Mode labels: "Paper", "Approve (HITL)", "Autonomous" |
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
| `ApprovalCard` | Approval request | `request` (bot, intent, source, risk preview, signal reasons, chart link, TTL), `lines?` (batched card) | Same capabilities as the Telegram card ([15 §1.3](../15-bots-hitl-and-worm-audit.md#13-hitl-approval-via-telegram)): **Approve** (C2) · **Approve ½** (C2, bot requests) · **Reject** (C1) · **Pause bot** (C1). TTL countdown (defaults per bot horizon; MCP cards 5 min; [16 §2.3](../16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl)); expiry = reject. Large orders (default > 2% of sleeve or > A$5,000) need hold-to-confirm. A batched card from one dynamic-selection bot has per-line toggles; there is no other bulk approve |
| `FillMarker` | Chart marker | `fill` | — |
| `ModeSwitch` | `paper` / `hitl` / `autonomous` per bot | `value`, `botId` | paper → hitl = C2; → autonomous = C3 (disabled while gates fail); autonomous → hitl and anything → paper = C1 |
| `KillSwitchButton` | Global halt | `state` | Kill level; never hidden |

## 4. Forms & controls

| Component | Notes |
|---|---|
| `Field`, `NumberInput` (`inputmode="decimal"`, steppers ≥ 44px on touch), `Select`, `Combobox` (instrument search), `Toggle`, `Slider` (leverage, risk %), `DateRangePicker`, `TagInput`, `CodeEditor` (Monaco, read-only on phones), `JsonViewer` | Labels above inputs < md; validation from zod schemas |
| `ConfirmSheet` | Levels C1/C2; dialog ≥ md, bottom sheet < md, full screen at xxs; hold-to-confirm on touch |
| `C3Flow` | Shows the Telegram approval status → TOTP → cool-down timer → applied; cancellable |
| `DiffView` | Before/after for risk policy and strategy params; marks tighten (mint) vs loosen (flare) |
| `ParamForm` | Generated from a strategy manifest param schema (types, ranges, defaults). Manifest values are **proposals**: each field shows the proposal next to your sleeve/system limits; looser than a parent layer is rejected |
| `SettingField` | One configurable value ([README §3.7](README.md#37-settings-show-configurable-defaults-and-their-layer)): effective value, the layer that set it (`LayerBadge`: L0–L4), the 16 default with a link, inherited value, override toggle, tighten/loosen tag on edit |
| `LayerBadge` | Small chip naming the configuration layer (L0 ceiling · L1 system · L2 venue · L3 sleeve · L4 bot) that sets an effective value; tooltip shows the value at each layer |

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
| `CustodyTierBadge` | Wallet tier (vault / HL master / warm / hot / identity / burner) with watch-only lock |
| `CostGateResult` | On-chain cost gate: expected edge vs gas + slippage + MEV + fees, pass/block |
| `LadderIndicator` | Fallback-ladder rung (1–6: normal · half size/observe · hold · rules only (exits) · halt sleeve · kill) with trigger reason; rungs come from the API |
| `CapitalStepCard` | Phase 7: a bot's or sleeve's live allocation, current step, clean weeks (n/4 by default), next step size, kill-criteria status, approve-step action (C3) |
| `GateChecklist` | Gate profile results ([16 §2.4](../16-configuration-and-safety-model.md#24-validation-gates-per-strategy-gate-profile)): each gate's threshold (default or overridden), observed value, pass/fail, waiver link |
| `VenueStatusChip` | Registry status, AUSTRAC check age, max leverage |
| `PostureCard` | Telegram-derived postures (counts only, no text) |
| `ProvenanceFlags` | `train_ok` / `model_input_ok` / retention badges on sources and rows |
