# Aggregators, Social Sources & Market Providers — Where They Fit

_Date: 2026-10-21. Extends [01-repo-vetting-report.md](01-repo-vetting-report.md) and [03-build-spec.md](03-build-spec.md). Raw evidence:_
- _[research/social-aggregators.md](research/social-aggregators.md)_
- _[research/listeningkit-log.md](research/listeningkit-log.md)_
- _[research/forex-macro-market-providers.md](research/forex-macro-market-providers.md)_

_(U) = unverified._

---

## 0. ⚠️ Time-sensitive actions

| When | What | Action |
|---|---|---|
| **Decision (2026-10-21)** | **Reddit and X are deferred** for v1, unless a free and permitted route appears | Free social coverage comes from **Telegram** (client + Bot API) and **Discord** (own server + followed announcement channels + own bot), plus Bluesky and Mastodon |
| By 2026-10-31 | Reddit reportedly stops accepting new public API access requests (U, from secondary reporting of a 2026-09-30 announcement) | **Applied 2026-10-29** (P0-T001). Reddit is in or out on Reddit's decision; the commitments made in the request are in [12 §4](12-policy-and-compliance.md#4-per-platform-data--automation-rules). Previously: deferred; if you change your mind, apply before this date. |
| 2026-11-13 | Reddit RSS reportedly ends (U) | Don't build on Reddit RSS (that includes RSS-Bridge's Reddit bridge and listeningkit's Reddit source) |
| 2027-01 → 2027-03 | Unregistered apps lose access, then the public Data API closes (U) | Treat Reddit as a **sunsetting** source; never core |
| Now | Telethon's GitHub repo is archived; development moved to Codeberg | Pin the version and keep RSS-Bridge's Telegram bridge as a fallback |
| Now | Nitter archived after X cease-and-desist letters; snscrape dead | No free legal X route, so X is deferred |

---

## 1. Verdicts on the tools you proposed

