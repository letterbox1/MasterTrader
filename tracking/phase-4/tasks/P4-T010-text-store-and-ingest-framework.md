---
id: P4-T010
kind: task
title: Build the mt_data.text store, source registry and ingest framework
phase: 4
type: BUILD
status: backlog
priority: critical
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T024, P0-T025, P0-T027, P1-T005, P1-T006, P1-T007, P1-T046]
requirements: [R4.01, R4.03, R4.06]
roadmap_todos: [T4.20]
modules: [M2]
dashboards: [D07, D08]
tools: [uv, git, docker]
mcp: []
env: []
services: [postgres, nats]
branch: p4/P4-T010-text-store-and-ingest-framework
pr: ""
doc_sync: [docs/03-build-spec.md, docs/02-v1-architecture.md, docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P4-T010 · Build the mt_data.text store, source registry and ingest framework

## Goal / expected outcome

`mt_data.text` has the shared pieces every connector uses: Alembic migrations (tables only; the `text` schema exists from P0) for `text.source`, `text.document`, `text.document_dup`, `text.telegram_mention`, `text.telegram_posture`; a source registry with per-source provenance defaults (from `source_terms.yaml`); a text `Connector` base built on the P1 connector framework (P1-T005) with quota tracking, polite fetch, retries and `feed_status` reporting to D07; and the normalised `RawTextItem` schema published on `raw.text.{source}`.

## Context & references

- Roadmap: [R4.01, R4.03, R4.06](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.20](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Spec: [03 M2](../../../docs/03-build-spec.md#m2-news--social--mt_datatext) · [03 §4 data model](../../../docs/03-build-spec.md#4-data-model-overview) · [02 §4 M2 row](../../../docs/02-v1-architecture.md#4-logical-components)
- Provenance: [12 §5](../../../docs/12-policy-and-compliance.md#5-data-provenance-tagging-one-mechanism-for-all-data-terms) (`source`, `licence`, `train_ok`, `model_input_ok`, `display_ok`, `retention_days`, `commercial_ok`)
- Cross-phase (`depends_on`): P0-T024 (schemas, all 13 created in P0 per 17 §B), P0-T025 (seven provenance columns), P0-T027 (`pit`), P1-T005 (connector framework), P1-T006 (quota tracker), P1-T007 (provenance tagging), P1-T046 (`/data/feeds`). P1-T008 (retention job) and P1-T030 (`feed_status`) are reused.
- Decision: [17 §D](../../../docs/17-decisions-register.md#d-other-decisions) (P4-B003): postures live in `text.telegram_posture`, subject `posture.telegram.*`, consumers M4/M11 rules only ([02 §4–§6](../../../docs/02-v1-architecture.md#4-logical-components)).

## Requirements

- `text.document`: `id uuidv7`, `source_id`, `url`, `canonical_url`, `content_hash`, `title`, `body` (nullable when `display_ok=false`/paywalled), `lang`, `published_at`, `published_approx bool`, `ingested_at` (our clock), `event_time`, `ingest_time`, `tickers text[]`, `entities jsonb`, `sentiment jsonb`, `relevance real`, `untrusted bool default true`, provenance columns. Rows are insert-only; revisions are new rows with `supersedes`.
- `text.source`: id, kind (rss/rss_bridge/gdelt/edgar/cb/finnhub/cryptopanic/telegram/discord/bluesky/mastodon/farcaster/stocktwits/youtube), config, status, muted, quota, provenance defaults, relevance hit-rate counters.
- `text.telegram_mention` (structured only: channel_id hash, message_id, ts, extracted `address`/`ticker`, chain; the posture calculator's input, never text) and `text.telegram_posture` (subject, window, mention_velocity, channel_count, new_channel_share, time_since_first_call) with **`model_input_ok=false`, `train_ok=false` enforced by a CHECK constraint**. Both are written only by the core-side `intel-writer` (P4-T008).
- Telegram sources: the CHECK constraint makes `model_input_ok=true` impossible for `source.kind='telegram'`.
- `Connector` base (extends P1-T005): async httpx client with declared User-Agent, robots.txt respect, ETag/If-Modified-Since, exponential backoff, quota tracker hook (throttle before the free limit), heartbeat, `feed_status` KV update (ok/degraded/stale/bad).
- Approximate timestamps: parser sets `published_approx=true` for date-only feed values or relative times ('2h ago').
- All writes via `mt_store`; research reads via `pit(as_of)` on `ingested_at`.

## ToDo

- [ ] Alembic migrations for the tables above, incl. CHECK constraints and indexes (`canonical_url`, `content_hash`, `(published_at)`, GIN on `tickers`).
- [ ] `mt_core.schemas.text`: `RawTextItem`, `TextDocNew`, `TelegramMention`, `TelegramPosture` (msgspec, versioned).
- [ ] `mt_data.text.registry`: load `feeds.yaml`, `watchlist.yaml`, `source_terms.yaml`; seed `text.source`.
- [ ] `mt_data.text.connector.Connector` base + timestamp normaliser + `feed_status` reporter.
- [ ] Register text sources in `/data/feeds?kind=text` so D07 shows them.
- [ ] Example config files under `config/intel/*.example.yaml` used by P4-T001–T003.
- [ ] Tests (below) and module docs in `packages/mt_data/text/README.md`.

## Verification

### Tests
- Unit: timestamp normaliser (RFC 822, ISO, date-only → approx, '2h ago' → approx, future dates clamped + flagged).
- Unit: provenance defaults applied per source; missing terms entry → source refuses to enable.
- Migration test: inserting a telegram-kind row with `model_input_ok=true` fails on the CHECK constraint.
- Property: canonical URL normalisation is idempotent (utm_* stripped, host lower-cased, fragment dropped).

### Scenarios
- Given a connector hits 90% of its quota, then it throttles and D07 shows the quota bar amber.
- Given a source returns 5xx for 10 min, then `feed_status` → stale and an alert fires once (deduplicated).
- Given Postgres is down (02 §9.3), then raw items stay in JetStream and are written on recovery without duplicates.

### Stress / failure injection
- Replay 100k synthetic raw items: insert throughput ≥ 200 docs/s on the host, no duplicate `content_hash` rows.

## Acceptance criteria

- [ ] Migrations apply/rollback cleanly; CHECK constraints proven by tests
- [ ] Connector base used by at least one real connector in a follow-up PR without changes
- [ ] Text sources visible in D07 with status and quota
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- Clock skew between feed and host: `ingested_at` always from our clock (chrony), `published_at` never trusted for PIT filters alone.

## Cardinal rules (do NOT)

- Do NOT store HTML; store extracted text only and mark it untrusted.
- Do NOT let any table path allow `model_input_ok=true` for Telegram rows.
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT skip, weaken or delete a test to get green.
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.

## Doc sync on completion

- `docs/03-build-spec.md`: M2: list the text tables and posture tables
- `docs/02-v1-architecture.md`: §4/§5.2 M2 tables: add `text.telegram_mention` next to `text.telegram_posture`
- `docs/roadmap/phase-4-intel.md`: tick T4.20 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T010-text-store-and-ingest-framework`
- PR title: `P4-T010: Build the mt_data.text store, source registry and ingest framework`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T010` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (canonical names text.telegram_posture / posture.telegram.* (17 §D P4-B003); schemas exist from P0 (17 §B); extends the P1 connector framework; explicit P0/P1 depends_on)
