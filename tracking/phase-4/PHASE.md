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
updated: 2026-10-22
---

# Phase 4 · News, social, events & calendars

## Summary

Free news, social, event and calendar intelligence flows into point-in-time features, document RAG and first-stage decision models (SemIf tier B stage 1), and calendar blackouts reach the risk manager (M11). **Telegram contributes postures only** (02 F3b: regex extractor → `text.telegram_posture` / `posture.telegram.*` → M4/M11 rules; D08 and the brief show the numbers). No Telegram text reaches any model, RAG index or training set. Deliverables: text/social/event/calendar ingestion, Telegram postures, document RAG, sentiment/regime features, SemIf tier B (prefix caching off on the decision path; stage-1 gate p95 ≤ 300 ms GPU / ≤ 3 s CPU, never on the order path), blackouts in M11 (16 §2.8 defaults), a minimal labelling tool, the regulatory & venue watch (`REG_CHANGE` tasks), D08 Intel, live D02 positioning/nowcast widgets and the morning brief (contents canonical in mobile-and-telegram §3).

The work is organised as: your inputs (channel lists + Telethon login, follows, keywords, keys/licences, labels) → ops (secrets, RSS-Bridge sidecar, containers/NATS accounts, SemIf serving) → the `mt_data.text` framework and **one connector task per source family, built on recorded fixtures** → the `nlp` chain (provenance gate → dedupe → relevance gate → linking → FinBERT → TEI → store) → decision-svc (question registry, SemIf readout) → RAG → events/exposure → calendars/blackouts → features → API/UI/brief → regulatory & venue watch → verification, **late live checks with your keys/accounts** (P4-T066–T068), a 2-week brief run and the exit demo.

## Entry criteria

With `phase_gating: "dependencies"` these are enforced per task through explicit cross-phase `depends_on` entries (see *Cross-phase prerequisites*), not as a phase gate.

- [ ] M11 event-blackout hook (P2-T017), risk policy (P2-T010), C3 change control (P2-T019), bot model (P2-T036), feature framework (P2-T120) and IC evaluator (P2-T123)
- [ ] Telegram dedicated account + `api_id`/`api_hash` (P0-T002) and Discord feeds server + bot (P0-T008); needed only by your USER steps and the live check P4-T068
- [ ] GPU decision made (P0-T005) or CPU fallback for SemIf accepted
- [ ] Finnhub, CryptoPanic and Myfxbook free keys (P0-T010); needed only by the live check P4-T067
- [ ] TEI `tei-embed` + `tei-rerank` (P0-T043); all 13 schemas incl. `rag`/`models` (P0-T024); provenance columns (P0-T025); networks (P0-T021); sops → tmpfs (P0-T022)
- [ ] P1 connector framework (P1-T005), quota tracker (P1-T006), provenance tagging (P1-T007), DQ/`audit.dq_event` (P1-T030), EDGAR client (P1-T028), FRED/COT/EIA/USDA flows (P1-T024, P1-T026), symbol master (P1-T009), D02 (P1-T049, P1-T050), open provider checks (P1-T056)

## Exit criteria

- [ ] 1. A morning Telegram brief arrives with sourced items, events mapped to assets and today's blackouts (P4-T047, P4-T060, P4-T061)
- [ ] 2. A calendar blackout pauses an affected paper strategy (an `event_sensitive` paper bot, 16 §2.8) (P4-T052, P4-T061)
- [ ] 3. The Telegram-text gate test passes (P4-T050, P4-T068, P4-T061)
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
| Build: decision-svc tier B stage 1 + labelling (R4.12, R4.16, R4.N2) | P4-T028, P4-T029, P4-T062, P4-T048 |
| Build: document RAG (R4.07) | P4-T031, P4-T032 |
| Build: events, exposure, prediction markets (R4.08–R4.09) | P4-T033, P4-T034, P4-T035, P4-T036 |
| Build: calendars + blackouts (R4.10) | P4-T037, P4-T038 |
| Build: positioning ingestion + features (R4.11) | P4-T039, P4-T040, P4-T041, P4-T042, P4-T065 |
| Build: API, D08, D01/D02 chips, morning brief (R4.13–R4.14) | P4-T043, P4-T044, P4-T045, P4-T046, P4-T047 |
| Build: regulatory & venue watch (R4.15) | P4-T063, P4-T064 |
| Verify (fixtures, CI) | P4-T050, P4-T051, P4-T052, P4-T053, P4-T054, P4-T055, P4-T056, P4-T057, P4-T058, P4-T059, P4-T069 |
| Verify (live, keys last) | P4-T066, P4-T067, P4-T068 |
| Run + exit | P4-T060, P4-T061 |

