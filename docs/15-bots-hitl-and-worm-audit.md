# Trading Bots (Autonomous & HITL) and WORM Records

This doc tightens two parts of the spec:
1. **Trading bots:** you deploy a strategy onto a market or a selection of markets, then choose **autonomous** or **human-in-the-loop (HITL) via Telegram** per bot.
2. **WORM records:** audit and journal data in Postgres are **write-once, read-many**, so they're tamper-evident and tamper-resistant.

Both build on existing modules: M0, M11, M12, M15 for bots; M17, M18 for WORM. The phases are in the [roadmap](roadmap/README.md).

---

## 1. Trading bots

### 1.1 What a bot is

A **bot** is one deployment of one **strategy version** onto a **market scope**, with its own mode, sleeve, venue account and approval policy. Several bots can run the same strategy on different markets in different modes, e.g. "Trend v3 on BTC/ETH: autonomous" and "Trend v3 on gold: HITL".

| Field | Meaning |
|---|---|
| `strategy_version` | Pinned version of an M0 strategy (it must have passed the gates required for the bot's mode) |
| **Market scope** | One of these: a **single instrument**; an **explicit list**; or a **dynamic selection** (a universe rule such as "top-20 liquid USDT perps on allowed venues", "FX majors", "US sector ETFs"), with a max number of concurrent instruments |
| Venue / account | The venue and sub-account it trades through (checked against the venue registry, [12 §2](12-policy-and-compliance.md#2-venue-access-registry)) |
| Sleeve | Capital bucket and limits ([14 §5](14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11)) |
| Timeframes & schedule | Data subscriptions, trading hours/sessions, blackout rules |
| Parameter overrides | Within the strategy's parameter schema |
| Risk overrides | **Only tighter** than the policy; never looser |
| **Mode** | `paper` · `hitl` · `autonomous` |
| Approval policy | For HITL bots (and escalations from autonomous bots), see §1.3 |
| Status | `draft` · `running` · `paused` · `stopped` · `halted` (by risk) |

### 1.2 Modes

| Mode | Behaviour | Changing to it |
|---|---|---|
| `paper` | Simulated fills through the real risk and execution path | Any time (C1) |
| `hitl` | Every **new entry** (and, if configured, every size increase or modification) is sent to you as an **approval card** on Telegram (and the web). Nothing executes without your tap. | From paper: C2. From autonomous: C1 (tightening, immediate) |
| `autonomous` | Orders go straight to the risk manager and the venue | **C3** (Telegram approve + TOTP + cool-down), and only while the strategy version passes all gates |

**Rules that apply in every mode:**
- Every order passes the risk manager (M11). The mode decides *who approves*, never *whether risk checks run*.
- **Protective exits never wait for approval:** stop-losses, take-profits set at entry, kill-switch flattening and risk-forced reductions run automatically even for HITL bots.
- **Never act late:** an approval that arrives after the TTL is rejected, and the bot logs "expired" (14 §5 decision deadline).

**Automatic downgrade:** an autonomous bot drops to `hitl` (or `paused`, configurable) on any of these:
- decay alert;
- fallback-ladder rung ≥ 3;
- DQ degraded on its instruments;
- N consecutive losses;
- model service down;
- a venue registry status change.

Upgrading back is C3 again.

**Escalation rules** (optional, per autonomous bot): orders above a notional, outside set hours or on newly added instruments are escalated to an HITL approval card instead of executing.

### 1.3 HITL approval via Telegram

**Approval card:**
- **Order:** bot, instrument, side, size, order type/price, stop and target.
- **Risk preview:** risk in R and % of sleeve, exposure after the fill, blackout or DQ warnings.
- **Why:** the signal reasons (top features / tier-B flags / agent summary).
- **Links:** a chart deep link and the TTL countdown.

**Buttons:** **Approve** · **Approve ½ size** · **Reject** · **Pause bot**.

| Setting | Default |
|---|---|
| TTL | Per bot; 60 s for intraday/scalping, 15 min for swing, 4 h for position |
| On expiry | Reject (never execute late) |
| Large orders | Above a per-bot notional, approval also needs **hold-to-confirm** (web) or a **TOTP** reply (Telegram) |
| Quiet hours | HITL bots don't open new entries during your quiet hours unless you set "wake me" |
| Batching | Several signals from one dynamic-selection bot can be grouped into one card with per-line toggles |

Approvals are bound to your Telegram user id. Every approval, rejection and expiry is recorded (WORM, §2) with the card content that was shown.

### 1.4 Telegram commands for bots

| Command | Effect | Level |
|---|---|---|
| `/bots` | List bots with mode, scope, status, today's P&L | C0 |
| `/bot <id>` | Status card: positions, open orders, last signals, mode, pending approvals | C0 |
| `/bot <id> pause` · `resume` · `stop` | Lifecycle | C1 |
| `/bot <id> mode paper` · `mode hitl` | Tightening, immediate | C1 |
| `/bot <id> mode auto` | Loosening: Approve → TOTP → cool-down | **C3** |
| `/approvals` | Pending approval cards | C0 |

### 1.5 API, data and UI

- **Commands (`mt_api`):**
  - `bot.create` (C1);
  - `bot.update_scope`, `bot.update_params` (C1; widening the scope of an autonomous bot is C3);
  - `bot.set_mode`: paper/hitl C1, autonomous **C3**;
  - `bot.start`, `bot.pause`, `bot.resume`, `bot.stop` (C1);
  - `bot.approval_policy.set` (tighten C1, loosen C3);
  - `approval.approve`, `approval.approve_partial`, `approval.reject` (C2).
- **Queries:** `/bots`, `/bots/{id}`, `/bots/{id}/approvals`, `/approvals?status=pending`.
- **Tables:** `strategy.bot`, `strategy.bot_version` (every scope/param/mode change is a new row), `risk.approval` (request, card snapshot, decision, latency, outcome).
- **NATS:**
  - `bot.{id}.status`;
  - `risk.approval.request` / `risk.approval.result` (existing), carrying `bot_id`.
- **UI:**
  - **D03 Strategies → Bots tab:** list, plus a create wizard (strategy → scope → venue & sleeve → mode → approval policy → review);
  - **D01 Needs-you:** approval cards;
  - **D05:** a bot column on orders and fills.
- **MCP (Phase 8):** the same commands. Autonomous is still C3.

---

## 2. WORM records (write-once, read-many)

### 2.1 Scope

**WORM tables:**
- all of `audit.*`: orders, fills, decisions, LLM calls, DQ/cost events, commands, approvals;
- `journal.*`;
- `risk.change`;
- `strategy.bot_version`;
- `curation.mandate` and `curation.exec_log`;
- the signer's signature ledger;
- `audit.seal`.

Market data hypertables and caches are **not** WORM, because they can be rebuilt from sources and Parquet.

### 2.2 Layers

| Layer | Mechanism |
|---|---|
| **Privileges** | WORM tables are owned by `worm_owner`, a role whose credentials **aren't present on the running host** (used only for migrations, from an offline secret). App roles get `INSERT` + `SELECT` only. `UPDATE`, `DELETE`, `TRUNCATE` are revoked. No `ON DELETE CASCADE` reaches a WORM table. |
| **Triggers** | `BEFORE UPDATE OR DELETE` and `BEFORE TRUNCATE` triggers **raise an exception** on every WORM table, as a second line if a grant is ever wrong. Partitions are never dropped inside the retention period (≥ 7 years). |
| **Row hash chain** | Each row carries `chain_id`, `seq`, `prev_hash` and `row_hash = sha256(prev_hash ‖ canonical_json(row))`, computed in a `BEFORE INSERT` trigger and serialised per chain (advisory lock). Timestamps come from `clock_timestamp()` with chrony-synced time. |
| **Daily seal** | A Merkle root per table per day goes to `audit.seal` and is **anchored outside the database**: (1) written to **immutable storage** (S3-compatible **Object Lock** in compliance mode, e.g. Backblaze B2; or a restic `rest-server --append-only` on a second box as the free option); (2) optionally an **OpenTimestamps** proof (free); (3) the root is sent to your Telegram as a timestamped witness. |
| **Corrections** | Never edits. A correction is a new row with `supersedes_id`. "Current" views pick the latest row per key. |
| **Backups** | pgBackRest repo + WAL archive on immutable/append-only storage. A **monthly immutable export** of WORM tables (Parquet + manifest with hashes) is kept ≥ 7 years. |
| **Verification** | `audit.verify` runs daily: it recomputes every chain and checks it against the anchored seals. A mismatch is a **critical incident**: alert on all channels, and (configurable, default on) **halt new trading**, because the records can no longer be trusted. |

### 2.3 What this protects against

- **Covered:**
  - application bugs;
  - compromised application credentials;
  - accidental edits;
  - a wrong migration.
- **Not prevented, but detected:** someone with OS root rewriting the database. The external seals make any rewrite **detectable**.
- **Legal fit:** ATO record-keeping (≥ 5 years, 7 kept) and any later need to show an auditor an unbroken trail.

### 2.4 Tests (part of every phase that adds a WORM table)

- An UPDATE, DELETE or TRUNCATE by any app role fails.
- A row edited directly as `worm_owner` is detected by `audit.verify`.
- A seal mismatch triggers the incident path.
- A restore from immutable backup re-verifies cleanly.
- Insert throughput with hashing stays within the SLOs (fills and commands on the order path never wait on seals).
