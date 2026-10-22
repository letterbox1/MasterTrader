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
| **Mode** | `paper` · `hitl` · `autonomous`, set **per bot** ("approve"/"auto" are retired aliases; UI labels Paper · Approve (HITL) · Autonomous) |
| Approval policy | For HITL bots (and escalations from autonomous bots), see §1.3 |
| Failure behaviour | `on_system_failure`: `flatten` (default) · `cancel_orders_only` · `hold` ([16 §3.1](16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch)) |
| Status | `draft` · `running` · `paused` · `stopped` · `halted` (by risk) |

### 1.2 Modes

| Mode | Behaviour | Changing to it |
|---|---|---|
| `paper` | Simulated fills through the real risk and execution path | Any time (C1, tightening) |
| `hitl` | Every **new entry** (and, if configured, every size increase or modification) is sent to you as an **approval card** on Telegram (and the web). Nothing executes without your tap. | From paper: **C2** (it starts real venue orders). From autonomous: C1 (tightening, immediate) |
| `autonomous` | Orders go straight to the risk manager and the venue | **C3** (Telegram approve + TOTP + cool-down), and only while the strategy version passes its gate profile ([16 §2.4](16-configuration-and-safety-model.md#24-validation-gates-per-strategy-gate-profile): DSR ≥ 0.95, paper/HITL ≥ 8 weeks **and** ≥ 50 trades by default) |

**Mode lives on the bot, gates on the strategy.** A strategy version is *promoted* through gates; a *bot* is switched between modes. There is no separate strategy-level mode: a bot can only use the modes its strategy version's gate status allows. Confirmation levels for each change are in [16 §2.3](16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl).

**Rules that apply in every mode:**
- Every order passes the risk manager (M11). The mode decides *who approves*, never *whether risk checks run*.
- **Protective exits never wait for approval:** stop-losses, take-profits set at entry, kill-switch flattening and risk-forced reductions run automatically even for HITL bots.
- **Never act late:** an approval that arrives after the TTL is rejected, and the bot logs "expired". Signals past the bot's decision deadline are dropped (defaults per horizon, [16 §2.3](16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl)).

**Automatic downgrade:** an autonomous bot drops to `hitl` (or `paused`, configurable) on any of these:
- decay alert: rolling 60-trade Sharpe or hit rate below the backtest's 5th percentile, or a CUSUM break ([16 §2.6](16-configuration-and-safety-model.md#26-decay-and-kill-signals-one-meaning-each));
- fallback-ladder rung ≥ 3;
- DQ degraded on its instruments;
- consecutive losses (default 5, configurable; [16 §2.6](16-configuration-and-safety-model.md#26-decay-and-kill-signals-one-meaning-each));
- model service down;
- a venue registry status change.

**Stronger signals halt rather than downgrade** (one meaning each, [16 §2.6](16-configuration-and-safety-model.md#26-decay-and-kill-signals-one-meaning-each)): a failed daily health check **halts the bot** pending your review; a kill criterion ([14 §7](14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7)) **halts the sleeve** and steps capital down.

Upgrading back is C3 again.

**Escalation rules** (optional, per autonomous bot): orders above a notional, outside set hours or on newly added instruments are escalated to an HITL approval card instead of executing.

### 1.3 HITL approval via Telegram

**Approval card:**
- **Order:** bot, instrument, side, size, order type/price, stop and target.
- **Risk preview:** risk in R and % of sleeve, exposure after the fill, blackout or DQ warnings.
- **Why:** the signal reasons (top features / tier-B flags / agent summary).
- **Links:** a chart deep link and the TTL countdown.

**Buttons:** **Approve** · **Approve ½ size** · **Reject** · **Pause bot**.

Defaults below are configurable per bot ([16 §2.3](16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl)).

| Setting | Default |
|---|---|
| TTL | Per bot; 60 s for intraday/scalping, 15 min for swing, 4 h for position |
| On expiry | Reject (never execute late) |
| Large orders | Orders > 2% of sleeve or > A$5,000 notional also need **hold-to-confirm** (web) or a **TOTP** reply (Telegram) |
| Quiet hours | HITL bots don't open new entries during your quiet hours unless you set "wake me" |
| Batching | Several signals from one dynamic-selection bot can be grouped into one card with per-line toggles. This is the **only** form of bulk approval; there is no "approve all" |
| MCP-originated orders | Always raise this approval card (Telegram/web), TTL 5 min, expiry = reject |

Approvals come **only from you, on Telegram or the web**, and are bound to your Telegram user id or web session. MCP can never approve anything (`approval.*` is never exposed, [16 §2.12](16-configuration-and-safety-model.md#212-mcp-phase-8)). Every approval, rejection and expiry is recorded (WORM, §2) with the card content that was shown.

### 1.4 Telegram commands for bots

| Command | Effect | Level |
|---|---|---|
| `/bots` | List bots with mode, scope, status, today's P&L | C0 |
| `/bot <id>` | Status card: positions, open orders, last signals, mode, pending approvals | C0 |
| `/bot <id> pause` · `resume` · `stop` | Lifecycle | C1 |
| `/bot <id> mode paper` | Tightening, immediate | C1 |
| `/bot <id> mode hitl` | From autonomous: tightening, immediate (C1). From paper: starts real venue orders (**C2**) | C1 / C2 |
| `/bot <id> mode autonomous` | Loosening: Approve → TOTP → cool-down | **C3** |
| `/approvals` | Pending approval cards | C0 |

### 1.5 API, data and UI

- **Commands (`mt_api`):**
  - `bot.create` (C1);
  - `bot.update_scope`, `bot.update_params` (C1; widening the scope of an autonomous bot is C3);
  - `bot.set_mode`: → paper C1; autonomous → hitl C1; paper → hitl **C2**; → autonomous **C3**;
  - `bot.start`, `bot.pause`, `bot.resume`, `bot.stop` (C1);
  - `bot.approval_policy.set` (tighten C1, loosen C3);
  - `approval.approve`, `approval.approve_partial` (C2); `approval.reject` (C1, it only tightens). Accepted from `web` and `telegram` sources only.
- **Queries:** `/bots`, `/bots/{id}`, `/bots/{id}/approvals`, `/approvals?status=pending`.
- **Tables:** `strategy.bot`, `strategy.bot_version` (every scope/param/mode change is a new row), `risk.approval` (request, card snapshot, decision, latency, outcome; the request and the decision are separate rows, never an update).
- **NATS:**
  - `bot.{id}.status`;
  - `risk.approval.request` / `risk.approval.result` (existing), carrying `bot_id`.
- **UI:**
  - **D03 Strategies → Bots tab:** list, plus a create wizard (strategy → scope → venue & sleeve → mode → approval policy → review);
  - **D01 Needs-you:** approval cards;
  - **D05:** a bot column on orders and fills.
- **MCP (Phase 8):** bot commands within each token's scopes ([16 §2.12](16-configuration-and-safety-model.md#212-mcp-phase-8)). MCP can never approve (`approval.*` is never exposed); MCP orders always raise your approval card; switching to autonomous and any other loosening stays C3 on Telegram + TOTP.

---

## 2. WORM records (write-once, read-many)

### 2.1 Scope

**WORM tables:**
- all of `audit.*`, with the canonical (singular) names from [17 §B](17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer): `audit.order`, `audit.fill`, `audit.command` (source `web` / `telegram` / `mcp` / `system`), `audit.llm_call` (from P0, via the LiteLLM callback), `audit.dq_event`, `audit.dq_ack`, `audit.cost_event`, `audit.recon`, `audit.decision_run`, `audit.seal`, `audit.integrity_incident`, `audit.mcp_call` (every MCP call, reads included; commands also land in `audit.command`);
- `risk.approval` (requests, decisions, expiries);
- `journal.*`;
- `risk.change` (every configuration version, [16 §1](16-configuration-and-safety-model.md#1-configuration-layers-tighten-only-inheritance));
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
| **Corrections** | Never edits. A correction is a new row with `supersedes_id`. "Current" views pick the latest row per key. **Acknowledgements are new rows too:** a DQ incident ack is an `audit.dq_ack` row referencing the incident, and an integrity ack is an `audit.integrity_incident` row; nothing is ever marked "acked" in place. |
| **Write path** | Rows are written as events happen; inserts stay fast (p99 < 5 ms) and the order path **never waits on seals**. If Postgres is unreachable, writes buffer in NATS JetStream (default bound 1 GB or 24 h; above 80% new entries stop, exits continue). Nothing executes without a record ([16 §3.3](16-configuration-and-safety-model.md#33-records-the-write-path-vs-the-integrity-check)). |
| **Encryption** | Sensitive columns use envelope encryption: yearly data keys wrapped by a master key. Key rotation **re-wraps the keys** in a non-WORM key table; rows are never re-encrypted (that would be an UPDATE). |
| **Backups** | pgBackRest: continuous WAL archive, nightly incremental, weekly full, on immutable/append-only storage; a **monthly restore test**. A **monthly immutable export** of WORM tables (Parquet + manifest with hashes) is kept ≥ 7 years. |
| **Verification** | `audit.verify` runs an **hourly incremental** check plus a **daily full verify**: it recomputes every chain and checks it against the anchored seals. A mismatch is a **critical incident** (see the integrity response below). |

**Integrity response** (defaults, configurable, [16 §2.11](16-configuration-and-safety-model.md#211-worm-integrity)):
- A mismatch writes an `audit.integrity_incident` row and sets the `audit.integrity` status in NATS KV, which M11 reads **before every trade**.
- **Default action `block_new_entries`:** critical alert on every channel; no new entries; exits and protective orders continue; no risk loosening. Options: `alert_only` · `block_new_entries` · `halt_all`.
- This is separate from the kill switch: it doesn't cancel or flatten anything by itself.
- It clears only when you acknowledge with `audit.integrity.ack` (**C3**) after investigating. The ack is a new `audit.integrity_incident` row.
- Why block: trades themselves don't "fail" verification, but positions, P&L, journal and tax records can no longer be trusted until you've checked.

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
- A seal mismatch triggers the incident path: an `audit.integrity_incident` row, `audit.integrity` set, and M11 rejecting new entries while exits still go through. Only a C3 `audit.integrity.ack` clears it, as a new row.
- An incident ack (DQ or integrity) adds a row and never updates the incident.
- A restore from immutable backup re-verifies cleanly.
- Insert latency with hashing stays within the SLO (p99 < 5 ms; fills and commands on the order path never wait on seals).