## Critical path

P4-T010 → P4-T025 → P4-T026 → P4-T027 → P4-T030 (with P4-T028 → P4-T029 and P4-T009) → P4-T043 → P4-T044 → P4-T062 → P4-T049 (you label) → P4-T053 (calibrate on your labels with the P4-T048 script, built in parallel, then measure) → P4-T060; in parallel P4-T037 → P4-T038 → P4-T047, and the live checks P4-T067 (after your keys, P4-T005/P0-T010) and P4-T068 (after your channel list, login and follows, P4-T001/T002) → P4-T060 (14-day run) → P4-T061. Connector builds no longer wait for your inputs (fixtures first), so up to six agents can work the source families, the nlp/decision chain, RAG, events/calendars, features and the UI in parallel. The 14-day brief run (P4-T060) is the longest elapsed item: get your labels (P4-T049 → P4-T053) and the live checks done early so it can start as soon as P4-T047 lands.

## Traceability

### Requirements → tasks

| Requirement | Summary | Tasks |
|---|---|---|
| R4.01 | News: RSS + trafilatura/crawl4ai; RSS-Bridge sidecar; GDELT; EDGAR; central banks; Finnhub; CryptoPanic | P4-T003, P4-T005, P4-T007, P4-T010, P4-T011, P4-T012, P4-T013, P4-T014, P4-T015, P4-T016, P4-T017, P4-T056, P4-T057, P4-T060, P4-T067 |
| R4.02 | Telegram postures only → `text.telegram_posture` / `posture.telegram.*`, consumers M4/M11 rules; FLOOD_WAIT queue; ≤ 500 channels | P4-T001, P4-T006, P4-T018, P4-T019, P4-T050, P4-T058, P4-T068 |
| R4.03 | No Telegram text reaches any model, RAG index or training set | P4-T010, P4-T019, P4-T025, P4-T050, P4-T061, P4-T068 |
| R4.04 | Discord bot on your server ingesting followed announcement channels | P4-T002, P4-T006, P4-T020, P4-T057, P4-T068 |
| R4.05 | Bluesky, Mastodon, Farcaster; StockTwits if T1.60 passed; YouTube if T4.65 passes | P4-T003, P4-T021, P4-T022, P4-T023, P4-T024, P4-T056, P4-T057, P4-T066 |
| R4.06 | Text chain (non-Telegram, provenance first): dedupe → gate → linking → FinBERT → TEI → `text.document` | P4-T008, P4-T010, P4-T025, P4-T026, P4-T027, P4-T030, P4-T057, P4-T058 |
| R4.07 | Document RAG with `as_of` filter | P4-T031, P4-T032, P4-T051 |
| R4.08 | Global events, exposure map, event score | P4-T005, P4-T013, P4-T033, P4-T034, P4-T035, P4-T067 |
| R4.09 | Polymarket/Kalshi read-only, lawful reach only | P4-T036, P4-T056, P4-T065 |
| R4.10 | Calendars + "event within N minutes" → M11 blackouts (16 §2.8 defaults) | P4-T037, P4-T038, P4-T045, P4-T052, P4-T061 |
| R4.11 | Features per market type; positioning + nowcasts ingested (D02 widgets go live); Fed path; VIX; PM; forecasts | P4-T036, P4-T039, P4-T040, P4-T041, P4-T042, P4-T054, P4-T065, P4-T067 |
| R4.12 | SemIf stage 1 + registry + KV + determinism (prefix caching off; shared-prefix offline only) | P4-T009, P4-T028, P4-T029, P4-T030, P4-T046, P4-T048, P4-T049, P4-T053, P4-T058, P4-T062, P4-T069 |
| R4.13 | D08 Intel; Telegram as postures only | P4-T043, P4-T044, P4-T045, P4-T046, P4-T057, P4-T058, P4-T059 |
| R4.14 | Morning brief per mobile-and-telegram §3 | P4-T047, P4-T060, P4-T061 |
| R4.15 | Regulatory & jurisdiction watch → `REG_CHANGE`; venue status → venue health; never auto-applied | P4-T063, P4-T064 |
| R4.16 | Minimal labelling tool (D08 Label mode) + `models.label.add` | P4-T049, P4-T062 |
| R4.N1 | Scraped text untrusted; LLMs never see secrets; RSS-Bridge has no DB route | P4-T007, P4-T008, P4-T012, P4-T055 |
| R4.N2 | Stage-1 gate p95 ≤ 300 ms GPU / ≤ 3 s CPU; queued, never on the order path | P4-T029, P4-T030, P4-T069 |

