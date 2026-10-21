# D08 · Intel (News, Social, Events & Calendar)

| | |
|---|---|
| **Route** | `/intel` (tabs: Feed · Events · Calendar · Sentiment · Sources) |
| **Modules** | M2 news & social, M3 global events, M5 calendars, M21 tier-B scores, M9 RAG |
| **Phase** | 4 |
| **Mock-up reference** | `social-sentiment-macro-geopolitical-firehose.png` |

## Purpose

Show what the world is saying and doing that could move the user's markets:
- filtered by relevance;
- scored by decision models;
- mapped to instruments;
- linked to the calendar and its trading blackouts.

## Layout by tier

| Tier | Layout |
|---|---|
| ≥ 2xl | Left: filters (6). Centre: feed (12). Right: events map/list + next calendar items (6). |
| xl/lg | Filters as a top bar; feed + right column |
| md | Tabs; feed full width |
| ≤ ph | Tabs; `DocumentCard` list with infinite scroll; filters in a sheet |

## Tabs & widgets

| Tab | Shows | Source |
|---|---|---|
| **Feed** | `DocumentCard`s: source (RSS / RSS-Bridge / Telegram / Discord / Bluesky / Mastodon / GDELT / EDGAR), time (published + ingested), title/snippet, linked tickers, FinBERT sentiment, **tier-B scores** (direction, event type, relevance, veto), dedup count ("+4 similar"). **Filters:** watchlist only, asset class, source, min relevance, sentiment, event type, language. | `/intel/documents`, WS `text.doc` |
| Document detail (sheet) | Full text (where licence allows; otherwise headline + link), entity links, tier-B probabilities with model version, related documents (RAG), "Ask agents" | `/intel/documents/{id}`, `/rag/search?similar=` |
| **Events** | Geo events (quakes, storms, fires, disasters, conflict, sanctions, prediction-market moves): severity, location, exposure-map links to instruments (FX, commodities, indices), event score. Map ≥ md (MapLibre, optional); list < md. | `/intel/events`, WS `evt` |
| **Calendar** | Macro releases (consensus/actual/previous, surprise), central-bank meetings, earnings, IPOs, COT/EIA/WASDE days, exchange holidays. **Blackout markers** where risk rules pause strategies. Filters: country, importance, instruments. | `/intel/calendar`, WS `cal` |
| **Sentiment** | Per instrument/sector: sentiment index over time, mention volume, sentiment vs price chart, retail positioning (Myfxbook/IG/OANDA), prediction-market probabilities | `/intel/sentiment` |
| **Sources** | Configured sources: status, items/day, relevance hit-rate, licence/ToS tag, mute/unmute, add new (RSS URL, RSS-Bridge bridge, Telegram channel, Discord inbox channel, Bluesky keywords). Shows deferred sources (Reddit, X) as disabled with the reason. | `/intel/documents?sources=1`, `/data/feeds?kind=text` |

## Actions

| Control | Command | Level |
|---|---|---|
| Add source | `intel.source.add` | C1 (paid/ToS-banned sources are rejected) |
| Mute / unmute source | `intel.source.mute` | C0 |
| Update watchlist / keyword filters | `intel.watchlist.update` | C0 |
| Ask decision model on a document | `models.tierb.ask` | C0 |
| Ask agents for analysis | `agents.run_analysis` (with document context) | C1 |
| Add calendar blackout rule | → D06 Policy (Blackouts) | C1 |
| Open original | External link (new tab, `rel=noopener`) | C0 |

## States & rules

- **Untrusted content:** scraped content is rendered as **text only** (no HTML injection). Links show their destination domain.
- **Timestamps:** approximate timestamps are flagged ("≈ 2h ago (source-claimed)").
- **Paywalled/licensed text:** never shown in full; headline + link only.

## Additions from the CryptoTrader review

- **Telegram is shown as postures only:** per contract/ticker, mention velocity, channel count, new-channel share and time since first call. **No Telegram text** is shown with tier-B scores or offered to "Ask agents" (Telegram API ToS; see [12 §4](../../12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Sources tab shows each source's provenance flags (`train_ok`, `model_input_ok`, `retention_days`).
- New sources: Farcaster, CryptoPanic. Polymarket and Kalshi are read-only probabilities.

## Acceptance criteria

1. **Speed:** new documents appear within 5 s of ingestion, with scores when available. "Scoring…" shows until tier B returns.
2. **Calendar:** blackout windows match the risk manager's (same source of truth).
3. **Phones:** the feed stays smooth at 1,000+ items (virtualised).

## Backend contract

- **Queries:** `/intel/documents` (+ `/{id}`), `/intel/events`, `/intel/calendar`, `/intel/sentiment`, `/rag/search`, `/data/feeds?kind=text`.
- **WebSocket topics:** `text.doc`, `evt`, `cal`, `tierb`.
- **Commands:** `intel.source.add|mute`, `intel.watchlist.update`, `models.tierb.ask`, `agents.run_analysis`.
