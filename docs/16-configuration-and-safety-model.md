# Configuration, Defaults & Failure-Safety Model

**Rule: nothing that shapes trading is hard-coded.** Limits, sizing, drawdown triggers, capital steps, wallet caps, gas budgets, validation gates, approval timers and failure behaviour are all **configuration**:
- set by you (UI, Telegram, later MCP) or proposed by a strategy/bot you create;
- versioned and recorded write-once (WORM, [15 §2](15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).

The numbers in this doc are **defaults**: the values a new install, sleeve or bot starts with until you change them. Where docs elsewhere quote a number, this doc is the reference.

This doc also covers the **failure-safety design** (what happens when the engine, host or network dies) and the **live inputs** that replace fixed constants (gas, fees, prices, regulation).

---

## 1. Configuration layers (tighten-only inheritance)

| Layer | Holds | Who edits | Changing it |
|---|---|---|---|
| **L0 Hard ceilings** | Absolute maxima: e.g. crypto-derivatives leverage ≤ 2×, max daily loss, max per-transaction signer value | You, in the agent/bot strategy settings (the ceilings section applies to every bot) | Tighten: immediate. Loosen: C3 (Telegram + TOTP + cool-down) |
| **L1 System policy** | Global limits, system drawdown stages, failure behaviour, WORM response, venue concentration | You (D06, Telegram) | Tighten: immediate. Loosen: C3 |
| **L2 Venue / account** | Per-venue notional, leverage, allowed products (venue registry), rate limits | You (D06 venue registry) | Tighten: immediate. Loosen: C3 |
| **L3 Sleeve** | Capital, risk budget, sleeve drawdown stages, capital-step plan, kill criteria | You (D06) | Tighten: immediate. Loosen: C3 |
| **L4 Bot** (strategy × market scope × mode, [15 §1](15-bots-hitl-and-worm-audit.md#1-trading-bots)) | Strategy parameters, sizing model, per-trade risk, approval policy, failure behaviour, decision deadline | You, or proposed by the strategy manifest when you create the bot | Tighten: C1. Loosen: C3 |

**Rules:**
- **Effective value = the strictest across layers.** A bot can never exceed its sleeve, a sleeve its system policy, or anything L0. The risk manager (M11) evaluates the merged view on every order, and the UI shows which layer set each effective limit.
- **A strategy manifest proposes values; it never imposes them.** When you create a bot, the wizard shows the manifest's proposals next to your sleeve/system limits. You accept or tighten, and anything looser than a parent layer is rejected.
- **Every change** is a typed `mt-api` command, recorded as a new version row (WORM). Rollback re-applies an earlier version as a new row.
- **Validation:** inconsistent settings are rejected at save time, with the reason. For example, a de-risk drawdown must be lower than the halt drawdown, and a per-transaction cap can't exceed the 24 h cap.

---

## 2. Default values (all configurable)

> Each value below is a starting default. Ranges in brackets are what the UI accepts without editing L0. Values marked (U) are unverified and should be reviewed during the relevant phase.

### 2.1 Risk, sizing and drawdown

| Setting | Layer | Default | Notes |
|---|---|---|---|
| Risk per trade | L4 (≤ L3) | 1% of sleeve equity [0.1–2%] | Memecoin sleeve: 0.25–0.5% of total equity |
| Max position | L4/L3 | 10% of sleeve (memecoin 2%) | — |
| Daily loss | L3 | 3% of sleeve | Sleeve halts until next day (Sydney time) |
| **Sleeve drawdown, stage 1: de-risk** | L3 | **10% below sleeve peak → halve new position sizes** | Two-stage trigger ([14 §5](14-strategy-evidence-and-validation.md#5-risk-engine-additions-m11)) |
| **Sleeve drawdown, stage 2: halt** | L3 | **15% below sleeve peak → halt the sleeve**: cancel orders, close per the sleeve's exit rule, alert; restart is C3 | Stage 1 must be below stage 2. Prefer "15% then a further 15%"? Set stage 1 = 15%, stage 2 = 30% |
| **System drawdown, stage 1** | L1 | **10% below portfolio peak → no new entries anywhere**; exits and protective orders continue; restart C3 | — |
| **System drawdown, stage 2** | L1 | **25% below portfolio peak → flatten to stablecoins/AUD + 30-day review lock**. Two such events end the trading programme; capital moves to hold-and-earn | [14 §7](14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7) |
| Open positions | L3 | 10 per sleeve | — |
| Leverage | L2/L4 | 1× until you approve more; crypto derivatives ≤ 2× (L0 ceiling) | [12 §1](12-policy-and-compliance.md#1-australian-boundary-the-load-bearing-assumption) |
| Drawdown basis | L1/L3 | **Trading equity** in AUD, marked to market (realised + unrealised; on-chain valued per §4.1), **excluding the vault and hold-and-earn**, adjusted for your deposits and withdrawals, measured from its running peak. The peak resets only after a review lock ends or by a C3 reset | Sleeve stages use the sleeve's own equity on the same basis |
| Venue concentration | L1 | ≤ 25% of total equity per venue [10–30%] | One value everywhere (replaces "25–30%") |
| Price collar | L2 | 2% from last trade (crypto majors), 0.5% (FX majors), 1% (ETFs) | Orders outside are rejected |
| API/RPC error pause | L2 | 5 errors in 60 s → pause that venue's orders 10 min | — |
| Cost blow-out | L3 | Realised ÷ modelled cost > 1.5× over the last 20 fills → pause the bot, alert | — |
| Kelly | L4 | Quarter-Kelly is a **ceiling**; never `2p − 1`; never stacked on vol targeting | [14 §4](14-strategy-evidence-and-validation.md#4-trading-methods-enforced-in-code-defaults-user-editable-in-d06) |

### 2.2 Data freshness (what "stale" means)

**Data age** = now (host monotonic clock, chrony-synced) − the time *we received* the last update for that instrument stream. It's not measured from the exchange's own timestamp; the gap between the two is tracked separately as clock-skew/latency.

| Setting | Default |
|---|---|
| Starting universe | `config/defaults/universe.yaml`, seeded by P1-T001: ~10 liquid crypto pairs (BTC/ETH/SOL… across the free venues, native L2 on ≤ 3), FX majors and metals (EURUSD, AUDUSD, USDJPY, XAUUSD, XAGUSD), ≤ 30 US ETFs/stocks incl. the benchmark ETFs, daily futures (`GC=F`, `CL=F`) and the core macro series (FRED/ALFRED, US Treasury curve, RBA/BoE/ECB rates, RBA F11, ABS CPI). Edit any time |
| DQ threshold tuning | The agent may tighten any threshold in this table after the soak (P1-T066); loosening is proposed in the go-live pack and needs C3 |
| Stale threshold, fast bots (scalping/intraday) | 2 s |
| Stale threshold, slow bots (swing/position) | 60 s |
| Session awareness | Closed sessions (weekend FX, exchange holidays) are not stale; they're `closed` |
| **Order-time check** | M11 checks data age **inline on every order**. Older than the bot's threshold → rejected, and the ladder holds. No order can act on stale data, whatever the monitor's timing |
| Monitor reaction | The DQ monitor flips `dq.status` to `stale` within **≤ 250 ms (p99)** of the threshold being crossed, which pauses strategies and turns the UI amber |
| Wide spread | Spread > 3× its normal level → pause the affected bots |
| Cross-source divergence | Mid-price difference between two free sources ≥ 25 bps (crypto) / 5 bps (FX majors) → alert |
| Bad tick | Robust z-score (median/MAD) ≥ 8, a price outside the spread band, or a crossed/locked book → flag and drop the tick |

This replaces the earlier "detection → paused < 2 s" SLO.

### 2.3 Decisions, approvals and HITL

| Setting | Default |
|---|---|
| Decision deadline (signal → order must be submitted) | Scalping 1 s · intraday 10 s · swing 5 min · position 1 h; late decisions are dropped |
| HITL approval TTL | 60 s intraday · 15 min swing · 4 h position; expiry = reject |
| Large-order extra confirmation | > 2% of sleeve or > A$5,000 notional → TOTP (Telegram) / hold-to-confirm (web) |
| Mode change paper → HITL | C2 · HITL → autonomous: C3 · autonomous → HITL/paper: C1 (tightening) |
| MCP-originated orders and any other C2 command (e.g. bot `paper` → `hitl`) | **Always create your approval card** (Telegram/web), TTL 5 min. MCP can never approve anything itself (§2.12) |
| C3 cool-down | 15 min between your C3 approval and the change taking effect |
| Confirm-token TTL (C1/C2) | 120 s from the preview call; single use. Expired → preview again |
| C3 approval TTL | 10 min for the approval and its TOTP; expiry = cancelled, nothing applies |
| Strategy mode ceiling | A strategy's mode (`strategy.set_mode`) caps the modes of its bots: the stricter of strategy and bot mode applies |
| Sleeve restart after a halt | `risk.sleeve.restart`, C3 |
| Exchange/broker key rotation | Every 90 days (alert when older), and immediately after any suspected leak ([07 §2](07-security-notes.md#2-secrets)) |

### 2.4 Validation gates (per-strategy gate profile)

| Gate | Default |
|---|---|
| **Deflated Sharpe ratio (DSR)** | **≥ 0.95**. DSR is a *probability* (0–1) that the strategy's true Sharpe is above zero after accounting for every variant tried; 0.95 = 95% confidence. (The old "DSR > 0" was a doc error) |
| Monte Carlo permutation | p < 0.05 |
| Walk-forward | ≥ 60% of folds positive **and** worst fold ≥ −(sleeve halt drawdown) |
| Cost stress | Still profitable at **2×** measured costs; 3× reported |
| Per-year / per-regime | Positive in each year and each regime (bull/bear/chop, §2.4.1), or labelled single-regime and only run in that regime |
| Benchmark | Beats the asset-class passive benchmark after costs |
| Leakage review + look-ahead analysers | Clean, or each finding waived by you (C2, audited) |
| Safety drills | Kill switch, dead-man and restart drills passed on the bot's venue |
| **Paper / HITL period before autonomous or a capital step** | ≥ 8 weeks **and** ≥ 50 trades (P1 sleeves: ≥ 8 weeks; memecoin: ≥ 300 trades). Low-frequency bots that can't reach the trade count use a time window (≥ 26 weeks) |
| Post-cutoff embargo (strategies with LLM or tier-B inputs) | Evaluation starts ≥ **30 days** after the latest training cutoff of every model in the chain; unknown cutoff → gate fails |
| Minimum out-of-sample window after the embargo | ≥ **90 days**; shorter → gate fails |

**Loosening any gate is C3.** Tightening is free.

#### 2.4.1 Regime labels (for per-regime results)

Per asset, daily:
- **bull:** price above its 200-day average **and** 90-day return > +10%;
- **bear:** price below its 200-day average **and** 90-day return < −10%;
- **chop:** everything else.

Configurable per asset class.

### 2.5 Capital steps (per sleeve/bot)

| Setting | Default |
|---|---|
| Paper auto-start (`paper.auto_start_on_validation`) | On: a strategy that passes validation starts paper trading without asking; live modes always need your approval | Turn off to start paper by hand (C1) |
| Paper notional capital | A$10,000 in total, split by the 14 §3 capital shares (P2-T049) | Notional only; no money |
| Starting live allocation | Set in each bot's strategy settings when it goes live (default A$2,000; suggested range A$2–5k micro-live) |
| **Clean week** | A calendar week (Mon–Sun, Sydney) with: no kill-criterion breach; no unexplained reconciliation mismatch; no S1/S2 incident on that bot; live implementation shortfall ≤ 1.5× modelled; weekly P&L inside the backtest's 5th–95th percentile band |
| Step up | After **4 consecutive clean weeks**: +25% of the **current** allocation (A → 1.25A), up to the sleeve's target cap. Each step needs your approval (C3) |
| Step down | A kill-criterion warning → back one step. A halt → back to the starting allocation after your review |
| Decay / kill signals | §2.6 |

### 2.6 Decay and kill signals: one meaning each

| Signal | Action |
|---|---|
| Rolling 60-trade Sharpe or hit rate below the backtest's 5th percentile (or a 26-week window for low-frequency bots) | Alert + **downgrade the bot autonomous → HITL** |
| CUSUM break on P&L residuals | Alert + downgrade to HITL |
| 5 consecutive losing trades (per bot) | Alert + downgrade to HITL |
| Daily health check fails (30-day Sharpe < ½ validated, or drawdown > 1.5× backtest max) | **Halt the bot** pending your review |
| Kill criteria ([14 §7](14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7)), e.g. implementation shortfall > 2× modelled, or the **sleeve's** live Sharpe, once it has 60 live trades (low-frequency sleeves: over a 26-week window), below the backtest's 5th percentile | **Halt the sleeve**; capital step-down |
| System drawdown stages | §2.1 |

### 2.7 Wallets, signer and gas ([13](13-wallets-treasury-and-onchain.md))

| Setting | Default | Notes |
|---|---|---|
| Hot (trading) wallet float | ≤ A$500 per chain | Above the float sweeps to the vault address daily |
| Airdrop identity wallet float | ≤ A$300 per chain | — |
| Burner float | ≤ A$50 | Refilled to the float only |
| Signer per-transaction cap | A$250 | — |
| Signer rolling 24 h cap | A$1,000 per wallet | — |
| Daily gas budget | Airdrops A$20/day · DEX trading A$50/day | Alert at 80%; stops at 100% |
| Cost-gate margin | Act only if expected benefit ≥ **2×** all-in cost (gas + fees + impact + MEV/tips) | [13 §7](13-wallets-treasury-and-onchain.md#7-on-chain-cost-gate--dex-execution-extends-m12--m16) |
| Gas window | Wait for base fee < its 7-day 30th percentile unless the deadline is < 48 h | Live gas comes from RPC fee APIs (§5) |
| EV hurdle for airdrops/launches | 5% p.a. on capital locked (AUD cash-rate proxy) | [08](08-airdrops-and-token-launches.md) |
| EV time value (`your_minutes × time_value`) | A$1.00 per minute of your time (A$60/h) | Conservative: it only removes opportunities that need your effort; [08 EV gate](08-airdrops-and-token-launches.md#expected-value-gate-airdrops-icosidos-points-programmes) |
| EV default haircut | 50% of the expected value at unlock, when the scorer has no better estimate | Covers vesting, sell pressure and delisting risk; per-opportunity estimates replace it |
| Stablecoin depeg | > 50 bps → reduce exposure; until the P6 treasury exists, alert + task | — |
| HLP (if Hyperliquid is approved) | ≤ 10% of stablecoins **and** ≤ 5% of total portfolio, whichever is smaller | — |
| Per-protocol cap (yield) | ≤ 20% of treasury | — |
| Treasury rebalance hurdle | Move yield only if the net improvement is ≥ 1.0% APY **and** the cost gate passes | P6 yield allocator |
| Stablecoin-issuer cap | ≤ 50% of stablecoins with any one issuer | Breach → rebalance proposal + alert (P6) |

**Mainnet signing stays disabled until you confirm these numbers (C3, P5-T004).** The agent seeds them as defaults (P5-T065); testnet and the Anvil fork sign inside the seeded caps so the build and its tests never wait on you.

### 2.8 Calendar blackouts

High-importance events (central-bank decisions, CPI, NFP, …):
- **15 min before to 15 min after**, block new entries for bots marked `event_sensitive` (scalping/intraday templates by default);
- exits and protective orders continue.

Configurable per bot and per event type.

### 2.9 Reconciliation

| Setting | Default |
|---|---|
| Positions and open orders | Every 60 s |
| Balances | Every 5 min |
| Full reconciliation | End of day (Sydney) |
| Tolerance | Position quantities must match exactly; balances within 0.01% or dust |
| Mismatch warning | A mismatch still unexplained after 12 h → warning alert |
| "Explained" mismatch | Matched to a known journal event within 24 h; otherwise it's unexplained, which halts everything (kill criterion) |

### 2.10 Models (tier B) and LLM budgets

| Setting | Default |
|---|---|
| Auto-decide coverage | At ≥ 0.75 precision |
| Direct veto | Only at ≥ 0.90 precision |
| Calibration | ECE ≤ 0.05 |
| Determinism | Flip rate ≤ 0.1% |
| Shadow period before promotion | ≥ 14 days in shadow (scored, never acting) and meeting the thresholds above |
| LLM spend | Monthly cap US$40. Daily per-role budgets: debate $1.00, strategy-gen $0.50, explain $0.30, memory $0.30, chat $0.40, shadow $0.30. Over budget → local model fallback |

### 2.11 WORM integrity

| Setting | Default |
|---|---|
| Chain check | Hourly incremental, plus the daily full verify against the external seal |
| On a verify mismatch | **`block_new_entries`**: critical alert on every channel; no new entries; exits and protective orders continue; no risk loosening until you acknowledge (C3) after investigating. Options: `alert_only` · `block_new_entries` · `halt_all` |

### 2.12 MCP (Phase 8)

| Setting | Default |
|---|---|
| Defaults for a new token | Scopes `read` + `analyse`; expiry 30 days; the write tool groups (`trade`, `strategy`, `risk_tighten`) off until you enable them (C3) |
| Token expiry | You choose per token: **1 day · 7 days · 30 days · 1 year · custom · indefinite**. Indefinite shows a red exposure/security warning, needs C3, and reminds you monthly |
| Scopes | `read`, `analyse`, `trade` (creates approval cards only), `strategy`, `risk_tighten`, `curation`. Loosening risk is never a scope; it's C3 |
| Never exposed | Withdrawals, `wallet.sweep`, `treasury.*` moves, `airdrop.claim.execute`, mandates, key/token management, `approval.*`, `mcp.*`, restore/delete, audit writes |
| Token creation | C1 for `read`, `analyse` and `curation` scopes; **C3** for `trade`, `strategy` and `risk_tighten` scopes and for any indefinite expiry |
| Rate limits | 60 reads/min, 10 writes/min per token |
| Response cap | 256 KB per tool result |

### 2.13 Curation

| Setting | Default |
|---|---|
| Discord delivery check | Re-prompt if a followed channel delivers nothing in 7 days |
| New servers suggested | ≤ 3 per week |

### 2.14 Platform & operations

| Setting | Default | Notes |
|---|---|---|
| Login lockout | 5 failed logins in 15 min → locked 15 min, doubling on each repeat up to 24 h | Sign-in is Supabase Auth ([18 §4.6](18-platform-and-deployment.md#46-auth)), on top of its own rate limits. `mt-api` keeps the per-IP and global counters (from the Supabase Auth audit log (U) or its own login route) and refuses every token while locked; alert on lockout |
| Session lifetime | Idle 12 h ([ui §3.6](ui/README.md#36-permissions--sessions)); absolute 7 d | Supabase Auth session settings where available (cloud may need a paid plan for them (U)); `mt-api` enforces both limits itself from the session's times either way. Re-login needs TOTP: commands need a JWT at MFA level `aal2` |
| Service heartbeat | Every service publishes `sys.heartbeat.{service}` every 1 s | The cadence the dead-man watches (§3.1) |
| Log retention (Loki) | 30 d [30–90 d] | — |
| WORM seal grace | The seal for day D runs after D closes (UTC) plus 10 min for late inserts | Rows arriving later count into D+1 and are flagged |
| Seal anchor retry | Hourly for 24 h after a failed anchor | Seal row marked `partial`; critical alert |
| Backups | Per mode ([18 §4.7](18-platform-and-deployment.md#47-backups)). **Workstation:** pgBackRest on the Supabase Postgres container: continuous WAL archive; nightly incremental 02:00 and weekly full Sun 02:00 (Australia/Sydney); keeps 4 full backups; restic off-site. **Supabase cloud:** Supabase's managed daily backups (point-in-time recovery is a paid add-on, your call) plus our own nightly logical dump at 02:00 to restic | Every mode: monthly restore test and WORM export ([17 §B](17-decisions-register.md#b-cross-doc-conflicts-one-canonical-answer) P0-B011) |
| Service-restart allow-list (`docker-proxy`) | `caddy`, `prefect-worker`, `mlflow`, `litellm`, `tei-embed`, `tei-rerank`, `llm-local`, `grafana`, `loki`, `prometheus`, `vector`, `alertmanager` | The Supabase services (`supabase-db`, `supabase-auth`, `supabase-storage`, `supabase-kong` and the rest of the stack), `nats`, `mt-api` and `docker-proxy` are never on it by default. Adding a container is C3; removing one is C1 |
| Intel pipeline | Poll intervals, per-source caps, Telegram join pacing and posture windows live in `config/intel/*.yaml`. Defaults: RSS poll 5 min (min 2 min, [P4-T011](../tracking/phase-4/tasks/P4-T011-rss-trafilatura-crawl4ai.md)); 200 docs/hour per source ([P4-T030](../tracking/phase-4/tasks/P4-T030-nlp-relevance-gate.md)); Telegram ≤ 500 channels ([P4-T001](../tracking/phase-4/tasks/P4-T001-telegram-channel-list.md)), ≤ 1 join per 10–20 min and ≤ 20 per day ([P4-T018](../tracking/phase-4/tasks/P4-T018-telethon-join-queue.md)); posture windows 15 min / 1 h / 24 h ([P4-T019](../tracking/phase-4/tasks/P4-T019-telegram-postures.md)) | Tightening is free; the Telegram caps never exceed the platform rules ([12 §4](12-policy-and-compliance.md#4-per-platform-data--automation-rules)) |

### 2.14a Optional modules

| Setting | Default | Notes |
|---|---|---|
| `modules.hummingbot.enabled` | off | Market-making sidecar (M13), behind M11 |
| `modules.social_drafts.enabled` | off | M23 drafts → your approval → web intent |
| `modules.credibility.enabled` | off | Account credibility scoring and shill-burst posture |
| `modules.crowdsim.enabled` | off | M14 research only |
| `modules.lightrag.enabled` | off | Offline graph over filings (research path) |
| `modules.persona_lenses.enabled` | off | Enabled only if they improve shadow results (17 §F) |

Enabling a module is C1 and changes nothing about risk; each still runs behind M11 and the data rules.

### 2.15 Platform, deployment and regions

See [18](18-platform-and-deployment.md). Changing the mode is an OPS task; loosening exposure or adding a region is C3.

| Setting | Default | Notes |
|---|---|---|
| `deploy.mode` | `workstation` | `workstation` \| `hybrid` \| `regional` ([18 §5](18-platform-and-deployment.md#5-deployment-modes)) |
| `db.target` | `local` (self-hosted Supabase on the workstation; Supabase CLI for tests) | `local` \| `supabase_cloud` |
| `db.region` | `ap-southeast-2` (Sydney) | Must match the primary engine region |
| `db.read_replica_regions` | `[]` | Cloud only; dashboards and reports, never the order path |
| `db.bars_hot_months` | Workstation: unlimited; cloud: 24 (1m bars) | Older bars move to Parquet; `pit` reads both |
| `db.bars_1s_hot_days` | 90 | 1s bars older than this live only in the Parquet catalog (same as the hot NVMe window) |
| `supabase.data_api` / `supabase.realtime` | `off` / `off` | The browser reads only through `mt-api` |
| `web.host` | `local` | `local` (Caddy) \| `vercel` |
| `api.exposure` | `tailnet` | `tailnet` \| `public` (Supabase Auth + TOTP, CORS allow-list, rate limits); changing to `public` is C3 |
| `deploy.engine_regions` | `[syd]` | Adding a region needs all four conditions in [18 §7](18-platform-and-deployment.md#7-latency-and-regions) |
| `deploy.region_min_benefit_bps` | 2 bps of latency-attributable slippage per trade | Measured by M16 TCA |
| `deploy.region_eval_trades` | 200 | Minimum sample before a region is considered |
| `risk.region_sync_s` | 1 s | Primary reconciles regional risk slices |
| `models.gpu_profile` | `auto` (GPU if detected, else CPU) | TEI, `llm-local`, decision-svc |
| `secrets.age_identity_store` | `keychain` until P7, then `yubikey` | `keychain` \| `file` \| `yubikey` ([18 §8](18-platform-and-deployment.md#8-tailscale-and-the-hardware-key-per-mode)) |

---

## 3. Failure safety

### 3.1 Three-layer dead-man's switch

| Layer | Watches | Runs where | Default action |
|---|---|---|---|
| **1. In-engine watchdog** | Feeds, risk service, DB, NATS heartbeats (1 s) | Inside the engine | Component missing **5 s** → cancel open orders for affected bots. Missing **10 s** → apply each bot's `on_system_failure` |
| **2. External watchdog** (`deadman` sidecar) | The **engine's** own heartbeat | A separate small process/container with its own trade-only keys and its own venue connections | Engine missing **5 s** → cancel all open orders. Missing **10 s** → flatten per `on_system_failure` |
| **3. Venue-side** | Our connection itself | At the exchange | **Cancel-on-disconnect / countdown timers** where the venue supports them (e.g. Kraken `CancelAllOrdersAfter`, OKX cancel-all-after, Binance USDⓈ-M `countdownCancelAll`; others (U)), refreshed every 15 s with a 60 s timeout, plus **resting stop-loss orders held at the venue**, placed at entry for every position |

`on_system_failure` is set per bot. The default is **`flatten`**: close the position at market, so a down system holds no live exposure. The alternatives are `cancel_orders_only` (keep the position under its resting venue stop; useful for long-horizon holds) and `hold`. Hold-and-earn positions are exempt.

**Important limit:** if the whole runtime host ([18 §5](18-platform-and-deployment.md#5-deployment-modes)) or its internet is down, nothing on our side can send orders. Then only layer 3 protects you: open orders get cancelled by the venue timer, and positions are protected by the **resting venue stop**. That's why every live position carries a venue-side stop from entry.

**Clean restart after an unplanned stop:**
1. The engine starts with every bot **paused**.
2. It reconciles each venue.
3. Any residual position or order is flattened or cancelled per policy, so trading resumes from **flat**.
4. Bots stay paused until you resume them: one tap (C1) on Telegram/web, or set `auto_resume_after_crash: true` per bot.

### 3.2 Network, egress and IP-locked keys

**What's at stake:**
- Exchange API keys are **IP-allow-listed**: a key only works from the public IP you registered.
- The plan adds a **4G backup link** for when the home broadband fails.
- On 4G the public IP is the mobile carrier's, shared and changing (CGNAT), so the exchanges would reject every API call, including closes, exactly when you need them.

**Design: route all exchange traffic through one fixed egress IP in Australia.**
- A small **WireGuard/Tailscale exit node** on a cloud VM in Sydney with a **static IP**. It can be a free-tier VM where available (e.g. an always-free instance in a Sydney region (U), otherwise a few dollars a month).
- **Only that IP** is allow-listed on every key.
- Broadband and 4G both reach the exit node over the tunnel, so failover doesn't change the IP the exchanges see.
- **When it's needed:** from go-live (Phase 7). Paper and testnet on the workstation use your broadband IP ([18 §5](18-platform-and-deployment.md#5-deployment-modes)).
- **If the runtime host is itself a Sydney cloud VM with a static IP** ([18 §8](18-platform-and-deployment.md#8-tailscale-and-the-hardware-key-per-mode)), that IP is the egress IP and no separate exit node is needed. The same rules apply: only that IP is allow-listed, and the egress check below runs.
- **Regional engines** (later, optional, [18 §7](18-platform-and-deployment.md#7-latency-and-regions)): each region has its own static egress IP, added to that venue's key allow-list, and its own `deadman` and venue timers. The region must be one where the venue serves an Australian-resident account.

**Compliance:**
- The exit node (or static-IP runtime host) is in Australia, matching your KYC country and residency.
- It isn't location masking, so it doesn't conflict with the "no VPN/proxy" rule ([12 §3](12-policy-and-compliance.md#3-exchange-conduct--self-trade-prevention)), which is about hiding location.

**If the tunnel itself is down:** fail-flat via layer 3 (venue timers + resting stops), alert on every channel.

**Egress check:**
- The monitor checks every minute that our exchange traffic leaves via the allow-listed IP, and that the IP's country matches your configured residency (free GeoIP database, e.g. DB-IP Lite (CC BY)). A regional engine is checked against its own IP and the allowed regions in the venue registry.
- A mismatch blocks new orders and alerts. This is a **safety check, not a tax input**: tax residency is your legal status (D15 residency timeline), never inferred from IP.

### 3.3 Records: the write path vs the integrity check

**At trade time (write path):**
- Every order, fill and command is written to the WORM tables **as it happens**.
- If the database (Supabase Postgres, local or cloud, [18 §4](18-platform-and-deployment.md#4-database-supabase-postgres)) is unreachable, writes buffer in NATS JetStream: bounded at 1 GB or 24 h. NATS runs on the runtime host next to the engine, so the buffer works the same in every mode.
- The writer is the Rust `mt-obs` crate ([18 §2.1](18-platform-and-deployment.md#21-rust-cargo-workspace-crates)).
- The engine doesn't keep opening positions meanwhile: the DB heartbeat is one of the components the dead-man watches (§3.1), so the buffer mainly carries exits and records already in flight ([02 §9.3](02-v1-architecture.md#93-degraded-modes)).
- Above 80% of the buffer, new entries stop; exits continue.
- The buffer is the JetStream subject `worm.buffer.>`. Its fill level is in NATS KV `worm_buffer`, which M11 reads pre-trade (80% → new entries stop).
- Nothing is ever executed without a record.

**Afterwards (integrity check):**
- `audit.verify` recomputes the hash chains and compares them with the externally anchored seals.
- The result is the integrity status `audit.integrity`, which M11 reads pre-trade. NATS KV bucket names can't contain dots, so it's stored as KV bucket `audit`, key `integrity`.
- A mismatch means stored history changed after it was written: disk or DB corruption, a bad restore, or tampering.
- Trades themselves don't "fail" verification. The reason to block new entries (§2.11) is that positions, P&L, journal and tax records can no longer be trusted until you've checked.
- You can set it to `alert_only` if you prefer.

---

## 4. Snapshot, valuation and tax pricing rules

### 4.1 Valuing crypto for the journal

Applied in order:
1. **Trades:** the actual fill price and fees. This is the transaction value.
2. **Non-trade events** (airdrops, staking rewards, income, transfers needing a value): VWAP of **our own recorded trades** on the primary AUD venue for the event minute. Otherwise the USD venue VWAP × the RBA AUD/USD rate.
3. **Long-tail tokens** with no recorded venue: the on-chain DEX pool price at the event block, read via our RPC.
4. **CoinGecko and other aggregators** are a cross-check only. The stored value is always our computed number, with its method and source references. This keeps 7-year retention free of third-party data terms.

### 4.2 Market-value snapshot (30 June 2027, and any residency change)

Defaults, configurable per asset class; your tax agent to confirm:

| Asset class | Snapshot price |
|---|---|
| Crypto | VWAP of recorded trades 23:55:00–23:59:59 AEST on the primary venue |
| ASX | Official close on the day |
| US/EU listed | Last trade at or before 23:59:59 AEST from recorded data (the US session is open then); if none, the previous official close |
| FX | RBA rate for the day (last business day if none published) |

Each snapshot row records the price source, the method and its timestamps.

### 4.3 Live inputs instead of constants

| Input | Source (free) | Used by |
|---|---|---|
| Gas / priority fees (EVM) | `eth_feeHistory` + base fee from our RPCs | Cost gate, gas windows, gas budgets |
| Solana fees & tips | `getRecentPrioritizationFees`, Helius fee estimate, Jito tip floor | Cost gate |
| Exchange fees & funding | Venue fee-tier / funding APIs (M16) | Backtests, cost gate, TCA |
| FX for tax | RBA F11 (missing days: last business day; currencies not in F11: via USD with RBA AUD/USD × ECB/Frankfurter) | Journal |
| Prices | Our own recorded market data | Snapshots, valuation, risk |
| **Regulatory & jurisdiction watch** | Official pages and feeds (ATO, Treasury, AUSTRAC, ASIC, RBA; plus UAE/Cyprus/Egypt authorities if a move is planned). Fetched on a schedule (RSS where offered, otherwise page fetch / headless browser at low frequency within each site's terms), diffed, and turned into `REG_CHANGE` review tasks | You and your tax agent. **Rules are never auto-applied**; a reviewed change becomes a versioned rule update |
| Egress IP / country | Own check + GeoIP DB (§3.2) | Safety gate, venue access |

Web crawling isn't used for prices or gas: direct APIs and our own recorded data are faster, more accurate, auditable and within terms. Headless browsing is reserved for official pages without feeds, such as regulatory updates.

### 4.4 Tax flags

| Setting | Default |
|---|---|
| Wash-sale flag window | Re-acquisition of the same asset within **30 days** either side of a loss disposal is flagged for your tax agent (flag only; nothing is blocked or adjusted automatically) |

### 4.5 Journal and tax defaults

Defaults, all configurable (`config/journal/*.yaml`); tightening is free.

| Setting | Default | Notes |
|---|---|---|
| FX prior-day limit | A missing RBA rate uses the last published business day's rate, flagged prior-day; older than **5 business days** → the event waits as `pending_fx` and an alert fires | §4.3 |
| Internal-transfer match window | Legs within **6 h** (**72 h** for fiat bank rails); amount out − fee = amount in within 0.1% or the venue's fee | Unmatched → review item, never a disposal |
| CARF difference threshold | Flag a difference above **1% or A$100** per venue, year and metric | Only where the venue provides a statement |
| PAYG reminder lead time | **14 days** before each instalment due date | Due dates default 28 Oct, 28 Feb, 28 Apr, 28 Jul (U), confirmed from your notice |
| Thin-market VWAP | A VWAP built from **fewer than 3** recorded trades in its window is flagged `thin_market` | Shown in the journal notes; the value is still ours (§4.1) |
