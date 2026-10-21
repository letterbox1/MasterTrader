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
  - The default MasterTrader leverage cap for crypto derivatives is **2×**, whatever a venue allows.
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
- **Moving countries:** if residency changes (UAE/Egypt/Cyprus, see [09](09-journal-and-tax.md)), the boundary flips to that jurisdiction's rules. The venue registry and jurisdiction plugins switch together. **Egypt: crypto activity is hard-blocked.**

## 2. Venue access registry

There's one registry table, `ops.venue_registry`. The risk manager blocks orders to any venue/product that isn't `allowed` for your current residency.

| Field | Purpose |
|---|---|
| venue, entity, ABN/licence ids | Who you contract with |
| AUSTRAC VASP register status + date checked | Re-checked **quarterly** (registrations have been cancelled, e.g. GetCoins, Sep 2026) |
| Products allowed for your status (spot / margin / perps / CFDs) + max leverage | E.g. "OKX AU perps: **unresolved** (retail 2:1 per help page vs wholesale-only AFSL 379035)" |
| Key model (scopes, IP allow-list, withdrawal whitelist) | Prefer venues with whitelist-only withdrawal roles (e.g. Independent Reserve) |
| STP parameter & mode (§3) | Sent on every order |
| Rate limits (from live headers) | Retry storms cause bans (Binance 418 escalates to 3-day bans) |
| Health: withdrawal delays, proof-of-reserve changes, incidents | Feeds M16 venue health |
| Concentration cap | Default ≤ 25–30% of equity per venue |
| Status | `allowed` / `read_only` / `blocked` + reason |

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
  - VPNs/proxies;
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

## 4. Per-platform data & automation rules

| Platform | Do | Don't |
|---|---|---|
| **Telegram (user client, Telethon)** | Own long-standing account; joined channels only; honour `FLOOD_WAIT`; joins go through a rate-limited queue; cap of 500 channels/supergroups (1,000 with Premium) | Mass-join; scrape member lists; auto-DM/forward; read-receipt tricks; **any Telegram text or Telegram-derived feature in a model input, RAG index or training set** (Telegram API ToS §1.5: no training, fine-tuning or deployment of AI on Telegram data). **Allowed:** regex-extracted contract addresses/tickers and counts → deterministic **postures** (mention velocity, channel count, new-channel share, time since first call) used by code/policy only. |
| Telegram Bot API | Alerts, approvals, digests; minimal data, encrypted at rest | > 30 msg/s; unsolicited messages |
| Discord | Own bot, added by an admin (your server); followed announcement channels | Self-bots / user tokens |
| X | (Deferred.) If used: official API, narrow filtered stream, hard monthly cap; posting only via **web intent from your account after approval** (M23) | Scraping (twscrape/Nitter/Apify); auto-replies/mentions; duplicate posts; bulk follows; pay-to-post schemes |
| Reddit | (Optional, if approved) official API | AI training on Reddit data without approval |
| Quest platforms (Galxe, Layer3, Zealy, TaskOn…) | Read public task pages; alert you; let platforms verify on-chain actions | Headless browsers, captcha solvers, internal endpoints, auto-follows, re-registering after a ban |
| CoinGecko / GeckoTerminal | One key; **cache ≤ 24 h, encrypted, deleted on exit**; attribution on display | Long-lived archive (build long price history from exchanges/on-chain instead); redistribution |
| DexScreener | Keyless API within limits (60/min profiles/boosts; ~300/min pairs; search ≤ 30 results) | Resale; a competing screener; search-driven discovery (use addresses) |
| DefiLlama | `api.llama.fi` only | Site scraping, unofficial APIs, republishing (damages clause) |
| Birdeye | — | Any use (bans storage; "not intended for actual trading") |
| Etherscan | Manual lookups | **Decision input** (terms bar use as a basis for financial gain); extra accounts → use **Blockscout** / own RPC |
| GoPlus / RugCheck | One key; cache per token; stay under limits | Proxies to beat limits; bulk data-mining |
| Jupiter | Issued keys only | Deprecated lite-api / V1 endpoints |
| Jito | Tip **inside** the trade transaction; cap tips from tip-floor percentiles | Tip in a separate transaction |
| RPC providers (Helius, Alchemy, Chainstack…) | One account each; spread load across *different* providers | Second accounts, key multiplexing, resale |
| Solana public RPC / PublicNode | Low-volume fallback | Production traffic; IP rotation |
| All exchanges | Trade-only, IP-locked keys; whitelist-only withdrawals; explicit STP; rate-limit from live headers | §3 list |
| Lido CSM / validators | Allow-listed relays; fixed fee recipient; timely exits | Changing the fee recipient; a second instance with the same keys |
| Anthropic / OpenAI | Human approval on trade decisions (usage policy treats financial decisions as high-risk) | Deceptive promotion/shilling drafts |
| Datasets: MemeTrans (CC BY-NC-SA), SolRPDS (CC BY), Pumpfun corpus (CC BY) | Private models; attribution | Shipping MemeTrans-trained models commercially |
| Tailscale Personal | Private use | Staying on the free plan if commercial |

## 5. Data-provenance tagging (one mechanism for all data terms)

- **Every stored row carries** `source`, `licence` and `use_flags`:
  - `train_ok`: may be used for training;
  - `model_input_ok`: may be fed to a model;
  - `display_ok`: may be shown;
  - `retention_days`: how long it may be kept;
  - `commercial_ok`: allowed in a commercial product.
- **Training pipelines** (M7, M21 distillation, Laya/decision-model fine-tunes, Hindsight retain) **refuse rows** whose `train_ok = false`.
  - Defaults: Telegram, Birdeye and Etherscan rows are false.
  - Models trained on MemeTrans are flagged `commercial_ok = false`.
- **Inference paths** (tier B, agents, RAG retrieval) refuse rows with `model_input_ok = false`. This covers Telegram.
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
  - AUSTRAC register entries by ABN for every venue, before funding and quarterly;
  - reconcile OKX AU derivatives (retail vs wholesale);
  - read each AU venue's conduct, STP and rate-limit terms;
  - FP Markets client-agreement clauses on algorithmic trading.
