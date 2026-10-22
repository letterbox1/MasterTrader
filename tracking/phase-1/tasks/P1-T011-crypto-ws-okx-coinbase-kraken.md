---
id: P1-T011
kind: task
title: Stream OKX, Coinbase and Kraken public trades, L1 and L2
phase: 1
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T010]
requirements: [R1.01]
roadmap_todos: [T1.20]
modules: [M1]
dashboards: [D02, D07]
tools: [git, uv, docker]
mcp: []
env: []
services: [nats]
branch: p1/P1-T011-crypto-ws-okx-coinbase-kraken
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/03-build-spec.md]
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

# P1-T011 · Stream OKX, Coinbase and Kraken public trades, L1 and L2

## Goal / expected outcome

The remaining three crypto venues publish the same normalised `md.*` streams as Binance/Bybit, giving the cross-source divergence check (P1-T034) independent references for every major pair.

## Context & references

- Roadmap: requirements [R1.01](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.20](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M1](../../../docs/03-build-spec.md#m1-market--macro-data--mt_datamarket) · [02 §6](../../../docs/02-v1-architecture.md#6-messaging-nats) · [12 §2](../../../docs/12-policy-and-compliance.md#2-venue-access-registry) (OKX AU derivatives unresolved → paper only; Kraken AU derivatives blocked; all fine as data sources)
- Pattern: reuse the connector and book builder from P1-T010
- Depends on (this phase): P1-T010

## Requirements

- OKX (spot + swaps), Coinbase (Advanced Trade public market data), Kraken (spot WS v2) via Nautilus clients where supported, else ccxt pro
- Book integrity inputs: keep venue checksums where offered (OKX `checksum`/`seqId`, Kraken CRC32 book checksum) on each book message for P1-T036
- Same payload schemas, sequence fields and `feed_status` updates as P1-T010

## ToDo

- [ ] Implement the three stream connectors on the shared base
- [ ] Map venue symbols to Nautilus `InstrumentId` via the instrument master
- [ ] Record fixtures; golden replay tests
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Unit: normaliser golden tests per venue; checksum field passed through unchanged
- Integration: golden replay per venue; live 60 s smoke (nightly)

### Scenarios

- Given Kraken sends a book checksum mismatch, when received, then the connector resubscribes and P1-T036 logs a `book_checksum` incident
- Given Coinbase public channel limits, when subscribing to many symbols, then subscriptions are batched within limits

### Stress / failure injection

- Burst replay at 10× on each venue; publish latency p99 < 50 ms

## Acceptance criteria

- [ ] Live `md.okx.*`, `md.coinbase.*`, `md.kraken.*` streams for every universe symbol listed on those venues
- [ ] Each major pair has ≥ 2 independent live sources (checked by a test over the universe)
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- A pair not listed on a venue is skipped with a logged reason, not an error
- Venue API version changes: connector fails loudly with a parse error count metric, never publishes malformed data

## Cardinal rules (do NOT)

- Do NOT send any private/authenticated request from `ingest-market`
- Do NOT place, modify or cancel orders from this code; P1 is read-only toward venues (orders arrive in P2 through M11).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).
- Do NOT add an image without pinning it by digest, or vendored code that carries telemetry or referral IDs.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.20 once every task traced to it in PHASE.md is done; note P1-T011 next to it.
- `docs/03-build-spec.md` §M1: list which venues provide book checksums

## Branch & PR

- Branch: `p1/P1-T011-crypto-ws-okx-coinbase-kraken`
- PR title: `P1-T011: Stream OKX, Coinbase and Kraken public trades, L1 and L2`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T011` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (run fields; keyless public streams)
