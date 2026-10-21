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
| Approve an order | Notification/Telegram → `ApprovalCard` → hold-to-confirm |
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
| Alerts | Severity-routed: critical (kill, dead-man, breach, DQ on traded instruments), warning, info; quiet hours (except critical) |
| Digests | Morning brief (positions, P&L, overnight news/events, calendar + blackouts, data health, new vetted airdrops), daily/weekly task digests |
| Approvals | Order approvals with inline **Approve / Reject**, risk preview text, TTL |
| **C3 confirmations** | "Approve risk change: raise BTC max position 0.5 → 0.8?" → Approve → bot asks for a **TOTP code** → server verifies → cool-down timer message → "Applied" |
| Commands | `/status`, `/pnl`, `/positions`, `/kill` (confirm button), `/pause <strategy>`, `/resume <strategy>`, `/tasks`, `/brief` |
| **Bots** ([15 §1](../15-bots-hitl-and-worm-audit.md#1-trading-bots)) | `/bots`, `/bot <id>`, `/bot <id> pause\|resume\|stop`, `/bot <id> mode paper\|hitl` (immediate), `/bot <id> mode auto` (C3: approve + TOTP + cool-down), `/approvals`. **HITL approval card:** bot, instrument, side, size, stop/target, risk preview, signal reasons, chart link, TTL; **Approve · Approve ½ · Reject · Pause bot**; expiry = reject; large orders need a TOTP reply. Protective exits never wait for approval. |
| Tasks | Inline **Done · Skip · Snooze 1d · Snooze 1w · Never** |
| Security | Bound to your Telegram user id only; the bot token lives in secrets. `/kill` works even if the web UI is down (bot → NATS `kill.set`). |

**Optional Telegram Mini App:** this reuses the web routes for Cockpit, Approvals and Tasks inside Telegram, with the same auth via a signed init-data → session exchange.

## 4. Acceptance criteria

1. **Kill switch:** `/kill` from Telegram halts trading within 1 s of the confirm tap, independently of mt-api's web worker.
2. **C3 completion:** every C3 change can be completed end to end on a phone (web or Telegram) without a desktop.
3. **Phone viewports:** all phone flows pass the DESIGN.md §6.8 phone viewports, including 280×653 (fold cover) and 568×320 (landscape).
