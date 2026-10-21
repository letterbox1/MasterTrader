---
phase: 4
title: News, social, events & calendars
roadmap: docs/roadmap/phase-4-intel.md
status: not_started
opens_after: [2]
force_open: false
started: ""
completed: ""
doc_sync_status: n/a
updated: 2026-10-21
---

# Phase 4 · News, social, events & calendars

## Summary

Free news, social, event and calendar intelligence flows into point-in-time features, document RAG and first-stage decision models (SemIf tier B stage 1), and calendar blackouts reach the risk manager (M11). **Telegram contributes postures only** (regex-extracted addresses/tickers and counts); no Telegram text reaches any model, RAG index or training set. Deliverables: text/social/event/calendar ingestion, Telegram postures, document RAG, sentiment/regime features, SemIf tier B, blackouts in M11, D08 Intel, and the morning brief.

The work is organised as: your inputs (channel lists, follows, keywords, keys, labels) → ops (secrets, RSS-Bridge sidecar, containers/NATS accounts, Qwen3.5-4B serving) → the `mt_data.text` framework and **one connector task per source family** → the `nlp` chain (provenance gate → dedupe → relevance gate → linking → FinBERT → TEI → store) → decision-svc (question registry, SemIf readout) → RAG → events/exposure → calendars/blackouts → features → API/UI/brief → verification, a 2-week brief run and the exit demo.

## Entry criteria

- [ ] Phase 2 exit met; the M11 event-blackout hook exists (P2 R2.16) and the feature framework + IC evaluator exist (P2 R2.46)
- [ ] Telegram dedicated account + `api_id`/`api_hash` + bot ready (P0 T0.06)
- [ ] Discord feeds server + bot app with Message Content intent ready (P0 T0.07)
- [ ] GPU decision made (P0 T0.01) or CPU fallback for SemIf accepted
- [ ] Finnhub and CryptoPanic free keys in secrets (P0 T0.10)
- [ ] TEI (bge-small-en-v1.5 + bge-reranker-v2-m3) and LiteLLM running (P0 R0.09); provenance columns in ingest tables (P0 R0.05); scrape network isolated (P0 R0.N3)
- [ ] P1 quota tracker (R1.08), provenance tagging + retention (R1.09), D07 feed health (R1.15), EDGAR client (R1.07) and FRED/COT/EIA/USDA flows (R1.06) in place; P1 open checks run (T1.60)

## Exit criteria

- [ ] 1. A morning Telegram brief arrives with sourced items, events mapped to assets and today's blackouts (P4-T047, P4-T060, P4-T061)
- [ ] 2. A calendar blackout pauses an affected paper strategy (P4-T052, P4-T061)
- [ ] 3. The Telegram-text gate test passes (P4-T050, P4-T061)
- [ ] All Phase 4 tasks are done or cancelled
- [ ] No open S1/S2 bugs in Phase 4

## Workstreams

| Workstream | Tasks |
|---|---|
| Your actions (USER) | P4-T001, P4-T002, P4-T003, P4-T004, P4-T005, P4-T049 |
| Ops & config | P4-T006, P4-T007, P4-T008, P4-T009 |
| Build: text framework & news sources (R4.01) | P4-T010, P4-T011, P4-T012, P4-T013, P4-T014, P4-T015, P4-T016, P4-T017 |
| Build: Telegram postures (R4.02–R4.03) | P4-T018, P4-T019 |
| Build: other social (R4.04–R4.05) | P4-T020, P4-T021, P4-T022, P4-T023, P4-T024 |
| Build: nlp chain + provenance gate (R4.06) | P4-T025, P4-T026, P4-T027, P4-T030 |
| Build: decision-svc tier B stage 1 (R4.12) | P4-T028, P4-T029, P4-T048 |
| Build: document RAG (R4.07) | P4-T031, P4-T032 |
| Build: events, exposure, prediction markets (R4.08–R4.09) | P4-T033, P4-T034, P4-T035, P4-T036 |
| Build: calendars + blackouts (R4.10) | P4-T037, P4-T038 |
| Build: features (R4.11) | P4-T039, P4-T040, P4-T041, P4-T042 |
| Build: API, D08, D01/D02 chips, morning brief (R4.13–R4.14) | P4-T043, P4-T044, P4-T045, P4-T046, P4-T047 |
| Verify | P4-T050, P4-T051, P4-T052, P4-T053, P4-T054, P4-T055, P4-T056, P4-T057, P4-T058, P4-T059, P4-T061 |
| Run | P4-T060 |

