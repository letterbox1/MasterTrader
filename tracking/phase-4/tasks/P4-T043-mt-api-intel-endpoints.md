---
id: P4-T043
kind: task
title: mt_api intel queries, commands and WebSocket topics
phase: 4
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T027, P4-T035, P4-T038, P4-T032, P4-T029]
requirements: [R4.13]
roadmap_todos: [T4.29]
modules: [M2, M3, M5, M9, M21]
dashboards: [D08, D01, D02]
branch: p4/P4-T043-mt-api-intel-endpoints
pr: ""
doc_sync: [docs/02-v1-architecture.md, docs/ui/dashboards/D08-intel.md, docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P4-T043 · mt_api intel queries, commands and WebSocket topics

## Goal / expected outcome

`mt_api` exposes `/intel/documents` (+ `/{id}`), `/intel/events`, `/intel/calendar`, `/intel/sentiment`, `/rag/search`, `/models/questions`, `/models/tierb/decisions`, `/data/feeds?kind=text`; commands `intel.source.add` (C1), `intel.source.mute` (C0), `intel.watchlist.update` (C0), `models.tierb.ask` (C0), `models.question.update` (C1); and WS topics `text.doc`, `evt`, `cal`, `tierb`, `posture` — the single backend contract for D08, the D01/D02 chips and the morning brief.

## Context & references

- Roadmap: [R4.13](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.29](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- API: [02 §7](../../../docs/02-v1-architecture.md#7-api-contract-mt_api) · [D08 backend contract](../../../docs/ui/dashboards/D08-intel.md)
- Cross-phase: P0 R0.08 (`mt_api` command bus, confirmation levels, WS envelope `{topic, seq, ts, data}`).

## Requirements

- Cursor pagination; filters per D08 (watchlist only, asset class, source, min relevance, sentiment, event type, language).
- Document detail returns full text only when `display_ok` and not paywalled; otherwise headline + link; **Telegram is never a document** — `/intel/sentiment` exposes `tg_posture` numbers only.
- `intel.source.add` rejects paid/ToS-banned kinds (deny-list: X scraping, Reddit RSS, Nitter, snscrape, twscrape, Instagram/TikTok/LinkedIn/Facebook/Threads scrapers, Discord self-bot) and Telegram adds go into the join queue, not a direct join.
- Every command audited in `audit.command`; WS server-side throttling ≤ 1 Hz per table topic.
- OpenAPI updated; response time p95 < 200 ms for list queries.

## ToDo

- [ ] Routers + pydantic models + OpenAPI.
- [ ] Command handlers with confirmation levels.
- [ ] WS fan-out from NATS subjects (`text.doc.new`, `evt.*`, `cal.*`, `dec.tierb.*`, `posture.tg.*`).
- [ ] Contract tests consumed by the web client types.
- [ ] Tests.

## Verification

### Tests
- API tests per endpoint incl. filters + pagination.
- Unit: deny-listed source kinds rejected with problem+json.
- Contract: generated TS types compile in the web app.

### Scenarios
- Given a paywalled doc, when detail is requested, then only headline + link are returned.
- Given `intel.source.add` with kind `telegram`, then it enqueues a join and returns the queue position.
- Given mt-api restarts, then WS clients re-sync via `seq` gap detection.

### Stress / failure injection
- 100 WS clients subscribed to `text.doc` during a 2,000-doc burst: throttling holds, p95 lag < 500 ms.

## Acceptance criteria

- [ ] All endpoints/commands/topics in OpenAPI and tested
- [ ] Deny-list enforced server-side
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- Postgres down: queries return 503 problem+json; WS continues for live NATS topics (read-only UI).

## Cardinal rules (do NOT)

- Do NOT enforce confirmation levels only in the UI.
- Do NOT return Telegram text from any endpoint.
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT UPDATE or DELETE WORM rows (`audit.*`); corrections are new rows ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/02-v1-architecture.md`: §7.1/§7.3: add `posture` WS topic and `models.question.update`
- `docs/ui/dashboards/D08-intel.md`: backend contract: confirm endpoints
- `docs/roadmap/phase-4-intel.md`: tick T4.29 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T043-mt-api-intel-endpoints`
- PR title: `P4-T043: mt_api intel queries, commands and WebSocket topics`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T043` run

## Progress log

- 2026-10-21 00:00 · planner · created
