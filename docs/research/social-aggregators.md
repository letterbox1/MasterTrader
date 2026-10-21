_Raw notes from the research agents. They back up [../06-aggregators-and-market-providers.md](../06-aggregators-and-market-providers.md). Checked 2026-10-21; (U) = unverified._

# Social / news aggregators: RSS-Bridge, threads-scraper, Spacebar, social-media-scraping topic

## Time-sensitive platform changes
- **Reddit** (reported 2026-09-30 via TechRepublic, ppc.land, TechWyse, dev.to; primary post not reached (U)):
  - no new public API access requests after **2026-10-31**;
  - unregistered apps lose access 2027-01-12;
  - the public Data API closes **March 2027**;
  - **Reddit RSS ends 2026-11-13**;
  - unauthenticated `.json` endpoints were already closed in mid-2026 (confirmed in RSS-Bridge `docs/10_Bridge_Specific/Reddit.md`).
- **Telethon**: GitHub repo archived 2026-02-21 and moved to codeberg.org/Lonami/Telethon (maintenance there unverified (U)).
- **Nitter**: archived 2026-10-09 after X cease-and-desist letters (2026-08-24).
- **snscrape**: last commit 2023-06-22, dead.

## RSS-Bridge — UNLICENSE, ~9.3k★, 4,555 commits, last commit 2026-10-19, 552 bridges, rolling master, Docker
| Bridge | Method | Auth | Status |
|---|---|---|---|
| TelegramBridge | t.me/s/<channel> web preview, 1h cache | none (public channels) | Works (#4985 open) |
| RedditBridge | old.reddit search.json, or OAuth with app creds | needs creds now | Broken without creds; ends 2027 |
| BlueskyBridge | official public.api.bsky.app | none | Works |
| MastodonBridge | ActivityPub outbox, 15-min cache | some instances need signed fetch | Works |
| YouTube bridges | HTML scrape | none | Works (U); native channel RSS is simpler |
| TwitterBridge | guest token + public bearer | — | Treat as broken |
| TwitterV2Bridge | official API | paid token | Works if you pay |
| FarsideNitterBridge | Nitter | — | Dead |
| Instagram / Threads / TikTok / Facebook | scrape, cookies | — | Fragile; skip |
| StockFilingsBridge | SEC browse-edgar | none | Works (U); prefer EDGAR JSON/Atom |
| Reuters, AP, NYT, Guardian, Economist, Euronews, Substack | scrape | optional cookies | Generally maintained (U) |
| WallmineNews, InvestorsObserver, Binance blog, Bundesbank, Worldbank | scrape | — | Optional |
| CssSelector / XPath / FeedMerge / Filter | generic | — | Useful; also the SSRF surface |

- **No bridge exists for:** StockTwits, Seeking Alpha, Investing.com, ForexFactory, CoinMarketCap, Yahoo, Bloomberg, CNBC, Discord, LinkedIn.
- **Hardening:**
  - `enabled_bridges[] = *` by default → set an explicit whitelist.
  - Auth is off by default → enable it, or publish no port (internal Docker network only).
  - The SSRF guard blocks private/reserved IPv4 and pins DNS; IPv6 coverage (U).
- **Cache:** 15 min–3 h, so it's not for low-latency signals. Always store our own `ts_ingest`.
- **Alternative:** RSSHub (AGPL-3.0, ~46.6k★) for routes RSS-Bridge lacks.

## threads-scraper — Avoid
- 6★, 3 commits, last commit 2026-08-25 ("add affiliate tracking to Apify links").
- **No licence** (all rights reserved).
- A paid Apify actor: Puppeteer driving logged-out `threads.net`, intercepting GraphQL.
- Defaults to Apify residential proxies; charges $0.004/post; README links carry affiliate tags.
- Timestamps are derived from relative times ("2h"), so they're poor for point-in-time data.
- Alternative: Meta's official Threads API keyword search (2,200 queries/24h per user).

## Spacebar (formerly Fosscord) — Avoid
- Self-hostable, Discord-compatible chat platform under AGPL-3.0.
- The `server` repo has ~2.2k★ and is still in development with no releases.
- It is **not a data source** and doesn't read Discord; reading other people's Discord servers means self-bots, which break Discord's terms.
- For alerts, use ntfy, a Telegram bot or a Discord webhook instead.

## social-media-scraping topic
- 50 repos (+86 under social-media-scraper).
- They're mostly lead-gen / email harvesters and vendor marketing (omkarcloud, ChocoData, ScrapingBee, Decodo, proxidize), nearly all under 50★.
- Nothing worth adopting. The real tools live outside the tag:

| Platform | Pick | Licence | Stars | Risk | Verdict |
|---|---|---|---|---|---|
| Bluesky | Jetstream firehose + MarshalX/atproto SDK | MIT/Apache, MIT | 43 (U) / 661 | None | **Adopt** |
| Mastodon | Mastodon.py / RSS-Bridge | MIT (U) | — | Low | Adopt (low volume) |
| Telegram | Telethon (Codeberg) + RSS-Bridge fallback | MIT | 12.1k | Low–moderate (secondary number) | **Adopt (pinned)** |
| Reddit | PRAW / Async PRAW | BSD-2 | 4.3k | Access ends by 2027 (U) | Optional; request access before 2026-10-31 |
| X (official) | API v2 pay-per-use, ~$0.005/post read (U) | proprietary | — | None | Optional, budget cap |
| X (scrape) | twscrape | MIT | 2.9k (active) | **High** (bans, legal) | Personal only, off by default |
| X | twikit | MIT | 4.7k | High | Reference |
| X | snscrape / Nitter | GPL / AGPL | 5.5k / 14.5k | — | Dead |
| YouTube | channel RSS + Data API v3; yt-dlp for subtitles | — | — | Low | Optional |
| StockTwits | v2 REST `streams/symbol/{SYM}.json` (U) | proprietary | — | Low–moderate | Optional, test first |
| Instagram | instaloader | MIT | 13.6k | High | Avoid |
| TikTok / LinkedIn / Facebook | — | — | — | High | Avoid |
| Threads | official API | — | — | None | Optional, low value |
| Discord | discord.py official bot (own / consenting servers) | MIT | — | Self-bots break ToS | Optional |

Sources:
- https://github.com/RSS-Bridge/rss-bridge
- https://github.com/DIYgod/RSSHub
- https://github.com/the-ai-entrepreneur-ai-hub/threads-scraper
- https://github.com/spacebarchat
- https://github.com/topics/social-media-scraping
- https://github.com/zedeus/nitter
- https://github.com/vladkens/twscrape
- https://www.techrepublic.com/article/news-reddit-rss-public-api-shutdown/
- https://ppc.land/reddit-to-halt-public-data-api-access-in-march-2027-as-14-000-apps-register/
- https://developers.facebook.com/documentation/threads/keyword-search
