---
id: P1-T006
kind: task
title: Build the shared per-connector quota tracker
phase: 1
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T005]
requirements: [R1.08]
roadmap_todos: [T1.25]
modules: [M1]
dashboards: [D07]
branch: p1/P1-T006-quota-tracker
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/03-build-spec.md, docs/ui/dashboards/D07-data-quality.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P1-T006 · Build the shared per-connector quota tracker

## Goal / expected outcome

Every connector asks one quota tracker before each call; it throttles before any free limit is reached, learns live budgets from response headers where available, and exposes usage for the D07 Quotas tab.

## Context & references

- Roadmap: requirements [R1.08](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.25](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Rule: [03 §1](../../../docs/03-build-spec.md#1-ground-rules) ("every connector has a quota tracker that throttles before the limit") · registry rate limits from live headers [12 §2](../../../docs/12-policy-and-compliance.md#2-venue-access-registry)
- Limits in docs: Twelve Data 800/day, Myfxbook 100/day, Finnhub 60/min, FMP 250/day ([06 §3](../../../docs/06-aggregators-and-market-providers.md#3-additional-forex--multi-asset-providers)); EDGAR ≤ 10 req/s ([03 M1](../../../docs/03-build-spec.md#m1-market--macro-data--mt_datamarket)); OANDA ≤ 4 quotes/s/instrument; Alpaca IEX 30 symbols; Telegram bot ≤ 30 msg/s ([12 §4](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules))
- UI: [D07 Data & Quality](../../../docs/ui/dashboards/D07-data-quality.md) Quotas tab (limit, used, headroom %, throttle state, next reset, warn at 80%)
- Depends on (this phase): P1-T005

## Requirements

- `mt_data.quota.QuotaTracker`: token buckets per (source, scope) with rolling windows (per second, minute, day, month); `acquire(cost)` blocks or raises `QuotaExhausted`
- Budgets from `config/quotas.yaml` with a documented source for each number; live overrides from headers (e.g. Binance `X-MBX-USED-WEIGHT-1M`, Alpaca/Finnhub `X-RateLimit-Remaining`, `Retry-After`)
- Throttle threshold default 80% of the free limit (warn) and hard stop at 95%; never exceed 100%
- State shared across processes via NATS KV `quota` (so `ingest-batch` workers share one budget) and snapshotted to `ops.quota_usage` every minute for history
- Prometheus: `mt_quota_used_ratio{source,window}`, `mt_quota_throttled_total`; alert at 80% (`alert.warning.quota`)
- Daily/monthly reset times in the provider's timezone (stored per source)

## ToDo

- [ ] Implement the token-bucket tracker with NATS KV backing and a local fallback bucket at 50% budget if KV is down
- [ ] Header parsers for Binance, Bybit, OKX, Alpaca, OANDA, FRED, Finnhub, generic `Retry-After`
- [ ] Create `config/quotas.yaml` with every P1 source and its cited free limit (mark unknown limits `verify: true` and run at a conservative default)
- [ ] Migration for `ops.quota_usage`; minute snapshot job
- [ ] Wire into the connector base (P1-T005) so no connector can call out without `acquire`
- [ ] Write the tests listed under Verification
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- Unit: bucket maths across windows; header override lowers budget; `Retry-After` pauses the scope
- Property (hypothesis): for any random call sequence, granted calls never exceed the configured limit in any window
- Integration: two worker processes share one KV budget and together stay under the limit

### Scenarios

- Given Twelve Data at 640/800 calls today, when another flow asks for 200 calls, then 120 are granted, the rest wait for the reset, and D07 shows "throttled" before any 429
- Given NATS KV is unreachable, when a connector asks for budget, then it uses the local fallback at half rate and raises `alert.warning.quota_kv_down`

### Stress / failure injection

- Fault injection: provider returns 429 with `Retry-After: 120` → all callers for that source pause 120 s, no retry storm (count requests during pause = 0)
- Load: 10k `acquire` calls/s from 8 coroutines; p99 acquire latency < 1 ms locally

## Acceptance criteria

- [ ] No connector code path performs an outbound request without `acquire` (enforced by a test that greps for raw `httpx` clients outside `mt_data.core`)
- [ ] Quota warnings appear at 80%, before throttling starts (D07 acceptance 3)
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check, gitleaks)

## Exceptions & edge cases

- Clock jumps (chrony step): windows use monotonic time for spacing and UTC for daily resets
- Provider changes its limit: header override wins and a `quota.limit_changed` event is logged for the monthly ToS check

## Cardinal rules (do NOT)

- Do NOT skip, weaken or delete a test (or widen a tolerance) to get CI green.
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).
- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.25 once every task traced to it in PHASE.md is done; note P1-T006 next to it.
- `docs/03-build-spec.md` §1: link `config/quotas.yaml` as the list of free limits in force
- `docs/ui/dashboards/D07-data-quality.md` Quotas tab: note fields actually exposed if they differ

## Branch & PR

- Branch: `p1/P1-T006-quota-tracker`
- PR title: `P1-T006: Build the shared per-connector quota tracker`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T006` run

## Progress log

- 2026-10-21 00:00 · planner · created