### Roadmap ToDos → tasks

| ToDo | Type | Summary | Tasks |
|---|---|---|---|
| T4.01 | USER | Telegram channel list (+ your Telethon login) | P4-T001 |
| T4.02 | USER | Discord follows | P4-T002 |
| T4.03 | USER | Watch keywords/cashtags and trusted feeds | P4-T003 |
| T4.04 | USER | Label ~200 documents with the labelling tool | P4-T049 |
| T4.05 | USER | Reddit access yes/no (optional) | P4-T004 |
| T4.06 | USER | FIRMS / ACLED keys, OpenSanctions licence | P4-T005 |
| T4.20 | BUILD | `mt_data.text` news sources | P4-T010, P4-T011, P4-T012, P4-T013, P4-T014, P4-T015, P4-T016, P4-T017 |
| T4.21 | BUILD | Telegram ingest → postures | P4-T018, P4-T019, P4-T068 |
| T4.22 | BUILD | Discord, Bluesky, Mastodon, Farcaster | P4-T020, P4-T021, P4-T022, P4-T023, P4-T024, P4-T068 |
| T4.23 | BUILD | `nlp` service | P4-T025, P4-T026, P4-T027, P4-T030 |
| T4.24 | BUILD | `mt_memory` RAG | P4-T031, P4-T032 |
| T4.25 | BUILD | Events + exposure + event score; Polymarket/Kalshi | P4-T013, P4-T033, P4-T034, P4-T035, P4-T036 |
| T4.26 | BUILD | Calendar + blackout API (±15 min, `event_sensitive`) | P4-T037, P4-T038 |
| T4.27 | BUILD | Feature pipelines | P4-T040, P4-T041, P4-T042 |
| T4.28 | BUILD | decision-svc stage 1 (determinism, queue off the order path) | P4-T028, P4-T029, P4-T030, P4-T048 |
| T4.29 | BUILD | D08 + tier-B chips + morning brief | P4-T043, P4-T044, P4-T045, P4-T046, P4-T047 |
| T4.30 | BUILD | Regulatory & venue watch, `REG_CHANGE` | P4-T063, P4-T064 |
| T4.31 | BUILD | Minimal labelling tool + `models.label.add` | P4-T062 |
| T4.32 | BUILD | Positioning and nowcast ingestion; D02 widgets live | P4-T036, P4-T039, P4-T065 |
| T4.40 | OPS | RSS-Bridge container | P4-T007, P4-T008 |
| T4.41 | OPS | Qwen3.5-4B serving | P4-T009 |
| T4.42 | OPS | Telethon session encrypted; Discord token in secrets | P4-T006 |
| T4.60 | VERIFY | Telegram-text gate test | P4-T050 |
| T4.61 | VERIFY | RAG benchmark + `as_of` leakage | P4-T051 |
| T4.62 | VERIFY | Blackout test (seeded NFP) | P4-T052 |
| T4.63 | VERIFY | SemIf precision/recall + flip rate | P4-T053 |
| T4.64 | VERIFY | Feature IC report | P4-T054 |
| T4.65 | VERIFY | YouTube check | P4-T066 |
| T4.66 | VERIFY | Live check of keyed sources | P4-T067 |
| T4.67 | VERIFY | Stage-1 latency benchmark | P4-T069 |
| T4.80 | RUN | Two weeks of morning briefs | P4-T060 |

