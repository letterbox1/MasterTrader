---
id: P4-T039
kind: task
title: Positioning, nowcast and macro inputs: Myfxbook, IG, OANDA books, nowcasts, Fed SEP, VIX, ZQ
phase: 4
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T010]
requirements: [R4.11]
roadmap_todos: [T4.27]
modules: [M1, M6]
dashboards: [D08]
branch: p4/P4-T039-positioning-macro-inputs
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

# P4-T039 · Positioning, nowcast and macro inputs: Myfxbook, IG, OANDA books, nowcasts, Fed SEP, VIX, ZQ

## Goal / expected outcome

Connectors land the raw series that P4-T040/T041 turn into features: Myfxbook Community Outlook (100 calls/day, poll 15–30 min), IG client sentiment, OANDA order/position books (if T1.60 confirmed), GDPNow, NY Fed Staff Nowcast, Cleveland Fed inflation nowcast, Fed SEP/dot plot, Cboe VIX history, and ZQ (30-day Fed funds) futures settlement prices.

## Context & references

- Roadmap: [R4.11](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.27](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Providers: [06 §3 retail sentiment, reports & nowcasts](../../../docs/06-aggregators-and-market-providers.md#3-additional-forex--multi-asset-providers) · research [forex-macro](../../../docs/research/forex-macro-market-providers.md)
- Cross-phase: P1 T1.60 (OANDA books, IG sentiment path checks), R1.06 (yfinance futures, FRED), R1.08 quota tracker.

## Requirements

- Myfxbook: one session per day (IP-bound), all symbols in one call, poll every 20 min → ≤ 72 calls/day (< 100).
- IG sentiment: per market id, poll 15 min, within IG demo API limits; OANDA books: hourly snapshots if the endpoint works, else disabled with reason.
- Nowcasts: scheduled pulls on publication days (GDPNow ~6–7×/quarter, NY Fed weekly Fri, Cleveland daily); store with vintages (PIT).
- VIX: Cboe daily history CSV + intraday from the P1 feed if available; ZQ: daily settlement for the next 12 contracts.
- All rows provenance-tagged (Myfxbook/IG personal-use: `commercial_ok=false`).

## ToDo

- [ ] Connectors + schedules (Prefect).
- [ ] Vintage-aware storage in `market.macro_series` / `features` raw tables.
- [ ] Fixtures + tests.

## Verification

### Tests
- Unit: each connector fixture → rows with vintage/event_time.
- Unit: Myfxbook scheduler never exceeds 100 calls/day (fake clock).

### Scenarios
- Given the OANDA books endpoint is gone (T1.60 failed), then that input is disabled with reason and features fall back to Myfxbook/IG only.
- Given GDPNow revises, then a new vintage row is stored, earlier vintage kept.

### Stress / failure injection
- n/a: low volume; quota-bound.

## Acceptance criteria

- [ ] All enabled inputs flowing on schedule; quotas respected
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- Myfxbook session expiry (1-month TTL, IP-bound): re-login once and alert.

## Cardinal rules (do NOT)

- Do NOT use CME FedWatch scraping or the paid API; compute from ZQ.
- Do NOT use CoinGlass (paid).
- Do NOT commit secrets or paste them into chats, issues or logs; they live only in the sops/age file ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.
- Do NOT skip, weaken or delete a test to get green.
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.

## Doc sync on completion

- `docs/06-aggregators-and-market-providers.md`: §3: confirm endpoints used and their status
- `docs/roadmap/phase-4-intel.md`: tick T4.27 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T039-positioning-macro-inputs`
- PR title: `P4-T039: Positioning, nowcast and macro inputs: Myfxbook, IG, OANDA books, nowcasts, Fed SEP, VIX, ZQ`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T039` run

## Progress log

- 2026-10-21 00:00 · planner · created
