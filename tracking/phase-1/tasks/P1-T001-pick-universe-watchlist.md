---
id: P1-T001
kind: task
title: Pick the starting universe and watchlist
phase: 1
type: USER
status: backlog
priority: high
size: S
severity: ""
owner: user
claimed_by: ""
depends_on: []
requirements: [R1.01, R1.04, R1.05, R1.06]
roadmap_todos: [T1.01]
modules: [M1]
dashboards: [D02]
branch: p1/P1-T001-pick-universe-watchlist
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

# P1-T001 · Pick the starting universe and watchlist

## Goal / expected outcome

You choose the instruments P1 records and monitors, written to `config/universe.yaml`, so connectors, the DQ monitor, the storage budget and the soak all work from one agreed list.

## Context & references

- Roadmap: requirements [R1.01](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.04](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.05](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements), [R1.06](../../../docs/roadmap/phase-1-data-and-monitoring.md#3-requirements) · ToDo [T1.01](../../../docs/roadmap/phase-1-data-and-monitoring.md#4-todo-sets)
- Spec: [03 M1](../../../docs/03-build-spec.md#m1-market--macro-data--mt_datamarket) (sources per asset class) · [03 §6](../../../docs/03-build-spec.md#6-smallest-free-timeframe-by-asset-class) (finest free timeframe per class)
- Storage budget is sized for ~10 liquid crypto symbols ([03 M1](../../../docs/03-build-spec.md#m1-market--macro-data--mt_datamarket), R1.N3); Alpaca free IEX allows 30 WebSocket symbols
- Unblocks: P1-T065 (soak runs on this universe); connectors use a default fixture universe until this is done

## Requirements

- ~10 crypto pairs (e.g. BTC/ETH/SOL vs USDT on Binance), and for each one say whether it needs L2 recorded (L2 drives disk use, see phase 1 §7 risks)
- FX and metal pairs available on OANDA practice and IG demo (e.g. EURUSD, AUDUSD, USDJPY, XAUUSD, XAGUSD); no LBMA
- Up to 30 US ETFs/stocks (hard Alpaca IEX free limit); include the ETFs you would use as passive benchmarks
- Daily futures you want visible (e.g. `GC=F`, `CL=F`) and the macro/rates series you care about (FRED IDs, RBA/ABS series, central banks)
- Output goes to a PR editing `config/universe.yaml` (no secrets in it), or a message to the agent with the list

## ToDo

- [ ] Read the default fixture universe in `config/universe.yaml` (created by P1-T005) and the per-class notes in 03 §6
- [ ] Pick ~10 crypto pairs and mark which need L2 (`l2: true`)
- [ ] Pick FX/metal pairs (OANDA + IG symbols) and up to 30 US ETFs/stocks
- [ ] List daily futures and macro/rates series (FRED IDs, ECB/BoE/RBA series, ABS CPI is always included)
- [ ] Commit the list (or hand it to the agent) and confirm the agent merged it

## Verification

### Tests

- Agent check after merge: `uv run mt-data universe validate` passes (symbols resolve on each venue, ≤ 30 Alpaca symbols, no paid source)

### Scenarios

- Given the universe lists 31 US symbols, when validated, then it fails with "Alpaca IEX free limit is 30"
- Given a crypto pair with `l2: true`, when the storage estimator runs (P1-T052), then its projected yearly bytes appear in D07 Storage

### Stress / failure injection

- n/a: a decision, not code

## Acceptance criteria

- [ ] `config/universe.yaml` holds your list and validates
- [ ] L2 symbols are marked explicitly, and the projected disk use stays inside ~0.3–1 TB/year (R1.N3)

## Exceptions & edge cases

- You can change the list later; changes take effect on connector restart, and history already recorded is kept
- Symbols delisted or renamed by a venue are flagged by the instrument master (P1-T009), not silently dropped

## Cardinal rules (do NOT)

- Do NOT include instruments that need paid data (e.g. CME real-time, LBMA fixes)
- Do NOT exceed 30 Alpaca IEX symbols
- Do NOT commit secrets or paste them into chats, issues, logs or test fixtures; credentials come only from the sops/age secrets file mounted on tmpfs ([07 §2](../../../docs/07-security-notes.md#2-secrets)).
- Do NOT add paid data or APIs, exceed a free tier, or scrape against a site's terms; no self-bots or user tokens ([03 §1](../../../docs/03-build-spec.md#1-ground-rules)).

## Doc sync on completion

- `docs/roadmap/phase-1-data-and-monitoring.md`: tick T1.01 once every task traced to it in PHASE.md is done; note P1-T001 next to it.
- `docs/03-build-spec.md` §M1: note the chosen starting universe size if it differs from "~10 liquid crypto symbols"

## Branch & PR

- Branch: `p1/P1-T001-pick-universe-watchlist`
- PR title: `P1-T001: Pick the starting universe and watchlist`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P1-T001` run

## Progress log

- 2026-10-21 00:00 · planner · created