## Critical path

P4-T010 → P4-T025 → P4-T026 → P4-T027 → (P4-T009 → P4-T028 → P4-T029) → P4-T030 → P4-T048 → P4-T049 (you label) → P4-T053; in parallel P4-T037 → P4-T038 → P4-T043 → P4-T047 → P4-T060 (14-day run) → P4-T061. The 14-day brief run (P4-T060) is the longest elapsed item: start it as soon as P4-T047 and P4-T030 land. The Telegram branch (P4-T006 → P4-T018 → P4-T019 → P4-T050) must finish before the exit demo.

## Traceability

### Requirements → tasks

| Requirement | Summary | Tasks |
|---|---|---|
| R4.01 | News: RSS + trafilatura/crawl4ai; RSS-Bridge sidecar (whitelisted bri… | P4-T003, P4-T005, P4-T007, P4-T010, P4-T011, P4-T012, P4-T013, P4-T014, P4-T015, P4-T016, P4-T017, P4-T056, P4-T057, P4-T060 |
| R4.02 | Telegram postures only: Telethon + Bot API + RSS-Bridge fallback; reg… | P4-T001, P4-T006, P4-T018, P4-T019, P4-T050, P4-T058 |
| R4.03 | No Telegram text reaches any model, RAG index or training set (rows `… | P4-T010, P4-T019, P4-T025, P4-T050, P4-T061 |
| R4.04 | Discord bot on your server ingesting followed announcement channels (… | P4-T002, P4-T006, P4-T020, P4-T057 |
| R4.05 | Bluesky Jetstream (cashtags/keywords), Mastodon, Farcaster (Hubble);… | P4-T003, P4-T021, P4-T022, P4-T023, P4-T024, P4-T056, P4-T057 |
| R4.06 | Text chain (non-Telegram, provenance checked first): dedupe → relevan… | P4-T008, P4-T010, P4-T025, P4-T026, P4-T027, P4-T030, P4-T057, P4-T058 |
| R4.07 | Document RAG (`rag` schema): pgvector HNSW (halfvec) + tsvector + pg_… | P4-T031, P4-T032, P4-T051 |
| R4.08 | Global events: USGS, GDACS, NOAA/NHC, FIRMS, ReliefWeb, UCDP, GDELT,… | P4-T005, P4-T013, P4-T033, P4-T034, P4-T035 |
| R4.09 | Polymarket/Kalshi read-only probabilities, only where lawfully reacha… | P4-T036, P4-T056 |
| R4.10 | Calendars: FRED/ALFRED releases, ForexFactory weekly JSON, central-ba… | P4-T037, P4-T038, P4-T045, P4-T052, P4-T061 |
| R4.11 | Features: sentiment + regime per market type (crypto, FX, metals, ene… | P4-T036, P4-T039, P4-T040, P4-T041, P4-T042, P4-T054 |
| R4.12 | Tier B stage 1: SemIf option-logit readout (Qwen3.5-4B) as the releva… | P4-T009, P4-T028, P4-T029, P4-T030, P4-T046, P4-T048, P4-T049, P4-T053, P4-T058 |
| R4.13 | D08 Intel: feed, document detail, events (map ≥ md), calendar with bl… | P4-T043, P4-T044, P4-T045, P4-T046, P4-T057, P4-T058, P4-T059 |
| R4.14 | Morning brief on Telegram (news, sentiment movers, events mapped to a… | P4-T047, P4-T060, P4-T061 |
| R4.N1 | Scraped text marked untrusted; LLMs never see secrets; RSS-Bridge has… | P4-T007, P4-T008, P4-T012, P4-T055 |

### Roadmap ToDos → tasks

| ToDo | Type | Summary | Tasks |
|---|---|---|---|
| T4.01 | USER | List the Telegram channels you want monitored (joined from… | P4-T001 |
| T4.02 | USER | Follow the Discord announcement channels into `#mt-inbox`/c… | P4-T002 |
| T4.03 | USER | Give watch keywords/cashtags and the RSS feeds/sites you tr… | P4-T003 |
| T4.04 | USER | Label ~200 sampled documents relevant/irrelevant to calibra… | P4-T049 |
| T4.05 | USER | Confirm whether Reddit access was granted (if yes it joins… | P4-T004 |
| T4.20 | BUILD | `mt_data.text`: RSS/trafilatura/crawl4ai, RSS-Bridge client… | P4-T010, P4-T011, P4-T012, P4-T013, P4-T014, P4-T015, P4-T016, P4-T017 |
| T4.21 | BUILD | Telegram ingest: Telethon session, join queue (`FLOOD_WAIT`… | P4-T018, P4-T019 |
| T4.22 | BUILD | Discord bot (discord.py), Bluesky Jetstream, Mastodon, Farc… | P4-T020, P4-T021, P4-T022, P4-T023, P4-T024 |
| T4.23 | BUILD | `nlp` service: provenance gate, dedupe, relevance gate, ent… | P4-T025, P4-T026, P4-T027, P4-T030 |
| T4.24 | BUILD | `mt_memory` RAG: chunkers, hybrid retrieval, RRF, rerank, `… | P4-T031, P4-T032 |
| T4.25 | BUILD | `mt_data.events` + exposure map + event score; Polymarket/K… | P4-T013, P4-T033, P4-T034, P4-T035, P4-T036 |
| T4.26 | BUILD | `mt_data.calendar` + blackout query API consumed by M11. | P4-T037, P4-T038 |
| T4.27 | BUILD | Feature pipelines for sentiment/regime per market type, pos… | P4-T039, P4-T040, P4-T041, P4-T042 |
| T4.28 | BUILD | `decision-svc` stage 1: question registry, SemIf readout, K… | P4-T028, P4-T029, P4-T030, P4-T048 |
| T4.29 | BUILD | D08 Intel + tier B chips on D01/D02; morning brief job. | P4-T043, P4-T044, P4-T045, P4-T046, P4-T047 |
| T4.40 | OPS | RSS-Bridge container (whitelist, auth, scrapers network onl… | P4-T007, P4-T008 |
| T4.41 | OPS | Model serving for Qwen3.5-4B (vLLM or llama-server; Vulkan… | P4-T009 |
| T4.42 | OPS | Telethon session file encrypted; Discord bot token in secre… | P4-T006 |
| T4.60 | VERIFY | Telegram-text gate test: a Telegram row can't reach FinBERT… | P4-T050 |
| T4.61 | VERIFY | RAG retrieval benchmark + `as_of` leakage test (future docu… | P4-T051 |
| T4.62 | VERIFY | Blackout test: a scalper pauses around a seeded NFP event. | P4-T052 |
| T4.63 | VERIFY | SemIf gate precision/recall on your labels; flip rate (dete… | P4-T053 |
| T4.64 | VERIFY | Feature IC report for the new features. | P4-T054 |
| T4.80 | RUN | Two weeks of morning briefs; tune sources by relevance hit-… | P4-T060 |

### Gaps / bugs filed

| ID | Severity | Summary |
|---|---|---|
| P4-B001 | S2 | 02 F3 lists Telegram as an input to the text → decision-model chain |
| P4-B002 | S3 | D08 Feed tab lists Telegram as a DocumentCard source |
| P4-B003 | S3 | No NATS subject, table or consumer rule for Telegram postures |
| P4-B004 | S3 | Calendar blackout defaults (window, scope, action) are unspecified |
| P4-B005 | S3 | R4.05 gates YouTube on a P1 check that P1 doesn't run |
| P4-B006 | S3 | `rag` and `models` schemas missing from the P0 schema list |
| P4-B007 | S3 | T4.04 labelling has no tool in P4; `models.label.add` missing from the command catalogue |
| P4-B008 | S3 | FIRMS and ACLED keys (and OpenSanctions licence) not in any USER ToDo |
| P4-B009 | S4 | Reddit timeline makes T4.05 likely moot by Phase 4; no connector ToDo if 'yes' |
| P4-B010 | S2 | SemIf 'shared-prefix mode' conflicts with 'prefix caching off'; no stage-1 latency target |
| P4-B011 | S4 | Morning brief contents differ between 04, the roadmap and mobile-and-telegram |

## Cross-phase prerequisites

| Phase | Roadmap IDs relied on | Used by |
|---|---|---|
| P0 | T0.01 (GPU decision), T0.06 (Telegram account/bot), T0.07 (Discord server/bot), T0.10 (Finnhub/CryptoPanic keys), R0.03/T0.22 (`text` schema, `pit`), R0.05 (provenance columns), R0.07/T0.23 (WORM for `audit.*`), R0.08/T0.24 (`mt_api`, confirmation levels, WS), R0.09/T0.41/T0.45 (TEI, LiteLLM), R0.N1/T0.43 (sops/age → tmpfs), R0.N3/T0.42 (scrape network), R0.11 (component library) | P4-T006–T010, T025, T027–T029, T043–T046 |
| P1 | R1.05 (symbol master, `exchange_calendars`), R1.06/T1.24 (FRED/ALFRED, COT, EIA, USDA, Baker Hughes, `sdmx1`), R1.07 (EDGAR client, ≤ 10 req/s), R1.08/T1.25 (quota tracker), R1.09/T1.26 (provenance + retention), R1.10 (`feed_status`/DQ), R1.14/T1.31 (Telegram alerts bot), R1.15 (D07, D02), T1.60 (StockTwits, OANDA books, IG sentiment checks), T1.01 (universe) | P4-T010, T014, T024, T026, T037, T039, T047 |
| P2 | R2.16 (event-blackout hook in M11), R2.11/T2.22 (risk policy model), R2.19 (C3 change control), R2.46/T2.29 (feature framework + IC evaluator), R2.44 (MLflow), R2.02/R2.30 (scalper template, paper engine), R2.50 (D01, D06), R2.52 (Telegram commands) | P4-T038, T040–T042, T046, T047, T052, T054 |
| P5 (downstream) | R5.10 consumes Telegram postures + Discord inbox; R5.21 reuses the Discord bot | P4-T019, P4-T020 |
| P6 (downstream) | Needs P4 text + RAG + SemIf running ≥ 4 weeks; R6.13/T6.62 reuse the provenance guard; D10 labelling queue reuses `models.label` | P4-T025, P4-T029, P4-T032, P4-T048 |

## Planning notes & risks

- **Telegram is the highest-risk area.** It's enforced in four layers: a DB CHECK constraint (P4-T010), `nlp` never subscribing to Telegram subjects plus a guard at every model boundary and a CI lint (P4-T025), a consumer allow-list for postures (P4-T019), and the canary-based gate test (P4-T050). Postures are **not** M6 features for tier A/B (12 §4 bans Telegram-derived model inputs; see P4-B003).
- **Volume vs relevance gate** (roadmap risk): a cheap keyword/entity pre-filter, per-source caps, hit-rate tracking and the 2-week tuning run (P4-T030, P4-T060); stress-tested in P4-T058.
- **CPU-only SemIf** (roadmap risk): P4-T029 runs relevance only in CPU mode; other questions come back when the GPU arrives. The determinism vs shared-prefix conflict is filed as P4-B010 (S2); P4 defaults to prefix caching **off**.
- **Stage-1 tier B is uncalibrated:** no `risk.event` vetoes until P4-T048/T053 set a calibrated high-precision threshold; UI shows an 'uncalibrated' badge (P4-T046).
- **Free-API terms** (Finnhub ML clause, CryptoPanic attribution, ACLED, OpenSanctions, ForexFactory ToS-grey): P4-T005 records decisions as provenance flags before enabling; P4-T056 reviews them.
- **Blackout defaults are a proposal** (15 min before/after high-importance events, block new entries for scalper/intraday tags) until P4-B004 is resolved; the rule is user-editable in D06 and loosening is C3.
- **Polymarket** stays disabled while residency is AU (ISP-blocked; never via VPN/proxy); Kalshi is read-only (P4-T036).
- **Reddit** (P4-T004) is most likely moot by P4's dates (P4-B009). X stays deferred.
- **Schema ownership:** P4 creates `rag` and `models` idempotently (P4-B006).
- Sizes: no XL items; the largest (L) are the text framework, SemIf readout, RAG retrieval, calendar sources, sentiment/regime and D08 feed.
- The 14-day brief run (P4-T060) fits inside the 4-week phase only if the brief and gate land by the end of week 2; otherwise the exit demo slips rather than shortening the run.
