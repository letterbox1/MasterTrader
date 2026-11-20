---
id: P1-T001
kind: task
title: Seed the starting universe and watchlist from the docs' default lists
phase: 1
type: BUILD
status: backlog
priority: high
size: S
severity: ""
owner: agent
claimed_by: ""
depends_on: [P1-T005, P1-T009, P1-T046]
requirements: [R1.01, R1.04, R1.05, R1.06]
roadmap_todos: [T1.01]
modules: [M1]
dashboards: [D02]
tools: [git, cargo, supabase]
mcp: []
env: []
services: [supabase-postgres, mt-api]
branch: p1/P1-T001-pick-universe-watchlist
pr: ""
doc_sync: [docs/roadmap/phase-1-data-and-monitoring.md, docs/03-build-spec.md, docs/16-configuration-and-safety-model.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-11-20
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
review_result: ""
---

# P1-T001 · Seed the starting universe and watchlist from the docs' default lists

## Goal / expected outcome

The universe P1 records and monitors starts populated: the agent drafts it from the docs' default lists (03 M1, 03 §6, roadmap R1.01–R1.06), keeps it in one machine-readable defaults file, and seeds it through `mt-api` with source `seed`. Connectors, the DQ monitor, the storage budget and the soak all work from this one list without asking you anything. You review it once in the go-live pack (P7-T070) and can edit it any time in settings; your edits always win.

## Context & references

- Roadmap: requirements [R1.01](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.04](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.05](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.06](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.01](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Sources of the default lists: [03 M1](../../../docs/03-build-spec.md#m1-market--macro-data--mt_datamarket) (sources per asset class: crypto venues, OANDA/IG FX and metals, Alpaca IEX 30 symbols, daily futures such as gold and crude via `mt-connectors` (terms-checked sources, P1-T023), FRED/ALFRED, central banks, ABS CPI, RBA F11) · [03 §6](../../../docs/03-build-spec.md#6-smallest-free-timeframe-by-asset-class) (finest free timeframe per class)
- Storage budget is sized for ~10 liquid crypto symbols ([03 M1](../../../docs/03-build-spec.md#m1-market--macro-data--mt_datamarket), R1.N3); Alpaca free IEX allows 30 WebSocket symbols
- Decisions: [17 §G](../../../docs/17-decisions-register.md#g-platform-rust-and-python-supabase-vercel-workstation-first-2026-11-19) (values you'd otherwise be asked to set are drafted by agents and approved once in the go-live pack) · [17 §E](../../../docs/17-decisions-register.md#e-ratification-2026-10-22) (configurable values are settings, not questions)
- Built on: P1-T005 (fixture universe, `universe validate`), P1-T009 (instrument master resolves symbols), P1-T046 (`data.universe.update` command in `mt-api`)
- Unblocks: P1-T065 (the soak runs on this universe). Review: P7-T070 (go-live pack)

## Requirements

- One defaults file `config/defaults/universe.yaml`, drafted from the cited docs, each entry carrying a `doc` link to the section it comes from:
  - ~10 liquid crypto pairs (e.g. BTC/ETH/SOL vs USDT on Binance, with the same pairs on Bybit/OKX/Coinbase/Kraken where listed, for cross-source checks); `l2: true` on at most 3 (`market.l2.max_native_symbols`, default 3, configurable); every other symbol gets 1 s book snapshots ([17 §D](../../../docs/17-decisions-register.md#d-other-decisions) P1-B002)
  - FX and metal pairs on OANDA practice and IG demo (e.g. EURUSD, AUDUSD, USDJPY, XAUUSD, XAGUSD); no LBMA
  - up to 30 US ETFs/stocks (hard Alpaca IEX free limit), including the passive-benchmark ETFs
  - daily futures (e.g. gold and crude continuous contracts, from the terms-checked sources of P1-T023) and the macro/rates series the docs name (FRED/ALFRED core series, US Treasury curve, RBA/BoE/ECB policy rates, RBA F11, ABS CPI, which is always included)
- `mt universe seed` (CLI over `mt-api`, command `data.universe.update`, C1) writes the effective universe with source `seed`: idempotent (no new version when nothing changed) and never overwriting a value you set (your rows win; the seed only fills what has no value)
- Every universe version is recorded (`audit.command` + a versioned settings row); connectors read the effective universe from settings and fall back to the P1-T005 fixture universe only when no version exists
- The universe and its source (`seed` or `user`) appear in the go-live pack generator (P7-T070 reads it) and in D02 watchlists
- No secrets in the file

## ToDo

- [ ] Draft `config/defaults/universe.yaml` from 03 M1, 03 §6 and R1.01–R1.06 (each entry with its doc link)
- [ ] Implement `mt universe seed` over `mt-api` (`data.universe.update`, source `seed`), idempotent, never overwriting user rows
- [ ] Validate with `mt universe validate` (symbols resolve on each venue via P1-T009, ≤ 30 Alpaca symbols, ≤ 3 native-L2 symbols by default, no paid source)
- [ ] Run the seed on the workstation stack; screenshot D02 watchlists showing the seeded universe
- [ ] Add the effective universe to the go-live pack generator (P7-T070)
- [ ] Write the tests listed under Verification
- [ ] Update the docs listed under Doc sync and tick the roadmap ToDo box(es)

## Verification

### Tests

- `cargo test -p mt-api universe_seed`: every seeded entry equals the defaults file; the defaults file's lists match the doc sections they cite (doc-link test)
- `cargo test -p mt-api universe`: `data.universe.update` with source `seed` is C1, audited, and refuses to overwrite a user-set version
- Re-run the seed: no new version. Edit one entry by hand, re-run: your edit stays

### Scenarios

- Given the universe lists 31 US symbols, when validated, then it fails with "Alpaca IEX free limit is 30"
- Given a crypto pair with `l2: true`, when the storage estimator runs (P1-T052), then its projected yearly bytes appear in D07 Storage
- Given 4 symbols marked `l2: true` with the default cap of 3, when validated, then it fails and names the setting that raises the cap (a setting, not code)
- Given a fresh workstation stack, when `mt universe seed` runs, then D02 shows the seeded watchlists with source `seed`

### Stress / failure injection

- Seed while Supabase Postgres restarts: the command fails cleanly with no partial version (one transaction)

## Acceptance criteria

- [ ] The effective universe exists with source `seed`, matches `config/defaults/universe.yaml` and validates
- [ ] Native-L2 symbols are marked explicitly (≤ 3 unless the setting is raised), and the projected disk use stays inside ~0.3–1 TB/year (R1.N3; re-measured in the soak, P1-T065)
- [ ] Seeding is idempotent and never overwrites your edits

## Exceptions & edge cases

- You can change the list any time; changes take effect on connector restart, and history already recorded is kept
- Symbols delisted or renamed by a venue are flagged by the instrument master (P1-T009), not silently dropped
- A doc list marked (U) is seeded as written and flagged `unverified` until its check (e.g. P1-T056) confirms it

## Cardinal rules (do NOT)

- Do NOT include instruments that need paid data (e.g. CME real-time, LBMA fixes)
- Do NOT exceed 30 Alpaca IEX symbols
- Do NOT overwrite a universe entry you set; the seed only fills gaps
- Do NOT hard-code the list in code; it lives in the defaults file and the settings store
- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file (kept outside the repo) mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.01 once every task traced to it in PHASE.md is done; note P1-T001 next to it (T1.01 is now an agent seed, reviewed in the go-live pack).
- `docs/03-build-spec.md` §M1: note the seeded starting universe size if it differs from "~10 liquid crypto symbols"
- `docs/16-configuration-and-safety-model.md`: list the default starting universe (or link `config/defaults/universe.yaml`) as a configurable default

## Branch & PR

- Branch: `p1/P1-T001-pick-universe-watchlist`
- PR title: `P1-T001: Seed the starting universe and watchlist from the docs' default lists`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T001` run

## Progress log

- 2026-10-21 00:00 · planner · created
- 2026-10-22 00:00 · aligner · updated for docs/16–17 (L2 native diffs only for ≤ 3 symbols by default, others 1 s snapshots (P1-B002); run fields)
- 2026-11-19 00:00 · aligner · re-platformed per docs/18 (converted from USER to an agent seed per 17 §G and the re-platform brief §2: the agent drafts the universe from 03 M1/§6 and R1.01–R1.06 and seeds it through `mt-api` with source `seed`; you review it in the go-live pack P7-T070; deps P1-T005, P1-T009, P1-T046; tools cargo/uv/supabase, services supabase-postgres, mt-api)
- 2026-11-20 00:00 · aligner · Rust-max per 17 §H (validation CLI `mt universe validate` (Rust); the seed test moves from pytest to `cargo test -p mt-api` with the same cases; daily futures named without yfinance tickers; tools drop uv)