P4-T068 (live Telegram/Discord check) also completes T4.21/T4.22 on your real accounts; P4-T055–T059 and P4-T061 verify requirements without their own ToDo.

### Gaps / bugs filed

| ID | Severity | Summary | Status |
|---|---|---|---|
| P4-B001 | S2 | 02 F3 lists Telegram as an input to the text → decision-model chain | done (17 §A; 02 F3/F3b) |
| P4-B002 | S3 | D08 Feed tab lists Telegram as a DocumentCard source | done (17 §D; D08) |
| P4-B003 | S3 | No NATS subject, table or consumer rule for Telegram postures | done (17 §D; 02 §4–§6, 03 M2/M6) |
| P4-B004 | S3 | Calendar blackout defaults unspecified | done (17 §C → 16 §2.8; 03 M5, 14 §5) |
| P4-B005 | S3 | R4.05 gates YouTube on a P1 check that P1 doesn't run | done (17 §D; roadmap T4.65, 06 §2) |
| P4-B006 | S3 | `rag` and `models` schemas missing from the P0 schema list | done (17 §B; R0.03, 02 §5.1) |
| P4-B007 | S3 | No P4 labelling tool; `models.label.add` missing | done (17 §D; 02 §7.2, D08, R4.16) |
| P4-B008 | S3 | FIRMS/ACLED keys and OpenSanctions licence not in any USER ToDo | done (17 §D; T4.06, 03 M3) |
| P4-B009 | S4 | Reddit timeline makes T4.05 likely moot | done (17 §D; T4.05, 06 §0/§2) |
| P4-B010 | S2 | SemIf shared-prefix vs prefix caching off; no stage-1 latency target | done (17 §A; 10 §4.3, 02 §9.2) |
| P4-B011 | S4 | Morning brief contents differ between docs | done (17 §D; mobile-and-telegram §3) |

## Cross-phase prerequisites

These are explicit `depends_on` entries on the tasks that need them (they replace the old `opens_after` gate under `phase_gating: "dependencies"`).

| Phase | Tasks relied on | Used by |
|---|---|---|
| P0 | P0-T001 (Reddit application), P0-T002 (Telegram account), P0-T005 (GPU decision), P0-T008 (Discord server/bot), P0-T010 (free keys), P0-T020 (Compose), P0-T021 (networks), P0-T022 (sops → tmpfs), P0-T024 (13 schemas), P0-T025 (provenance columns), P0-T027 (`pit`), P0-T029/T030 (WORM triggers, hash chain), P0-T034 (command bus), P0-T036 (WS hub), P0-T043 (TEI embed/rerank), P0-T049 (component library) | P4-T001, T002, T004, T006–T010, T027, T028, T031, T032, T043, T044, T067 |
| P1 | P1-T004 (streams/KV), P1-T005 (connector framework), P1-T006 (quota tracker), P1-T007 (provenance tagging), P1-T009 (symbol master), P1-T013 (bars), P1-T024 (FRED/macro), P1-T026 (EIA/USDA/COT/BH), P1-T028 (EDGAR), P1-T030 (DQ, `audit.dq_event`), P1-T043 (venue health), P1-T045 (alert fan-out), P1-T046 (`/data/feeds`), P1-T049/T050 (D02), P1-T056 (open checks T1.60) | P4-T008, T010, T014, T024, T025, T026, T037, T039, T042, T046, T063, T064, T065 |
| P2 | P2-T008 (scalping template), P2-T010 (risk policy), P2-T017 (RiskGate blackout check), P2-T019 (C3 change control), P2-T021 (paper engine), P2-T035 (Telegram commands), P2-T036 (bots, `event_sensitive`), P2-T042 (D06), P2-T046 (MLflow), P2-T120 (feature registry), P2-T123 (IC evaluator), P2-T142 (D01) | P4-T009, T035, T036, T038, T040–T042, T046–T048, T052, T054 |
| P3 | P3-T031 (residency timeline), P3-T038 (minimal `curation.task`) | P4-T063 |
| P5 (downstream) | R5.10 consumes Telegram postures (M4 rules) + Discord inbox; R5.21 reuses the Discord bot; the brief's airdrop section | P4-T019, P4-T020, P4-T047 |
| P6 (downstream) | P4 text + RAG + SemIf running ≥ 4 weeks; R6.13 reuses the provenance guard; D10 labelling queue reuses `models.label` / `models.label.add` | P4-T025, P4-T029, P4-T032, P4-T062 |

