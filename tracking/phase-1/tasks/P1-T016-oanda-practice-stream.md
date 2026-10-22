---
id: P1-T016
kind: task
title: Stream OANDA v20 practice prices for FX and metals
phase: 1
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T005, P1-T006, P1-T007, P1-T009]
requirements: [R1.04]
roadmap_todos: [T1.23]
modules: [M1]
dashboards: [D02, D07]
tools: [git, uv, docker]
mcp: []
env: []
services: [nats]
branch: p1/P1-T016-oanda-practice-stream
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

# P1-T016 · Stream OANDA v20 practice prices for FX and metals

## Goal / expected outcome

`ingest-market` holds an OANDA v20 practice pricing stream for the universe's FX pairs and broker spot XAU/XAG and publishes `md.oanda.{symbol}.quote`, with heartbeats feeding the stale check.

## Context & references

- Roadmap: requirements [R1.04](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.23](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M1](../../../docs/03-build-spec.md#m1-market--macro-data--mt_datamarket) (OANDA v20 practice stream, max 4 quotes/s per instrument; spot XAU/XAG from brokers, **no LBMA**) · [03 §6](../../../docs/03-build-spec.md#6-smallest-free-timeframe-by-asset-class) (no L2 in FX) · [06 §3 Skip list](../../../docs/06-aggregators-and-market-providers.md#skip-list) (oandapyV20 is stale → thin httpx client)
- Build first, keys last ([17 §E](../../../docs/17-decisions-register.md#e-ratification-2026-10-22)): built and tested keyless against fixtures in OANDA's documented stream format; the live practice stream is checked with your token in P1-T073 (token from P0-T009 / P1-T002 in the sops file)
- Depends on (this phase): P1-T005, P1-T006, P1-T007, P1-T009

## Requirements

- Thin async httpx client for `/v3/accounts/{accountID}/pricing/stream` (practice host), no oandapyV20
- Publish bid/ask/mid quotes with `event_time` from OANDA `time`; treat stream `HEARTBEAT` messages as liveness for KV `feed_status` (connection-level staleness)
- Throttle-aware: OANDA sends ≤ 4 quotes/s per instrument; record actual rate per instrument
- Respect REST/stream connection limits via the quota tracker; reconnect with backoff
- Metals: XAU_USD, XAG_USD from OANDA tagged `licence=personal`, `source=oanda_practice`
- Also fetch daily `InstrumentFinancing`-related instrument metadata for P1-T039 (no orders)

## ToDo

- [ ] Implement the pricing stream connector and normaliser
- [ ] Map OANDA instruments (EUR_USD) to Nautilus IDs via the instrument master
- [ ] Golden fixtures in OANDA's documented stream format (PRICE + HEARTBEAT lines); P1-T073 replaces them with scrubbed real recordings
- [ ] Write the tests listed under Verification
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Unit: parse PRICE and HEARTBEAT lines; tradeable flag false → quote marked `indicative`
- Integration: golden replay of a recorded stream; reconnect after chunked-stream stall
- Live practice stream: checked in P1-T073 (needs your token); CI runs keyless

### Scenarios

- Given the stream stalls without closing, when no HEARTBEAT arrives for 2× the heartbeat interval, then the connector reconnects, and the DQ monitor marks the instruments `stale` once their data age crosses the threshold (P1-T031)
- Given the FX market is closed for the weekend, when no prices arrive, then the session calendar suppresses stale alerts

### Stress / failure injection

- Fault: inject a 30 s TCP blackhole (no FIN); detection and reconnect happen without manual action

## Acceptance criteria

- [ ] Golden replay and reconnect tests pass keyless; the live `md.oanda.*.quote` check for every universe FX/metal pair runs in P1-T073
- [ ] No LBMA source anywhere in config
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- `tradeable=false` periods (rollover ~5 pm New York) are not bad ticks; mark and pass through
- Token rotation: connector reloads secrets on SIGHUP without a restart

## Cardinal rules (do NOT)

- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file (kept outside the repo) mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT use keys with withdrawal rights, or without an IP allow-list where the venue supports one; practice/testnet/paper only, no live money before the P7 gates.
- Do NOT place, modify or cancel orders from this code; P1 is read-only toward venues (orders arrive in P2 through M11).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.23 once every task traced to it in PHASE.md is done; note P1-T016 next to it.
- `docs/03-build-spec.md` §M1: note the client choice and measured quote rate

## Branch & PR

- Branch: `p1/P1-T016-oanda-practice-stream`
- PR title: `P1-T016: Stream OANDA v20 practice prices for FX and metals`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T016` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (keyless build on fixtures, live stream moved to P1-T073; data-age stale wording)
