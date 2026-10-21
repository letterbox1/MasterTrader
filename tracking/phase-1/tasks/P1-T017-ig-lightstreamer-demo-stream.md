---
id: P1-T017
kind: task
title: Stream IG demo prices via Lightstreamer
phase: 1
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T005, P1-T006, P1-T007, P1-T009]
requirements: [R1.04]
roadmap_todos: [T1.23]
modules: [M1]
dashboards: [D02, D07]
branch: p1/P1-T017-ig-lightstreamer-demo-stream
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/03-build-spec.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P1-T017 · Stream IG demo prices via Lightstreamer

## Goal / expected outcome

IG demo streaming prices for the universe's FX, metals and index CFDs publish as `md.ig.{symbol}.quote`, giving a second live FX source for divergence checks.

## Context & references

- Roadmap: requirements [R1.04](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.23](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M1](../../../docs/03-build-spec.md#m1-market--macro-data--mt_datamarket) (IG Lightstreamer demo) · [06 §3](../../../docs/06-aggregators-and-market-providers.md#3-additional-forex--multi-asset-providers) (IG REST + Lightstreamer, `trading-ig` BSD-3)
- Demo credentials from sops (P0 T0.09); IG historical price allowance is limited, so history comes from Dukascopy (P1-T018)
- Depends on (this phase): P1-T005, P1-T006, P1-T007, P1-T009

## Requirements

- Use `trading-ig` (pinned) for session login (demo host) and the Lightstreamer client for `MARKET:{epic}` / `CHART:{epic}:TICK` subscriptions
- Publish bid/offer/mid with `event_time` from `UPDATE_TIME`/`UTM`; map epics to Nautilus IDs in the instrument master
- Session token refresh before expiry; reconnect with backoff; respect IG API allowances through the quota tracker
- Read-only usage: only login, market details and streaming

## ToDo

- [ ] Implement IG stream connector with session refresh
- [ ] Epic mapping for universe instruments
- [ ] Golden fixtures; tests; docs
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Unit: update parsing incl. partial field updates (Lightstreamer sends only changed fields)
- Integration: golden replay; forced session expiry → re-login and resubscribe

### Scenarios

- Given IG returns "exceeded API key allowance", when it happens, then the connector pauses per quota tracker and D07 shows throttled
- Given a market is in auction/closed state, when updates stop, then the session calendar suppresses stale

### Stress / failure injection

- Fault: drop the Lightstreamer session every 5 min for 1 h; no manual action needed and no duplicate subscriptions

## Acceptance criteria

- [ ] Live `md.ig.*.quote` for every universe FX/metal pair during market hours
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- IG demo prices can differ from live; tag `source=ig_demo` so they are never mistaken for live quotes

## Cardinal rules (do NOT)

- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT use keys with withdrawal rights or without an IP allow-list; practice/testnet/paper only, no live money before the P7 gates.
- Do NOT place, modify or cancel orders from this code; P1 is read-only toward venues (orders arrive in P2 through M11).
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).
- Do NOT add an image without pinning it by digest, or vendored code that carries telemetry or referral IDs.

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.23 once every task traced to it in PHASE.md is done; note P1-T017 next to it.
- `docs/03-build-spec.md` §M1: note IG allowances observed

## Branch & PR

- Branch: `p1/P1-T017-ig-lightstreamer-demo-stream`
- PR title: `P1-T017: Stream IG demo prices via Lightstreamer`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T017` run

## Progress log

- 2026-10-21 00:00 · planner · created