## Planning notes & risks

- **Telegram is the highest-risk area.** Enforced in five layers: a DB CHECK constraint (P4-T010), `nlp` never subscribing to Telegram subjects plus a guard at every model boundary and a CI lint (P4-T025), a consumer allow-list for `posture.telegram.>` limited to M4/M11 rules and the display paths (P4-T019), the canary gate test on fixtures (P4-T050) and again on the live stack (P4-T068). Postures are never M6 features, tier A/B, agents, RAG or MCP inputs (17 §D).
- **Scrape side has no DB route** (02 §3.1): `ingest-text`/`ingest-events` publish to `raw.>` and `posture.telegram.>` only; a core `intel-writer` (P4-T008) persists geo events and postures; connector state (join queue, cursors) lives in local state files.
- **Build first, keys last** (17 §E): every connector is built and tested on recorded fixtures without keys; live checks are P4-T066 (YouTube), P4-T067 (FIRMS, ACLED, OpenSanctions, Finnhub, CryptoPanic, Myfxbook/IG/OANDA) and P4-T068 (Telegram, Discord), each depending on the USER task that provides the key, licence or account.
- **Determinism** (17 §A P4-B010): prefix caching off and fixed batch on the decision path; shared-prefix mode only offline/backfill, tagged non-deterministic and refused by decisions, tier A and backtests (P4-T009, P4-T029). Stage-1 gate latency p95 ≤ 300 ms GPU / ≤ 3 s CPU, queued, never on the order path (P4-T069).
- **Tier-B thresholds** come from 16 §2.10 (auto-decide ≥ 0.75 precision, veto ≥ 0.90, ECE ≤ 0.05, flip ≤ 0.1%, ≥ 14 days shadow): stage-1 output stays advisory and badged 'uncalibrated' until P4-T048/T053 show them.
- **Blackouts** follow 16 §2.8: ±15 min around high-importance events for `event_sensitive` bots, exits continue, configurable per bot and event type; loosening is C3 (P4-T038, P4-T052).
- **Volume vs relevance gate:** cheap pre-filter, per-source caps, hit-rate tracking and the 2-week tuning run (P4-T030, P4-T060); stress in P4-T058. Intel-pipeline numbers not in 16 (poll intervals, per-source caps, join pacing, posture windows) are configurable defaults in `config/intel/*.yaml`.
- **Free-API terms** (Finnhub ML clause, CryptoPanic attribution, ACLED, OpenSanctions, ForexFactory ToS-grey): P4-T005 records your decisions as provenance flags; connectors start with conservative flags; P4-T056 reviews.
- **Regulatory & venue watch** (R4.15): fetch + diff → `REG_CHANGE` review tasks in the P3 `curation.task`; rules and venue status are never auto-applied or loosened (P4-T063, P4-T064).
- **Polymarket** stays disabled while residency is AU (never via VPN/proxy); Kalshi read-only (P4-T036).
- **Reddit** is optional (17 §D P4-B009; P4-T004). X stays deferred.
- **Schemas** are all created in P0 (17 §B); P4 adds tables only.
- Sizes: no XL items; the largest (L) are the text framework, SemIf readout, RAG retrieval, calendar sources, sentiment/regime and D08 feed.
- The 14-day brief run (P4-T060) now also waits for the live checks; if they slip, the exit demo slips rather than shortening the run.
