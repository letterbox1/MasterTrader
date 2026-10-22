---
id: P4-T037
kind: task
title: Calendar sources: FRED/ALFRED releases, ForexFactory, central banks, COT/EIA/WASDE/Baker Hughes, earnings/IPOs, holidays
phase: 4
type: BUILD
status: backlog
priority: critical
size: L
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T010, P4-T014, P1-T024, P1-T026, P1-T009]
requirements: [R4.10]
roadmap_todos: [T4.26]
modules: [M5]
dashboards: [D08, D06]
tools: [uv, git]
mcp: []
env: []
services: [postgres, nats, prefect-server]
branch: p4/P4-T037-calendar-sources
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-4-intel.md]
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

# P4-T037 · Calendar sources: FRED/ALFRED releases, ForexFactory, central banks, COT/EIA/WASDE/Baker Hughes, earnings/IPOs, holidays

## Goal / expected outcome

`mt_data.calendar` fills `text.calendar_event` from FRED/ALFRED release dates, the ForexFactory weekly JSON (consensus/previous/actual, cached), central-bank meeting schedules (Fed, ECB, BoE, BoJ, SNB, RBA, BoC, RBNZ), CFTC COT / EIA (petroleum + natgas storage) / USDA WASDE / Baker Hughes days, EDGAR + Finnhub (+ FMP cross-check) earnings and IPO dates, and `exchange_calendars` holidays/sessions; actuals update as new rows and publish `cal.{kind}`.

## Context & references

- Roadmap: [R4.10](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.26](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Spec: [03 M5](../../../docs/03-build-spec.md#m5-calendars--mt_datacalendar) · [06 §3 calendars & reports](../../../docs/06-aggregators-and-market-providers.md#3-additional-forex--multi-asset-providers) · research [forex-macro](../../../docs/research/forex-macro-market-providers.md) (`nfs.faireconomy.media/ff_calendar_thisweek.json`, ToS-grey, personal use, cached)
- Cross-phase (`depends_on`): P1-T024 (FRED/ALFRED), P1-T026 (EIA, USDA, COT, Baker Hughes), P1-T009 (instrument master with `exchange_calendars` sessions).
- Blackout defaults that read `importance`: [16 §2.8](../../../docs/16-configuration-and-safety-model.md#28-calendar-blackouts).

## Requirements

- `text.calendar_event`: id, kind (macro_release/cb_meeting/report/earnings/ipo/holiday/session), country/currency, title, importance (low/med/high), scheduled_at (UTC), consensus, previous, actual, surprise (z or %), instruments[], source, event_time, ingest_time, `supersedes`.
- ForexFactory: fetch weekly JSON at most every 1 h (cache), polite UA; map impact → importance; personal use only (`commercial_ok=false`).
- FRED/ALFRED release dates for the US backbone; central-bank schedules from official pages/ICS (annual, refreshed monthly).
- Instrument mapping rules (currency → FX pairs & indices; EIA → CL/NG; WASDE → grains; earnings → ticker).
- Times stored UTC; displayed Australia/Sydney; DST-safe tests.

## ToDo

- [ ] Connectors per source + importance normalisation.
- [ ] Instrument mapping rules (`config/intel/calendar_mapping.yaml`).
- [ ] Actual/surprise updater (actuals from FF and FRED vintages).
- [ ] Publisher `cal.{kind}`.
- [ ] Tests incl. DST transitions.

## Verification

### Tests
- Unit: FF JSON fixture → events with importance and consensus.
- Unit: DST transition week (US and AU) → correct UTC.
- Integration: FRED release schedule → NFP event with `instruments` incl. USD pairs, US indices, gold.

### Scenarios
- Given FF JSON is unavailable, then FRED/CB schedules still provide high-importance US/CB events and D08 shows 'consensus unavailable'.
- Given a meeting is rescheduled, then a new row supersedes the old and blackouts recompute.

### Stress / failure injection
- n/a: low volume; correctness focus.

## Acceptance criteria

- [ ] Next 14 days of high-importance events present for USD, EUR, GBP, JPY, CHF, AUD, CAD, NZD
- [ ] DST tests green
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- FF ToS-grey: if it blocks or changes terms, disable and rely on FRED/CB (no consensus).

## Cardinal rules (do NOT)

- Do NOT scrape Investing.com, Trading Economics or Myfxbook calendar.
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.
- Do NOT skip, weaken or delete a test to get green.
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.

## Doc sync on completion

- `docs/03-build-spec.md`: M5: table + mapping rules
- `docs/roadmap/phase-4-intel.md`: tick T4.26 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T037-calendar-sources`
- PR title: `P4-T037: Calendar sources: FRED/ALFRED releases, ForexFactory, central banks, COT/EIA/WASDE/Baker Hughes, earnings/IPOs, holidays`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T037` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (explicit cross-phase depends_on P1-T024/T026/T009; importance feeds 16 §2.8 blackouts)
