---
id: P1-T073
kind: task
title: Live connector check with your credentials and keys
phase: 1
type: VERIFY
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P0-T009, P0-T010, P1-T002, P1-T006, P1-T016, P1-T017, P1-T021, P1-T022, P1-T024, P1-T026, P1-T029, P1-T034, P1-T038, P1-T039]
requirements: [R1.01, R1.04, R1.05, R1.06, R1.08, R1.11]
roadmap_todos: [T1.66]
modules: [M1, M16]
dashboards: [D07, D02]
tools: [git, uv, docker, sops]
mcp: []
env: [OANDA_PRACTICE_TOKEN, OANDA_PRACTICE_ACCOUNT_ID, IG_DEMO_API_KEY, IG_DEMO_USERNAME, IG_DEMO_PASSWORD, ALPACA_PAPER_KEY_ID, ALPACA_PAPER_SECRET_KEY, FRED_API_KEY, EIA_API_KEY, COINGECKO_DEMO_API_KEY, FINNHUB_API_KEY, BINANCE_TESTNET_READ_KEY, BINANCE_TESTNET_READ_SECRET, BYBIT_TESTNET_READ_KEY, BYBIT_TESTNET_READ_SECRET, USDA_QUICKSTATS_API_KEY]
services: [nats, postgres, prefect-server, oanda-practice, ig-demo, alpaca-paper, binance-testnet, bybit-testnet]
branch: p1/P1-T073-verify-live-connectors-with-keys
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/06-aggregators-and-market-providers.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-22
updated: 2026-10-22
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P1-T073 · Live connector check with your credentials and keys

## Goal / expected outcome

With your practice/demo/paper credentials and free API keys loaded from the secrets file, every keyed connector that was built keyless (against fixtures) is proven live: the OANDA, IG and Alpaca streams deliver, the keyed batch flows (FRED, EIA, CoinGecko Demo, Alpaca history, Finnhub cross-check) load real data, the keyed cost collectors (testnet fee tiers, OANDA/IG financing) read real values, and the quota tracker reads live rate-limit headers. Real recorded fixtures replace the documented-format fixtures where they differ.

## Context & references

