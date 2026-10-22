# MasterTrader — Plan of Action (v2)

Personal-use build, one developer plus AI pair-programming. Time estimates assume evenings and weekends; halve them if full-time.

**Order of work:**
1. Make the **platform workable** first: data, storage, monitoring, strategy framework, risk, journal.
2. Then **strategies get added and experimented with by you**. The plan never assumes a trading style or timeframe.
3. Each phase ends with a **demo you can actually use**.
4. **MCP is last** (Phase 8), and only if you want it.
5. **How work runs** ([17 §E](17-decisions-register.md#e-ratification-2026-10-22)): a task starts as soon as its own dependencies are done, in any phase (Phases 7 and 8 stay hard-gated on their prerequisite phases). Integrations are built and tested against mocks, fixtures, testnets and paper accounts first; live checks that need your keys, accounts or money are final `VERIFY` tasks. Up to 6 agents work in parallel, and every task passes an independent review before it's done.

Every number in this plan (periods, sizes, limits, timers) is a **default you can change in settings** ([16](16-configuration-and-safety-model.md)), not a fixed rule.

Module numbers (M0–M23) refer to [03-build-spec.md](03-build-spec.md).

**Detailed scoping per phase** (requirements with IDs, ToDos split into `USER` / `BUILD` / `OPS` / `VERIFY` / `RUN`, exit criteria, traceability to every doc) lives in the **[roadmap](roadmap/README.md)**, and execution is tracked task-by-task on per-phase kanbans in [`tracking/`](../tracking/README.md) (project board: [`KANBAN.md`](../KANBAN.md) / `kanban.html`). This page is the summary.

## ⚠️ Do this week regardless of phase
- [ ] **Telegram:**
  - register `api_id`/`api_hash` at my.telegram.org with a **dedicated number** (try the landline via voice-call code, otherwise a prepaid SIM);
  - set a 2-step password;
  - create a bot via @BotFather.
- [ ] **Discord:**
  - create a private "MasterTrader Feeds" server with `#mt-inbox` (+ category channels);
  - register a bot app with the Message Content intent;
  - start following the announcement channels you already know about.
- [ ] **Reddit (optional):** apply for free personal API access before 2026-10-31 (see [06 §0](06-aggregators-and-market-providers.md#0-️-time-sensitive-actions)). X stays deferred.
- [ ] **Free demo/practice accounts:**
  - OANDA practice, IG demo, Alpaca paper, IBKR paper;
  - Binance and Bybit testnets.
- [ ] **Free API keys:** FRED, EIA, Myfxbook, CoinGecko Demo, CryptoRank Sandbox, Helius, Alchemy, GoPlus, Finnhub, CryptoPanic, NASA FIRMS, ACLED (research account); OpenSanctions licence (needed by Phase 4). (Blockscout needs no key; Etherscan only for manual lookups; Anvil is local, so no Tenderly.)
- [ ] **LLM keys:** Anthropic API key (with a spend limit) and your custom endpoint URL/key, put into the secrets file (needed by Phase 0).
- [ ] **Venue checks:** look up each AU venue on the AUSTRAC register by ABN; pre-register withdrawal addresses (Travel Rule); seed `ops.venue_registry` ([12 §2](12-policy-and-compliance.md#2-venue-access-registry)).

## Phase 0 — Foundations & security baseline (weeks 1–2)
Full scope: [roadmap phase 0](roadmap/phase-0-foundations.md).
- [ ] **Monorepo and code quality:**
  - `uv` workspace, packages per [build spec §3](03-build-spec.md#3-repository-layout);
  - ruff, mypy, pytest, pre-commit with **gitleaks**;
  - `third_party/LICENSES.md`.
- [ ] **Host:**
  - LUKS full-disk encryption, firewall deny-inbound;
  - Tailscale-only access;
  - chrony for time sync.
- [ ] **`infra/docker-compose.yml`** (images pinned by digest):
  - Postgres 16 + TimescaleDB (TSL image) + pgvector;
  - NATS JetStream;
  - Prefect;
  - Grafana + Loki + Prometheus + Vector;
  - MLflow;
  - Caddy (serves the web app, Tailscale only);
  - a restricted Docker-socket proxy that lets `system.service.restart` restart only allow-listed containers.
- [ ] **Core code:**
  - `mt_core` types;
  - `mt_store` schemas: all 13 canonical schemas (`market`, `text`, `features`, `strategy`, `risk`, `audit`, `journal`, `curation`, `ops`, `rag`, `models`, `treasury`, `hindsight`, [03 §4](03-build-spec.md#4-data-model-overview)) + Alembic migrations;
  - `pit(as_of)` API + CI test.
- [ ] **WORM audit and logging** ([15 §2](15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)):
  - offline `worm_owner`, INSERT/SELECT-only app roles, blocking triggers, per-row hash chain, daily seal anchored outside the DB;
  - `audit.verify` → `audit.integrity` status (default `block_new_entries`; cleared by `audit.integrity.ack`, C3) ([16 §2.11](16-configuration-and-safety-model.md#211-worm-integrity));
  - `audit.llm_call` written from day one via the LiteLLM callback;
  - structured logging (structlog) with `trace_id`.
- [ ] **Secrets and backups:**
  - `sops`/`age` secrets; the encrypted file lives outside the repo (e.g. `~/.config/mastertrader/`);
  - pgBackRest + restic off-site backups: continuous WAL, nightly incremental, weekly full, monthly immutable WORM export;
  - monthly automated restore test.
- [ ] **`mt_api` command layer skeleton:** login + TOTP, C0–C3/Kill enforced server-side, every command written to `audit.command`. The UI and Telegram will call it; MCP will later wrap it. Until Telegram C3 exists (P2), C3 completes via the host-only break-glass CLI (`mtctl approve <id>` + TOTP), audited.
- [ ] **Web shell:** top bar, nav, status bar, kill-switch placeholder and the D16 System dashboard on the DESIGN.md v2 Tailwind preset.
- [ ] **Model gateway:**
  - LiteLLM proxy (≥ 1.83, pinned by digest) with Claude + your custom endpoint + a local model;
  - `llm-local` (llama-server on CPU, or vLLM on GPU) serving the `local-advisor` route;
  - per-role budgets;
  - two **TEI** containers: `tei-embed` (bge-small-en-v1.5) and `tei-rerank` (bge-reranker-v2-m3).

**Demo:** `docker compose up` gives a healthy stack, with Grafana showing DB/NATS/host health and logs in Loki; you log in with TOTP to the responsive web shell.

## Phase 1 — Market data, recording & live monitoring (weeks 3–6)
- [ ] **Crypto real-time** via Nautilus/ccxt WebSockets: trades, L1, L2. Recorded to the **Parquet catalog** (raw L2 diffs only for symbols a bot needs order-book data for, default ≤ 3; 1 s snapshots for the rest), plus a bar builder writing 1s bars to Timescale with continuous aggregates at 1m, 5m, 15m, 1h, 4h, 1D, 1W.
- [ ] **Crypto history:** data.binance.vision backfill (trades/aggTrades/1s klines).
- [ ] **FX & metals:**
  - OANDA practice stream + IG demo stream;
  - Dukascopy tick history;
  - ECB/Frankfurter reference rates;
  - **RBA F11 FX** (for tax).
- [ ] **Stocks/ETFs:** Alpaca IEX + yfinance daily; FinanceDatabase symbol master; `exchange_calendars`.
- [ ] **Macro:**
  - FRED/ALFRED, Treasury, `sdmx1` (ECB/IMF/OECD/BIS/Eurostat), BoE/BoC/RBA/SNB;
  - EIA, USDA, CFTC COT;
  - **ABS CPI** (All groups, weighted average of eight capital cities).
- [ ] **Fundamentals:** EDGAR via edgartools.
- [ ] **Quota tracker** per connector (free-tier throttling).
- [ ] **M16 data-quality monitor:** stale (data age vs per-bot thresholds, [16 §2.2](16-configuration-and-safety-model.md#22-data-freshness-what-stale-means)), gaps, bad ticks, cross-source divergence, clock skew, book integrity → `audit.dq_event`. One alert fan-out: Grafana alerts → webhook → `alert.*` → Telegram / ntfy / email.
- [ ] **M16 cost monitor:**
  - fee tiers, funding, swap/financing, spreads by hour-of-week;
  - venue balance/position reconciliation (defaults in [16 §2.9](16-configuration-and-safety-model.md#29-reconciliation)) → `audit.recon`.
- [ ] Run the open provider checks in [06 §3](06-aggregators-and-market-providers.md#open-checks-do-these-in-phase-1).
- [ ] **Row-level provenance tags** (`source`, `licence`, `train_ok`, `model_input_ok`, `display_ok`, `retention_days`, `commercial_ok`) on every ingested row, plus retention jobs ([12 §5](12-policy-and-compliance.md#5-data-provenance-tagging-one-mechanism-for-all-data-terms)).
- [ ] **ntfy** (self-hosted, Tailscale only) as the second alert channel; email via your own provider's SMTP or off; venue-health monitor (our measured withdrawal times, venue status feeds, quarterly AUSTRAC check as a USER task).

**Demo:** Grafana shows live prices at every timeframe from ticks to 1D across all asset classes, plus live spread/funding/swap panels and data-quality alerts arriving on Telegram.

## Phase 2 — Strategy framework, risk manager & research lab (weeks 7–11)
- [ ] **M0 strategy framework:**
  - templates for scalping, intraday, EMA/MA, mean-reversion, breakout, swing, grid/DCA, pairs, event, ML;
  - manifest schema; registry; multi-timeframe helpers.
- [ ] **M11 risk manager:**
  - policy model at global, venue, strategy, instrument and portfolio levels;
  - sizing models;
  - pre-trade checks (incl. DQ status and event blackout);
  - kill switch (no vault sweep until P5; P2 has a logged no-op hook);
  - **three-layer dead-man's switch**: in-engine watchdog, external `deadman` sidecar, venue-side cancel-after timers + resting stops; per-bot `on_system_failure` (default `flatten`); restart flat with bots paused ([16 §3.1](16-configuration-and-safety-model.md#31-three-layer-dead-mans-switch));
  - change control: tighten instantly, loosen = C3 (Telegram + TOTP + cool-down);
  - L0 hard ceilings in the agent/bot strategy settings (tighten immediate, loosen C3);
  - inline data-age check and `audit.integrity` check on every order;
  - audit;
  - **venue access registry** check on every order, **2× crypto-derivatives leverage cap**, explicit **STP mode** on every order where the venue supports it (netting brokers: `stp: n/a`);
  - **sleeves**, two-stage sleeve/system drawdowns and the **fallback ladder**, all with defaults from [16 §2.1](16-configuration-and-safety-model.md#21-risk-sizing-and-drawdown).
- [ ] **Trading bots** with modes `paper` / `hitl` / `autonomous` ([15 §1](15-bots-hitl-and-worm-audit.md#1-trading-bots)); decay/kill signals for paper ([16 §2.6](16-configuration-and-safety-model.md#26-decay-and-kill-signals-one-meaning-each)).
- [ ] **M12 engine wrapper:** Nautilus sandbox/paper on testnets/practice accounts. Custom **Alpaca, OANDA and IG** adapters.
- [ ] **M7 lab:**
  - fast screener + Nautilus truth backtests using **measured costs from M16**;
  - validation suite (walk-forward, purged CV, MC permutation, bootstrap Sharpe, deflated Sharpe with the default gate DSR ≥ 0.95);
  - **validation extensions:** per-year/per-regime breakdown (`regime_v1`), 2×/3× cost stress, automatic trial counter, worst fold, LLM leakage review, CUSUM decay monitoring ([14 §6](14-strategy-evidence-and-validation.md#6-validation-harness-extends-03-8));
  - vendored freqtrade look-ahead/recursive analysers;
  - Optuna;
  - MLflow tracking.
- [ ] **M6 core features:** TA-Lib, Alpha158, microstructure; IC evaluator.
- [ ] **Sandboxed LLM strategy generator.**
- [ ] **M21 Decision One tier A:**
  - train (forward-return / triple-barrier labels until the P6 teacher exists) → calibrate → compile (ONNX/Treelite) → in-process runtime;
  - latency benchmark (target < 50 µs);
  - MLflow model registry.
- [ ] **Design system:** implement DESIGN.md v2 tokens/breakpoints as a shared Tailwind preset + component library, with a Playwright viewport-matrix CI check (DESIGN.md §6.8).
- [ ] **M15 web UI v1:** strategy builder/registry, backtest viewer, risk-policy editor, positions, manual trade ticket. **Telegram bot v1:** alerts, `/kill`, `/status`, `/pause`, HITL approval cards and the C3 approve + TOTP path (retiring the break-glass CLI as the main path).

**Demo:** you create any strategy type on any timeframe (template, code or "describe it"), backtest it with realistic costs, validate it, and run it on paper behind the risk manager.

## Phase 3 — Journal & tax (weeks 12–15)
- [ ] **M18 journal ingestion:** Nautilus fills, ccxt ledgers (funding, fees, transfers), broker statements (IBKR Flex, OANDA, IG), and on-chain events.
- [ ] **FX and valuation:** RBA F11 for AUD (missing days: last business day; other currencies via USD); crypto valued per the hierarchy in [16 §4.1](16-configuration-and-safety-model.md#41-valuing-crypto-for-the-journal); source and method recorded per event.
- [ ] **Lot engine:** specific-ID → FIFO; FX-cash lots (Div 775); Decimal.
- [ ] **Rules plugins:**
  - **AU_2026** plugin plus golden tests from ATO examples;
  - PAYG-instalment estimator (both ATO methods computed);
  - wash-sale flags (default window 30 days either side of a loss disposal, flag only);
  - myTax worksheet.
- [ ] **AU_2027_REFORM** scaffolding plus the **30 June 2027 snapshot job** (price conventions per asset class, [16 §4.2](16-configuration-and-safety-model.md#42-market-value-snapshot-30-june-2027-and-any-residency-change)); `tax.fy.lock`/`unlock` (C3).
- [ ] **`ops.wallets`** registry and a minimal Accounts page; a minimal `curation.task` table for tax-agent questions (P5 extends both).
- [ ] **Residency timeline**, with AE/EG/CY/GENERIC plugin stubs.
- [ ] **Trading-journal UI:** per trade, with strategy, signal, chart snapshot, notes and tags.
- [ ] **Exports:**
  - Beancount (+ Fava) export;
  - accountant pack;
  - daily reconciliation journal ↔ venues.
- [ ] Log the tax-agent questions as tasks ([09](09-journal-and-tax.md#questions-for-your-tax-agent-tracked-as-tasks)).

**Demo:** every paper trade, fee and funding payment appears automatically in the journal; an FY-to-date AU tax summary and PAYG estimate are generated.

## Phase 4 — News, social, events & calendars (weeks 16–19)
- [ ] **News:** RSS + trafilatura/crawl4ai; **RSS-Bridge** sidecar (whitelist, auth, internal network); GDELT.
- [ ] **Social:**
  - Telegram (Telethon + Bot API + RSS-Bridge fallback) as **postures only** (counts/addresses → `text.telegram_posture` / `posture.telegram.*`, consumed only by M4/M11 rules; no text to models, RAG or training);
  - Farcaster (Hubble), CryptoPanic;
  - Discord bot on followed announcement channels;
  - Bluesky Jetstream; Mastodon;
  - StockTwits conditional; the YouTube check happens in this phase.
- [ ] **Text processing:** tier-B stage-1 relevance gate (SemIf) → entity linking → FinBERT → embeddings (TEI) → `document`. `models.label.add` + a minimal labelling tool.
- [ ] **M9 document RAG** (`rag` schema):
  - hybrid pgvector + tsvector with RRF;
  - rerank;
  - point-in-time filter;
  - filing/news chunking;
  - retrieval benchmarks.
- [ ] **Events:** USGS, GDACS, NOAA/NHC, FIRMS, ReliefWeb, UCDP, OpenSanctions, Kalshi/Polymarket + exposure map.
- [ ] **Calendars:** FRED release dates, ForexFactory weekly JSON, central-bank schedules, earnings/IPOs. Blackout windows feed M11 (default ±15 min around high-importance events for `event_sensitive` bots, [16 §2.8](16-configuration-and-safety-model.md#28-calendar-blackouts)).
- [ ] **Features:** retail positioning (Myfxbook, IG, OANDA books), nowcasts, Fed-path probabilities, VIX regime.

**Demo:** a morning Telegram brief covering news, sentiment movers, global events mapped to assets, today's calendar with risk blackouts, and data/cost health. The canonical brief contents are in [mobile-and-telegram §3](ui/mobile-and-telegram.md#3-telegram-bot).

## Phase 5 — Airdrops, launches & curation queue (weeks 20–23)
- [ ] **Custody tiers + intents-only signer** ([13 §1–2](13-wallets-treasury-and-onchain.md#1-custody-tiers)); the signer accepts intents only from the policy service; durable-nonce hard block; sized approvals; cost gate library `mt_onchain.costgate`. Vault and warm are watch-only.
- [ ] **USER:** confirm wallet floats, signer caps and gas budgets ([16 §2.7](16-configuration-and-safety-model.md#27-wallets-signer-and-gas-13)); signing stays disabled until you do. Prove control of each address by signing a challenge in your own wallet app.
- [ ] **Wallet-indexer + unified wallet view** (D18) extending `ops.wallets`, internal-transfer tagging into the journal, approval/nonce/depeg monitors (depeg: alert + task until the P6 treasury exists). Kill switch sweep of hot trading balances to the vault (default on).
- [ ] **M4 additions:** corroboration score, EV gate, burner-first + one identity wallet per chain, campaign record, project dossier, blacklist, wallet-cluster detection, disposal rule ([08](08-airdrops-and-token-launches.md#additions-from-the-cryptotrader-review-see-11-13)).
- [ ] **M19 task queue:** canonical task types ([03 M19](03-build-spec.md#m19-user-task-queue--community-curation--mt_curation)), extending the P3 `curation.task` table; Telegram Done/Skip/Snooze/Details/Never; daily and weekly digests. Airdrop disposal is a USER task until Phase 7.
- [ ] **M19 community curation:** Discord servers + announcement channels to follow, Telegram channels, Galxe spaces.
- [ ] **M4 discovery:** DefiLlama tokenless protocols, CryptoRank, CoinGecko, DexScreener, Galxe (read-only), Snapshot/forums, Discord inbox.
- [ ] **M4 risk scoring:**
  - GoPlus, RugCheck, Honeypot.is;
  - blocklists;
  - re-implemented solana-rugchecker + CRPWarner heuristics;
  - evaluation on the SoK dataset.
- [ ] **Viability scoring:** includes AU geo/KYC exclusion.
- [ ] **Claim executor** (the chain's **airdrop identity wallet**, never the hot trading wallet):
  - signed mandates;
  - Anvil fork / `simulateTransaction` pre-checks;
  - caps;
  - approval revokes/sweeps.
- [ ] **Airdrop/staking income** goes to the journal with tax classification.

**Demo:** a weekly digest of vetted airdrops/launches with step-by-step tasks; eligible claims executed automatically from the identity wallet with simulation proof; scams rejected with reasons.

## Phase 6 — AI decision layer, memory & anomalies (weeks 24–28)
- [ ] **M8 decision graph:** LangGraph debate graph (TradingAgents-derived) with FinRobot valuation tools and a macro/events analyst; structured `Signal` ([03 M8](03-build-spec.md#m8-ai-decision-layer--mt_agents) fields).
- [ ] **M9 memory:**
  - **Hindsight** self-hosted (slim, our Postgres schema, TEI embeddings/rerank, LLM via gateway);
  - memory banks;
  - decision settlement + reflection;
  - point-in-time recall (derived memories excluded when their latest source time > `as_of`; otherwise memory off in backtests; mandatory PIT test).
- [ ] **M21 tier B decision models:**
  - question registry;
  - SemIf readout in production;
  - train our own Qwen3-0.6B/1.7B + LoRA + classification head (distilled + outcome-corrected, calibrated, abstention);
  - serve via vLLM `/classify` or ONNX;
  - scores to NATS KV as tier-A features;
  - thresholds and latency: [16 §2.10](16-configuration-and-safety-model.md#210-models-tier-b-and-llm-budgets) defaults, p95 < 50 ms on GPU.
- [ ] **Decision-model bake-off:**
  - **Contenders:** own head vs fine-tuned Laya vs Clef-flash vs SemIf vs JSON generation, plus Kev-4B/9B only if a public, licence-compatible release exists (U).
  - **Data:** our data + FinMMEval Buy/Hold/Sell.
  - **Metrics:** Brier/ECE per regime, coverage, latency, flip rate.
  - **Promotion:** only via gates.
- [ ] **M21 distillation loop:** teacher log (M8) + outcomes → tier A retrain / tier B decision-head retrain → calibration → gated promotion; teacher in shadow.
- [ ] **Optional:** LightRAG graph over filings (offline).
- [ ] **M10:** anomaly detectors + explain agent.
- [ ] **LLM-signal strategy template** (M0) consuming M8 signals; LLM-signal paper trading starts in this phase and is checked at Phase 7 entry.
- [ ] **Evaluation and cost:** evaluate on post-training-cutoff data; monthly LLM cap + per-role daily budgets with local fallback ([16 §2.10](16-configuration-and-safety-model.md#210-models-tier-b-and-llm-budgets)) and spend panel; `audit.llm_call` (live since P0) extended with the prompt registry and training cutoff.
- [ ] **Optional:** Hummingbot MM sidecar; MiroFish/OASIS crowd-sim experiment (local memory backend and hardened config only, no Zep Cloud; otherwise skipped).
- [ ] **M22 hold-and-earn + treasury** with the on-chain cost gate ([13 §4–7](13-wallets-treasury-and-onchain.md#4-hold-and-earn-module-m22-mt_treasury)); automated depeg reduction; HLP cap.
- [ ] **Optional M23 social drafts** (approval → web intent; nothing auto-posts).
- [ ] **Decision-model operating rules:** 5% shadow checks, labels endpoint + D10 labelling queue tab, per-question thresholds, monthly fine-tune ([10 §4.3](10-memory-rag-and-models.md#43-design)).

**Demo:** ask for an analysis of any instrument and get a sourced signal; anomalies are explained on Telegram; LLM-signal strategies run on paper.

## Phase 7 — Prove it, then go small-live (months 7–10+)
**Opens after Phase 3** (hard-gated). Items that need Phase 5 or 6 deliverables carry their own task dependencies, so a P1 sleeve can go micro-live without waiting for them. Full scope: [roadmap phase 7](roadmap/phase-7-prove-and-go-live.md).
- [ ] Your bots run in `paper`/`hitl` mode for the gate period (default ≥ 8 weeks and ≥ 50 trades, [16 §2.4](16-configuration-and-safety-model.md#24-validation-gates-per-strategy-gate-profile)).
- [ ] **Weekly review:**
  - paper vs backtest tracking error;
  - realised vs modelled costs;
  - DQ incidents;
  - journal reconciliation;
  - clean-week status per bot ([16 §2.5](16-configuration-and-safety-model.md#25-capital-steps-per-sleevebot)).
- [ ] **Static AU egress:** a WireGuard/Tailscale exit node with a fixed IP; only that IP allow-listed on every key; egress IP/country check ([16 §3.2](16-configuration-and-safety-model.md#32-network-egress-and-ip-locked-keys)).
- [ ] **Safety drills** (kill switch, dead-man, restart) passed on each live venue.
- [ ] Promote strategies that pass the [gates](03-build-spec.md#8-promotion-gates-per-strategy-configurable) to small live allocations (starting allocation set per bot, default A$2,000), using separate live sub-accounts with withdrawals disabled.
- [ ] MT5 bridge (on a hardened, Tailscale-only Windows VPS with a trade-only MT5 login and no other secrets) / cTrader / Saxo adapters if needed; share risk, journal and data libraries with **MasterTradingBot** (FP Markets MT5) rather than duplicating them ([14 §8](14-strategy-evidence-and-validation.md#8-mastertradingbot-integration)).
- [ ] **Capital steps and kill criteria** per [14 §7](14-strategy-evidence-and-validation.md#7-phase-capital-steps--kill-criteria-refines-04-phase-7) and [16 §2.5–2.6](16-configuration-and-safety-model.md#25-capital-steps-per-sleevebot): +25% of the current allocation after 4 consecutive clean weeks, each step C3; step down on warnings and halts; decay/kill signals extended to live.

Phase 7 closes once micro-live is stable. The **12-month keep/kill review** is a recurring calendar review (a scheduled task), not a phase item.

## Phase 8 — MCP control plane (last; only if you want it)
- [ ] **`mt_mcp` adapter over `mt_api`:** read & analyse, talk to agents, trade & adjust positions, strategies, risk, curation. See [build spec M20](03-build-spec.md#m20-mcp-control-plane--mt_mcp-built-last-phase-8-only-if-wanted).
- [ ] **Safeguards** ([16 §2.12](16-configuration-and-safety-model.md#212-mcp-phase-8)):
  - every MCP order creates your approval card (TTL default 5 min); MCP can never approve anything;
  - loosening risk is C3 (Telegram + TOTP), never a token scope;
  - the never-exposed list (withdrawals, sweeps, treasury moves, claims, mandates, keys/tokens, `approval.*`, `mcp.*`, restore/delete, audit writes);
  - responses pass the provenance filter (no Telegram text) with PII redacted;
  - scoped, hashed, revocable tokens with chosen expiry; default rate limits and response cap;
  - every call, reads included, logged to `audit.mcp_call`.

**Demo:** from Claude, "how are my strategies doing, tighten BTC max position to X, and close half my EURUSD", with the order confirmed on Telegram.

## Standing rules
- **Platform first, strategies second.** The system never hard-codes a trading style or timeframe.
- **Paper first, always.** Live keys have no withdrawal rights, are IP-locked to the fixed egress IP, and start with small caps.
- **Settings, not constants:** every limit, threshold and allocation is a default you change in settings ([16](16-configuration-and-safety-model.md)); tightening is immediate, loosening is C3.
- **Tests:** nothing merges without passing them. The point-in-time, risk-manager and tax golden tests are mandatory.
- **Vendored code:** review every third-party bump (diff for telemetry, referral IDs, network calls).
- **Monthly upkeep:**
  - check data-source API/ToS changes;
  - rotate keys every 90 days;
  - run a restore test;
  - export the immutable WORM backup.
- **Recurring reviews** (calendar tasks): quarterly AUSTRAC register check per venue (USER); the 12-month keep/kill review for each live sleeve.
