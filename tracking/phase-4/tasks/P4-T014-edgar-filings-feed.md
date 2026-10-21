---
id: P4-T014
kind: task
title: EDGAR filings feed connector (Atom/JSON, ≤ 10 req/s)
phase: 4
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T010]
requirements: [R4.01]
roadmap_todos: [T4.20]
modules: [M2]
dashboards: [D07, D08]
branch: p4/P4-T014-edgar-filings-feed
pr: ""
doc_sync: [docs/06-aggregators-and-market-providers.md, docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P4-T014 · EDGAR filings feed connector (Atom/JSON, ≤ 10 req/s)

## Goal / expected outcome

`mt_data.text.edgar` follows SEC EDGAR current-filings Atom and per-CIK submissions JSON for the watchlist (8-K, 10-Q, 10-K, S-1, 424B, 13D/G, Form 4), downloads primary documents with edgartools, and publishes them as filing documents with form/period/section metadata for section-aware RAG chunking.

## Context & references

- Roadmap: [R4.01](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.20](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Sources: [06 §2](../../../docs/06-aggregators-and-market-providers.md#2-final-m2-social--news-ingestion-stack) · Spec: [03 M2](../../../docs/03-build-spec.md#m2-news--social--mt_datatext)
- RAG chunking: [10 §3 item 5](../../../docs/10-memory-rag-and-models.md#3-document-rag-design-postgres)
- Cross-phase: P1 R1.07/T1.24 (edgartools fundamentals flow; reuse its client and User-Agent).
- Related: P4-T031 (filing chunker), P4-T037 (earnings/IPO calendar uses the same client).

## Requirements

- Declared User-Agent (`MasterTrader <your email>` from config) and a global **≤ 10 req/s** limiter shared with the P1 flow.
- Watchlist CIKs from the symbol master; current-filings Atom polled every 2 min for all forms of interest.
- Store `form`, `cik`, `ticker`, `period`, `filed_at` (`published_at`), `accepted_at`, item list (8-K items) and the primary document text.
- Prefer the official feeds over RSS-Bridge's StockFilings bridge.

## ToDo

- [ ] Shared EDGAR rate limiter (token bucket, process-wide; Redis-free, NATS KV or in-proc).
- [ ] Atom poller + submissions JSON fetcher.
- [ ] Primary-document fetch + text extraction (HTML → text, tables kept as markdown).
- [ ] Fixtures for 8-K/10-K/10-Q/S-1.
- [ ] Tests.

## Verification

### Tests
- Unit: Atom fixture → filings list; 8-K item parsing.
- Unit: limiter never exceeds 10 req/s under 50 concurrent requests (property test with fake clock).
- Integration: a 10-K fixture keeps Item headings for the chunker.

### Scenarios
- Given SEC returns 429/403, then back off 10 min and alert once; never retry faster.
- Given an amended filing (10-K/A), then a new document row with `supersedes` is written.

### Stress / failure injection
- Simulate 2,000 filings on a 10-K season day: limiter holds ≤ 10 req/s; backlog clears; no 429s.

## Acceptance criteria

- [ ] Watchlist filings appear within 5 min of acceptance during a test day
- [ ] Limiter test proves ≤ 10 req/s
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- Filings for instruments not in the symbol master are stored but unlinked until the master updates.
- Postgres down (02 §9.3): raw items stay in `RAW_TEXT` and are processed on recovery; the connector itself never needs the DB.

## Cardinal rules (do NOT)

- Do NOT omit or fake the declared User-Agent.
- Do NOT commit secrets or paste them into chats, issues or logs; they live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT skip, weaken or delete a test to get green.
- Do NOT use unpinned images (`:latest`) or vendored code with telemetry/referral IDs; pin by digest.

## Doc sync on completion

- `docs/06-aggregators-and-market-providers.md`: §2 EDGAR row: forms followed and poll cadence
- `docs/roadmap/phase-4-intel.md`: tick T4.20 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T014-edgar-filings-feed`
- PR title: `P4-T014: EDGAR filings feed connector (Atom/JSON, ≤ 10 req/s)`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T014` run

## Progress log

- 2026-10-21 00:00 · planner · created