- Roadmap: requirements [R1.01](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.04](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements)–[R1.06](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.08](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.11](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.66](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Build first, keys last: [17 §E](../../../docs/17-decisions-register.md#e-ratification-2026-10-22) (live checks needing your keys are separate final VERIFY tasks)
- Keys and accounts: [07 §3](../../../docs/07-security-notes.md#3-broker--exchange-keys) (practice/paper accounts use their normal credentials; read-only keys where the testnet offers them) · secrets [07 §2](../../../docs/07-security-notes.md#2-secrets) (sops file outside the repo)
- Sources and quotas: [06 §3](../../../docs/06-aggregators-and-market-providers.md#3-additional-forex--multi-asset-providers) · [03 §1](../../../docs/03-build-spec.md#1-ground-rules)
- Cross-phase prerequisites: P0-T009 (practice/testnet accounts: OANDA practice, IG demo, Alpaca paper, Binance + Bybit testnets), P0-T010 (free API keys: FRED, EIA, CoinGecko Demo, Finnhub)
- Depends on (this phase): P1-T002 (your T1.02 credentials in the secrets file), the keyless builds P1-T006, P1-T016, P1-T017, P1-T021, P1-T022, P1-T024, P1-T026, P1-T029, P1-T034, P1-T038, P1-T039
- The `env` names are the sops keys; run the checks with `sops exec-env ~/.config/mastertrader/secrets.sops.yaml 'make verify-live-connectors'` so values never touch disk or logs. USDA QuickStats is checked live with the free key from P0-T010 (P1-B019)

## Requirements

- Streams (during market hours): OANDA practice pricing stream, IG Lightstreamer demo and Alpaca IEX each deliver quotes/trades for every universe instrument on that venue for ≥ 30 min; `feed_status` live; DQ status `ok`; heartbeats observed
- Batch (keyed): FRED/ALFRED universe series with vintages; EIA series; CoinGecko Demo enrichment cached with `retention_days=1` and encrypted; Alpaca IEX history for universe stocks (the full load from P1-T022) with a backfill report; Finnhub low-frequency quotes feeding the stocks cross-source check
- Costs (keyed, read-only): Binance/Bybit testnet fee tiers via ccxt `fetchTradingFees`; OANDA `InstrumentFinancing` rates; IG funding where the demo account exposes it
- Quota tracker: live headers parsed for each keyed source that sends them (Alpaca/Finnhub `X-RateLimit-*`, Binance `X-MBX-USED-WEIGHT-1M`, OANDA limits); recorded budgets in `config/quotas.yaml` checked against observed limits (unknowns marked `verify: true` resolved or left with a note)
- Record a sanitised fixture set from the live sessions (tokens, account IDs and balances scrubbed) and replace any documented-format fixture that differs; golden tests stay green
- Report under `reports/verify/P1-T073/`: per connector pass/fail, message counts, first/last timestamps, quota headers seen, fixture diffs; never any credential or account number

## ToDo

- [ ] Run `./kanban preflight P1-T073`; if a key is missing, block this item and point at the USER task (P0-T009, P0-T010 or P1-T002)
- [ ] Start the keyed connectors with secrets loaded via `sops exec-env`; run the streams for ≥ 30 min in market hours
- [ ] Run the keyed batch flows once (FRED, EIA, CoinGecko, Alpaca history, Finnhub) and the keyed cost collectors
- [ ] Capture quota headers and reconcile `config/quotas.yaml`
- [ ] Record scrubbed fixtures; update golden tests where the real format differs (never loosen an assertion)
- [ ] Write and store the report
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box

## Verification

### Tests

- `make verify-live-connectors` (pytest marker `live`, excluded from normal CI) exits 0 only if every connector passes
- Fixture scrubber test: no token, account ID or balance pattern survives in recorded fixtures (gitleaks + a regex test)

### Scenarios

- Given an expired OANDA practice token, when the check runs, then OANDA fails with `auth_failed`, the report names it, and the other connectors still run
- Given CoinGecko rows were cached, when 25 h pass, then the retention job has removed them (cross-check with P1-T059)
- Given a live rate-limit header shows a lower limit than `config/quotas.yaml`, when parsed, then the header wins and a `quota.limit_changed` event is logged for the monthly ToS check

### Stress / failure injection

- Disconnect each stream once during the run (block its host for 60 s): reconnect with backoff, DQ marks it stale then recovers, no duplicate subscriptions

## Acceptance criteria

- [ ] Every keyed stream, batch flow and cost collector passes live; report stored
- [ ] Quota tracker shows live headers for every source that sends them
- [ ] Recorded fixtures are scrubbed and golden tests pass with them

## Exceptions & edge cases

- Run the stream part when FX and US equities are open (e.g. Tuesday 00:30–06:00 Sydney); outside hours a stream that is correctly `closed` is recorded as "re-run in session", not a pass
- IG demo allowances are small: keep subscriptions to the universe and stop after the check if the soak is not running yet
- A provider that now needs a paid plan is disabled in `config/sources.yaml` with the reason, never upgraded

## Cardinal rules (do NOT)

- Do NOT print, log or commit credentials; load them only via `sops exec-env` ([07 §2](../../../docs/07-security-notes.md#2-secrets))
- Do NOT use live (real-money) accounts or keys; practice/demo/paper/testnet only; no live money before the P7 gates
- Do NOT place, modify or cancel orders; P1 is read-only toward venues (orders arrive in P2 through M11)
- Do NOT exceed a free tier or add paid data/APIs ([03 §1](../../../docs/03-build-spec.md#1-ground-rules))
- Do NOT skip, weaken or delete a test (or widen a tolerance) to get green

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.66; note P1-T073 next to it.
- `docs/06-aggregators-and-market-providers.md` §3: record any observed free-tier limits that differ from the doc.

## Branch & PR

- Branch: `p1/P1-T073-verify-live-connectors-with-keys`
- PR title: `P1-T073: Live connector check with your credentials and keys`
- PR checklist: report stored · fixtures scrubbed · no secrets in diff · docs synced · task file ticked · `./kanban done P1-T073` run

## Progress log

- 2026-10-22 00:00 · aligner · created for T1.66 (docs/16–17 alignment: live checks split from the keyless builds)
