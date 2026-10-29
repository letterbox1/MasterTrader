# Policy, Compliance & Data-Use Guardrails

_Adopted from the CryptoTrader spec review ([11](11-cryptotrader-crossover-review.md)) and merged with MasterTrader's own research._

**Notes on sources:**
- Australian items reflect research up to 1 Oct 2026.
- Items marked **(U)** were not read first-hand.
- **This is not legal, tax or financial advice.** The items in §6 need a lawyer or tax agent.

**These rules are enforced in code and config** (risk manager, venue registry, provenance filters, signer), not left to judgement at runtime.

## 1. Australian boundary (the load-bearing assumption)

- **Your status:** you trade your own funds as a **retail trader/investor**. No AUSTRAC registration or AFS licence is needed for you. AUSTRAC/ASIC checks in this system are about the **venues** you use.
- **Platform regulation:**
  - The **Digital Assets Framework** (Royal Assent 8 Apr 2026, commencing **9 Apr 2027**) binds platforms, not traders.
  - Onshore venues may change products through 2027, so the venue registry (§2) is re-checked quarterly.
- **Derivatives:**
  - Crypto derivatives are **financial products**.
  - Wash trading, spoofing or layering on perps/CFDs could engage the Corporations Act market-manipulation provisions.
  - Whether these provisions reach **spot tokens** is unresolved, so **the system behaves as if they do** (no self-trading, spoofing, layering or quote stuffing on any venue).
