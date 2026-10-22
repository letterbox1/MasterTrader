---
id: P3-T010
kind: task
title: FX service core with RBA F11 AUD rates and USD cross
phase: 3
type: BUILD
status: backlog
priority: critical
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P3-T005, P1-T020, P1-T019, P0-T027]
requirements: [R3.03]
roadmap_todos: [T3.21]
modules: [M18]
dashboards: []
tools: [git, uv, docker]
mcp: []
env: []
services: [postgres]
branch: p3/P3-T010-fx-service-rba-usd
pr: ""
doc_sync: [docs/09-journal-and-tax.md, docs/roadmap/phase-3-journal-and-tax.md]
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

# P3-T010 · FX service core with RBA F11 AUD rates and USD cross

## Goal / expected outcome

`mt_journal.fx` returns, for any (currency, date/time), the AUD and USD rate with `fx_rate_source` and `fx_rate_ts`, sourced from RBA F11 for AUD, with the decided rule for weekends, public holidays and currencies not in F11 (last published business day; via USD), and every rate used is persisted in `journal.fx_rate` so reports are reproducible.

## Context & references

- Roadmap: [R3.03, T3.21](../../../docs/roadmap/phase-3-journal-and-tax.md)
- [09 goals §5](../../../docs/09-journal-and-tax.md#goals) (native + USD + AUD, RBA daily) · [11 §3 base currency resolution](../../../docs/11-cryptotrader-crossover-review.md#3-conflicts-and-how-they-were-resolved) · [02 F9 step 2](../../../docs/02-v1-architecture.md#8-end-to-end-flows)
- Rule: [09 FX and valuation rules](../../../docs/09-journal-and-tax.md#fx-and-valuation-rules) · [16 §4.3 FX for tax](../../../docs/16-configuration-and-safety-model.md#43-live-inputs-instead-of-constants) · decision [17 §D P3-B008](../../../docs/17-decisions-register.md#d-other-decisions)
- Cross-phase prerequisites (depends_on): P1-T020 (RBA F11 daily FX), P1-T019 (Frankfurter/ECB reference rates), P0-T027 (`pit(as_of)`)

## Requirements

- Source of truth for AUD: RBA F11 daily series loaded by P1 into `market.macro_series` (read via `pit(as_of)`); copy each used rate into `journal.fx_rate` (`base`, `quote`, `rate`, `source = RBA_F11`, `published_date`, `as_of_ts`, provenance).
- Rule (decided, 09/16 §4.3): use the F11 rate for the **taxpayer-local date** of the event; if none (weekend/holiday/before publication), use the **last published business day's** rate and set `fx_rate_ts` to that publication date with flag `fx_prior_day = true`.
- Currencies not in F11: via USD (RBA AUD/USD × the ECB/Frankfurter USD cross for that date), source `RBA_F11×ECB` recorded.
- USD amounts: native→USD via the same day's cross (or 1 for USD); AUD→USD via F11 AUD/USD.
- API: `fx.rate(ccy_from, ccy_to, at_ts, purpose)` → `FxQuote(rate: Decimal, source, ts, flags)`; purpose `tax` always uses RBA for AUD (base-currency setting only changes display).
- Missing data never silently defaults to 1. A prior rate older than `fx.max_prior_business_days` (setting, default 5) → raise `FxUnavailable`; events wait in `pending_fx` state and an alert fires. The setting lives in `config/journal/fx.yaml` and is shown in D16 Settings; no constant in code.

## ToDo

- [ ] Implement `packages/mt_journal/fx/service.py`, `fx/rba.py` (reader over `market.macro_series`), `fx/cross.py`
- [ ] Persist used rates to `journal.fx_rate` (append-only, idempotent per (pair, date, source))
- [ ] Pending-FX queue + retry flow (Prefect `journal-fx-backfill`, hourly)
- [ ] Unit + golden tests with a fixture of F11 rows (incl. a long weekend and Christmas)
- [ ] Docs: FX rule in 09

## Verification

### Tests

- Golden: fixture of RBA F11 for Dec 2026–Jan 2027; events on 25 Dec and 26 Dec use the 24 Dec rate with `fx_prior_day`.
- Unit: EUR event → AUD via cross equals F11 EUR/AUD where F11 has EUR (consistency check within 0.5%).
- Unit: FxUnavailable when last rate is > 5 business days old (default limit, [16 §4.5](../../../docs/16-configuration-and-safety-model.md#45-journal-and-tax-defaults)).
- Property: rate × inverse rate = 1 within Decimal precision.

### Scenarios

- Given a USD fill at 2027-01-26 (Australia Day), when stamped, then AUD uses the 25 Jan F11 rate, flagged prior-day.
- Given the RBA flow failed for 2 days, when events arrive, then they're stamped with the prior rate and flagged; after 5 business days they go to `pending_fx` and alert.

### Stress / failure injection

- Stamp 100k events across 3 years in a batch; < 60 s on the target host with rate caching per (pair, date).

## Acceptance criteria

- [ ] All AUD values for tax come from RBA F11 (test asserts source)
- [ ] Every rate used is in `journal.fx_rate` with source and timestamp
- [ ] Weekend/holiday rule documented and tested
- [ ] CI green (lint, types, tests, `pit` check; `tax-golden` once P3-T045 lands)

## Exceptions & edge cases

- RBA revises a published rate → new `journal.fx_rate` row; already-stamped events keep the original rate (reports record the rate version they used).
- Timezone: taxpayer-local date, not UTC date, picks the rate.

## Cardinal rules (do NOT)

- Do NOT fall back to CoinGecko or any ≤ 24 h-retention source for stored rates ([16 §4.1](../../../docs/16-configuration-and-safety-model.md#41-valuing-crypto-for-the-journal), [12 §4](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT default a missing rate to 1 or interpolate silently.
- Do NOT commit secrets or paste them into chats/issues; secrets live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT UPDATE or DELETE `journal.*` (WORM) rows; corrections are new rows referencing the superseded row ([15 §2](../../../docs/15-bots-hitl-and-worm-audit.md#2-worm-records-write-once-read-many)).
- Do NOT use floats for money, quantities, FX rates or tax; `Decimal` in Python and `numeric` in Postgres only ([02 §5.2](../../../docs/02-v1-architecture.md#52-key-conventions)).
- Do NOT use paid data/APIs or scraping that breaks terms; free tiers only (03 §1).
- Do NOT skip, weaken or delete a test to get green; pin images by digest; no telemetry or referral IDs in vendored code.

## Doc sync on completion

- `docs/09-journal-and-tax.md` FX rules: add the `pending_fx` state and the `fx.max_prior_business_days` setting.
- `docs/roadmap/phase-3-journal-and-tax.md`: tick T3.21 once every item mapped to it is done.

## Branch & PR

- Branch: `p3/P3-T010-fx-service-rba-usd`
- PR title: `P3-T010: FX service core with RBA F11 AUD rates and USD cross`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P3-T010` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (RBA gap rule = last published business day, non-F11 via USD (P3-B008 closed); staleness limit is a setting; explicit P1/P0 depends_on; tools/services filled)