| Tool | What it really is | Licence | Verdict | Where it slots |
|---|---|---|---|---|
| **[RSS-Bridge](https://github.com/RSS-Bridge/rss-bridge)** | PHP service turning ~550 sites without feeds into Atom/JSON feeds; ~9.3k★, active (2026-10-19) | Unlicense (public domain) | **Adopt as an internal sidecar** | M2: `rss-bridge` Docker service on the internal network only, with an explicit whitelist and auth on. The RSS ingester reads `?format=Json`. |
| [spacebarchat](https://github.com/spacebarchat) | Self-hosted **Discord-compatible chat server** (formerly Fosscord). It can't read Discord. | AGPL-3.0 | **Avoid** | No role in ingestion. Alerts go through the one fan-out to Telegram / ntfy / email (M15, see [Alert delivery](#alert-delivery--broker-gateways-m15--m12)). |
| [threads-scraper](https://github.com/the-ai-entrepreneur-ai-hub/threads-scraper) | Source of a paid Apify actor (logged-out Puppeteer on Threads); 6★; affiliate links | **No licence** (all rights reserved) | **Avoid** | If Threads is ever wanted: the official Threads API keyword search. Low value for trading. |
| [topics/social-media-scraping](https://github.com/topics/social-media-scraping) | ~50 repos, mostly lead-gen email harvesters and vendor marketing | mixed / none | **Nothing to adopt** | Real picks per platform in §2 |
| [listeningkit](https://github.com/matthewdonsemail-lab/listeningkit) | A **fork of [obris-dev/openmagpie](https://github.com/obris-dev/openmagpie)**: B2B lead-gen social listening (Django; Reddit RSS, HN, GitHub, RSS, X via twikit). PostHog telemetry is on by default. | Apache-2.0 open-core | **Reference only** (use the upstream if ever) | Borrow two ideas: the Feed → Watch → action-chain pattern, and a **cheap local-LLM relevance gate** before FinBERT |
| [log](https://github.com/matthewdonsemail-lab/log) | Convex hackathon lead-gen app; scrapes X and Facebook via your logged-in browser session and a residential proxy; its extension uploads your session cookies | MIT | **Avoid** | — |

**Bottom line:** of the six links, only **RSS-Bridge** earns a place in the stack. The others are lead-generation tools, a chat server, or unlicensed scrapers.

---

## 2. Final M2 social & news ingestion stack

| Tier | Source | Tool | Risk | Notes |
|---|---|---|---|---|
| **Core: news** | Wire, financial and crypto news RSS; central banks (Fed, ECB, BoE, BoJ, SNB, RBA, BoC, RBNZ); regulators | feedparser + **trafilatura**, **crawl4ai** for JS pages | Low | Respect paywalls and robots.txt |
| **Core: news** | Sites without feeds (AP, Reuters, Economist WIB, Substack, Bundesbank, Binance blog, any page) | **RSS-Bridge** (whitelisted; CssSelector/XPath for custom pages) | Low | 15-min to 3-h cache, so context only, not latency signals |
| **Core: news** | Global news volume and tone | **GDELT** | None | — |
| **Core: filings** | SEC EDGAR | edgartools / official JSON and Atom (declared User-Agent, ≤10 req/s) | None | Prefer this over RSS-Bridge's StockFilings bridge |
| **Core: social** | Telegram channels and groups | **Telethon** client API (pinned, secondary number) + **Bot API** for channels where your bot is admin; RSS-Bridge Telegram bridge as fallback | Low–moderate | Real-time, free. **Postures only:** Telegram API ToS §1.5 bars AI training/deployment on Telegram data, so text never reaches models, RAG or training. Only regex-extracted addresses/tickers and counts feed deterministic postures (`text.telegram_posture`, subject `posture.telegram.*`, consumed by M4/M11 rules only; [12 §4](12-policy-and-compliance.md#4-per-platform-data--automation-rules)) |
| **Core: social** | Discord | Your own private server + Discord's **"Follow" on public announcement channels** (cross-posted into your server) + your own **discord.py** bot (Message Content intent) | Low | Free and within Discord's terms. **No self-bots / user tokens.** Follow works only for **Community-server announcement channels the project actually publishes**; each receiving channel takes ~10–15 follower webhooks, so spread follows over category channels. Message Content intent is self-serve for apps in < 10k servers (U, policy as of Jun 2026) |
| **Core: social** | Bluesky | **Jetstream firehose + atproto SDK**, filtered on cashtags and keywords | None | Free and explicitly permitted |
| Core: social | Mastodon / fediverse | Mastodon.py or the RSS-Bridge Mastodon bridge | Low | Low volume |
| Core: social | **Farcaster** | Self-hosted **Hubble** node or a free hub endpoint | None | Crypto-native; useful for airdrop/launch chatter |
| Core: news | **CryptoPanic** (free tier) | REST | Low | Crypto headline aggregation with votes; attribution required |
| **Pending (access requested 2026-10-29)** | Reddit | (PRAW, official OAuth, read-only) | Low | Aggregates only, raw text ≤ 24 h, no training, local model only ([12 §4](12-policy-and-compliance.md#4-per-platform-data--automation-rules)). In or out on Reddit's decision. Closing to new apps 2026-10-31, sunset 2027 (U). Stays optional: if access is ever granted, a connector is an optional item, and not worth building once the public Data API closes |
| Conditional | StockTwits | v2 REST `streams/symbol/{SYM}` (U) | Low–moderate | Most finance-relevant social source if still reachable; checked in Phase 1 (open checks, §3) |
| Conditional | YouTube | Channel RSS + Data API v3; yt-dlp for subtitles and transcripts | Low | Finance channels, earnings calls. Checked in **Phase 4** (P4-T066; connector P4-T024), not Phase 1 (open checks, §3) |
| **Deferred** | X / Twitter | (Official API v2 is pay-per-use, ~$0.005 per post read (U)) | — | Revisit if budget allows; scraping (twscrape) not in v1 |
| Optional | Extra routes (Asian finance/crypto) | **RSSHub** (AGPL, fine for personal use) | Varies | Only for routes RSS-Bridge lacks |
| **Excluded** | Instagram, TikTok, LinkedIn, Facebook, Threads scrapers, Discord self-bots / user-token scraping, Nitter, snscrape, twscrape, threads-scraper, log, Spacebar | — | — | — |

**Processing chain (unchanged, plus one step).** Telegram never enters this chain: its messages go only to the regex posture extractor (02 F3b, [12 §4](12-policy-and-compliance.md#4-per-platform-data--automation-rules)). Every other source runs:
1. Fetch.
2. Dedupe (canonical URL + content hash).
3. **Local-LLM relevance gate** ("is this about a tradable instrument / macro event?", the OpenMagpie idea).
4. Ticker/entity linking.
5. FinBERT sentiment.
6. Embeddings.
7. Store in `document` with `ts_ingest` from our clock. `ts_published` is flagged `approx=true` when it comes from coarse feed dates or relative times ("2h ago").

---

## 3. Additional forex & multi-asset providers

> **Free-only rule (2026-10-21):** only free sources and free tiers are implemented. Paid items mentioned below (CoinGlass, the CME FedWatch API, X API, Trading Economics, Glassnode) are **excluded**; see [03-build-spec §1](03-build-spec.md#1-ground-rules).

### Execution / broker adapters (M12)
| Provider | Why | Lib | Priority |
|---|---|---|---|
| **IG** (REST + Lightstreamer) | FX/indices/commodities CFDs, free demo, **client-sentiment endpoint** | `trading-ig` (BSD-3, active 2026-08) | High |
| **cTrader Open API / FIX** | Free; works with any cTrader broker | `ctrader-open-api` (MIT, official) | Medium |
| Saxo OpenAPI | Multi-asset; free SIM (24-h tokens) | Thin httpx client (the library is stale) | Optional |
| FOREX.com / GAIN | REST + streaming | AppKey requested via support | Low |
| OANDA, IBKR, MT5, Alpaca | Already planned. IBKR needs a running **IB Gateway**: an `ib-gateway` container (IBC-managed login and re-auth, digest-pinned) is added when IBKR is used | — | — |
| ~~FXCM~~ | API deprecated | — | Skip |

### Market data (M1)
- **ECB Data Portal** reference rates + a self-hosted **Frankfurter** (MIT).
- **TrueFX** / **HistData** tick and M1 data to cross-check Dukascopy (test TrueFX availability).
- **Twelve Data** free tier (800/day) for backup bars.
- **Binance data.binance.vision** for free bulk crypto history (top pick).
- **akshare** (MIT, very active) for China/Asia futures and commodities.
- **FinanceDatabase** (MIT) as the symbol master.
- Tardis monthly free samples (U) for order-book research.

### Crypto enrichment & cache (M1 / M4)
| Source | Use | Terms we follow |
|---|---|---|
| **CoinGecko Demo** (one key) | Categories, new listings, official links (`links.chat_url`, homepage), metadata for M4 enrichment and display | Cache **≤ 24 h**, **encrypted** at rest (pgcrypto with a key from the sops file) and **purged on shutdown/exit**; attribution on display ([12 §4](12-policy-and-compliance.md#4-per-platform-data--automation-rules)). Display and cross-check only: never persisted to `journal.*` and never the stored tax value ([16 §4.1](16-configuration-and-safety-model.md#41-valuing-crypto-for-the-journal)) |
| **DefiLlama** | Protocols/TVL (`api.llama.fi`) and yield pools (`yields.llama.fi`) | Only the **official free API hosts** `api.llama.fi` and `yields.llama.fi`. No site scraping, unofficial APIs or republishing; results cached |

### Calendars & central banks (M5 / M3)
- **US calendar backbone:** FRED/ALFRED release dates (point-in-time).
- **Consensus forecasts:** ForexFactory weekly JSON. It's the only practical free source; ToS-grey, so personal use only, cached, and polled politely.
- **One SDMX client, `sdmx1` (Apache-2.0):** ECB, IMF (SDMX 3.0), OECD, BIS, Eurostat.
- **Direct fetchers:** BoE IADB, BoC Valet, RBA, SNB, BoJ.
- **Catch-all:** **DBnomics** (its library is AGPL, fine for personal use).
- **Event feeds:** central-bank RSS for statements, minutes and speeches.
- **ABS CPI (tax input):** **All groups CPI, weighted average of eight capital cities**, quarterly, series **A2325846C** (U, verify the ID). This is the series the 2027 cost-base indexation uses ([09](09-journal-and-tax.md#️-key-findings-that-shape-the-design)); other ABS CPI series (e.g. the monthly indicator) are display-only. Stored point-in-time with release dates, so revisions never rewrite an earlier value.

### Reports, nowcasts & forecasts (M6 features, M5 release events)

_Ingested from Phase 4. Until then D02 shows these widgets as "arrives in P4" rather than placeholder data._
- **Nowcasts:** GDPNow, NY Fed Staff Nowcast, Cleveland Fed inflation nowcast.
- **Official projections:** Fed SEP / dot plot, ECB SPF, IMF WEO, OECD Economic Outlook.
- **Commodity reports:** EIA STEO, USDA WASDE (keyless report files) and USDA NASS QuickStats (free API key, P0 T0.10), Baker Hughes rig count.
- **Positioning and risk:** CFTC COT, Cboe VIX history.
- **Fed-path probabilities:** compute implied probabilities yourself from ZQ (Fed funds) futures; that's free and avoids FedWatch's ToS.

### Retail sentiment & positioning (M6)

_Phase 4 sources (CFTC COT is already ingested in Phase 1)._
- **Myfxbook Community Outlook:** free, 100 calls/day, all symbols in one call. Poll every 15–30 min.
- **IG client sentiment.**
- **OANDA order/position books** (verify the endpoints still work).
- **CFTC COT.**
- Optional: Dukascopy SWFX index (low frequency); free Binance futures long/short ratios. (CoinGlass is paid, so excluded by the free-only rule.)

### Prediction markets as macro-event probabilities (M3 / M6)

_Phase 4 sources._
- **Kalshi:** public reads, no auth. CFTC-regulated Fed/CPI/NFP/GDP markets. Use httpx; the official library has a proprietary licence.
- **Polymarket:** Gamma + CLOB, public reads.
- Manifold and Metaculus are optional (weak signal / restrictive terms).

### On-chain & crypto-infrastructure providers (M4 / M12 / M22; added from the CryptoTrader review)
| Provider | Use | Free tier notes |
|---|---|---|
| **Blockscout** (API + self-hostable) | Contract source, creator, holders, txs for **decision inputs** | Open source; replaces Etherscan as a decision input (Etherscan terms bar use as a basis for financial gain) |
| Own RPC + Alchemy / Helius / Chainstack free tiers | Reads, `eth_call`, `simulateTransaction`, webhooks | One account per provider; spread load across *different* providers |
| **Anvil** (Foundry) mainnet fork | Local transaction simulation before any signature | Free, local. With Solana `simulateTransaction`, the only simulators used; **Tenderly is not used** |
| Own RPCs (gas / fee APIs) | **Live** EVM gas: `eth_feeHistory` + base fee; Solana: `getRecentPrioritizationFees`, the Helius priority-fee estimate, the Jito tip floor | Free with the RPC tiers above. Feeds the cost gate, gas windows and gas budgets; no fixed gas constants ([16 §4.3](16-configuration-and-safety-model.md#43-live-inputs-instead-of-constants)) |
| Venue fee-tier and funding APIs | Live exchange fees and funding rates (M16) | Free with venue keys; used by backtests, the cost gate and TCA |
| DefiLlama (`api.llama.fi`, `yields.llama.fi`) | TVL, protocol lists, yield pools (M4 discovery, M22 allocator) | Official free API hosts only (see *Crypto enrichment & cache*) |
| The Graph (free query allowance) | Protocol subgraphs (pools, positions, governance) | Key required; cache results |
| Jupiter (issued key) / 1inch / 0x | DEX quotes and routing | Use issued keys only; deprecated lite-api / V1 endpoints are out |
| Jito | Solana bundle submission | Tip **inside** the trade transaction, capped from tip-floor percentiles |
| Flashbots Protect RPC | Private EVM transaction submission (MEV protection) | Free |
| Finnhub (free) | Equity/FX/crypto quotes, IPO + earnings calendar | Personal use; 60 calls/min |
| FMP (free) | Earnings/IPO calendar cross-check | 250 calls/day |

### Skip list
| Item | Reason |
|---|---|
| FXCM | API deprecated |
| investpy / investiny / Investing.com | Dead, and scraping is banned |
| tvdatafeed / TradingView data | No official data API; ToS bans extraction |
| `duka` | Dead since 2016; use dukascopy-node or our own bi5 parser |
| **LBMA gold/silver fixes** | IBA licence required, even for history; use broker spot XAU/XAG + COMEX GC/SI instead |
| CME FedWatch scraping | ToS; use the paid API or compute from ZQ futures |
| Kitco scraping, Trading Economics guest access | ToS / discontinued |
| CryptoCompare free tier | Reportedly retired 2026-05 (U) |
| Glassnode | No free API |
| exchangerate.host (100/month), Alpha Vantage (25/day) | Free tiers too small |
| MT4 ZMQ bridges | Unmaintained; MT4 is end-of-life |
| Stale libraries: pandasdmx, oandapyV20, saxo_openapi, coinpaprika | Use `sdmx1` or thin httpx clients |
| **Birdeye** | Terms ban storage and say "not intended for actual trading" |
| **Etherscan as a decision input** | Terms bar use as a basis for financial gain; manual lookups only → Blockscout / own RPC |
| **Tenderly** | Not used, on any plan (the free plan has no simulation API) → Anvil fork / `simulateTransaction` |
| Dune (free) | View-only for our purposes; no free API worth wiring |
| Tardis.dev | Paid beyond the free monthly samples |
| TokenSniffer | No free API; GoPlus/RugCheck/Honeypot.is cover it |
| CoinGecko as a price archive | Demo terms: cache ≤ 24 h; build long history from exchanges/on-chain instead |
| Scraping DefiLlama's site | Terms; use the official API hosts only |

### Regulatory & venue watch (M5 / M16)

Official pages and feeds that can change the rules or a venue's standing ([16 §4.3](16-configuration-and-safety-model.md#43-live-inputs-instead-of-constants)).

| Group | Sources |
|---|---|
| **Australia** | ATO (crypto and investor guidance, rulings), Treasury (tax law changes), AUSTRAC (VASP register, Travel Rule), ASIC (product interventions, warnings), RBA (cash rate, F11 notes) |
| **If a move is planned** | UAE (Ministry of Finance, Federal Tax Authority, VARA/SCA), Cyprus (Tax Department, CySEC), Egypt (Egyptian Tax Authority, Central Bank of Egypt, FRA). Added only while the residency timeline has a planned period there |
| **Venues** | Each venue's official status page / incident feed, announcements page and proof-of-reserve page |

**How it's fetched:**
- RSS/Atom where offered.
- Otherwise a **low-frequency page fetch** (trafilatura) or a **headless browser** (crawl4ai) for JS-only pages, always within each site's terms and robots.txt.
- Each fetch is diffed against the last one. A change becomes a `REG_CHANGE` review task for you (and your tax agent where relevant).
- **Rules are never auto-applied.** A reviewed change becomes a versioned rule or venue-registry update through the normal C-level commands.

**Venue health inputs (M16, [12 §2](12-policy-and-compliance.md#2-venue-access-registry)):**
- **Our own measured withdrawal and deposit times** from journal transfers (the primary signal).
- Deposit/withdraw-enabled flags per asset from venue APIs (e.g. ccxt `fetchCurrencies`).
- Venue status pages and incident feeds, and proof-of-reserve pages, via the watch above.
- Your own notes on a venue.
- **AUSTRAC register re-check: a quarterly USER task**, not automated (the register has no API). Until the task queue (M19) exists in Phase 5, the reminder goes out as a Telegram/notification alert.

**Egress check (M16):** the free **DB-IP Lite** country database (CC BY 4.0, attribution required; refreshed monthly) confirms that exchange traffic leaves via the allow-listed IP in the configured country ([16 §3.2](16-configuration-and-safety-model.md#32-network-egress-and-ip-locked-keys)). It's a safety gate only, never a tax input; tax residency comes from the residency timeline in [09](09-journal-and-tax.md#jurisdiction-plugin-interface).

### Alert delivery & broker gateways (M15 / M12)
- **One alert fan-out:** Grafana alerts → webhook → the `alert.*` consumer → Telegram / ntfy / email.
- **Email:** your own mail provider's SMTP with an app password (stored in the sops file), or email turned off; Telegram and ntfy remain.
- **ntfy:** self-hosted on the host and reachable via Tailscale only. iOS push uses ntfy's upstream relay, which carries only a message ID, never the content.
- **IB Gateway:** an `ib-gateway` container (IBC-managed) is added when IBKR is used; its login is a USER step.

### Open checks (do these in Phase 1)
- OANDA order/position book endpoints still work.
- TrueFX downloads still work.
- The live IMF SDMX 3.0 base URL.
- The IG sentiment endpoint path.
- StockTwits API reachability.
- Tardis free samples.
- BoC Valet / BoJ work without a key.
- The ABS CPI series ID (A2325846C) and its release calendar.

**Phase 4 check (P4-T066):** YouTube: channel RSS still reachable, Data API v3 quota, and yt-dlp subtitle use for the chosen channels.

---

## 4. SaaS note for these sources

**Defensible in a SaaS, all official or open:**
- Bluesky, Mastodon, the Telegram client API, the paid X API, Reddit under a commercial deal, the YouTube API, the Threads API.
- News headlines and links.
- Public-domain government and central-bank data, and GDELT.

**Must be replaced or dropped:**
- **Personal-use-only sources:** ForexFactory, Myfxbook, Twelve Data individual plans, yfinance, finviz.
- **Scrapers:** twscrape and any cookie-based scraper.
- **AGPL components** if you modify them: RSSHub, DBnomics' library.

See [05-saas-legal-and-licensing.md](05-saas-legal-and-licensing.md).
