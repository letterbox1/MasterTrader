# Phase 4 · News, Social, Events & Calendars

| | |
|---|---|
| **Goal** | Free news, social, event and calendar intelligence flows into point-in-time features, document RAG and first-stage decision models, and calendar blackouts reach the risk manager. Telegram contributes **postures only**. |
| **Duration** | Weeks 16–19 |
| **Depends on** | P0 (TEI, gateway, provenance columns), P1 (store patterns, monitor), P2 (risk blackout hook, features framework) |
| **Unlocks** | P5 (Discord/Telegram discovery for airdrops), P6 (agents, RAG, tier B stage 2 training data) |
| **Modules** | M2 news & social, M3 global events, M5 calendars, M6 sentiment/regime features, M9 document RAG, M21 tier B stage 1 (SemIf) |
| **Containers** | `ingest-text`, `rss-bridge`, `nlp`, `ingest-events`, `decision-svc` (SemIf) |
| **Dashboards** | [D08](../ui/dashboards/D08-intel.md) Intel; tier B outputs on [D02](../ui/dashboards/D02-markets.md) and [D01](../ui/dashboards/D01-cockpit.md) |
| **Primary docs** | [03 M2](../03-build-spec.md#m2-news--social--mt_datatext) · [03 M3](../03-build-spec.md#m3-global-events--mt_dataevents) · [03 M5](../03-build-spec.md#m5-calendars--mt_datacalendar) · [03 M6](../03-build-spec.md#m6-features--mt_features) · [06 §2](../06-aggregators-and-market-providers.md#2-final-m2-social--news-ingestion-stack) · [10 §3](../10-memory-rag-and-models.md#3-document-rag-design-postgres) · [10 §4.3](../10-memory-rag-and-models.md#43-design) · [12 §4](../12-policy-and-compliance.md#4-per-platform-data--automation-rules) · [02 F3](../02-v1-architecture.md#8-end-to-end-flows) |

## 1. Scope

**In:** news (RSS, RSS-Bridge, trafilatura/crawl4ai, GDELT, EDGAR, central banks, Finnhub, CryptoPanic); social (Telegram postures, Discord followed channels, Bluesky, Mastodon, Farcaster; StockTwits/YouTube conditional); text pipeline; document RAG; global events + exposure map; calendars + blackouts; sentiment/regime per market type and positioning/nowcast features; SemIf relevance gate and first flags; morning brief; D08.

**Out:** Reddit (optional, only if approved) and X (deferred); agent debate and Hindsight (P6); own decision-model heads (P6).

## 2. Entry criteria

- P2 exit met (risk blackout hook exists). Telegram account + Discord server/bot ready (T0.06, T0.07). GPU decision made (T0.01) or CPU fallback accepted.

## 3. Requirements

| ID | Requirement | Source | Verified by |
|---|---|---|---|
| R4.01 | News: RSS + trafilatura/crawl4ai; **RSS-Bridge** sidecar (whitelisted bridges, auth on, scrapers network); GDELT; EDGAR feeds; central-bank RSS; Finnhub; CryptoPanic | [03 M2](../03-build-spec.md#m2-news--social--mt_datatext), [06 §2](../06-aggregators-and-market-providers.md#2-final-m2-social--news-ingestion-stack) | Feed health in D07 |
| R4.02 | **Telegram postures only:** Telethon + Bot API + RSS-Bridge fallback; regex-extracted addresses/tickers and counts → mention velocity, channel count, new-channel share, time since first call; `FLOOD_WAIT`-aware join queue; ≤ 500 channels | [12 §4](../12-policy-and-compliance.md#4-per-platform-data--automation-rules), [03 M2](../03-build-spec.md#m2-news--social--mt_datatext) | Posture tests |
| R4.03 | **No Telegram text reaches any model, RAG index or training set** (rows `model_input_ok = false`, `train_ok = false`) | [12 §5](../12-policy-and-compliance.md#5-data-provenance-tagging-one-mechanism-for-all-data-terms), [SPEC NN10](../../SPEC.md#non-negotiable-requirements) | Gate test |
| R4.04 | Discord bot on your server ingesting followed announcement channels (no self-bots/user tokens) | [06 §2](../06-aggregators-and-market-providers.md#2-final-m2-social--news-ingestion-stack), [12 §4](../12-policy-and-compliance.md#4-per-platform-data--automation-rules) | Ingest test |
| R4.05 | Bluesky Jetstream (cashtags/keywords), Mastodon, Farcaster (Hubble); StockTwits/YouTube only if checks passed in P1 | [06 §2](../06-aggregators-and-market-providers.md#2-final-m2-social--news-ingestion-stack) | Ingest tests |
| R4.06 | Text chain (non-Telegram, provenance checked first): dedupe → relevance gate → entity/ticker linking → FinBERT → TEI embeddings → `text.document`; approximate timestamps flagged | [03 M2](../03-build-spec.md#m2-news--social--mt_datatext), [02 F3](../02-v1-architecture.md#8-end-to-end-flows) | Pipeline tests |
| R4.07 | **Document RAG** (`rag` schema): pgvector HNSW (halfvec) + tsvector + pg_trgm, RRF, cross-encoder rerank, recency decay, **`as_of` filter**, section-aware chunking, caches | [10 §3](../10-memory-rag-and-models.md#3-document-rag-design-postgres), [03 M9](../03-build-spec.md#m9-memory--rag--mt_memory) | Retrieval benchmark |
| R4.08 | Global events: USGS, GDACS, NOAA/NHC, FIRMS, ReliefWeb, UCDP, GDELT, OpenSanctions, ACLED (research); exposure map; event score = severity × exposure × novelty | [03 M3](../03-build-spec.md#m3-global-events--mt_dataevents) | Event tests |
| R4.09 | **Polymarket/Kalshi read-only** probabilities, only where lawfully reachable, never via VPN; no trading | [12 §1](../12-policy-and-compliance.md#1-australian-boundary-the-load-bearing-assumption), [03 M3](../03-build-spec.md#m3-global-events--mt_dataevents) | Config review |
| R4.10 | Calendars: FRED/ALFRED releases, ForexFactory weekly JSON, central-bank schedules, COT/EIA/WASDE/Baker Hughes days, EDGAR earnings/IPOs, exchange holidays; **"event within N minutes" query → M11 blackouts** | [03 M5](../03-build-spec.md#m5-calendars--mt_datacalendar) | Blackout test |
| R4.11 | Features: sentiment + regime **per market type** (crypto, FX, metals, energy, equities) + macro layer; retail positioning (Myfxbook, IG, OANDA books); nowcasts; Fed-path from ZQ; VIX regime; prediction-market probabilities; Chronos/TimesFM/Kronos vol forecasts | [03 M6](../03-build-spec.md#m6-features--mt_features) | IC evaluator |
| R4.12 | Tier B stage 1: **SemIf option-logit readout** (Qwen3.5-4B) as the relevance gate + first flags; question registry v1; scores to NATS KV; determinism controls | [10 §4.3](../10-memory-rag-and-models.md#43-design), [03 M21](../03-build-spec.md#m21-decision-one--model-serving--mt_models) | Precision sample |
| R4.13 | D08 Intel: feed, document detail, events (map ≥ md), calendar with blackout markers, sentiment, sources with provenance flags; **Telegram shown as postures only** | [D08](../ui/dashboards/D08-intel.md) | Playwright |
| R4.14 | Morning brief on Telegram (news, sentiment movers, events mapped to assets, calendar + blackouts, data/cost health) | [04 Phase 4](../04-plan-of-action.md#phase-4--news-social-events--calendars-weeks-1619) | Daily brief |
| R4.N1 | Scraped text marked untrusted; LLMs never see secrets; RSS-Bridge has no DB route | [07 §5](../07-security-notes.md#5-network--host), [02 §9.1](../02-v1-architecture.md#91-security) | Network test |

## 4. ToDo sets

### A. Your actions (`USER`)
- [ ] **T4.01** `USER` List the Telegram channels you want monitored (joined from your dedicated account, slowly). → R4.02 · [07 §10](../07-security-notes.md#10-social--scraping-accounts)
- [ ] **T4.02** `USER` Follow the Discord announcement channels into `#mt-inbox`/category channels (≈10–15 follows per receiving channel). → R4.04
- [ ] **T4.03** `USER` Give watch keywords/cashtags and the RSS feeds/sites you trust. → R4.01, R4.05
- [ ] **T4.04** `USER` Label ~200 sampled documents relevant/irrelevant to calibrate the SemIf gate threshold. → R4.12
- [ ] **T4.05** `USER` Confirm whether Reddit access was granted (if yes it joins as optional). → [06 §2](../06-aggregators-and-market-providers.md#2-final-m2-social--news-ingestion-stack)

### B. Build (`BUILD`, code)
- [ ] **T4.20** `BUILD` `mt_data.text`: RSS/trafilatura/crawl4ai, RSS-Bridge client, GDELT, EDGAR, central banks, Finnhub, CryptoPanic. → R4.01
- [ ] **T4.21** `BUILD` Telegram ingest: Telethon session, join queue (`FLOOD_WAIT`), regex extractors, posture calculators; rows tagged `model_input_ok = false`. → R4.02, R4.03
- [ ] **T4.22** `BUILD` Discord bot (discord.py), Bluesky Jetstream, Mastodon, Farcaster clients. → R4.04, R4.05
- [ ] **T4.23** `BUILD` `nlp` service: provenance gate, dedupe, relevance gate, entity linking, FinBERT, TEI embeddings. → R4.06
- [ ] **T4.24** `BUILD` `mt_memory` RAG: chunkers, hybrid retrieval, RRF, rerank, `as_of`, caches. → R4.07
- [ ] **T4.25** `BUILD` `mt_data.events` + exposure map + event score; Polymarket/Kalshi read-only clients. → R4.08, R4.09
- [ ] **T4.26** `BUILD` `mt_data.calendar` + blackout query API consumed by M11. → R4.10
- [ ] **T4.27** `BUILD` Feature pipelines for sentiment/regime per market type, positioning, nowcasts, Fed path, VIX regime, forecasts. → R4.11
- [ ] **T4.28** `BUILD` `decision-svc` stage 1: question registry, SemIf readout, KV publishing, determinism logging. → R4.12
- [ ] **T4.29** `BUILD` D08 Intel + tier B chips on D01/D02; morning brief job. → R4.13, R4.14

### C. Ops & config (`OPS`)
- [ ] **T4.40** `OPS` RSS-Bridge container (whitelist, auth, scrapers network only). → R4.01, R4.N1
- [ ] **T4.41** `OPS` Model serving for Qwen3.5-4B (vLLM or llama-server; Vulkan on AMD); pinned revisions. → R4.12
- [ ] **T4.42** `OPS` Telethon session file encrypted; Discord bot token in secrets. → R4.02, R4.04

### D. Verify & test (`VERIFY`)
- [ ] **T4.60** `VERIFY` **Telegram-text gate test:** a Telegram row can't reach FinBERT, tier B, RAG, agents or a training set. → R4.03
- [ ] **T4.61** `VERIFY` RAG retrieval benchmark + `as_of` leakage test (future documents never returned). → R4.07
- [ ] **T4.62** `VERIFY` Blackout test: a scalper pauses around a seeded NFP event. → R4.10
- [ ] **T4.63** `VERIFY` SemIf gate precision/recall on your labels; flip rate (determinism). → R4.12
- [ ] **T4.64** `VERIFY` Feature IC report for the new features. → R4.11

### E. Run / soak (`RUN`)
- [ ] **T4.80** `RUN` Two weeks of morning briefs; tune sources by relevance hit-rate. → R4.14

## 5. Deliverables

Text/social/event/calendar ingestion · Telegram postures · RAG · sentiment/regime features · SemIf tier B · blackouts in M11 · D08 · morning brief.

## 6. Exit criteria (demo)

1. A morning Telegram brief arrives with sourced items, events mapped to assets and today's blackouts.
2. A calendar blackout pauses an affected paper strategy.
3. The Telegram-text gate test passes.

## 7. Risks & open questions

| Risk | Mitigation |
|---|---|
| Source volume overwhelms the relevance gate | Per-source caps; mute in D08; relevance hit-rate tracking |
| CPU-only SemIf is slow | Restrict to the relevance gate until the GPU arrives |
| Free-API terms change (Finnhub ML clause, CryptoPanic) | Read terms before enabling; provenance flags per source |
