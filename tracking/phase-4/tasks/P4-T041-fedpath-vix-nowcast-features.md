---
id: P4-T041
kind: task
title: Fed-path from ZQ, VIX regime, nowcast, positioning and prediction-market features
phase: 4
type: BUILD
status: backlog
priority: high
size: M
severity: ""
owner: agent
claimed_by: ""
depends_on: [P4-T039, P4-T036]
requirements: [R4.11]
roadmap_todos: [T4.27]
modules: [M6]
dashboards: [D08, D02]
branch: p4/P4-T041-fedpath-vix-nowcast-features
pr: ""
doc_sync: [docs/03-build-spec.md, docs/roadmap/phase-4-intel.md]
doc_sync_status: n/a
found_in: ""
created: 2026-10-21
updated: 2026-10-21
started: ""
completed: ""
blocked_reason: ""
checkpoint: ""
---

# P4-T041 · Fed-path from ZQ, VIX regime, nowcast, positioning and prediction-market features

## Goal / expected outcome

Versioned features exist for: **Fed-path probabilities** per FOMC meeting computed from ZQ futures (implied rate = 100 − price, meeting-weighted step-ups), **VIX regime** (percentile bands + term-structure if available), nowcast surprises (GDPNow/NY Fed/Cleveland vs consensus), retail positioning (net long %, contrarian z per FX/metal pair), COT net positioning z, BIS effective exchange rates changes, and prediction-market probabilities.

## Context & references

- Roadmap: [R4.11](../../../docs/roadmap/phase-4-intel.md#3-requirements) · ToDo [T4.27](../../../docs/roadmap/phase-4-intel.md#4-todo-sets)
- Spec: [03 M6 sentiment, positioning and macro features](../../../docs/03-build-spec.md#m6-features--mt_features) · [06 §3 Fed-path from ZQ](../../../docs/06-aggregators-and-market-providers.md#3-additional-forex--multi-asset-providers)
- Cross-phase: P1 COT and BIS (`sdmx1`) flows.

## Requirements

- Fed path: for each meeting in the next 12 months, P(hike/hold/cut by 25/50 bp) from the contract spanning the meeting, using day-count weighting; validated against a published worked example.
- VIX regime: `{calm <15th pct, normal, elevated >80th, stress >95th}` over a 5-year window; versioned thresholds.
- Positioning: Myfxbook/IG/OANDA long % → contrarian z (90-day); COT non-commercial net z (3-year).
- Prediction markets: probability levels and 1-day change as features.
- All features PIT (vintages honoured) and registered in `features.def`.

## ToDo

- [ ] Fed-path calculator + meeting calendar link (P4-T037 CB schedule).
- [ ] VIX regime + thresholds.
- [ ] Positioning, COT, BIS, PM feature writers.
- [ ] Tests.

## Verification

### Tests
- Golden: Fed-path calculator matches a hand-computed example to 1e-6.
- Unit: VIX band boundaries.
- PIT: nowcast feature at T uses the vintage available at T.

### Scenarios
- Given a ZQ contract is missing for a day, then Fed-path is carried forward with `stale=true` for ≤ 1 day, then null.
- Given an emergency inter-meeting cut, then the next meeting's base rate updates on the next settlement.

### Stress / failure injection
- n/a: daily/low-frequency features.

## Acceptance criteria

- [ ] Features registered and populated daily; golden Fed-path test green
- [ ] CI green (ruff, mypy, pytest, `pit` bypass check)

## Exceptions & edge cases

- ZQ illiquid far contracts: cap the horizon where open interest < threshold.

## Cardinal rules (do NOT)

- Do NOT scrape CME FedWatch.
- Do NOT use Telegram-derived inputs.
- Do NOT add paid data/APIs, scraping that breaks a site's terms, self-bots/user tokens, or any sybil/fake engagement.
- Do NOT let Telegram text (or any `model_input_ok = false` row) reach a model, RAG index or training set ([12 §4–5](../../../docs/12-policy-and-compliance.md#4-per-platform-data--automation-rules)).
- Do NOT bypass `mt_api`, the risk manager (M11) or `mt_store.pit(as_of)`; every order goes through M11.
- Do NOT skip, weaken or delete a test to get green.

## Doc sync on completion

- `docs/03-build-spec.md`: M6: Fed-path method and VIX bands
- `docs/roadmap/phase-4-intel.md`: tick T4.27 when all items mapped to it are done

## Branch & PR

- Branch: `p4/P4-T041-fedpath-vix-nowcast-features`
- PR title: `P4-T041: Fed-path from ZQ, VIX regime, nowcast, positioning and prediction-market features`
- PR checklist: tests added · docs synced · task file ticked · `./kanban done P4-T041` run

## Progress log

- 2026-10-21 00:00 · planner · created
