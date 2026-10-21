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
| By 2026-10-31 | Reddit reportedly stops accepting new public API access requests (U, from secondary reporting of a 2026-09-30 announcement) | Deferred, so no action. If you change your mind, apply before this date. |
| 2026-11-13 | Reddit RSS reportedly ends (U) | Don't build on Reddit RSS (that includes RSS-Bridge's Reddit bridge and listeningkit's Reddit source) |
| 2027-01 → 2027-03 | Unregistered apps lose access, then the public Data API closes (U) | Treat Reddit as a **sunsetting** source; never core |
| Now | Telethon's GitHub repo is archived; development moved to Codeberg | Pin the version and keep RSS-Bridge's Telegram bridge as a fallback |
| Now | Nitter archived after X cease-and-desist letters; snscrape dead | No free legal X route, so X is deferred |

---

## 1. Verdicts on the tools you proposed

| Tool | What it really is | Licence | Verdict | Where it slots |
|---|---|---|---|---|
| **[RSS-Bridge](https://github.com/RSS-Bridge/rss-bridge)** | PHP service turning ~550 sites without feeds into Atom/JSON feeds; ~9.3k★, active (2026-10-19) | Unlicense (public domain) | **Adopt as an internal sidecar** | M2: `rss-bridge` Docker service on the internal network only, with an explicit whitelist and auth on. The RSS ingester reads `?format=Json`. |
| [spacebarchat](https://github.com/spacebarchat) | Self-hosted **Discord-compatible chat server** (formerly Fosscord). It can't read Discord. | AGPL-3.0 | **Avoid** | No role in ingestion. For alerts use a Telegram bot / ntfy / Discord webhook (M15). |
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
| **Core: social** | Telegram channels and groups | **Telethon** client API (pinned, secondary number) + **Bot API** for channels where your bot is admin; RSS-Bridge Telegram bridge as fallback | Low–moderate | Real-time, free |
| **Core: social** | Discord | Your own private server + Discord's **"Follow" on public announcement channels** (cross-posted into your server) + your own **discord.py** bot (Message Content intent) | Low | Free and within Discord's terms. **No self-bots / user tokens.** |
| **Core: social** | Bluesky | **Jetstream firehose + atproto SDK**, filtered on cashtags and keywords | None | Free and explicitly permitted |
| Core: social | Mastodon / fediverse | Mastodon.py or the RSS-Bridge Mastodon bridge | Low | Low volume |
| **Deferred** | Reddit | (PRAW, official OAuth) | — | Closing to new apps 2026-10-31, sunset 2027 (U) |
| Conditional | StockTwits | v2 REST `streams/symbol/{SYM}` (U) | Low–moderate | Most finance-relevant social source if still reachable; test first |
| Conditional | YouTube | Channel RSS + Data API v3; yt-dlp for subtitles and transcripts | Low | Finance channels, earnings calls |
| **Deferred** | X / Twitter | (Official API v2 is pay-per-use, ~$0.005 per post read (U)) | — | Revisit if budget allows; scraping (twscrape) not in v1 |
| Optional | Extra routes (Asian finance/crypto) | **RSSHub** (AGPL, fine for personal use) | Varies | Only for routes RSS-Bridge lacks |
| **Excluded** | Instagram, TikTok, LinkedIn, Facebook, Threads scrapers, Discord self-bots / user-token scraping, Nitter, snscrape, twscrape, threads-scraper, log, Spacebar | — | — | — |

**Processing chain (unchanged, plus one step):**
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
| OANDA, IBKR, MT5, Alpaca | Already planned | — | — |
| ~~FXCM~~ | API deprecated | — | Skip |

### Market data (M1)
- **ECB Data Portal** reference rates + a self-hosted **Frankfurter** (MIT).
- **TrueFX** / **HistData** tick and M1 data to cross-check Dukascopy (test TrueFX availability).
- **Twelve Data** free tier (800/day) for backup bars.
- **Binance data.binance.vision** for free bulk crypto history (top pick).
- **akshare** (MIT, very active) for China/Asia futures and commodities.
- **FinanceDatabase** (MIT) as the symbol master.
- Tardis monthly free samples (U) for order-book research.

### Calendars & central banks (M5 / M3)
- **US calendar backbone:** FRED/ALFRED release dates (point-in-time).
- **Consensus forecasts:** ForexFactory weekly JSON. It's the only practical free source; ToS-grey, so personal use only, cached, and polled politely.
- **One SDMX client, `sdmx1` (Apache-2.0):** ECB, IMF (SDMX 3.0), OECD, BIS, Eurostat.
- **Direct fetchers:** BoE IADB, BoC Valet, RBA, SNB, BoJ.
- **Catch-all:** **DBnomics** (its library is AGPL, fine for personal use).
- **Event feeds:** central-bank RSS for statements, minutes and speeches.

### Reports, nowcasts & forecasts (M6 features, M5 release events)
- **Nowcasts:** GDPNow, NY Fed Staff Nowcast, Cleveland Fed inflation nowcast.
- **Official projections:** Fed SEP / dot plot, ECB SPF, IMF WEO, OECD Economic Outlook.
- **Commodity reports:** EIA STEO, USDA WASDE, Baker Hughes rig count.
- **Positioning and risk:** CFTC COT, Cboe VIX history.
- **Fed-path probabilities:** compute implied probabilities yourself from ZQ (Fed funds) futures; that's free and avoids FedWatch's ToS.

### Retail sentiment & positioning (M6)
- **Myfxbook Community Outlook:** free, 100 calls/day, all symbols in one call. Poll every 15–30 min.
- **IG client sentiment.**
- **OANDA order/position books** (verify the endpoints still work).
- **CFTC COT.**
- Optional: Dukascopy SWFX index (low frequency); CoinGlass ($29/mo) or free Binance futures long/short ratios.

### Prediction markets as macro-event probabilities (M3 / M6)
- **Kalshi:** public reads, no auth. CFTC-regulated Fed/CPI/NFP/GDP markets. Use httpx; the official library has a proprietary licence.
- **Polymarket:** Gamma + CLOB, public reads.
- Manifold and Metaculus are optional (weak signal / restrictive terms).

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

### Open checks (do these in Phase 1)
- OANDA order/position book endpoints still work.
- TrueFX downloads still work.
- The live IMF SDMX 3.0 base URL.
- The IG sentiment endpoint path.
- StockTwits API reachability.
- Tardis free samples.
- BoC Valet / BoJ work without a key.

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
