# Mobile, PWA & Telegram

Phones are a first-class client for supervision and approvals. Deep research and editing are best on desktop, but every dashboard works down to 240px (DESIGN.md §6).

## 1. PWA

- **Install:** installable (manifest + service worker) with the Signal M app icon (`brand/app-icon.svg`).
- **Offline:**
  - the shell loads offline and shows the last known state with a clear **"Offline: data may be stale"** banner;
  - **no actions are queued offline**, except Kill, which tries every channel (see §3).
- **Notifications:** web push for critical alerts is optional; Telegram is the primary channel.

## 2. Phone flows (must be ≤ 3 taps from a cold open)

| Flow | Path |
|---|---|
| **HALT** | Top bar HALT → confirm |
| Approve an order | Notification/Telegram → `ApprovalCard` → hold-to-confirm (web) or Approve (Telegram; TOTP reply for large orders) |
| Check safety | Cockpit (Safety + Needs-you are first) |
| See P&L | Cockpit KPI scroller |
| Close a position | Execution → position card → Close → hold-to-confirm |
| Complete a task | Tasks → swipe Done (or a Telegram button) |
| Read the morning brief | Telegram digest → deep link to Intel |

**Phone landscape** (`landscape-short`) is for charts and tables: the rail replaces the bottom nav and the chart fills the height.

## 3. Telegram bot

The bot covers the C3 channel and phone-friendly control, using the **same commands** as the web via `mt_api`.

| Feature | Detail |
|---|---|
| Alerts | Severity-routed: critical (kill, dead-man, breach, DQ on traded instruments, audit-integrity mismatch, egress IP/country mismatch), warning, info; quiet hours (except critical). One fan-out: Grafana alerts → webhook → the `alert.*` consumer → Telegram / ntfy / email |
| Digests | **Morning brief** (contents below, canonical), daily/weekly task digests |
| Approvals | Order approvals using the HITL approval card below (**Approve · Approve ½ · Reject · Pause bot**), risk preview text, TTL. MCP-originated orders arrive here too (TTL default 5 min, [16 §2.3](../16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl)); MCP can never approve anything itself |
| **C3 confirmations** | "Approve risk change: raise BTC max position 0.5 → 0.8?" → Approve → bot asks for a **TOTP code** → server verifies → cool-down timer message → "Applied". The message names the layer being loosened (L0 ceiling … L4 bot) and the default. Before this path exists (Phase 0–1), C3 completes via the host-only break-glass CLI (`mtctl approve <id>` + TOTP), audited |
| Commands | `/status`, `/pnl`, `/positions`, `/kill` (confirm button), `/pause <strategy>`, `/resume <strategy>`, `/tasks`, `/brief` |
| **Bots** ([15 §1](../15-bots-hitl-and-worm-audit.md#1-trading-bots)) | `/bots`, `/bot <id>`, `/bot <id> pause\|resume\|stop`, `/bot <id> mode paper` (C1), `/bot <id> mode hitl` (C2 from paper; C1 from autonomous), `/bot <id> mode autonomous` (C3: approve + TOTP + cool-down; `auto` is accepted as a retired alias), `/approvals`. **HITL approval card:** bot, instrument, side, size, stop/target, risk preview, signal reasons, chart link, TTL; **Approve · Approve ½ · Reject · Pause bot**; expiry = reject; large orders (default > 2% of sleeve or > A$5,000, configurable) need a TOTP reply. TTL defaults: 60 s intraday · 15 min swing · 4 h position ([16 §2.3](../16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl)). Protective exits never wait for approval. |
| Tasks | Inline **Done · Skip · Snooze 1d · Snooze 1w · Never · Details** (Details deep-links to the task detail in D13) |
| Security | Bound to your Telegram user id only; the bot token lives in secrets. `/kill` works even if the web UI is down (bot → NATS `kill.set`): the bot's NATS credentials may publish **only** `kill.set`, and the engine writes the kill event to WORM with source `telegram`. |

**Morning brief (canonical contents).** This list is the single source; [04](../04-plan-of-action.md) and the roadmap link here. Sent daily at a time you set (Sydney time, in D13 Digests), from Phase 4:
1. Overnight news that matters to your positions and watchlist.
2. Sentiment movers.
3. Events mapped to the assets they affect.
4. Today's calendar with trading blackouts (default 15 min either side of high-importance events, [16 §2.8](../16-configuration-and-safety-model.md#28-calendar-blackouts)).
5. Telegram postures as **numbers only** (mention velocity, channel counts); never Telegram text ([12 §4](../12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
6. Positions and P&L (paper and live labelled separately).
7. Data and cost health (stale/bad feeds, cost blow-outs, quota headroom).
8. New vetted airdrops (from Phase 5).

Each item deep-links to the matching dashboard (D08, D01, D07, D12).

**Optional Telegram Mini App:** this reuses the web routes for Cockpit, Approvals and Tasks inside Telegram, with the same auth via a signed init-data → session exchange.

## 4. Acceptance criteria

1. **Kill switch:** `/kill` from Telegram halts trading within 1 s of the confirm tap, independently of mt-api's web worker.
2. **C3 completion:** every C3 change can be completed end to end on a phone (web or Telegram) without a desktop.
3. **Phone viewports:** all phone flows pass the DESIGN.md §6.8 phone viewports, including 280×653 (fold cover) and 568×320 (landscape).