- **Leverage:**
  - ASIC's product intervention order caps **retail crypto CFDs at 2:1**. The order expires 23 May 2027, with a renewal consultation in Q4 2026 (U).
  - MasterTrader caps crypto-derivatives leverage with an **L0 hard ceiling, default 2×**, whatever a venue allows. You edit it in the agent/bot strategy settings (the ceilings section applies to every bot): tightening is immediate, loosening is C3 ([16 §1](16-configuration-and-safety-model.md#1-configuration-layers-tighten-only-inheritance)). Bots start at 1× until you approve more ([16 §2.1](16-configuration-and-safety-model.md#21-risk-sizing-and-drawdown)).
  - Never misstate wholesale status: ASIC fined Binance Australia Derivatives **A$10m** for misclassifying retail clients.
- **Travel Rule:**
  - AUSTRAC's Travel Rule has applied at a **zero threshold since 1 Jul 2026**.
  - Withdrawal addresses must be pre-registered with proof of control on every AU venue.
  - Cross-venue strategies budget for withdrawal holds and keep **inventory pre-funded**.
- **Polymarket:**
  - Blocked for Australians: an ACMA warning (2 Jul 2025) and an ISP block (13 Aug 2025) under the Interactive Gambling Act.
  - **No Polymarket trading.** Read-only probabilities only where lawfully reachable, and **never via VPN or proxy**.
  - Kalshi is read-only too.
- **Hyperliquid:**
  - Australia isn't on its restricted list, but it provides no Australian consumer protections, and masking your location breaches its terms.
  - Use it **only after professional advice**, with a consistent KYC country and location.
- **Moving countries:** if residency changes (UAE/Egypt/Cyprus, see [09](09-journal-and-tax.md)), the boundary flips to that jurisdiction's rules. The venue registry and jurisdiction plugins switch together: a residency change emits `tax.residency.changed`, the venue registry recomputes, and any loosening that results (e.g. removing a block) is C3. **Egypt: crypto activity is hard-blocked.**

## 2. Venue access registry

There's one registry table, `ops.venue_registry`. The risk manager blocks **live** orders to any venue/product that isn't `allowed` for your current residency.

**Paper and testnet orders** are allowed for venues/products marked `allowed` or `read_only`; a `blocked` product takes paper orders only if it's also marked `paper_ok` (e.g. carry research on perps you can't trade live). Testnets are registered as their own rows.

| Field | Purpose |
|---|---|
| venue, entity, ABN/licence ids | Who you contract with |
| AUSTRAC VASP register status + date checked | Re-checked **quarterly** (registrations have been cancelled, e.g. GetCoins, Sep 2026) |
| Products allowed for your status (spot / margin / perps / CFDs) + max leverage | E.g. "OKX AU perps: **unresolved** (retail 2:1 per help page vs wholesale-only AFSL 379035)" |
| Key model (scopes, IP allow-list, withdrawal whitelist) | Prefer venues with whitelist-only withdrawal roles (e.g. Independent Reserve) |
| STP parameter & mode (§3) | Sent on every order. Netting brokers with no STP field are marked `stp: n/a (netting)` |
| Rate limits (from live headers) | Retry storms cause bans (Binance 418 escalates to 3-day bans) |
| Health: withdrawal delays, proof-of-reserve changes, incidents | Feeds M16 venue health. Inputs: our own measured withdrawal/deposit times, venue deposit/withdraw flags, status pages and proof-of-reserve pages via the regulatory & venue watch ([06](06-aggregators-and-market-providers.md#regulatory--venue-watch-m5--m16)). The AUSTRAC check is a quarterly USER task (`VENUE_CHECK`); the register has no API |
| Concentration cap | Default **≤ 25% of total equity per venue** [10–30%], one value everywhere, configurable in the L1 risk policy ([16 §2.1](16-configuration-and-safety-model.md#21-risk-sizing-and-drawdown)); loosening is C3 |
| Status | `allowed` / `read_only` / `blocked` + reason; `paper_ok` flag for paper/testnet use of `blocked` products |

**Starting classification** (from CryptoTrader research, Sep–Oct 2026; verify before funding):

| Venue | Spot | Derivatives (AU retail) | Notes |
|---|---|---|---|
| Independent Reserve | ✅ (AUSTRAC status U) | — | Best AU key model (whitelist-only withdrawal role); ccxt |
| BTC Markets | ✅ (U) | — | `selfTrade: "P"`; 50 calls/10 s; ccxt |
| Kraken AU (Bit Trade) | ✅ (registered) | Wholesale-only → **blocked** | Scoped keys, IP lock |
| Binance AU | ✅ (registered; under an AUSTRAC-ordered audit) | **None for retail** → blocked | Full STP modes |
| OKX AU | ✅ (registered) | **Unresolved** → paper only until reconciled | **Don't attempt the derivatives test until reconciled:** five failed attempts lock derivatives permanently |
| CoinSpot | ✅ (U) | — | Low priority |
| Swyftx, CoinJar | (U) | — | No ccxt; CoinJar standard keys can transfer funds → **avoid for bots** |
| Bybit, Bitget, MEXC, Gate, KuCoin | Read-only market data | **Not licensed for AU derivatives** → blocked | Fine as **data sources** (public WebSockets) |
| Hyperliquid | — | Read-only until professional advice | §1 |
| IBKR, OANDA, IG, Alpaca, FP Markets (MT5/cTrader) | Per their AU entity | CFDs/FX at retail ASIC limits | Check each AU client agreement (algo trading, scalping, hedging clauses (U) for FP Markets) |

## 3. Exchange conduct & self-trade prevention

- **Never:**
  - wash trading, spoofing, layering, quote stuffing;
  - self-matching across sub-accounts;
  - multiple KYC accounts;
  - VPNs/proxies that hide your location. (The fixed-IP exit node in Australia that all exchange traffic leaves through ([16 §3.2](16-configuration-and-safety-model.md#32-network-egress-and-ip-locked-keys)) isn't location masking: it matches your KYC country and residency.)
  - exploiting pricing bugs.
- **Arbitrage scope:** only genuine price differences between independent venues.
- **STP:**
  - **The STP mode is sent explicitly on every order, never left to the default.**
  - STP cancels are recorded as non-fills in reconciliation.
  - Strategies sharing one account use cancel-both; market-making legs use cancel-taker so resting quotes survive.

| Venue | Parameter | Modes | Venue default |
|---|---|---|---|
| OKX | `stpMode` per order, `acctStpMode` per account | cancel_maker / cancel_taker / cancel_both (not with FOK) | cancel_maker; mandatory at master level incl. sub-accounts |
| Binance | `selfTradePreventionMode` | EXPIRE_TAKER / EXPIRE_MAKER / EXPIRE_BOTH / NONE / DECREMENT / TRANSFER (per symbol) | EXPIRE_MAKER (read per symbol from exchangeInfo) |
| Kraken spot | `stptype` (REST) / `stp_type` (WS) / FIX 7928 | cancel-newest / cancel-oldest / cancel-both | cancel-newest (the arriving order is the one killed) |
| BTC Markets | `selfTrade` | `P` = prevent | — |
| OANDA, IG, Alpaca, IBKR (netting brokers) | None | `stp: n/a (netting)`: positions net per account, so there's no STP field. Where netting would merge two bots' positions, each strategy gets its own account/sub-account | — |

## 4. Per-platform data & automation rules

| Platform | Do | Don't |
|---|---|---|
| **Telegram (user client, Telethon)** | Own long-standing account; joined channels only; honour `FLOOD_WAIT`; joins go through a rate-limited queue; cap of 500 channels/supergroups (1,000 with Premium) | Mass-join; scrape member lists; auto-DM/forward; read-receipt tricks; **any Telegram text or Telegram-derived feature in a model input, RAG index or training set** (Telegram API ToS §1.5: no training, fine-tuning or deployment of AI on Telegram data). **Allowed:** regex-extracted contract addresses/tickers and counts → deterministic **postures** (mention velocity, channel count, new-channel share, time since first call) used by code/policy only: table `text.telegram_posture` (`model_input_ok = false`, `train_ok = false`), subject `posture.telegram.*`, consumed only by M4 and M11 rules; never by M6 features, tier A/B models, agents, RAG or MCP. |
| Telegram Bot API | Alerts, approvals, digests; minimal data, encrypted at rest | > 30 msg/s; unsolicited messages |
| Discord | Own bot, added by an admin (your server); followed announcement channels | Self-bots / user tokens |
| X | (Deferred.) If used: official API, narrow filtered stream, hard monthly cap; posting only via **web intent from your account after approval** (M23) | Scraping (twscrape/Nitter/Apify); auto-replies/mentions; duplicate posts; bulk follows; pay-to-post schemes |
| Reddit | (Optional; Data API access requested 2026-10-29, in or out on Reddit's decision) Official OAuth Data API (PRAW script app), **read-only**, from a dedicated account, for the public subreddits named in the request; ~4–6 requests/min with back-off. Store **hourly aggregates only** (per asset: mentions, sentiment, volume); raw text processed transiently and deleted within **24 h**; sentiment scored by a **local** model | Posting, commenting, voting, messaging or any write; storing usernames; keeping raw text > 24 h or in WORM/journal tables; AI training or fine-tuning on Reddit data; sending Reddit text to any third-party AI service or third party; redistribution; Reddit RSS (ends 2026-11-13) |
| Quest platforms (Galxe, Layer3, Zealy, TaskOn…) | Read public task pages; alert you; let platforms verify on-chain actions | Headless browsers, captcha solvers, internal endpoints, auto-follows, re-registering after a ban |
| CoinGecko / GeckoTerminal | One key; **cache ≤ 24 h, encrypted at rest** (pgcrypto with a key from the sops file), **purged on shutdown/exit**; attribution on display; display and cross-check only, never the stored journal/tax value ([16 §4.1](16-configuration-and-safety-model.md#41-valuing-crypto-for-the-journal)) | Long-lived archive (build long price history from exchanges/on-chain instead); persisting to `journal.*`; redistribution |
| DexScreener | Keyless API within limits (60/min profiles/boosts; ~300/min pairs; search ≤ 30 results) | Resale; a competing screener; search-driven discovery (use addresses) |
| DefiLlama | The official free API hosts only: `api.llama.fi` (protocols/TVL) and `yields.llama.fi` (yield pools); cache results | Site scraping, unofficial APIs, republishing (damages clause) |
| Birdeye | — | Any use (bans storage; "not intended for actual trading") |
| Etherscan | Manual lookups | **Decision input** (terms bar use as a basis for financial gain); extra accounts → use **Blockscout** / own RPC |
| GoPlus / RugCheck | One key; cache per token; stay under limits | Proxies to beat limits; bulk data-mining |
| Jupiter | Issued keys only | Deprecated lite-api / V1 endpoints |
| Jito | Tip **inside** the trade transaction; cap tips from tip-floor percentiles | Tip in a separate transaction |
| RPC providers (Helius, Alchemy, Chainstack…) | One account each; spread load across *different* providers | Second accounts, key multiplexing, resale |
| Solana public RPC / PublicNode | Low-volume fallback | Production traffic; IP rotation |
| All exchanges | Trade-only, IP-locked keys; whitelist-only withdrawals; explicit STP; rate-limit from live headers | §3 list |
| Lido CSM / validators | Allow-listed relays; fixed fee recipient; timely exits | Changing the fee recipient; a second instance with the same keys |
| Anthropic / OpenAI | Human approval on trade decisions (usage policy treats financial decisions as high-risk). **MCP-originated orders always need your approval card** (Telegram/web, TTL 5 min, expiry = reject); MCP can never approve ([16 §2.3, §2.12](16-configuration-and-safety-model.md#23-decisions-approvals-and-hitl)) | Deceptive promotion/shilling drafts; any "skip approval" or auto rule for MCP orders |
| Datasets: MemeTrans (CC BY-NC-SA), SolRPDS (CC BY), Pumpfun corpus (CC BY) | Private models; attribution | Shipping MemeTrans-trained models commercially |
| Tailscale Personal | Private use | Staying on the free plan if commercial |

## 5. Data-provenance tagging (one mechanism for all data terms)

- **Every stored row carries seven separate provenance columns** (not a grouped field): `source`, `licence`, and five use columns:
  - `train_ok`: may be used for training;
  - `model_input_ok`: may be fed to a model;
  - `display_ok`: may be shown;
  - `retention_days`: how long it may be kept;
  - `commercial_ok`: allowed in a commercial product.
- **Training pipelines** (M7, M21 distillation, Laya/decision-model fine-tunes, Hindsight retain) **refuse rows** whose `train_ok = false`.
  - Defaults: Telegram, Birdeye and Etherscan rows are false.
  - Models trained on MemeTrans are flagged `commercial_ok = false`.
- **Inference paths** (tier B, agents, RAG retrieval, **MCP responses**) refuse rows with `model_input_ok = false`. This covers Telegram.
  - MCP tool results go into an external model's context, so `mt_api` filters every `source = mcp` response like any model input: no Telegram text (postures only), no `model_input_ok = false` rows, PII (TFN, addresses, statements) redacted, untrusted text wrapped and marked.
- **Retention jobs** enforce `retention_days` (e.g. CoinGecko ≤ 1 day).
- **The licence tag on each source** (06) is the default for its rows. A SaaS pivot becomes a retrain on `commercial_ok` rows, not a redesign.

## 6. Professional advice triggers (tracked as tasks in D13 / D15)

- **Lawyer:**
  - whether market-manipulation law reaches spot tokens;
  - Hyperliquid exposure for an Australian;
  - a written boundary for "private, non-commercial", and what triggers a review.
- **Tax agent:**
  - investor vs trader-in-business, before any live trade (see 09);
  - the 2027 CGT reform status (sources conflict, see 11 §3).
- **Venue checks:**
  - AUSTRAC register entries by ABN for every venue, before funding and quarterly (a `VENUE_CHECK` USER task; until the task queue exists in P5, a Telegram/notification reminder);
  - reconcile OKX AU derivatives (retail vs wholesale);
  - read each AU venue's conduct, STP and rate-limit terms;
  - FP Markets client-agreement clauses on algorithmic trading.
